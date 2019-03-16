"""
POI Based transition
--------------------

Transition functions for POI based changes in area
"""
import numpy as np
import functions
import matplotlib.pyplot as plt

from numba import njit, prange, jit, float32

@jit(nopython=True, nogil=True)
def find_x (ald, pl):
    return (ald / pl) - 1

@jit(nopython=True, nogil=True)
def calc_mask (frac_area, ald, pl, aoi):
    pl_breach = ald >= pl
    present = frac_area > 0

    return np.logical_and(np.logical_and(aoi, present),  pl_breach)

@jit( nogil=True, cache = True)
def calc_poi(shape, current_cell_mask, ald, pl, fn, last_poi, p_above, p_below, above_idx):
    ## find 'x'
    # x = np.zeros(shape)
    x = find_x(ald, pl)
    
    # POI_above = np.zeros(shape)
    POI_above = functions.call_function(
        fn, x, p_above
    )
    
    # POI_below  = np.zeros(shape)

    POI_below = functions.call_function(
        fn, x, p_below
    )

    POI = POI_below 
   
    POI[above_idx] = POI_above[above_idx]

    ## update cumulative POI
    new_poi = last_poi + POI
    new_poi[np.logical_not( current_cell_mask )] = 0.0
    return new_poi
    


@jit#(nopython=True, nogil=True)
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
    x = (ALD / PL) - 1


    present = from_cohort > 0
    pl_breach = ALD >= PL
    current_cell_mask = np.logical_and(np.logical_and(AOI, present),  pl_breach)




    ## update cumulative POI
    
    B_a = 0
    N_a = 1
    B_b = 2
    N_b = 3
    above = (params[B_a] * (x ** params[N_a])) / (1. + (x ** params[N_a]))
    below = (params[B_b] * (x ** params[N_b])) / (1. + (x ** params[N_b]))
    above[np.logical_not(above_idx)] = below[np.logical_not(above_idx)] 
    
    POIn = POInm1 + above
    POIn[np.logical_not( current_cell_mask )] = 0.0
    

    ## change PL[year] if ALD > PL
    ALD[ current_cell_mask ] = (ALD + (ALD - PL) * porosity)[current_cell_mask]


    rate_of_transition = POIn * ice_slope * max_rot
    rate_of_transition[ rate_of_transition > max_rot ] = max_rot
    ## calculate chage
    change = rate_of_transition * from_cohort

    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    change[np.logical_and(present, change > from_cohort )] = \
        from_cohort[np.logical_and(present, change > from_cohort )]

    
    ## apply change
    to_cohort_a0[ present] = (to_cohort + change)[ present]

    # grids.area[ transitions_to + '--0', year][present] = \
    #     (grids.area[transitions_to, year] + change)[present]


    from_cohort_a0[ present] = (from_cohort - change)[ present]

    # grids.area[name + '--0', year][present] = \
    #     (current - change)[present]


    # print grids.area[name, year-1].flatten()[157]
    # print grids.area[name, year].flatten()[157]

    

