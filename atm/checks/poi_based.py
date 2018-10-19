"""
POI Based transition
--------------------

Transition functions for POI based changes in area
"""
import numpy as np
import functions

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
        An object containg the control keys(type): name + '_Control' (Dict).
        Where name + '_Control' is the the cohort spesfic contntrol dict that 
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
    cohort_config = control['Cohorts'][name + '_Control'] 
    
    ## mask out non-test area
    model_area_mask = grids.area.area_of_interest()
    
    ## get_ice contents
    ice_slope = grids.ice.get_ice_slope_grid( name )
    
    ## get_cell with 'current cohort present'
    cohort_present_mask = grids.area[ year, name ] > 0
    
    ### where is ald >= PL
    pl_breach_mask = grids.ald['ALD', year] >= grids.ald[name, year]
    
    ### cells where change may occur
    current_cell_mask = np.logical_and(
        np.logical_and(
            model_area_mask, cohort_present_mask
        ),  
        pl_breach_mask 
    )
    
    ## find 'x'
    x = np.zeros(grids.shape)
    x[current_cell_mask] = (
        grids.ald['ALD',year] / grids.ald[name ,year]
    )[current_cell_mask] - 1

    ## caclualte POI
    fn = functions.table[cohort_config['POI_Function'].lower()]
    
    POI_above = np.zeros(grids.shape)
    POI_above[current_cell_mask] = fn(
        x, cohort_config['Parameters']['above']
    )[current_cell_mask]
    
    POI_below  = np.zeros(grids.shape)
    POI_below[current_cell_mask] = fn(
        x, cohort_config['Parameters']['below']
    )[current_cell_mask]
    
    POI = POI_below 
    above_idx = grids.drainage.grid.reshape(grids.shape) == 'above'
    POI[above_idx] = POI_above[above_idx]

    ## update cumulative POI
    grids.poi[year, name] = grids.poi[year-1, name] + POI
    ### POI where ALD < PL, reset cumulative POI to 0
    grids.poi[year, name][np.logical_not( current_cell_mask )] = 0.0

    ## change PL[year] if ALD > PL
    porosity = grids.ald.porosity[name]
    grids.ald[name, year ][ current_cell_mask ] = (
        grids.ald[name, year-1 ] + \
        (grids.ald['ALD', year] - grids.ald[name, year-1 ] ) * porosity
    )[ current_cell_mask ] 

    ## use POI to find rate of transtion
    max_rot = cohort_config['max_terrain_transition']
    rate_of_transition = \
        grids.poi[year, name] * ice_slope.reshape(grids.shape) * max_rot
    rate_of_transition[ rate_of_transition > max_rot ] = max_rot

    ## calculate chage
    change = rate_of_transition * grids.area[ year, name ]

    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    current = grids.area[ year, name]
    change[np.logical_and(cohort_present_mask, change > current )] = \
        current [np.logical_and(cohort_present_mask, change > current )]
    
    ## apply change
    transitions_to = cohort_config['transitions_to']
    grids.area[ year, transitions_to + '--0'][cohort_present_mask ] = \
        (grids.area[ year, transitions_to] + change)[cohort_present_mask ]

    grids.area[ year, name + '--0' ][cohort_present_mask ] = \
        (current - change)[cohort_present_mask ]

    

