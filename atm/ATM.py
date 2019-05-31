#!/usr/bin/env python
"""
Alaska Thermokarst Model (ATM)
-------------------------------

The purpose of this script is to provide a protype source
code for testing and development of the Alaska Thermokarst
Model (ATM) to be integrated into the Alaska Integrated
Ecosystem Model (AIEM).

Created: May 2014. Bob Bolton


The ATM code is python based and is executed with the following command:
$ python ATM.py <control file name>

The control file is used to set up the simulation input/output locations,
defines the model domain, etc. 

See readme for more infromation

"""
# import matplotlib.pyplot as plt

################################################################################
# Authorship moved to __init__.py
################################################################################


################################################################################
# Required Modules
################################################################################
import sys
import os
import datetime
import shutil
import faulthandler
import tarfile
import glob

import numpy as np

import checks
import climate_events
import lake_pond_expansion
import results
from control import Control
from grids.grids import ModelGrids
from grids import area_grid
from cohorts import find_canon_name, DISPLAY_COHORT_NAMES

from logger import Logger

from multigrids import figures

#_______________________________________________________________________________
class ATM(object):
    """ATM class
    """
 
    def __init__(self, control_file, logger=Logger(None)):
        """Arctic Thermokarst Model(ATM) class. Sets up and run the ATM model
        
        Parameters
        ----------
        control_file: path
            path to control file
            
        Attributes
        ----------
        control: control.Control
            ATM control file object
        grids: grids.Grids
            ATM grids object
        stop: int
            # of years to run model for
        
        """

        self.logger = logger
        # ----------------------
        # Simulation Start Time
        # ----------------------
        
        # '==================='
        # ' Initializing ATM'
        # '==================='
        self.logger.add('===== Initializing ATM =====')
        self.control = Control(control_file)
        
        
        faulthandler.enable()
        
        # '==================='
        # ' Creating Grids'
        # '==================='
        self.logger.add('===== Creating Grids =====')
        self.grids = ModelGrids(self.control, self.logger)
        #--------------------------------------

        if self.control['Test_code'] or \
                str(self.control['Test_code']).lower() == 'yes':
            self.stop = self.control['Test_code_duration']
        else:
            self.stop = int(self.grids.get_max_time_steps())
        
        ########################################################################
        # Execute the script
        ########################################################################
        
        self.remove_old()
        self.run_atm()
        
    def remove_old(self):
        """Removes old model results from results directory if they exist,
        but saves the the archived results 
        """
        if os.path.exists(self.control['Output_dir']):
            for d in os.listdir( self.control['Output_dir'] ):
                if d == 'Archive' or d == 'runtime_data':
                    continue
                shutil.rmtree(os.path.join(self.control['Output_dir'],d), True)
            
        pth = os.path.join(self.control['Output_dir'],'Archive','*.txt')
        text_files = glob.glob(pth)
        for f in text_files:
             os.remove(f)
            
            
    def save_figures(self):
        """saves model figures
        """
        self.logger.add("Finishing up -- saving figures")
        
        outdir = self.control['Output_dir']
        start_year = self.control['start_year']
        self.logger.add("  -- Initial Figures")
        for figure in self.control['Initialize_Control']:
            cohort = '_'.join(figure.split('_')[:-1])
            if cohort not in self.grids.area.get_cohort_list():
                continue              
            cohort_path = os.path.join(outdir, cohort)
            try: 
                os.makedirs(cohort_path)
            except:
                pass
            disp_name = DISPLAY_COHORT_NAMES[cohort]
            if self.control['Initialize_Control']['Initial_Cohort_Age_Figure'] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('age') > 0:
                fig_args = {
                    'title': disp_name + ' - Present In Initial Area',
                    "categories": ['not present', 'present']
                    }
                self.grids.area.save_figure(
                    cohort, start_year, 
                    os.path.join(cohort_path, cohort+'_age.png'), 
                    figure_func=figures.categorical_threshold, 
                    figure_args=fig_args
                )
            
            if self.control['Initialize_Control'][
                        'Normalized_Cohort_Distribution_Figure'
                     ] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('normal') > 0:
                fig_args = {
                    'title': disp_name + ' - Initial Fractional Area',
                    # "categories": ['not present', 'present']
                     'vmin': 0, 'vmax': 1,
                    }
                self.grids.area.save_figure(
                    cohort, start_year, 
                    os.path.join(cohort_path, cohort+'_fractional_cohorts.png'), 
                    figure_func=figures.default, 
                    figure_args=fig_args
                )

            if self.control['Initialize_Control'][
                        'Initial_Cohort_Distribution_Figure'
                     ] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('figure') > 0:
                fig_args = {
                    'title': disp_name + ' - Initial Fractional Area',
                    # "categories": ['not present', 'present']
                    #  'vmin': 0, 'vmax': 1,
                    }
                self.grids.area.save_figure(
                    cohort, start_year, 
                    os.path.join(cohort_path, 'Initial_' + cohort +'.png'), 
                    figure_func=figures.threshold, 
                    figure_args=fig_args
                )
                # self.grids.area.save_init_dist_figure(cohort, cohort_path)
                    
            
        init_path = os.path.join( outdir, 'Initialization')
        try: 
            os.makedirs(init_path)
        except:
            pass
            
        self.logger.add("  -- Terrestrial Figures")
        self.logger.add("    -- Ice_Distribution_Figure")
        if self.control['Terrestrial_Control']['Ice_Distribution_Figure']:
            fig_args = {
                'title': 'Ground Ice Content',
                "categories": ['none'] + [t for t in self.grids.ice.config['ice types']],
                'vmin': 0, 'vmax': 4,
            }
            self.grids.ice.save_figure( 
                os.path.join(init_path,'Ground_Ice_Content.png'), 
                figures.categorical, fig_args
            )
            # self.grids.ice.show_figure(figures.categorical, fig_args)

            # self.grids.ice.binary(
            #     os.path.join(init_path,'Ground_Ice_Content.bin')
            # )
        self.logger.add("    -- Drainage_Efficiency_Figure")
        if self.control['Terrestrial_Control']['Drainage_Efficiency_Figure']:
            fig_args = {
                'title': 'Drainage efficiency',
                "categories": ['none', 'above', 'below'],
                'vmin': 0, 'vmax': 4,
                'cmap': 'Greys'    
                }
            # print self.grids.drainage.as_numbers()
            self.grids.drainage.save_figure( os.path.join(init_path,'Drainage_efficiency.png'), figures.categorical, fig_args)
            # self.grids.drainage.show_figure(figures.categorical, fig_args)

            # self.grids.drainage.binary(
            #     os.path.join(init_path,'Drainage_efficiency.bin')
            # )
        
        self.logger.add( "    -- ALD_Distribution_Output")
        if self.control['Terrestrial_Control']['ALD_Distribution_Output']:
            fig_args = {
                'title': 'Initial Active Layer Depth',
                'cbar_extend': 'max',
                # "categories": ['none', 'above', 'below'],
                # 'vmin': 0, 'vmax': 4,
                'cmap': 'bone'    
                }
            self.grids.ald.save_figure('ALD', start_year, 
                os.path.join(init_path,'Initial_ALD.png'),
                figure_args = fig_args
            )
            # self.grids.ald.init_ald_binary(
            #     os.path.join(init_path,'Initial_ALD.bin')
            # )
        self.logger.add("    -- ALD_Factor_Output")
        if self.control['Terrestrial_Control']['ALD_Factor_Output']:

            fig_args = {
                'title': 'Initial Active Layer Depth Constants',
                'cbar_extend': 'max',
                # "categories": ['none', 'above', 'below'],
                # 'vmin': 0, 'vmax': 4,
                'cmap': 'bone'    
                }
            self.grids.ald.save_figure('ALD', start_year, 
                os.path.join(init_path,'Active_Layer_Factor.png'),
                figure_args = fig_args,
                data = self.grids.ald.ald_constants
            )
            # self.grids.ald.ald_constants_binary(
            #     os.path.join(init_path,'Active_Layer_Factor.bin')
            # )
        
        dom_path = os.path.join( outdir, 'All_cohorts', 'year_cohorts')
        try: 
            os.makedirs(dom_path)
        except:
            pass
        
        self.logger.add("    -- Dominant Cohort Figure")
        dc_data = self.grids.area.create_dominate_cohort_dataset()
        dc_frames = []
        fig_args = {
                'title': '',
                'cbar_extend': 'max',
                "categories": sorted(dc_data.config['cohort list']),
                # 'vmin': 0, 'vmax': 4,
                'cmap': 'viridis', 
                'ax_labelsize': 5 ,  
                }
        if self.control['Terrestrial_Control']['Figure']:
            
            for year in range(start_year, start_year + self.stop-1):
                fig_args['title'] = 'Dominant Cohort -' + str(year)
                dc_data.save_figure(
                    year, 
                    os.path.join(
                        dom_path,
                        'Dominant_Cohort_'+ str(year) + '.png'
                    ),
                    figures.categorical, 
                    fig_args
                )
                dc_frames.append(
                    os.path.join(
                        dom_path,
                        'Dominant_Cohort_'+ str(year) + '.png'
                    )
                )
        if self.control['Terrestrial_Control']['Movie']:
            dom_path = os.path.join( outdir, 'All_cohorts')
            clip_args = {
                'figure_args': fig_args,
            }
            outfile = os.path.join(dom_path, 'dominate-cohort-time-series.mp4')
            if dc_frames != []:
                clip_args['frames list'] = dc_frames
                # print frames
                # complete = dc_data.save_clip(outfile, clip_args=clip_args)
            else:
                clip_args['end_ts'] = self.stop
            complete = dc_data.save_clip(outfile, clip_args=clip_args)
            
            if complete:
                self.logger.add("       -- Clip output success")
            else:
                self.logger.add("       --  Clip output failed")
            
        
        self.logger.add( "  -- Met Figures" )
        self.logger.add( "    -- Degree Days")
        dd_path = os.path.join( outdir, 'Initialization', 'Degree_Days')
        try: 
            os.makedirs(dd_path)
        except:
            pass
        if self.control['Met_Control']['Degree_Day_Output']:
            tdd = self.control['Met_Control']['TDD_Output']
            try: 
                os.makedirs(os.path.join(dd_path, tdd))
            except:
                pass
            fdd = self.control['Met_Control']['FDD_Output']
            try: 
                os.makedirs(os.path.join(dd_path, fdd))
            except:
                pass
            
            fig_args = {
                'title': '',
                'cbar_extend': 'both'
                }


            for year in range(start_year, start_year + self.stop-1):
                fig_args['title'] = 'Thawing Degree Days -' + str(year)
                fig_args['vmin'] = 0
                fig_args['vmax'] = 1250
                self.grids.degreedays.thawing.save_figure(
                    year, 
                    os.path.join(dd_path, tdd, 'tdd_'+ str(year) + '.png'),
                    figures.default, 
                    fig_args
                )
                fig_args['title'] = 'Freezing Degree Days -' + str(year)
                fig_args['vmin'] = -6000
                fig_args['vmax'] = -2000
                self.grids.degreedays.freezing.save_figure(
                    year, 
                    os.path.join(dd_path, fdd, 'fdd_'+ str(year) + '.png'),
                    figures.default, 
                    fig_args
                )

            
        
        lp_types = \
                self.control['_FAST_get_pond_types'] +\
                self.control['_FAST_get_lake_types']   
        self.logger.add( "  -- Lake Pond Figures" )
        for figure in self.control['Lake_Pond_Control']['figures']:
            if not self.control['Lake_Pond_Control']['figures'][figure]:
                continue
            lpt = '_'.join(figure.split('_')[:-2])
            if lpt not in lp_types:
                continue 
            
            self.logger.add("    -- " + lpt + ' Depth')
            path = os.path.join(outdir, lpt)
            try: 
                os.makedirs(path)
            except:
                pass
            fig_args = {
                'title': 
                    'Initial Depth ('+str(start_year)+') \n' + \
                    DISPLAY_COHORT_NAMES[lpt],
                # 'cbar_extend': 'both',
                'mask': self.grids.aoi,
                }
            self.grids.lake_pond.save_figure(
                lpt+'_depth', start_year,
                os.path.join(path,'Initial_'+lpt+'_Depth.png'),
                figure_args=fig_args
            )

        self.logger.add("  -- Cohort Figures/Video")
        for control in sorted(self.control['cohorts']):
            if type(self.control['cohorts'][control]) is str:
                continue
            
            
            cohort = '_'.join(control.split('_')[:-1])
            path = os.path.join(outdir, cohort, 'year_cohorts')
            try: 
                os.makedirs(path)
            except:
                pass
            
            self.logger.add( "    -- " + cohort + " Figures/Video")
            fig_args = {
                'title': '',
                # 'cbar_extend': 'both'
                'mask': self.grids.aoi,
                'vmin': 0,
                'vmax': 1,
                }

            frames = []
            if self.control['cohorts'][control]['Figures']:
                for year in range(start_year, start_year + self.stop-1):
                    fig_args['title'] = \
                        DISPLAY_COHORT_NAMES[cohort] +' - ' + str(year)
                    fname = \
                        os.path.join(
                            path, 
                            cohort + '_Fractional_Area_'+ str(year)+'.png'
                        )
                    self.grids.area.save_figure(
                        cohort, year, fname, figures.default, fig_args
                    )
                    frames.append(fname)
            
            clip_args = {
                'figure_args': fig_args,
            }
            if self.control['cohorts'][control]['Movie']:
                if frames != []:
                    clip_args['frames list'] = frames
                    # print frames
                    path = os.path.join(outdir, cohort)
                    complete = self.grids.area.save_clip(
                        None,
                        os.path.join(path, cohort + '_Fractional_Area.mp4'),
                        clip_args=clip_args
                    )
                else:
                    path = os.path.join(outdir, cohort)
                    clip_args['end_ts'] = self.stop
                    complete = self.grids.area.save_clip(
                        cohort,
                        os.path.join(path, cohort + '_Fractional_Area.mp4'),
                        clip_args=clip_args
                    )
                    

                if complete:
                    self.logger.add(
                        "       -- " + cohort + " Clip output success"
                    )
                else:
                    self.logger.add(
                        "       -- " + cohort + " Clip output failed"
                    )



            
        
    def archive(self, name):
        """archive results
        
        Parametes
        ---------
        name: str
            name of archive
        """
        path = os.path.join( self.control['Output_dir'], 'Archive')
        try:
            os.makedirs(path)
        except:
            pass
        archive_file = tarfile.open(os.path.join(path,name), mode='w:gz')
        
        control = self.control['Archive_data']
        
        if control['Simulation_Summary']:
            pth = os.path.join(path,'*.txt')
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(f, os.path.split(f)[1])
                
        if control['Met'] and  control['Figures']:
            for d in [
                self.control['Met_Control']['TDD_Output'], 
                self.control['Met_Control']['FDD_Output']
            ]:
                pth = os.path.join(
                    self.control['Output_dir'],
                    'Initialization','Degree_Days',d, '*.png'
                )
                text_files = glob.glob(pth)
                for f in text_files:
                    archive_file.add(f, os.path.join(
                        'Initialization','Degree_Days',d,os.path.split(f)[1]
                    ))
        
        archive_file.add(self.control['Control_dir'], 'Control_Files')
        archive_file.add(self.control['Control_dir'], 'runtime_data')
        
        for directory in os.listdir(self.control['Output_dir']):
            if directory == 'Archive':
                continue
            if not control['All_Cohorts']:
                if not control['Lakes'] and directory.lower().find('lake')!= -1:
                    continue
                elif not control['Ponds'] and \
                        directory.lower().find('pond')!= -1:
                    continue
                else:
                    if control['Other_Cohorts']:
                        continue
            
            pth = os.path.join( self.control['Output_dir'],directory,'*.bin')
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(f, os.path.join(directory,os.path.split(f)[1]))
            
            pth = os.path.join(
                self.control['Output_dir'],directory, "year_cohorts",'*.bin'
            )
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(
                    f, os.path.join(
                        directory,"year_cohorts",os.path.split(f)[1]
                    )
                )
            if not control['Figures']:
                continue
            pth = os.path.join( self.control['Output_dir'],directory,'*.png')
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(f, os.path.join(directory,os.path.split(f)[1]))
            
            pth = os.path.join(
                self.control['Output_dir'],directory, "year_cohorts",'*.png'
            )
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(
                    f, os.path.join(
                        directory,"year_cohorts",os.path.split(f)[1]
                    )
                )
            pth = os.path.join( self.control['Output_dir'],directory,'*.mp4')
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(f, os.path.join(directory,os.path.split(f)[1]))
            
            pth = os.path.join(
                self.control['Output_dir'],directory, "year_cohorts",'*.mp4'
            )
            text_files = glob.glob(pth)
            for f in text_files:
                archive_file.add(
                    f, os.path.join(
                        directory,"year_cohorts",os.path.split(f)[1]
                    )
                )
        archive_file.close()
            
            
    def to_screen(self, start_time, end_time):
        """print results on screen
        
        Parameters
        ----------
        start_time: datetime.datetime
        end_time: datetime.datetime
        """
        self.logger.add(results.as_string(self, start_time, end_time), 'info')
    
    def to_file(self,name, start_time, end_time):
        """save results to file
        
        Parameters
        ----------
        start_time: datetime.datetime
        end_time: datetime.datetime
        """
        r = results.as_string(self, start_time, end_time)
    
        path = os.path.join( self.control['Output_dir'], 'Archive')
        try:
            os.makedirs(path)
        except:
            pass
            
        with open(os.path.join(path,name),'w') as fd:
            fd.write(r)
#_______________________________________________________________________________
    def run_atm(self):
        """Run the framework. Creating the results.
        """
        #====================================================
        # Initialization Process
        #====================================================

        mode = ''
        try: 
            if self.control['use_jit'] == "yes":
                self.logger.add("use_jit set to yes, starting precompilation")
                mode = '_jit'
                for f in checks.jit_precompile:
                    f()
                self.logger.add("finished precompilation")
            elif self.control['use_jit'] == "cuda":
                self.logger.add("use_jit set to cuda, starting precompilation")
                mode = '_cuda'
                for f in checks.cuda_precompile:
                    f()
                self.logger.add("finished precompilation")
        except KeyError:
            pass

        start_time = datetime.datetime.now()
        
    
        # '=================================================='
        # '            Starting the MAIN LOOP '
        # '=================================================='

        self.logger.add('===== Starting the MAIN LOOP ======')
        self.run_model(self.control['Transition_order'], mode)
        self.logger.add('===== Finished the MAIN LOOP ======')
        # '=================================================='
        # '            Finished the MAIN LOOP '
        # '=================================================='


        # -------------------
        # Simulation End Time
        # -------------------
        #~ clock.finish(self)
        end_time = datetime.datetime.now()
        #===========================
        # Output Simulation Results
        #===========================
        t = datetime.datetime.now()
        t = t.strftime("%Y_%m.%d_%H%M")
      
        
        if self.control['Results_onscreen'] or \
                self.control['Results_onscreen'].lower() == 'yes':
            self.to_screen(start_time, end_time)
        if self.control['Archive_simulation'] or \
                self.control['Archive_simulation'].lower() == 'yes':
            name = t +'_' +self.control['Simulation_name'] + '.txt'
            self.to_file(name, start_time, end_time)
        
        self.save_figures()

        name = t +'_' + self.control['Simulation_name'] +".tar.gz"
        self.archive(name)


        self.logger.add('===== Simulation Complete ======')
        # '----------------------------------------'
        # '        Simulation Complete             '
        # '----------------------------------------'        

    def run_model(self, cohort_list, mode = ''):
        """run actual model
        
        Parameters
        ----------
        cohort_list ordered list of cohorsts to run
        """
        self.control['global jit options'] = "yes"

        init_year = self.control['initialization year']
        init_tdd = self.grids.degreedays.thawing[init_year+1]

        pond_types = self.control['_FAST_get_pond_types']
        lp_types = \
                pond_types +\
                self.control['_FAST_get_lake_types']
        
        ## ts zero is initial data state 
        ## ts one is frist year to make chages
        try:
            log_ts = self.control['log_each_time_step']
        except KeyError:
            log_ts = False

        for time in range(1, self.stop):

            if log_ts:
                self.logger.add('    at time step: '+ str(time))
            
            current_year = init_year + time

            cohort_start = \
                self.grids.area.get_all_cohorts_at_time_step().sum(0)
                
    
                ### Loop through each of the cohort checks for area
                #~ active_layer_depth.active_layer_depth(self, time, element)
            self.grids.climate_event.create_climate_events(self.logger,log_ts)
                
            # self.grids.add_time_step()
            self.grids.increment_time_step()
            self.grids.area[current_year] = self.grids.area[current_year-1]
            
           
            climate_events.drain_lakes(
                self.control['Met_Control']['lakes_drain_to'],
                current_year,
                self.grids,
                self.control
            )
            
            ## update ALD
            current_tdd = self.grids.degreedays.thawing[current_year]
            ald = self.grids.ald.calc_ald(init_tdd, current_tdd, False)
            self.grids.ald['ALD', current_year] = ald
            
            ## set current ice thickness(depth)
            current_fdd = self.grids.degreedays.freezing[current_year]
            self.grids.lake_pond.calc_ice_depth(current_fdd)

            ## transition list
            for cohort in cohort_list:
                cohort_control = cohort + '_Control'
                try:
                    check_type = \
                        self.control['cohorts'][cohort_control]\
                        ['Transition_check_type'].lower()
                except KeyError as e:
                    check_type = 'base'

                name = find_canon_name(cohort)
                
                try:
                    checks.check_metadata[check_type + mode](
                        name,  current_year, self.grids, self.control
                    )
                except KeyError:
                    self.logger.add("using fallback for " + check_type + mode)
                    checks.check_metadata[check_type](
                        name,  current_year, self.grids, self.control
                    )

            lake_pond_expansion.expansion(
                lp_types, current_year, self.grids, self.control
            )
            lake_pond_expansion.infill(
                pond_types, current_year, 
                self.grids, self.control
            )
                



            cohort_end = \
                self.grids.area.get_all_cohorts_at_time_step().sum(0)
            
            diff = abs(cohort_start - cohort_end)
           
            #~ ## check mass balance, MOVE to function?
            if (diff > 0.1).any():
                
                # with open('err.pkl','wb') as e:
                #     pickle.dump(self.grids, e )
                
                location = np.where(diff > 0.1)[0]
                self.logger.add('Mass Balance change greater thatn 10 % in '
                        ''+ str(len(location)) + ' cells ', 'error')
                
                sys.exit()
                
                ## to do add frist cell report
            try:
                self.grids.area.check_mass_balance()
                self.grids.area.check_mass_balance(current_year - init_year)
            except area_grid.MassBalanceError as e:
                if str(e) == 'mass balance problem 1':
                    self.logger.add('mass has been added', 'error')
                    for cohort in sorted(self.grids.area.key_to_index):
                        if cohort.find('--') != -1:
                            continue
                            
                        s = self.grids.area[cohort, init_year,].sum()
                        e = self.grids.area[cohort, current_year].sum()
                        
                        if s == e:
                            d = 'equal'
                        elif s < e:
                            d = 'growth'
                        else:
                            d = 'reduction'
                        self.logger.add(
                            cohort + 'start:'+ s+ 'end:'+ e+ d, 
                            'error'
                        )
                else:
                    self.logger.add('mass has been removed')
                sys.exit()
                        
        
        ### debug stuff
        print('start: ', cohort_start.sum())
        print( 'end: ', cohort_end.sum())
        for cohort in sorted(self.grids.area.key_to_index):
            if cohort.find('--') != -1:
                continue
                
            s = self.grids.area[cohort, init_year].sum()
            e = self.grids.area[cohort, current_year].sum()
            
            if s == e:
                d = 'equal'
            elif s < e:
                d = 'growth'
            else:
                d = 'reduction'
            print (cohort, 'start:', s, 'end:', e, d)

    def __del__(self):
        """
        destructor
        """
    
        # print(self.control['save_log_to'])
        try:
            if self.control['save_log_to']:
                self.logger.save(self.control['save_log_to'], False)
        except (KeyError, AttributeError):
            pass
            
#_______________________________________________________________________________

## runs model from comand line
if __name__ == "__main__":
    Variable = ATM(sys.argv[1], Logger(None, also_print=True))
    # del(Variable)

