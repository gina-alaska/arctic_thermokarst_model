#! /usr/bin/env python

"""
The purpose of this script is to self-contain all
of the initialization processes for the Barrow
Peninsula simulations in order to keep the ATM
code clean.
"""
import numpy as np

#---------------------------------------------------------------------
#~ import active_layer_depth
#~ import check_climate_event
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
#~ import climate_expansion_arrays
import cohorts
#~ import cohort_check
#~ import cohort_present
#~ import ice_thickness
#~ import initial_cohort_age
#~ import initial_cohort_check
#~ import initial_cohort_population
#~ import initialize
#~ import lake_pond_expansion
#~ import Output_cohorts_by_year
#~ import read_drainage_efficiency
#~ import read_ice_content
#~ import read_initial_ALD
#~ import set_ALD_array
#~ import set_ALD_constant
#~ import set_ice_thickness_array
#~ import set_initial_cumulative_probability
#~ import set_lake_ice_depth_constant
#~ import set_lake_pond_depth
#~ import set_pond_growth_array
#~ import set_protective_layer

import climate_events
import lake_pond_expansion

from grids import area_grid
import sys

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

from cohorts import find_canon_name

def run(self, cohort_check_list, init_function):
    """
    cohort_list ordered list of cohorsts to run
    """
    
    start_year = self.control['start year']

    
    init_tdd = self.grids.degreedays.thawing[start_year+1] ## need to fix start year vs initilization year
    
    ## ts zero is initial data state 
    ## ts one is frist year to make chages
    for time in range(1, self.stop):
        #~ if time == 0:
            ## TODO fix this
            #~ init_function(self)
            #~ pass
        print '    at time step: ', time
        
        current_year = start_year + time
        # ++++++++++++++++++++++++++++++++++++++
        # Check for significant climatic event
        # ++++++++++++++++++++++++++++++++++++++
        ## << start HERE
        
        ## NEED to re write this
        
        #~ check_climate_event.check_climate_event(self)  

        # ----------------------------------------------------------
        # Looping over elements
        # ----------------------------------------------------------
        #~ for element in range(0, self.ATTM_nrows * self.ATTM_ncols):
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
            #~ cohort_start = cohort_check.cohort_start(self, element, time)
        cohort_start = \
            self.grids.area.get_all_cohorts_at_time_step().sum(0)
            

            ### Loop through each of the cohort checks for area
            #~ active_layer_depth.active_layer_depth(self, time, element)
        self.grids.climate_event.create_climate_events()
            
        self.grids.add_time_step()
        
       
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
        
        ## lake pond expansion: move out of loop to end
        
        for cohort in cohort_check_list:
           
            cohort_control = cohort + '_Control'
            try:
                check_type = \
                    self.control[cohort_control]['Transition_check_type'].lower()
            except:    
                check_type = 'base'
            print cohort, check_type
            #~ continue ## for testing
            
            #~ self.control[cohort_control]['cohort'] = find_canon_name(cohort)
            name = find_canon_name(cohort)
            checks.check_metadata[check_type](
                name,  current_year, self.grids, self.control
            )
        
        lp = self.grids.lake_pond.lake_types + self.grids.lake_pond.pond_types 
        lake_pond_expansion.expansion(lp, current_year, self.grids, self.control)
        #~ lake_pond_expansion.pond_infill
            
        cohort_end = \
            self.grids.area.get_all_cohorts_at_time_step().sum(0)
        
        diff = abs(cohort_start - cohort_end)
        
        #~ ## check mass balance, MOVE to function?
        if (diff > 0.1).any():
            import pickle
            
            with open('err.pkl','wb') as e:
                pickle.dump(self.grids, e )
            
            location = np.where(diff > 0.1)[0]
            print ('Mass Balance chage greater thatn 10 % in '
                    ''+ str(len(location)) + ' cells ')
            
            
            print location
            print 'start: ', cohort_start[location[0]]
            print 'end: ', cohort_end[location[0]]
            
            sys.exit()
            

            
            ## to do add frist cell report
        try:
            self.grids.area.check_mass_balance()
            self.grids.area.check_mass_balance(current_year - start_year)
        except area_grid.MassBalanceError as e:
            if e == 'mass balance problem 1':
                print 'mass has been added'
            else:
                print 'mass has been removed'
            sys.exit()
                    
            

            # NOTE: Just do this outside of loop
            #~ if time == self.stop -1:
                #~ cohorts.final_barrow(self)
            # ========================================================================
            # END MAIN LOOP 
            # ========================================================================
        # ========================================================================
        # OUTPUT RESULTS (if requested)
        # ========================================================================
        #  - - - - - - - - -
        # Fractional Areas
        #  - - - - - - - - -
        #~ Output_cohorts_by_year.Output_cohorts_by_year(self, time)
        #  - - - - - - - - - - - - -
        # Dominant Fractional Area
        #  - - - - - - - - - - - - - 
        #~ Output_cohorts_by_year.dominant_cohort(self)                 # Terrestrial_Control
        #~ Output_cohorts_by_year.dominant_fractional_plot(self, time)  # Terrestrial_Control
    for cohort in self.grids.area.key_to_index:
        if cohort.find('--') != -1:
            continue
            
        s = self.grids.area[start_year,cohort].sum()
        e = self.grids.area[current_year,cohort].sum()
        
        if s == e:
            d = 'equal'
        elif s < e:
            d = 'growth'
        else:
            d = 'reduction'
        print cohort, 'start:', s, 'end:', e, d
        
    # =================================
    # OUTPUT ANIMATIONS (if requested)
    # =================================
    # - - - - - - - - - - - - - - -
    # Fractional Area of Cohorts
    # - - - - - - - - - - - - - - - -
    #~ Output_cohorts_by_year.write_Fractions_avi(self)
    #~ Output_cohorts_by_year.write_Dominant_Cohort_avi(self) # Terrestrial_Control
#---------------------------------------------------------------------
