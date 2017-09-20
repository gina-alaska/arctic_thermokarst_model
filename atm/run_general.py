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
#~ from checks import check_climate_event
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
def run(self, cohort_list):
    """
    cohort_list ordered list of cohorsts to run
    """
    cohorts = { 

        'lake_pond_expansion': lake_pond_expansion.lake_pond_expansion,
        'pond_infill': lake_pond_expansion.pond_infill,

        'active_layer_depth': active_layer_depth.active_layer_depth,

        ### terrestrial cohorts
        'Meadow_WT_Y': checks.check_Meadow_WT.check_Meadow_WT_Y
        'Meadow_WT_M': checks.check_Meadow_WT.check_Meadow_WT_M,
        'Meadow_WT_O': checks.check_Meadow_WT.check_Meadow_WT_O,
        'Meadow_WT_NA': checks.check_Meadow_WT.check_Meadow_WT_NA,
        
        'LCP_WT_Y': checks.check_LCP_WT.check_LCP_WT_Y,
        'LCP_WT_M': checks.check_LCP_WT.check_LCP_WT_M,
        'LCP_WT_O': checks.check_LCP_WT.check_LCP_WT_O,
        'LCP_WT_NA': checks.check_LCP_WT.check_LCP_WT_NA,
        
        'CLC_WT_Y': checks.check_CLC_WT.check_CLC_WT_Y,
        'CLC_WT_M': checks.check_CLC_WT.check_CLC_WT_M,
        'CLC_WT_O': checks.check_CLC_WT.check_CLC_WT_O,
        'CLC_WT_NA': checks.check_CLC_WT.check_CLC_WT_NA,
        
        'FCP_WT_Y': checks.check_FCP_WT.check_FCP_WT_Y,
        'FCP_WT_M': checks.check_FCP_WT.check_FCP_WT_M,
        'FCP_WT_O': checks.check_FCP_WT.check_FCP_WT_O,
        'FCP_WT_NA': checks.check_FCP_WT.check_FCP_WT_NA,
        
        'HCP_WT_Y': checks.check_HCP_WT.check_HCP_WT_Y,
        'HCP_WT_M': checks.check_HCP_WT.check_HCP_WT_M,
        'HCP_WT_O': checks.check_HCP_WT.check_HCP_WT_O,
        'HCP_WT_NA': checks.check_HCP_WT.check_HCP_WT_NA,
        
        
        
        
        ### NOTE: 17 Oct 2016. The following are place holders
        ### until we figure out if/how these sets of cohorts
        ### can transition into other cohorts.
        #~ 'CoastalWaters_WT_O': checks.check_CoastalWaters_WT.check_CoastalWaters_WT_O,
        #~ 'DrainedSlope_WT_Y': checks.check_DrainedSlope_WT.check_DrainedSlope_WT_Y,
        #~ 'DrainedSlope_WT_M': checks.check_DrainedSlope_WT.check_DrainedSlope_WT_M,
        #~ 'DrainedSlope_WT_O': checks.check_DrainedSlope_WT.check_DrainedSlope_WT_O,
        #~ 'NoData_WT_O': checks.check_NoData_WT.check_NoData_WT_O,
        #~ 'SandDunes_WT_Y': checks.check_SandDunes_WT.check_SandDunes_WT_Y,
        #~ 'SandDunes_WT_M': checks.check_SandDunes_WT.check_SandDunes_WT_M,
        #~ 'SandDunes_WT_O': checks.check_SandDunes_WT.check_SandDunes_WT_O,
        #~ 'SaturatedBarrens_WT_Y': checks.check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_Y,
        #~ 'SaturatedBarrens_WT_M': checks.check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_M,
        #~ 'check_SaturatedBarrens_WT_O': checks.check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_O,
        #~ 'Shrubs_WT_O': checks.check_Shrubs_WT.check_Shrubs_WT_O,
        #~ 'Urban_WT': checks.check_Urban_WT.check_Urban_WT,
        
        
        ### Note: 17 Oct 2016. The following checks are pretty much obsolete
        ### at this point. Will clean up once everything is working well.
        #~ 'Wet_NPG': checks.check_Wet_NPG.check_Wet_NPG,
        #~ 'Wet_LCP': checks.check_Wet_LCP.check_Wet_LCP,
        #~ 'Wet_CLC': checks.check_Wet_CLC.check_Wet_CLC,
        #~ 'Wet_FCP': checks.check_Wet_FCP.check_Wet_FCP,
        #~ 'Wet_HCP': checks.check_Wet_HCP.check_Wet_HCP,
        
        'ice_thickness': checks.ice_thickness.ice_thickness,
        
        
        'check_Ponds_WT_Y': checks.check_Ponds_WT.check_Ponds_WT_Y,
        'check_Ponds_WT_M': checks.check_Ponds_WT.check_Ponds_WT_M,
        'check_Ponds_WT_O': checks.check_Ponds_WT.check_Ponds_WT_O,
        'check_Ponds_WT_NA': checks.check_Ponds_WT.check_Ponds_WT_NA,
        
        'check_LargeLakes_WT_Y': checks.check_Lakes_WT.check_LargeLakes_WT_Y,
        'check_LargeLakes_WT_M': checks.check_Lakes_WT.check_LargeLakes_WT_M,
        'check_LargeLakes_WT_O': checks.check_Lakes_WT.check_LargeLakes_WT_O,
        'check_LargeLakes_WT_NA': checks.check_Lakes_WT.check_LargeLakes_WT_NA,
        
        'check_MediumLakes_WT_Y': checks.check_Lakes_WT.check_MediumLakes_WT_Y,
        'check_MediumLakes_WT_M': checks.check_Lakes_WT.check_MediumLakes_WT_M,
        'check_MediumLakes_WT_O': checks.check_Lakes_WT.check_MediumLakes_WT_O,
        'check_MediumLakes_WT_NA': checks.check_Lakes_WT.check_MediumLakes_WT_NA,
        
        'check_SmallLakes_WT_Y': checks.check_Lakes_WT.check_SmallLakes_WT_Y,
        'check_SmallLakes_WT_M': checks.check_Lakes_WT.check_SmallLakes_WT_M,
        'check_SmallLakes_WT_O': checks.check_Lakes_WT.check_SmallLakes_WT_O,
        'check_SmallLakes_WT_NA': checks.check_Lakes_WT.check_SmallLakes_WT_NA,
    } 
    
    for time in range(0, self.stop):
        if time == 0:
            cohorts.initial_barrow(self)
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
            # ----------------------------------------------------
            # Expand/Infill lake & ponds by prescribed rates
            # ----------------------------------------------------
            #~ lake_pond_expansion.lake_pond_expansion(self, element)
            #~ lake_pond_expansion.pond_infill(self, element, time)

            # ----------------------------------------------------------
            # Set active layer depth
            # ---------------------------------------------------------
            active_layer_depth.active_layer_depth(self, time, element)

            #~ # ----------------------------------
            #~ # Cycle through terrestrial cohorts
            #~ # ----------------------------------
            #~ check_Meadow_WT.check_Meadow_WT_Y(self, element, time)
            #~ check_Meadow_WT.check_Meadow_WT_M(self, element, time)
            #~ check_Meadow_WT.check_Meadow_WT_O(self, element, time)
            #~ check_LCP_WT.check_LCP_WT_Y(self, element, time)
            #~ check_LCP_WT.check_LCP_WT_M(self, element, time)
            #~ check_LCP_WT.check_LCP_WT_O(self, element, time)
            #~ check_CLC_WT.check_CLC_WT_Y(self, element, time)
            #~ check_CLC_WT.check_CLC_WT_M(self, element, time)
            #~ check_CLC_WT.check_CLC_WT_O(self, element, time)
            #~ check_FCP_WT.check_FCP_WT_Y(self, element, time)
            #~ check_FCP_WT.check_FCP_WT_M(self, element, time)
            #~ check_FCP_WT.check_FCP_WT_O(self, element, time)
            #~ check_HCP_WT.check_HCP_WT_Y(self, element, time)
            #~ check_HCP_WT.check_HCP_WT_M(self, element, time)
            #~ check_HCP_WT.check_HCP_WT_O(self, element, time)
            #~ #=====================================================
            #~ # NOTE: 17 Oct 2016. The following are place holders
            #~ # until we figure out if/how these sets of cohorts
            #~ # can transition into other cohorts.
            #~ #-----------------------------------------------------
            #~ #check_CoastalWaters_WT.check_CoastalWaters_WT_O(self, element, time)
            #~ #check_DrainedSlope_WT.check_DrainedSlope_WT_Y(self, element, time)
            #~ #check_DrainedSlope_WT.check_DrainedSlope_WT_M(self, element, time)
            #~ #check_DrainedSlope_WT.check_DrainedSlope_WT_O(self, element, time)
            #~ #check_NoData_WT.check_NoData_WT_O(self, element, time)
            #~ #check_SandDunes_WT.check_SandDunes_WT_Y(self, element, time)
            #~ #check_SandDunes_WT.check_SandDunes_WT_M(self, element, time)
            #~ #check_SandDunes_WT.check_SandDunes_WT_O(self, element, time)
            #~ #check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_Y(self, element, time)
            #~ #check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_M(self, element, time)
            #~ #check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_O(self, element, time)
            #~ #check_Shrubs_WT.check_Shrubs_WT_O(self, element, time)
            #~ #check_Urban_WT.check_Urban_WT(self, element, time)
            #~ #====================================================
            #~ # Note: 17 Oct 2016. The following checks are pretty much obsolete
            #~ # at this point. Will clean up once everything is working well.
            #~ # ----------------------------------------------------
#~ #            check_Wet_NPG.check_Wet_NPG(self, element, time)
#~ #            check_Wet_LCP.check_Wet_LCP(self, element, time)
#~ #            check_Wet_CLC.check_Wet_CLC(self, element, time)
#~ #            check_Wet_FCP.check_Wet_FCP(self, element, time)
#~ #            check_Wet_HCP.check_Wet_HCP(self, element, time)
            #~ #=====================================================

            #~ # ----------------------------------
            #~ # Set pond/lake ice thickness depth
            #~ # ----------------------------------
            #~ ice_thickness.ice_thickness(self, time, element)
            # ------------------------------
            # Cycle through ponds and lakes
            # ------------------------------
            #~ check_Ponds_WT.check_Ponds_WT_Y(self, element, time)
            #~ check_Ponds_WT.check_Ponds_WT_M(self, element, time)
            #~ check_Ponds_WT.check_Ponds_WT_O(self, element, time)
            #~ check_Lakes_WT.check_LargeLakes_WT_Y(self, element, time)
            #~ check_Lakes_WT.check_LargeLakes_WT_M(self, element, time)
            #~ check_Lakes_WT.check_LargeLakes_WT_O(self, element, time)
            #~ check_Lakes_WT.check_MediumLakes_WT_Y(self, element, time)
            #~ check_Lakes_WT.check_MediumLakes_WT_M(self, element, time)
            #~ check_Lakes_WT.check_MediumLakes_WT_O(self, element, time)
            #~ check_Lakes_WT.check_SmallLakes_WT_Y(self, element, time)
            #~ check_Lakes_WT.check_SmallLakes_WT_M(self, element, time)
            #~ check_Lakes_WT.check_SmallLakes_WT_O(self, element, time)
            
            # -------------------------------------------------
            # Cohort Fraction Check (mass balance of cohorts)
            # -------------------------------------------------
            
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
