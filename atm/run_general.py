#! /usr/bin/env python

"""
The purpose of this script is to self-contain all
of the initialization processes for the Barrow
Peninsula simulations in order to keep the ATM
code clean.
"""
import numpy as np

#---------------------------------------------------------------------
import active_layer_depth
import check_climate_event
#~ #from checks import check_Lakes
#~ #from checks import check_Ponds
#~ from checks import check_Lakes_WT
#~ from checks import check_Ponds_WT
#~ from checks import check_Meadow_WT
#~ from checks import check_LCP_WT
#~ from checks import check_CLC_WT
#~ from checks import check_FCP_WT
#~ from checks import check_HCP_WT
import checks
import climate_expansion_arrays
import cohorts
import cohort_check
import cohort_present
import ice_thickness
import initial_cohort_age
import initial_cohort_check
import initial_cohort_population
import initialize
import lake_pond_expansion
import Output_cohorts_by_year
import read_drainage_efficiency
import read_ice_content
import read_initial_ALD
import set_ALD_array
import set_ALD_constant
import set_ice_thickness_array
import set_initial_cumulative_probability
import set_lake_ice_depth_constant
import set_lake_pond_depth
import set_pond_growth_array
import set_protective_layer

#=====================================================================
def initialize_barrow(self):
    initial_cohort_population.barrow_initial_cohort_population(self)
    initial_cohort_check.barrow_initial_cohort_check(self)
    cohort_present.barrow_cohort_present(self)
#---------------------------------------------------------------------
def initialize_barrow_cohorts(self):
    print '=================================== '
    print ' Initializing Lake & Pond Properties'
    print '===================================='
    initialize.LakePond(self)
    set_lake_pond_depth.set_lake_pond_depth(self)
    set_lake_ice_depth_constant.set_lake_ice_depth_constant(self)
    set_ice_thickness_array.set_ice_thickness_array(self)
    climate_expansion_arrays.set_climate_expansion_arrays(self)
    set_pond_growth_array.set_pond_growth_array(self)
    print '====================================='
    print ' Initializing Terrestrial Properties'
    print '====================================='
    initialize.Terrestrial_Barrow(self)
    read_ice_content.read_ice_content(self)
    read_drainage_efficiency.read_drainage_efficiency(self)
    read_initial_ALD.read_initial_ALD(self)
    set_ALD_constant.set_ALD_constant(self)
    set_ALD_array.set_ALD_array(self)
    set_protective_layer.set_protective_layer(self)
    set_initial_cumulative_probability.set_initial_cumulative_probability(self)
    # Initializing Terrestrial Cohort Properties
    initialize.CLC_WT(self)
    initialize.CoastalWaters_WT(self)
    initialize.DrainedSlope_WT(self)
    initialize.FCP_WT(self)
    initialize.HCP_WT(self)
    initialize.LCP_WT(self)
    initialize.Meadow_WT(self)
    initialize.NoData_WT(self)
    initialize.SandDunes_WT(self)
    initialize.SaturatedBarrens_WT(self)
    initialize.Shrubs_WT(self)
    initialize.Urban_WT(self)
    initial_cohort_age.initial_cohort_age(self)
#---------------------------------------------------------------------

barrow = [ 
    'lake_pond_expansion', 'pond_infill', 
    'Meadow_WT_Y', 'Meadow_WT_M', 'Meadow_WT_O',
    'LCP_WT_Y','LCP_WT_M','LCP_WT_O',
    'CLC_WT_Y', 'CLC_WT_M', 'CLC_WT_O',
    'FCP_WT_Y', 'FCP_WT_M', 'FCP_WT_O',
    'HCP_WT_Y', 'HCP_WT_M', 'HCP_WT_O',
    'check_Ponds_WT_Y', 'check_Ponds_WT_M', 'check_Ponds_WT_O',
    'check_LargeLakes_WT_Y', 'check_LargeLakes_WT_M', 'check_LargeLakes_WT_O',
    'check_MediumLakes_WT_Y', 'check_MediumLakes_WT_M', 'check_MediumLakes_WT_O',
    'check_SmallLakes_WT_Y', 'check_SmallLakes_WT_M', 'check_SmallLakes_WT_O',
] 

def run(self, cohort_check_list, init_function):
    """
    cohort_list ordered list of cohorsts to run
    """
    
    
    for time in range(0, self.stop):
        if time == 0:
            ## TODO fix this
            init_function(self)
        print '    at time step: ', time
        
        # ++++++++++++++++++++++++++++++++++++++
        # Check for significant climatic event
        # ++++++++++++++++++++++++++++++++++++++
        check_climate_event.check_climate_event(self)  

        # ----------------------------------------------------------
        # Looping over elements
        # ----------------------------------------------------------
        for element in range(0, self.ATTM_nrows * self.ATTM_ncols):
            #### NEW IDEA
            ## for cohort in cohort_list:
            ##      cohorts[cohort](self, element, time)
            ##      ## run checks in Y,M,O,NA order, where each check function 
            ##      ## for age data masks out data without age data,
            ##      ## and vice versa 
            ###
            #### ALSO remove the element argument if possible,
            #### it should be possible to do these things Array by array

            # ----------------------------------------------------
            # Define the total fractional area of cohorts for
            # each element
            # ----------------------------------------------------
            cohort_start = cohort_check.cohort_start(self, element, time)

            ### Loop through each of the cohort checks for area
            active_layer_depth.active_layer_depth(self, time, element)
            ice_thickness.ice_thickness(self, time, element)
            
            for check in cohort_check_list:
                checks.cohort_metadata[check](self, element, time)
            
            cohort_check.cohort_check(self, element, time, cohort_start)

            # NOTE: Just do this outside of loop
            if time == self.stop -1:
                cohorts.final_barrow(self)
            # ========================================================================
            # END MAIN LOOP 
            # ========================================================================
        # ========================================================================
        # OUTPUT RESULTS (if requested)
        # ========================================================================
        #  - - - - - - - - -
        # Fractional Areas
        #  - - - - - - - - -
        Output_cohorts_by_year.Output_cohorts_by_year(self, time)
        #  - - - - - - - - - - - - -
        # Dominant Fractional Area
        #  - - - - - - - - - - - - - 
        Output_cohorts_by_year.dominant_cohort(self)                 # Terrestrial_Control
        Output_cohorts_by_year.dominant_fractional_plot(self, time)  # Terrestrial_Control

    # =================================
    # OUTPUT ANIMATIONS (if requested)
    # =================================
    # - - - - - - - - - - - - - - -
    # Fractional Area of Cohorts
    # - - - - - - - - - - - - - - - -
    Output_cohorts_by_year.write_Fractions_avi(self)
    Output_cohorts_by_year.write_Dominant_Cohort_avi(self) # Terrestrial_Control
#---------------------------------------------------------------------
