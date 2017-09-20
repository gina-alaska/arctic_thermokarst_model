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
import read_control
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
#_______________________________________________________________________________
class ATM(object):

    # TODO contoll file IO out of ATM class
    Control_file        = sys.argv[1]
 
    def __init__(self):
        # ----------------------
        # Simulation Start Time
        # ----------------------
        faulthandler.enable()
        clock.start(self)
        
        #--------------------------------------
        # Read the Control File for Simulation
        #--------------------------------------
        self.Control_file     = sys.argv[1]
        
        ########################################################################
        # Execute the script
        ########################################################################
        self.run_atm()
#_______________________________________________________________________________
    def run_atm(self):
        
        """ Program sequence """
        #====================================================
        # Initialization Process
        #====================================================
        print '==================='
        print ' Initializing ATM'
        print '==================='
        
        ### ICK
        read_control.read_control(self)
        initialize.initialize(self)
        read_layers.read_layers(self)
        model_domain.model_domain(self)
        create_attm_cohort_arrays.create_attm_cohort_arrays(self)


        #=========================================
        # Initializing Site Specific Information
        #=========================================
        if self.Simulation_area.lower() == 'barrow':
            run_barrow.initialize_barrow(self)
        elif self.Simulation_area.lower() == 'tanana':
            run_tanana.initialize_tanana(self)
        elif self.Simulation_area.lower() == 'yukon':
            run_yukon.initialize_yukon(self)
         
        #=======================================
        # READ MET Data, Calculate Degree Days,
        # and Calculate Climatic Data needed
        # for ecotype changes.
        #=======================================
        initialize.Met(self)

        #++++++++++++++++++++++++++++++++++++++++++++++
        #  ========================================
        #    INITIALIZE COHORT PROPERTIES
        #  ========================================
        #++++++++++++++++++++++++++++++++++++++++++++++
    	print '======================================'
        print ' Initializing Terrestrial Properties '
        print '======================================'
        if self.Simulation_area.lower() == 'barrow':
            run_barrow.initialize_barrow_cohorts(self)
        elif self.Simulation_area.lower() == 'tanana':
            run_tanana.Terrestrial_Tanana(self)

        print '=================================================='
        print '            Starting the MAIN LOOP '
        print '=================================================='

        initialize.run(self)
        if self.Simulation_area.lower() == 'barrow':
            ## move to else where
            barrow_checks = [ 
                'lake_pond_expansion', 'pond_infill', 
                'Meadow_WT_Y', 'Meadow_WT_M', 'Meadow_WT_O',
                'LCP_WT_Y', 'LCP_WT_M', 'LCP_WT_O',
                'CLC_WT_Y', 'CLC_WT_M', 'CLC_WT_O',
                'FCP_WT_Y', 'FCP_WT_M', 'FCP_WT_O',
                'HCP_WT_Y', 'HCP_WT_M', 'HCP_WT_O',
                'check_Ponds_WT_Y', 'check_Ponds_WT_M', 'check_Ponds_WT_O',
                'check_LargeLakes_WT_Y', 'check_LargeLakes_WT_M', 
                    'check_LargeLakes_WT_O',
                'check_MediumLakes_WT_Y', 'check_MediumLakes_WT_M', 
                    'check_MediumLakes_WT_O',
                'check_SmallLakes_WT_Y', 'check_SmallLakes_WT_M', 
                    'check_SmallLakes_WT_O',
            ] 
            
            run_general.run(self, barrow_checks, initial_barrow)
        elif self.Simulation_area.lower() == 'tanana':
            tanana_checks = []
            run_general.run(self, tanana_checks, initial_tanana)

        print '=================================================='
        print '            Finished the MAIN LOOP '
        print '=================================================='


        # -------------------
        # Simulation End Time
        # -------------------
        clock.finish(self)
        
        #===========================
        # Output Simulation Results
        #===========================
        if self.results_onscreen.lower() == 'yes':
            results.on_screen(self)
        if self.archive_simulation.lower() == 'yes':
            results.on_file(self)

        
        # ================
        # Archive Results
        # ================
        if self.archive_simulation.lower() == 'yes':
            archive.read_archive(self)
            archive.archive(self)
        #----------------------------------------------------------------------------------------------------------
        # Create the tarfile
        #----------------------------------------------------------------------------------------------------------
            self.archive_file =tarfile.open(self.control['Run_dir']+self.Output_directory+str('/Archive/')+ \
                                            self.archive_time+str('_')+self.simulation_name+".tar.gz", mode='w:gz')
        #----------------------------------------------------------------------------------------------------------
            if self.Simulation_area.lower() == 'barrow':
                os.chdir(self.control['Run_dir']+self.Input_directory+'/Barrow/')
                

            
        print '----------------------------------------'
        print '        Simulation Complete             '
        print '----------------------------------------'        
        
#_______________________________________________________________________________
Variable = ATM()
