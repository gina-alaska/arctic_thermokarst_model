#!/usr/bin/env python

"""
________________________________________________________________________________
Alaska Landscape Evolution Model (ALEM)
________________________________________________________________________________
The purpose of this script is to provide a protype source
code for testing and development of the Alaska Landscape
Evolution Model (ALEM) to be integrated into the Alaska Integrated
Ecosystem Model (IEM).  The ALEM is reworked code from the Alaska
Thermokarst Model (ATM) in an effort to consolidate the various
test regions and sets of code.   
________________________________________________________________________________
Created: May 2017. Bob Bolton
Modified: 
________________________________________________________________________________
The ALEM code is python based and is executed with the following command:
$ python ATM.py <control file name>

The control file is used to set up the simulation input/output locations,
defines the model domain, etc.
________________________________________________________________________________

"""

################################################################################
# Authorship
################################################################################
__author__     = "Bob Bolton"
__copyright__  = "Copyright 2017, Bob Bolton"
__credits__    = ["Bob Bolton", "Vladimir Romanovsky", "Dave McGuire", "IEM Thermokarst Team"]
__license__    = "GPL"
__version__    = "0.1"
__maintainer__ = "Bob Bolton"
__email__      = "bbolton@iarc.uaf.edu"
__status__     = "Development"

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


# Import ALEM Modules
import clock
import read_control
import read_met_data
import read_degree_days
import calc_degree_days
import read_layers
import model_domain
import create_attm_cohort_arrays
import run_barrow
import run_tanana
import run_yukon
import initialize

import Output_cohorts_by_year
import results
import archive
#=================================================================================
class ALEM(object):

    Control_file        = sys.argv[1]
 
    def __init__(self):
        #_______________________
        # Simulation Start Time
        #-----------------------
        faulthandler.enable()
        clock.start(self)
        
        #______________________________________
        # Read the Control File for Simulation
        #--------------------------------------
        self.Control_file     = sys.argv[1]
        
        #_________________________
        # Execute the ALEM script
        #-------------------------
        self.run_alem()
#==================================================================================
    def run_alem(self):
        """
        _________________
        Program sequence:
        -----------------
        Initialization
        -- ALEM needs
        -- Model domain
        -- Meteorologic data
        -- Terrestrial properties
        -- Non-terrestrial properties
        Main Loop
        -- Landscape evolution
        -- Ecotype change
        Output Results
        -- Output data (data files, figures, animations)
        -- Archive Results
        """

        #___________________________
        """ INITIALIZE ALEM """
        #---------------------------
        print '====================='
        print ' Initializing ALEM '
        print '====================='
        read_control.read_alem_control(self)
#_______________________________________________________________________________
Variable = ALEM()
