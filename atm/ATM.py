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
import matplotlib.pyplot as plt

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
from cohorts import find_canon_name



#_______________________________________________________________________________
class ATM(object):
    """ATM class
    """
 
    def __init__(self, control_file):
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
        # ----------------------
        # Simulation Start Time
        # ----------------------
        
        print '==================='
        print ' Initializing ATM'
        print '==================='
        self.control = Control(control_file)
        
        #~ print 'Control loaded'
        
        faulthandler.enable()
        #~ clock.start(self)
        
        print '==================='
        print ' Creating Grids'
        print '==================='
        
        self.grids = ModelGrids(self.control)
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
        print "Finishing up \n-- saving figures"
        
        outdir = self.control['Output_dir']
        
        print "  -- Initial Figures"
        for figure in self.control['Initialize_Control']:
            cohort = '_'.join(figure.split('_')[:-1])
            if cohort not in self.grids.area.get_cohort_list():
                continue              
            cohort_path = os.path.join(outdir, cohort)
            try: 
                os.makedirs(cohort_path)
            except:
                pass
            
            if self.control['Initialize_Control']['Initial_Cohort_Age_Figure'] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('age') > 0:
                self.grids.area.save_init_age_figure(cohort, cohort_path)
            if self.control['Initialize_Control'][
                        'Normalized_Cohort_Distribution_Figure'
                     ] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('normal') > 0:
                self.grids.area.save_init_normal_figure(cohort, cohort_path)
            if self.control['Initialize_Control'][
                        'Initial_Cohort_Distribution_Figure'
                     ] and\
                     self.control['Initialize_Control'][figure] and \
                     figure.lower().find('figure') > 0:
                self.grids.area.save_init_dist_figure(cohort, cohort_path)
                    
            
        init_path = os.path.join( outdir, 'Initialization')
        try: 
            os.makedirs(init_path)
        except:
            pass
            
        print "  -- Terrestrial Figures"
        print "    -- Ice_Distribution_Figure"
        if self.control['Terrestrial_Control']['Ice_Distribution_Figure']:
            self.grids.ice.figure(
                os.path.join(init_path,'Ground_Ice_Content.png')
            )
            self.grids.ice.binary(
                os.path.join(init_path,'Ground_Ice_Content.bin')
            )
        print "    -- Drainage_Efficiency_Figure"
        if self.control['Terrestrial_Control']['Drainage_Efficiency_Figure']:
            self.grids.drainage.figure(
                os.path.join(init_path,'Drainage_efficiency.png')
            )
            self.grids.drainage.binary(
                os.path.join(init_path,'Drainage_efficiency.bin')
            )
        
        print "    -- ALD_Distribution_Output"
        if self.control['Terrestrial_Control']['ALD_Distribution_Output']:
            self.grids.ald.init_ald_figure(
                os.path.join(init_path,'Initial_ALD.png')
            )
            self.grids.ald.init_ald_binary(
                os.path.join(init_path,'Initial_ALD.bin')
            )
        print "    -- ALD_Factor_Output"
        if self.control['Terrestrial_Control']['ALD_Factor_Output']:
            self.grids.ald.ald_constants_figure(
                os.path.join(init_path,'Active_Layer_Factor.png')
            )
            self.grids.ald.ald_constants_binary(
                os.path.join(init_path,'Active_Layer_Factor.bin')
            )
        
        dom_path = os.path.join( outdir, 'All_cohorts', 'year_cohorts')
        try: 
            os.makedirs(dom_path)
        except:
            pass
        
        print "    -- Dominant Cohort Figure"
        if self.control['Terrestrial_Control']['Figure']:
            vid = self.control['Terrestrial_Control']['Movie']
            self.grids.area.dominate_cohort_timeseries( dom_path, vid)
        
        
        
        print "  -- Met Figures"  
        print "    -- Degree Days"
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
            
            self.grids.degreedays.thawing.figures(
                    os.path.join(dd_path, tdd), (0, 1250)
                )
            self.grids.degreedays.freezing.figures(
                    os.path.join(dd_path, fdd), (-6000, -2000)
                )
            
        
        lp_types = \
                self.control['_FAST_get_pond_type'] +\
                self.control['_FAST_get_lake_type']   
        print "  -- Lake Pond Figures"
        for figure in self.control['Lake_Pond_Control']:

            lpt = '_'.join(figure.split('_')[:-2])
            #~ print lpt, lp_types
            if lpt not in lp_types:
                continue 
            
            print "    -- " + lpt + ' Depth'
            path = os.path.join(outdir, lpt)
            try: 
                os.makedirs(path)
            except:
                pass
            self.grids.lake_pond.depth_figure(
                lpt, os.path.join(path,'Initial_'+lpt+'_Depth.png') , 1
            )
        
        print "  -- Cohort Figures/Video"
        for control in sorted(self.control['cohorts']):
            if type(self.control['cohorts'][control]) is str:
                continue
            if not self.control['cohorts'][control]['Figures']:
                continue
            
            cohort = '_'.join(control.split('_')[:-1])
            path = os.path.join(outdir, cohort, 'year_cohorts')
            try: 
                os.makedirs(path)
            except:
                pass
            vid = self.control['cohorts'][control]['Movie']
            print "    -- " + cohort + " Figures/Video"
            self.grids.area.save_cohort_timeseries(cohort, path, vid)
            
        
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
            
            
    def on_screen(self, start_time, end_time):
        """print results on screan
        
        Parameters
        ----------
        start_time: datetime.datetime
        end_time: datetime.datetime
        """
        r = results.construnct_results(self, start_time, end_time)
        print r
    
    def on_file(self,name, start_time, end_time):
        """save results to file
        
        Parameters
        ----------
        start_time: datetime.datetime
        end_time: datetime.datetime
        """
        r = results.construnct_results(self, start_time, end_time)
    
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


        start_time = datetime.datetime.now()
        
    
        print '=================================================='
        print '            Starting the MAIN LOOP '
        print '=================================================='


            
        self.run_model(self.control['Transition_order'])


        print '=================================================='
        print '            Finished the MAIN LOOP '
        print '=================================================='


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
            self.on_screen(start_time, end_time)
        if self.control['Archive_simulation'] or \
                self.control['Archive_simulation'].lower() == 'yes':
            name = t +'_' +self.control['Simulation_name'] + '.txt'
            self.on_file(name, start_time, end_time)
        
        print("The save figures feature must be re-enabled before 0.5.0 is ready")
        # self.save_figures()

        name = t +'_' + self.control['Simulation_name'] +".tar.gz"
        self.archive(name)

        print '----------------------------------------'
        print '        Simulation Complete             '
        print '----------------------------------------'        

    def run_model(self, cohort_list):
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
        

        for time in range(1, self.stop):

            print '    at time step: ', time
            
            current_year = init_year + time

            cohort_start = \
                self.grids.area.get_all_cohorts_at_time_step().sum(0)
                
    
                ### Loop through each of the cohort checks for area
                #~ active_layer_depth.active_layer_depth(self, time, element)
            self.grids.climate_event.create_climate_events()
                
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
           
            
            # for cohort in cohort_list:
            #     print cohort
            
            #     plt.imshow(self.grids.area[cohort, current_year-1])
            #     plt.show()
            #     plt.imshow(self.grids.area[cohort, current_year])
            #     plt.show()

            ## transition list
            for cohort in cohort_list:
                # print cohort
            
                # plt.imshow(self.grids.area[cohort, current_year-1])
                # plt.show()
                # plt.imshow(self.grids.area[cohort, current_year])
                # plt.show()
                cohort_control = cohort + '_Control'
                try:
                    check_type = \
                        self.control['cohorts'][cohort_control]\
                        ['Transition_check_type'].lower()
                except KeyError as e:
                    #~ print e    
                    check_type = 'base'

                name = find_canon_name(cohort)
                # print "main", current_year,hex(id(self.grids['area'])),hex(id(self.grids.area[name,current_year-1]))
                # plt.imshow(self.grids.area[cohort, current_year-1])
                # plt.show()
                cc = self.control['cohorts'][name + '_Control']
                # if cc['Transition_check_type'].lower() == 'poi' and cc['POI_Function'].lower() == "hill":
                #     year = current_year
                #     from_cohort_a0 = self.grids.area[name + '--0', year]
                #     from_cohort = self.grids.area[name, year]
                #     transitions_to = cc['transitions_to']
                #     to_cohort_a0 = self.grids.area[transitions_to + '--0', year]
                #     to_cohort = self.grids.area[transitions_to + '--0', year]
                #     ice_slope = self.grids.ice.get_ice_slope_grid( name ).reshape(self.grids.shape)
                #     ALD, PL = self.grids.ald['ALD', year], self.grids.ald[name ,year] 
                #     AOI = self.grids.area.area_of_interest()
                #     POIn = self.grids.poi[name, year]
                #     POInm1 = self.grids.poi[name, year-1]
                #     drainage = self.grids.drainage.grid.reshape(self.grids.shape)
                #     above_idx = drainage == 'above'
                #     porosity = self.grids.ald.porosity[name]
                #     params = np.array([
                #         cc['Parameters']['above']['hill_B'],
                #         cc['Parameters']['above']['hill_N'],
                #         cc['Parameters']['below']['hill_B'],
                #         cc['Parameters']['below']['hill_N'],
                #     ])
                #     max_rot = cc['max_terrain_transition']

                #     checks.poi_based_hill.transition(
                #         from_cohort, from_cohort_a0, to_cohort, to_cohort_a0, 
                #         ice_slope, ALD, PL, AOI, POIn, POInm1, 
                #         above_idx, porosity, params, max_rot
                #     )
                if cc['Transition_check_type'].lower() == 'poi' and cc['POI_Function'].lower() == "sigmoid2":
                    year = current_year
                    from_cohort_a0 = self.grids.area[name + '--0', year]
                    from_cohort = self.grids.area[name, year]
                    transitions_to = cc['transitions_to']
                    to_cohort_a0 = self.grids.area[transitions_to + '--0', year]
                    to_cohort = self.grids.area[transitions_to + '--0', year]
                    ice_slope = self.grids.ice.get_ice_slope_grid( name ).reshape(self.grids.shape).astype(np.float32)
                    ALD, PL = self.grids.ald['ALD', year], self.grids.ald[name ,year] 
                    AOI = self.grids.area.area_of_interest()
                    POIn = self.grids.poi[name, year]
                    POInm1 = self.grids.poi[name, year-1]
                    drainage = self.grids.drainage.grid.reshape(self.grids.shape)
                    above_idx = drainage == 'above'
                    porosity = self.grids.ald.porosity[name]
                    params = np.array([
                        cc['Parameters']['above']['sigmoid2_K'],
                        cc['Parameters']['above']['sigmoid2_C'],
                        cc['Parameters']['above']['sigmoid2_A'],
                        cc['Parameters']['above']['sigmoid2_B'],
                        cc['Parameters']['below']['sigmoid2_K'],
                        cc['Parameters']['below']['sigmoid2_C'],
                        cc['Parameters']['below']['sigmoid2_A'],
                        cc['Parameters']['below']['sigmoid2_B'],
                    ])
                    max_rot = cc['max_terrain_transition']

                    checks.poi_based_sigmoid2_jit.transition(
                        from_cohort, from_cohort_a0, to_cohort, to_cohort_a0, 
                        ice_slope, ALD, PL, AOI, POIn, POInm1, 
                        above_idx, porosity, params, max_rot
                    )
                else:
                    checks.check_metadata[check_type](
                        name,  current_year, self.grids, self.control
                    )
                # plt.imshow(self.grids.area[cohort, current_year-1])
                # plt.show()
                # plt.imshow(self.grids.area[cohort, current_year])
                # plt.show()

            lake_pond_expansion.expansion(
                lp_types, current_year, self.grids, self.control
            )
            lake_pond_expansion.infill(
                pond_types, current_year, 
                self.grids, self.control
            )
                

            # for cohort in cohort_list:
            #     print cohort
            
            #     plt.imshow(self.grids.area[cohort, current_year-1])
            #     plt.show()
            #     plt.imshow(self.grids.area[cohort, current_year])
            #     plt.show()



            cohort_end = \
                self.grids.area.get_all_cohorts_at_time_step().sum(0)
            
            diff = abs(cohort_start - cohort_end)
           
            #~ ## check mass balance, MOVE to function?
            if (diff > 0.1).any():
                # import pickle
                print "here"
                
                # with open('err.pkl','wb') as e:
                #     pickle.dump(self.grids, e )
                
                location = np.where(diff > 0.1)[0]
                print ('Mass Balance change greater thatn 10 % in '
                        ''+ str(len(location)) + ' cells ')
                
                
                print location
                print 'start: ', cohort_start[location[0]]
                print 'end: ', cohort_end[location[0]]
                
                sys.exit()
                
                ## to do add frist cell report
            try:
                self.grids.area.check_mass_balance()
                self.grids.area.check_mass_balance(current_year - init_year)
            except area_grid.MassBalanceError as e:
                #~ print e
                if str(e) == 'mass balance problem 1':
                    print 'mass has been added'
                    print 'start: ', cohort_start.sum()
                    print 'end: ', cohort_end.sum()
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
                        print cohort, 'start:', s, 'end:', e, d
                else:
                    print 'mass has been removed'
                sys.exit()
                        
                
    
        
        
        print 'start: ', cohort_start.sum()
        print 'end: ', cohort_end.sum()
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
            print cohort, 'start:', s, 'end:', e, d
            
#_______________________________________________________________________________

## runs model from comand line
if __name__ == "__main__":
    Variable = ATM(sys.argv[1])
