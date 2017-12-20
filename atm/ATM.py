 #!/usr/bin/env python
"""
________________________________________________________________________________
Alaska Thermokarst Model (ATM)
________________________________________________________________________________
The purpose of this script is to provide a protype source
code for testing and development of the Alaska Thermokarst
Model (ATM) to be integrated into the Alaska Integrated
Ecosystem Model (AIEM).
________________________________________________________________________________
Created: May 2014. Bob Bolton
Modified: October 2015. Bob Bolton.
          Incorporating Tanana Flats Frames & Logic

________________________________________________________________________________

The ATM code is python based and is executed with the following command:
$ python ATM.py <control file name>

The control file is used to set up the simulation input/output locations,
defines the model domain, etc.
________________________________________________________________________________

"""

################################################################################
# Authorship moved to __init__.py
################################################################################


################################################################################
# Required Modules
################################################################################
import numpy as np
import gdal, os, sys, glob, random, time, datetime
from gdalconst import *
from osgeo import *
import pylab as pl
import xlrd, xlwt
from scipy import interpolate
from scipy import integrate
import subprocess
import tarfile
import faulthandler


# Import ATM Modules
import clock
#~ import read_control
import read_met_data
import read_degree_days
import calc_degree_days
import read_layers
import model_domain
import create_attm_cohort_arrays
## still needed for initilzation stuff
import run_barrow
import run_tanana
import run_yukon
import initialize

## new way of running model
import run_general 
from cohorts import initial_barrow, initial_tanana

import Output_cohorts_by_year
import results
import archive


from control import Control
from grids.grids import ModelGrids
#_______________________________________________________________________________
class ATM(object):

    # TODO contoll file IO out of ATM class
    #~ Control_file        = sys.argv[1]
 
    def __init__(self, control_file):
        # ----------------------
        # Simulation Start Time
        # ----------------------
        
        self.control = Control(control_file)
        from pprint import pprint
        print pprint(self.control.init_control)
        print 'Control loaded'
        
        faulthandler.enable()
        clock.start(self)
        
        
        self.grids = ModelGrids(self.control)
        #--------------------------------------
        # Read the Control File for Simulation
        #--------------------------------------
        #~ self.Control_file     = sys.argv[1]
        
        ## srt up # time steps
        if self.control.Test_code or \
                str(self.control.Test_code).lower() == 'yes':
            self.stop = self.control.Test_code_duration
        else:
            self.stop = int(self.grids.get_max_time_steps())
        
        ########################################################################
        # Execute the script
        ########################################################################
        self.run_atm()
        
    def save_figures(self):
        """
        """
        
        print "Finishing up -- saving figures"
        
        outdir = self.control.Output_dir
        
        print "  -- Initial Figures"
        for figure in self.control.Initialize_Control:
            cohort = '_'.join(figure.split('_')[:-1])
            if cohort not in self.grids.area.get_cohort_list():
                continue              
            cohort_path = os.path.join(outdir, cohort)
            try: 
                os.makedirs(cohort_path)
            except:
                pass
            
            if self.control.Initialize_Control['Initial_Cohort_Age_Figure'] and\
                     self.control.Initialize_Control[figure] and \
                     figure.lower().find('age') > 0:
                self.grids.area.save_init_age_figure(cohort, cohort_path)
            if self.control.Initialize_Control[
                        'Normalized_Cohort_Distribution_Figure'
                     ] and\
                     self.control.Initialize_Control[figure] and \
                     figure.lower().find('normal') > 0:
                self.grids.area.save_init_normal_figure(cohort, cohort_path)
            if self.control.Initialize_Control[
                        'Initial_Cohort_Distribution_Figure'
                     ] and\
                     self.control.Initialize_Control[figure] and \
                     figure.lower().find('figure') > 0:
                self.grids.area.save_init_dist_figure(cohort, cohort_path)
                    
            
        
        #~ img = self.grids.area[1900, 'CLC_WT_Y']
        #~ plt.imshow(img,cmap='bone')
        #~ plt.colorbar( extend = 'max', shrink = 0.92)
        #~ plt.show()
            
            
        #~ for key in self.control.Terrestrial_Control:
        init_path = os.path.join( outdir, 'Initialization')
        try: 
            os.makedirs(init_path)
        except:
            pass
            
        print "  -- Terrestrial Figures"
        print "    -- Ice_Distribution_Figure"
        if self.control.Terrestrial_Control['Ice_Distribution_Figure']:
            self.grids.ice.figure(
                os.path.join(init_path,'Ground_Ice_Content.png')
            )
            self.grids.ice.binary(
                os.path.join(init_path,'Ground_Ice_Content.bin')
            )
        print "    -- Drainage_Efficiency_Figure"
        if self.control.Terrestrial_Control['Drainage_Efficiency_Figure']:
            self.grids.drainage.figure(
                os.path.join(init_path,'Drainage_efficiency.png')
            )
            self.grids.drainage.binary(
                os.path.join(init_path,'Drainage_efficiency.bin')
            )
        
        print "    -- ALD_Distribution_Output"
        if self.control.Terrestrial_Control['ALD_Distribution_Output']:
            self.grids.ald.init_ald_figure(
                os.path.join(init_path,'Initial_ALD.png')
            )
            self.grids.ald.init_ald_binary(
                os.path.join(init_path,'Initial_ALD.bin')
            )
        print "    -- ALD_Factor_Output"
        if self.control.Terrestrial_Control['ALD_Factor_Output']:
            self.grids.ald.ald_constants_figure(
                os.path.join(init_path,'Active_Layer_Factor.png')
            )
            self.grids.ald.ald_constants_binary(
                os.path.join(init_path,'Active_Layer_Factor.bin')
            )
        
        
        
        print "  -- Met Figures"  
        print "    -- Degree Days"
        dd_path = os.path.join( outdir, 'Initialization', 'Degree_Days')
        try: 
            os.makedirs(dd_path)
        except:
            pass
        if self.control.Met_Control['Degree_Day_Output']:
            tdd = self.control.Met_Control['TDD_Output']
            try: 
                os.makedirs(os.path.join(dd_path, tdd))
            except:
                pass
            fdd = self.control.Met_Control['FDD_Output']
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
                self.control.get_pond_types() + self.control.get_lake_types()    
        print "  -- Lake Pond Figures"
        for figure in self.control.Lake_Pond_Control:

            lpt = '_'.join(figure.split('_')[:-2])
            #~ print lpt, lp_types
            if lpt not in lp_types:
                continue 
            
            print "    -- " + lpt + ' Depth'
            path = os.path.join(outdir, lpt)
            try: 
                os.makedirs(cohort_path)
            except:
                pass
            self.grids.lake_pond.depth_figure(
                lpt, os.path.join(path,'Initial_'+lpt+'_Depth.png') , 1
            )
        
        print "Cohort =============="
        for control in self.control.init_control['Cohorts']:
            if control.lower().find('control') == -1:
                continue
            if control == 'Initialize_Control':
                continue
            for key in self.control['Cohorts'][control]:
                if key.lower().find('figure') == -1:
                    continue
                print control, key, self.control['Cohorts'][control][key]
        
        
#_______________________________________________________________________________
    def run_atm(self):
        
        """ Program sequence """
        #====================================================
        # Initialization Process
        #====================================================
        print '==================='
        print ' Initializing ATM'
        print '==================='
        start_time = datetime.datetime.now()
        ## haneled in control and grids
        #~ read_control.read_control(self)
        #~ initialize.initialize(self)
        #~ read_layers.read_layers(self)
        #~ model_domain.model_domain(self)
        #~ create_attm_cohort_arrays.create_attm_cohort_arrays(self)

        


        #=========================================
        # Initializing Site Specific Information
        #=========================================
        
        ## handeled in grids
        #~ if self.control['Simulation_area'].lower() == 'barrow':
            #~ run_barrow.initialize_barrow(self)
        #~ elif self.control['Simulation_area'].lower() == 'tanana':
            #~ run_tanana.initialize_tanana(self)
        #~ elif self.control['Simulation_area'].lower() == 'yukon':
            #~ run_yukon.initialize_yukon(self)
         
        
        #=======================================
        # READ MET Data, Calculate Degree Days,
        # and Calculate Climatic Data needed
        # for ecotype changes.
        #=======================================
        #~ initialize.Met(self)

        #++++++++++++++++++++++++++++++++++++++++++++++
        #  ========================================
        #    INITIALIZE COHORT PROPERTIES
        #  ========================================
        #++++++++++++++++++++++++++++++++++++++++++++++
        
        ## ** most of this happes in the Cotrol object
    	print '======================================'
        print ' Initializing Terrestrial Properties '
        print '======================================'
        #~ if self.control['Simulation_area'].lower() == 'barrow':
            #~ run_barrow.initialize_barrow_cohorts(self)
        #~ elif self.control['Simulation_area'].lower() == 'tanana':
            #~ run_tanana.Terrestrial_Tanana(self)
        ## **
        
        print '=================================================='
        print '            Starting the MAIN LOOP '
        print '=================================================='

        ## this should be renamed, to set_end or somthing
        
        #~ initialize.run(self)
        
        
        if self.control['Simulation_area'].lower() == 'barrow':
            ## move to else where
            barrow_checks = [ 
                #~ 'lake_pond_expansion', 'pond_infill', 
                'Meadow_WT_Y', 'Meadow_WT_M', 'Meadow_WT_O',
                'LCP_WT_Y', 'LCP_WT_M', 'LCP_WT_O',
                'CLC_WT_Y', 'CLC_WT_M', 'CLC_WT_O',
                'FCP_WT_Y', 'FCP_WT_M', 'FCP_WT_O',
                'HCP_WT_Y', 'HCP_WT_M', 'HCP_WT_O',
                'Ponds_WT_Y', 'Ponds_WT_M', 'Ponds_WT_O',
                'LargeLakes_WT_Y', 'LargeLakes_WT_M', 
                    'LargeLakes_WT_O',
                'MediumLakes_WT_Y', 'MediumLakes_WT_M', 
                    'MediumLakes_WT_O',
                'SmallLakes_WT_Y', 'SmallLakes_WT_M', 
                    'SmallLakes_WT_O',
            ] 
            
            run_general.run(self, barrow_checks, initial_barrow)
        elif self.control['Simulation_area'].lower() == 'tanana':
            tanana_checks = []
            run_general.run(self, tanana_checks, initial_tanana)

        print '=================================================='
        print '            Finished the MAIN LOOP '
        print '=================================================='


        # -------------------
        # Simulation End Time
        # -------------------
        clock.finish(self)
        end_time = datetime.datetime.now()
        #===========================
        # Output Simulation Results
        #===========================
        if self.control['Results_onscreen'] or \
                self.control['Results_onscreen'].lower() == 'yes':
            results.on_screen(self, start_time, end_time)
        if self.control.Archive_simulation or \
                self.control.Archive_simulation.lower() == 'yes':
            results.on_file(self, start_time, end_time)
            
        self.save_figures()

        
        # ================
        # Archive Results
        # ================
        #~ if self.control.Archive_simulation.lower() == 'yes':
            #~ archive.read_archive(self)
            #~ archive.archive(self)
        #~ #----------------------------------------------------------------------------------------------------------
        #~ # Create the tarfile
        #~ #----------------------------------------------------------------------------------------------------------
            #~ self.archive_file =tarfile.open(self.control['Run_dir']+self.Output_directory+str('/Archive/')+ \
                                            #~ self.archive_time+str('_')+self.simulation_name+".tar.gz", mode='w:gz')
        #~ #----------------------------------------------------------------------------------------------------------
            #~ if self.control['Simulation_area'].lower() == 'barrow':
                #~ os.chdir(self.control['Run_dir']+self.Input_directory+'/Barrow/')
                

            
        print '----------------------------------------'
        print '        Simulation Complete             '
        print '----------------------------------------'        
        
#_______________________________________________________________________________



Variable = ATM(sys.argv[1])
