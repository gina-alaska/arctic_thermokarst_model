"""
POI Based transition
--------------------

Transition functions for POI based changes in area
"""
import numpy as np
import functions
import matplotlib.pyplot as plt

from numba import njit, prange, jit, float32





@jit(nopython=True, nogil=True)#), parallel=True)
def transition (from_cohort, from_cohort_a0, to_cohort, to_cohort_a0, ice_slope,
                ALD, PL, AOI, POIn, POInm1, above_idx, porosity, params, max_rot):
    """This checks for any area in the cohort 'name' that should be transitioned
    to the next cohort, and then transitions the area. 

    Note: .. 
        Assuming year '0' is the inital data, this should start with year 1
        
    Parameters
    ----------
    name: string
        Name of the current cohort.
    year: int
        The current year >= control['start_year'].
    grids: atm.grids.grids.ModelGrids
        The Grids representing the model area
    control: Dict or Dict like
        An object containing the control keys(type): name + '_Control' (Dict).
        Where name + '_Control' is the the cohort specific control dict that 
        contains the following keys (type): 'POI_Function'(String), 
        'A1_above'(float),'A2_above'(float),'x0_above'(float),'x0_above'(float),
        'a_above'(float),'b_above'(float),'K_above'(float),'C_above'(float),
        'A_above'(float),'B_above'(float),'HillB_above'(float),
        'HillN_above'(float),'A1_below'(float),'A2_below'(float),
        'x0_below'(float),'x0_below'(float),
        'a_below'(float),'b_below'(float),'K_below'(float),'C_below'(float),
        'A_below'(float),'B_below'(float),'HillB_below'(float),
        'HillN_below'(float), 'max_terrain_transition'(float), 
        'transitions_to'(str).
        See https://github.com/gina-alaska/arctic_thermokarst_model/wiki/POI-transition-function

    """
    K_a = 0
    C_a = 1
    A_a = 2
    B_a = 3
    K_b = 0
    C_b = 1
    A_b = 2
    B_b = 3
    for row in range(above_idx.shape[0]):
        for col in range(above_idx.shape[1]):
            present = from_cohort[row,col] > 0
            pl_breach = ALD[row,col] >= PL[row,col]
            current_cell_mask = pl_breach and present and AOI[row, col]

            x = 0
            if  PL[row,col] != 0:
                x = (ALD[row,col] / PL[row,col]) - 1
            POIn[row, col] = 0
            if above_idx[row,col] and current_cell_mask:
                POIn[row, col] = POInm1[row, col] + params[K_a] / (params[C_a] + (params[A_a] * x**params[B_a]))
                # if divisor != 0:
                #      / divisor
                # else: 
                #      POIn[row, col] = 0
            elif not above_idx[row,col] and current_cell_mask:
                POInm1[row, col] + params[K_b] / (params[C_b] + (params[A_b] * x**params[B_b]))
                # if divisor != 0:
                #     POIn[row, col] = POInm1[row, col] + params[K_b] / divisor
                # else: 
                #      POIn[row, col] = 0
          

            if current_cell_mask:
                ALD[ row, col ] = (ALD + (ALD - PL) * porosity)[ row, col ]

            rate_of_transition = POIn[ row, col ] * ice_slope[ row, col ] * max_rot
            if rate_of_transition > max_rot:
                rate_of_transition = max_rot
            
            change = rate_of_transition * from_cohort[row, col]
            if present and change > from_cohort[row, col]:
                change = from_cohort[row,col]
            
            if present:
                to_cohort_a0[ row, col ] = to_cohort[ row, col] + change
                from_cohort_a0[row, col] = from_cohort[ row, col] - change

            
            
    # x = (ALD / PL) - 1


    # present = from_cohort > 0
    # pl_breach = ALD >= PL
    # current_cell_mask = np.logical_and(np.logical_and(AOI, present),  pl_breach)




    ## update cumulative POI
    # above_idx = drainage == 'above'

    # K_a = 0
    # C_a = 1
    # A_a = 2
    # B_a = 3
    # K_b = 0
    # C_b = 1
    # A_b = 2
    # B_b = 3
    
    # above = params[K_a] / (params[C_a] + (params[A_a] * x**params[B_a])) 
    # below = params[K_b] / (params[C_b] + (params[A_b] * x**params[B_b]))
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if above_idx[row,col] == False: 
    #             above[row, col] = below[row, col]
    
    
    # POIn = POInm1 + above
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if current_cell_mask[row,col] == False: 
    #             POIn[row, col] = 0.0
    

    ## change PL[year] if ALD > PL
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if current_cell_mask[row,col]: 
    #             ALD[ row, col ] = (ALD + (ALD - PL) * porosity)[ row, col ]


    # rate_of_transition = POIn * ice_slope * max_rot
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if rate_of_transition [row, col] > max_rot:
    #             rate_of_transition[ row, col ] = max_rot
    ## calculate chage
    # change = rate_of_transition * from_cohort

    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if present[row, col] and change[row, col] > from_cohort[row, col]:
    #             change[row, col] = from_cohort[row,col]
    # change[np.logical_and(present, change > from_cohort )] = \
    #     from_cohort[np.logical_and(present, change > from_cohort )]

    
    ## apply change

    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if present[row, col]:
    #             to_cohort_a0[ row, col ] = (to_cohort + change)[ row, col]


    #             from_cohort_a0[row, col] = (from_cohort - change)[ row, col]

    # grids.area[name + '--0', year][present] = \
    #     (current - change)[present]


    # print grids.area[name, year-1].flatten()[157]
    # print grids.area[name, year].flatten()[157]

    

