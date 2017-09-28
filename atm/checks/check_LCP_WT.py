import numpy as np
import gdal, os, sys, glob, random
import pylab as pl
from math import exp as exp

#==================================================================================================
def check_LCP_WT_NA(self, element, time):
    """No age place holder
    """
    pass
    
def check_LCP_WT_Y(self, element, time):

    # ! Determine the position on the POI curve
    if self.ATTM_Meadow_WT_Y_PL[element] == 0.0 : # Outside of area of interest
        x = -1.0
    else:
        x = (self.ALD[element] / self.ATTM_LCP_WT_Y_PL[element]) - 1.0
            
    # Maximum rate of terrain transition
    max_rate_terrain_transition = self.LCP_WT_Y['max_terrain_transition']
    
    # Rate of terrain transition as f(ice)
    if self.ice[element] == 'poor'    : ice_slope = self.LCP_WT_Y['ice_slope_poor']
    if self.ice[element] == 'pore'    : ice_slope = self.LCP_WT_Y['ice_slope_pore']
    if self.ice[element] == 'wedge'   : ice_slope = self.LCP_WT_Y['ice_slope_wedge']
    if self.ice[element] == 'massive' : ice_slope = self.LCP_WT_Y['ice_slope_massive']
    
    # check if Wetland Non-polygonal ground is present in the element
    if self.ATTM_LCP_WT_Y[element] > 0.0:

        # Active Layer > Protective Layer
        if self.ALD[element] >= self.ATTM_LCP_WT_Y_PL[element]:
            # Determine the Probability of Initiation (POI) for time-step
            if self.LCP_WT_Y['POI_Function'].lower() == 'sigmoid':
                if self.drainage_efficiency[element] == 'above':
                    A1 = self.LCP_WT_Y['A1_above']
                    A2 = self.LCP_WT_Y['A2_above']
                    x0 = self.LCP_WT_Y['x0_above']
                    dx = self.LCP_WT_Y['dx_above']
                else:
                    # Drainage efficiency = 'below'
                    A1 = self.LCP_WT_Y['A1_below']
                    A2 = self.LCP_WT_Y['A2_below']
                    x0 = self.LCP_WT_Y['x0_below']
                    dx = self.LCP_WT_Y['dx_below']
                
                # Probability of Initiation (POI) at current time
                POI = A2 + (A1 - A2)/(1.+exp((x - x0)/dx))
            elif self.LCP_WT_Y['POI_Function'].lower() == 'linear':
                if self.drainage_efficiency[element] == 'above':
                    a = self.LCP_WT_Y['a_above']
                    b = self.LCP_WT_Y['b_above']
                else:
                    a = self.LCP_WT_Y['a_below']
                    b = self.LCP_WT_Y['b_below']
                # Probability of Initiation (POI) at current time
                POI = a + (b * x)
            elif self.LCP_WT_Y['POI_Function'].lower() == 'sigmoid2':
                if self.drainage_efficiency[element] == 'above':
                    K = self.LCP_WT_Y['K_above']
                    C = self.LCP_WT_Y['C_above']
                    A = self.LCP_WT_Y['A_above']
                    B = self.LCP_WT_Y['B_above']
                else:
                    K = self.LCP_WT_Y['K_below']
                    C = self.LCP_WT_Y['C_below']
                    A = self.LCP_WT_Y['A_below']
                    B = self.LCP_WT_Y['B_below']
                # Probability of Initation (POI) at current time
                POI = K / (C + (A * x**B))
            elif self.LCP_WT_Y['POI_Function'].lower() == 'hill':
                if self.drainage_efficiency[element] == 'above':
                    B = self.LCP_WT_Y['HillB_above']
                    N = self.LCP_WT_Y['HillN_above']
                else:
                    B = self.LCP_WT_Y['HillB_below']
                    N = self.LCP_WT_Y['HillN_below']
                # Probability of Intiation (POI) at current time
                POI = (B * (x**N))/(1. + (x**N))
            # Cumulative POI
            if time == 0:
                self.ATTM_LCP_WT_Y_POI[element, time] = POI
            else:
                self.ATTM_LCP_WT_Y_POI[element, time] = self.ATTM_LCP_WT_Y_POI[element, time -1] + POI
            
            # Check that 0.0 < POI < 1.0
            if self.ATTM_LCP_WT_Y_POI[element, time] < 0.0: self.ATTM_LCP_WT_Y_POI[element, time] = 0.0
            if self.ATTM_LCP_WT_Y_POI[element, time] > 1.0: self.ATTM_LCP_WT_Y_POI[element, time] = 1.0

            # Adjust the Protective layer depth
            self.ATTM_LCP_WT_Y_PL[element] = self.ATTM_LCP_WT_Y_PL[element] + ((self.ALD[element] - \
                                                                   self.ATTM_LCP_WT_Y_PL[element])* \
                                                                   self.LCP_WT_Y['porosity'])

            # Determine rate of terrain transition from Wetland Tundra LCP -> Wetland Tundra CLC/FCP
            rate_of_transition = (self.ATTM_LCP_WT_Y_POI[element, time] * ice_slope) * max_rate_terrain_transition
            # error check
            if rate_of_transition > max_rate_terrain_transition: rate_of_transition = max_rate_terrain_transition

            # Determine the fractional change from Wetland Tundra LCP -> Wetland Tundra CLC/FCP
            cohort_change = self.ATTM_LCP_WT_Y[element] * rate_of_transition

            # cohort_change > Wetland Tundra LCP  available
            if cohort_change > self.ATTM_LCP_WT_Y[element]:
                clc_ratio = self.ATTM_CLC_WT_Y[element] / (self.ATTM_CLC_WT_Y[element] + self.ATTM_FCP_WT_Y[element])
                fcp_ratio = self.ATTM_FCP_WT_Y[element] / (self.ATTM_CLC_WT_Y[element] + self.ATTM_FCP_WT_Y[element])
                self.ATTM_CLC_WT_Y[element] = self.ATTM_CLC_WT_Y[element] + (self.ATTM_LCP_WT_Y[element] * clc_ratio)
                self.ATTM_FCP_WT_Y[element] = self.ATTM_FCP_WT_Y[element] + (self.ATTM_LCP_WT_Y[element] * fcp_ratio)
                self.ATTM_LCP_WT_Y[element] = 0.0
            else:
                # cohort_change < Wetland Tundra LCP available
                if self.ATTM_CLC_WT_Y[element] == 0.0 and self.ATTM_FCP_WT_Y[element] == 0.0:
                    # assume that if the drainage efficiency is 'above' then flat center polygons emerge
                    # assume that if the drainage efficiency is 'below' then coalescent low center polygons emerge
                    if self.drainage_efficiency[element] == 'above':
                        self.ATTM_FCP_WT_Y[element] = cohort_change
                        self.ATTM_LCP_WT_Y[element] = self.ATTM_LCP_WT_Y[element] - cohort_change
                    else: # self.drainage_efficiency[element] == 'below':
                        self.ATTM_CLC_WT_Y[element] = cohort_change
                        self.ATTM_LCP_WT_Y[element] = self.ATTM_LCP_WT_Y[element] - cohort_change
                else:
                    clc_ratio = self.ATTM_CLC_WT_Y[element] / (self.ATTM_CLC_WT_Y[element] + self.ATTM_FCP_WT_Y[element])
                    fcp_ratio = self.ATTM_FCP_WT_Y[element] / (self.ATTM_CLC_WT_Y[element] + self.ATTM_FCP_WT_Y[element])
                    self.ATTM_CLC_WT_Y[element] = self.ATTM_CLC_WT_Y[element] + (cohort_change * clc_ratio)
                    self.ATTM_FCP_WT_Y[element] = self.ATTM_FCP_WT_Y[element] + (cohort_change * fcp_ratio)
                    self.ATTM_LCP_WT_Y[element] = self.ATTM_LCP_WT_Y[element] - cohort_change
        else:
            # Active layer depth < Protective layer -> reset the cumulative POI to 0.0
            self.ATTM_LCP_WT_Y_POI[element,time] = 0.0
                                     
            
#===================================================================================================
def check_LCP_WT_M(self, element, time):

    # ! Determine the position on the POI curve
    if self.ATTM_LCP_WT_M_PL[element] == 0.0 : # Outside of area of interest
        x = -1.0
    else:
        x = (self.ALD[element] / self.ATTM_LCP_WT_M_PL[element]) - 1.0
            
    # Maximum rate of terrain transition
    max_rate_terrain_transition = self.LCP_WT_M['max_terrain_transition']
    
    # Rate of terrain transition as f(ice)
    if self.ice[element] == 'poor'    : ice_slope = self.LCP_WT_M['ice_slope_poor']
    if self.ice[element] == 'pore'    : ice_slope = self.LCP_WT_M['ice_slope_pore']
    if self.ice[element] == 'wedge'   : ice_slope = self.LCP_WT_M['ice_slope_wedge']
    if self.ice[element] == 'massive' : ice_slope = self.LCP_WT_M['ice_slope_massive']
    
    # check if Wetland Non-polygonal ground is present in the element
    if self.ATTM_LCP_WT_M[element] > 0.0:

        # Active Layer > Protective Layer
        if self.ALD[element] >= self.ATTM_LCP_WT_M_PL[element]:
            # Determine the Probability of Initiation (POI) for time-step
            if self.LCP_WT_M['POI_Function'].lower() == 'sigmoid':
                if self.drainage_efficiency[element] == 'above':
                    A1 = self.LCP_WT_M['A1_above']
                    A2 = self.LCP_WT_M['A2_above']
                    x0 = self.LCP_WT_M['x0_above']
                    dx = self.LCP_WT_M['dx_above']
                else:
                    # Drainage efficiency = 'below'
                    A1 = self.LCP_WT_M['A1_below']
                    A2 = self.LCP_WT_M['A2_below']
                    x0 = self.LCP_WT_M['x0_below']
                    dx = self.LCP_WT_M['dx_below']
                
                # Probability of Initiation (POI) at current time
                POI = A2 + (A1 - A2)/(1.+exp((x - x0)/dx))
            elif self.LCP_WT_M['POI_Function'].lower() == 'linear':
                if self.drainage_efficiency[element] == 'above':
                    a = self.LCP_WT_M['a_above']
                    b = self.LCP_WT_M['b_above']
                else:
                    a = self.LCP_WT_M['a_below']
                    b = self.LCP_WT_M['b_below']
                # Probability of Initiation (POI) at current time
                POI = a + (b * x)
            elif self.LCP_WT_M['POI_Function'].lower() == 'sigmoid2':
                if self.drainage_efficiency[element] == 'above':
                    K = self.LCP_WT_M['K_above']
                    C = self.LCP_WT_M['C_above']
                    A = self.LCP_WT_M['A_above']
                    B = self.LCP_WT_M['B_above']
                else:
                    K = self.LCP_WT_M['K_below']
                    C = self.LCP_WT_M['C_below']
                    A = self.LCP_WT_M['A_below']
                    B = self.LCP_WT_M['B_below']
                # Probability of Initation (POI) at current time
                POI = K / (C + (A * x**B))
            elif self.LCP_WT_M['POI_Function'].lower() == 'hill':
                if self.drainage_efficiency[element] == 'above':
                    B = self.LCP_WT_M['HillB_above']
                    N = self.LCP_WT_M['HillN_above']
                else:
                    B = self.LCP_WT_M['HillB_below']
                    N = self.LCP_WT_M['HillN_below']
                # Probability of Intiation (POI) at current time
                POI = (B * (x**N))/(1. + (x**N))
            # Cumulative POI
            if time == 0:
                self.ATTM_LCP_WT_M_POI[element, time] = POI
            else:
                self.ATTM_LCP_WT_M_POI[element, time] = self.ATTM_LCP_WT_M_POI[element, time -1] + POI
            
            # Check that 0.0 < POI < 1.0
            if self.ATTM_LCP_WT_M_POI[element, time] < 0.0: self.ATTM_LCP_WT_M_POI[element, time] = 0.0
            if self.ATTM_LCP_WT_M_POI[element, time] > 1.0: self.ATTM_LCP_WT_M_POI[element, time] = 1.0

            # Adjust the Protective layer depth
            self.ATTM_LCP_WT_M_PL[element] = self.ATTM_LCP_WT_M_PL[element] + ((self.ALD[element] - \
                                                                   self.ATTM_LCP_WT_M_PL[element])* \
                                                                   self.LCP_WT_M['porosity'])

            # Determine rate of terrain transition from Wetland Tundra Meadow -> Wetland Tundra LCP
            rate_of_transition = (self.ATTM_LCP_WT_M_POI[element, time] * ice_slope) * max_rate_terrain_transition
            # error check
            if rate_of_transition > max_rate_terrain_transition: rate_of_transition = max_rate_terrain_transition

            # Determine the fractional change from Wet_NPG ->: Wet_LCP
            cohort_change = self.ATTM_LCP_WT_M[element] * rate_of_transition

            # cohort_change > Wetland Tundra LCP  available
            if cohort_change > self.ATTM_LCP_WT_M[element]:
                clc_ratio = self.ATTM_CLC_WT_M[element] / (self.ATTM_CLC_WT_M[element] + self.ATTM_FCP_WT_M[element])
                fcp_ratio = self.ATTM_FCP_WT_M[element] / (self.ATTM_CLC_WT_M[element] + self.ATTM_FCP_WT_M[element])
                self.ATTM_CLC_WT_M[element] = self.ATTM_CLC_WT_M[element] + (self.ATTM_LCP_WT_M[element] * clc_ratio)
                self.ATTM_FCP_WT_M[element] = self.ATTM_FCP_WT_M[element] + (self.ATTM_LCP_WT_M[element] * fcp_ratio)
                self.ATTM_LCP_WT_M[element] = 0.0
            else:
                # cohort_change < Wetland Tundra LCP available
                if self.ATTM_CLC_WT_M[element] == 0.0 and self.ATTM_FCP_WT_M[element] == 0.0:
                    # assume that if the drainage efficiency is 'above' then flat center polygons emerge
                    # assume that if the drainage efficiency is 'below' then coalescent low center polygons emerge
                    if self.drainage_efficiency[element] == 'above':
                        self.ATTM_FCP_WT_M[element] = cohort_change
                        self.ATTM_LCP_WT_M[element] = self.ATTM_LCP_WT_M[element] - cohort_change
                    else: # self.drainage_efficiency[element] == 'below':
                        self.ATTM_CLC_WT_M[element] = cohort_change
                        self.ATTM_LCP_WT_M[element] = self.ATTM_LCP_WT_M[element] - cohort_change
                else:
                    clc_ratio = self.ATTM_CLC_WT_M[element] / (self.ATTM_CLC_WT_M[element] + self.ATTM_FCP_WT_M[element])
                    fcp_ratio = self.ATTM_FCP_WT_M[element] / (self.ATTM_CLC_WT_M[element] + self.ATTM_FCP_WT_M[element])
                    self.ATTM_CLC_WT_M[element] = self.ATTM_CLC_WT_M[element] + (cohort_change * clc_ratio)
                    self.ATTM_FCP_WT_M[element] = self.ATTM_FCP_WT_M[element] + (cohort_change * fcp_ratio)
                    self.ATTM_LCP_WT_M[element] = self.ATTM_LCP_WT_M[element] - cohort_change                
        else:
            # Active layer depth < Protective layer -> reset the cumulative POI to 0.0
            self.ATTM_LCP_WT_M_POI[element,time] = 0.0            
            
                     
#===================================================================================================
def check_LCP_WT_O(self, element, time):

    # ! Determine the position on the POI curve
    if self.ATTM_LCP_WT_O_PL[element] == 0.0 : # Outside of area of interest
        x = -1.0
    else:
        x = (self.ALD[element] / self.ATTM_LCP_WT_O_PL[element]) - 1.0
            
    # Maximum rate of terrain transition
    max_rate_terrain_transition = self.LCP_WT_O['max_terrain_transition']
    
    # Rate of terrain transition as f(ice)
    if self.ice[element] == 'poor'    : ice_slope = self.LCP_WT_O['ice_slope_poor']
    if self.ice[element] == 'pore'    : ice_slope = self.LCP_WT_O['ice_slope_pore']
    if self.ice[element] == 'wedge'   : ice_slope = self.LCP_WT_O['ice_slope_wedge']
    if self.ice[element] == 'massive' : ice_slope = self.LCP_WT_O['ice_slope_massive']
    
    # check if Wetland Non-polygonal ground is present in the element
    if self.ATTM_LCP_WT_O[element] > 0.0:

        # Active Layer > Protective Layer
        if self.ALD[element] >= self.ATTM_LCP_WT_O_PL[element]:
            # Determine the Probability of Initiation (POI) for time-step
            if self.LCP_WT_O['POI_Function'].lower() == 'sigmoid':
                if self.drainage_efficiency[element] == 'above':
                    A1 = self.LCP_WT_O['A1_above']
                    A2 = self.LCP_WT_O['A2_above']
                    x0 = self.LCP_WT_O['x0_above']
                    dx = self.LCP_WT_O['dx_above']
                else:
                    # Drainage efficiency = 'below'
                    A1 = self.LCP_WT_O['A1_below']
                    A2 = self.LCP_WT_O['A2_below']
                    x0 = self.LCP_WT_O['x0_below']
                    dx = self.LCP_WT_O['dx_below']
                
                # Probability of Initiation (POI) at current time
                POI = A2 + (A1 - A2)/(1.+exp((x - x0)/dx))
            elif self.LCP_WT_O['POI_Function'].lower() == 'linear':
                if self.drainage_efficiency[element] == 'above':
                    a = self.LCP_WT_O['a_above']
                    b = self.LCP_WT_O['b_above']
                else:
                    a = self.LCP_WT_O['a_below']
                    b = self.LCP_WT_O['b_below']
                # Probability of Initiation (POI) at current time
                POI = a + (b * x)
            elif self.LCP_WT_O['POI_Function'].lower() == 'sigmoid2':
                if self.drainage_efficiency[element] == 'above':
                    K = self.LCP_WT_O['K_above']
                    C = self.LCP_WT_O['C_above']
                    A = self.LCP_WT_O['A_above']
                    B = self.LCP_WT_O['B_above']
                else:
                    K = self.LCP_WT_O['K_below']
                    C = self.LCP_WT_O['C_below']
                    A = self.LCP_WT_O['A_below']
                    B = self.LCP_WT_O['B_below']
                # Probability of Initation (POI) at current time
                POI = K / (C + (A * x**B))
            elif self.LCP_WT_O['POI_Function'].lower() == 'hill':
                if self.drainage_efficiency[element] == 'above':
                    B = self.LCP_WT_O['HillB_above']
                    N = self.LCP_WT_O['HillN_above']
                else:
                    B = self.LCP_WT_O['HillB_below']
                    N = self.LCP_WT_O['HillN_below']
                # Probability of Intiation (POI) at current time
                POI = (B * (x**N))/(1. + (x**N))
            # Cumulative POI
            if time == 0:
                self.ATTM_LCP_WT_O_POI[element, time] = POI
            else:
                self.ATTM_LCP_WT_O_POI[element, time] = self.ATTM_LCP_WT_O_POI[element, time -1] + POI
            
            # Check that 0.0 < POI < 1.0
            if self.ATTM_LCP_WT_O_POI[element, time] < 0.0: self.ATTM_LCP_WT_O_POI[element, time] = 0.0
            if self.ATTM_LCP_WT_O_POI[element, time] > 1.0: self.ATTM_LCP_WT_O_POI[element, time] = 1.0

            # Adjust the Protective layer depth
            self.ATTM_LCP_WT_O_PL[element] = self.ATTM_LCP_WT_O_PL[element] + ((self.ALD[element] - \
                                                                   self.ATTM_LCP_WT_O_PL[element])* \
                                                                   self.LCP_WT_O['porosity'])

            # Determine rate of terrain transition from Wetland Tundra Meadow -> Wetland Tundra LCP
            rate_of_transition = (self.ATTM_LCP_WT_O_POI[element, time] * ice_slope) * max_rate_terrain_transition
            # error check
            if rate_of_transition > max_rate_terrain_transition: rate_of_transition = max_rate_terrain_transition

            # Determine the fractional change from Wet_NPG ->: Wet_LCP
            cohort_change = self.ATTM_LCP_WT_O[element] * rate_of_transition

            # cohort_change > Wetland Tundra LCP  available
            if cohort_change > self.ATTM_LCP_WT_O[element]:
                clc_ratio = self.ATTM_CLC_WT_O[element] / (self.ATTM_CLC_WT_O[element] + self.ATTM_FCP_WT_O[element])
                fcp_ratio = self.ATTM_FCP_WT_O[element] / (self.ATTM_CLC_WT_O[element] + self.ATTM_FCP_WT_O[element])
                self.ATTM_CLC_WT_O[element] = self.ATTM_CLC_WT_O[element] + (self.ATTM_LCP_WT_O[element] * clc_ratio)
                self.ATTM_FCP_WT_O[element] = self.ATTM_FCP_WT_O[element] + (self.ATTM_LCP_WT_O[element] * fcp_ratio)
                self.ATTM_LCP_WT_O[element] = 0.0
            else:
                # cohort_change < Wetland Tundra LCP available
                if self.ATTM_CLC_WT_O[element] == 0.0 and self.ATTM_FCP_WT_O[element] == 0.0:
                    # assume that if the drainage efficiency is 'above' then flat center polygons emerge
                    # assume that if the drainage efficiency is 'below' then coalescent low center polygons emerge
                    if self.drainage_efficiency[element] == 'above':
                        self.ATTM_FCP_WT_O[element] = cohort_change
                        self.ATTM_LCP_WT_O[element] = self.ATTM_LCP_WT_O[element] - cohort_change
                    else: # self.drainage_efficiency[element] == 'below':
                        self.ATTM_CLC_WT_O[element] = cohort_change
                        self.ATTM_LCP_WT_O[element] = self.ATTM_LCP_WT_O[element] - cohort_change
                else:
                    clc_ratio = self.ATTM_CLC_WT_O[element] / (self.ATTM_CLC_WT_O[element] + self.ATTM_FCP_WT_O[element])
                    fcp_ratio = self.ATTM_FCP_WT_O[element] / (self.ATTM_CLC_WT_O[element] + self.ATTM_FCP_WT_O[element])
                    self.ATTM_CLC_WT_O[element] = self.ATTM_CLC_WT_O[element] + (cohort_change * clc_ratio)
                    self.ATTM_FCP_WT_O[element] = self.ATTM_FCP_WT_O[element] + (cohort_change * fcp_ratio)
                    self.ATTM_LCP_WT_O[element] = self.ATTM_LCP_WT_O[element] - cohort_change  
        else:
            # Active layer depth < Protective layer -> reset the cumulative POI to 0.0
            self.ATTM_LCP_WT_O_POI[element,time] = 0.0            
 
            
                     
        
        