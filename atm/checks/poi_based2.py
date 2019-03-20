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
    


@jit( nogil=True, cache = True)
def transition (name, year, grids, control):
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
    
    cohort_config = control['cohorts'][name + '_Control'] 
    
    ## mask out non-test area
    # model_area_mask = grids.area.area_of_interest()
    
    ## get_ice contents
    ice_slope = grids.ice.get_ice_slope_grid( name )
    
    ## get_cell with 'current cohort present'
    cohort_present_mask = grids.area[name, year] > 0

    current_cell_mask = calc_mask(
        grids.area[name, year], 
        grids.ald['ALD', year],
        grids.ald[name, year],
        grids.area.area_of_interest() 
    )

    ald, pl = grids.ald['ALD', year], grids.ald[name ,year]

    fn = cohort_config['POI_Function'].lower()
    # print(fn)

    ## update cumulative POI
    above_idx = grids.drainage.grid.reshape(grids.shape) == 'above'
    grids.poi[name, year] = calc_poi(
        grids.shape, current_cell_mask, ald, pl, fn,  grids.poi[name, year-1],
        cohort_config['Parameters']['above'], 
        cohort_config['Parameters']['below'], above_idx 
    )

    ## change PL[year] if ALD > PL
    porosity = grids.ald.porosity[name]
    grids.ald[name, year ][ current_cell_mask ] = (
        grids.ald[name, year-1 ] + \
        (grids.ald['ALD', year] - grids.ald[name, year-1 ] ) * porosity
    )[ current_cell_mask ] 

    ## use POI to find rate of transtion
    max_rot = cohort_config['max_terrain_transition']

    rate_of_transition = \
        grids.poi[name, year] * ice_slope.reshape(grids.shape) * max_rot
    rate_of_transition[ rate_of_transition > max_rot ] = max_rot
    ## calculate chage
    change = rate_of_transition * grids.area[name, year]

    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    current = grids.area[name, year]
    change[np.logical_and(cohort_present_mask, change > current )] = \
        current [np.logical_and(cohort_present_mask, change > current )]
    
    ## apply change
    transitions_to = cohort_config['transitions_to']
    grids.area[ transitions_to + '--0', year][cohort_present_mask ] = \
        (grids.area[transitions_to, year] + change)[cohort_present_mask ]

    grids.area[name + '--0', year][cohort_present_mask ] = \
        (current - change)[cohort_present_mask ]

    # print grids.area[name, year-1].flatten()[157]
    # print grids.area[name, year].flatten()[157]

    

