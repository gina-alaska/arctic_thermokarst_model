

import numpy as np

def check_base(grids, cohort_config, year):
    """assuming year '0' is the inital data, this should start with year 1
    """
    name = cohort_config['cohort']
    ## mask out non-test area
    model_area_mask = grids.area_grid.area_of_intrest()
    
    ## get_ice contents
    ice_slope = grids.ice.make_ice_slope_grid(config ['ice content'])
    
    ## get_cell with 'current cohort present'
    
    cohort_present_mask = grids.area_grid[ cohort_config['cohort'] ] > 0
    pl_breach_mask = ALD[year] >= PL[year]
    
    current_cell_mask = np.logical_and(
        np.logical_and(
            model_area_mask, cohort_present_mask
        ),  
        pl_breach_mask 
    )
    
    ## find 'x'
    x = np.zeros(grids.shape)
    x[current_cell_mask] = (
        grids.ald['ALD',year] / grids.ald[cohort_config['cohort'],year]
    )[current_cell_mask] - 1
    
    ## get function type
    function = cohort_config['transition function'] 
    POI = function( x ,cohort_config['transition parameters'])
    


    grids.POI[year, cohort_config['cohort']] = \
        grids.POI[year-1, cohort_config['cohort']] + POI

    ## set PL[year+1]
    grids.ALD[name, year ] = grids.ALD[name, year-1 ] + \
        (grids.ALD['ALD', year] - grids.ALD[name, year-1 ] ) * porosity
    
    max_rot = cohort_config['max rate of transition']
    rate_of_transition = grids.POI[year, name] * ice_slope * max_rot
        
    
    rate_of_transition[ rate_of_transition > max_rot ] = max_rot
    
    change = rate_of_transition * grids.area_grid[ cohort_config['cohort'] ]
    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    current = grids.area[ year - 1, cohort_config['cohort'] ]
    change[ change > current ] = current
    
    transitions_to = cohort_config['transitions to']
    grids.area[ year, transitions_to] = grids.area[ year - 1, transitions_to] +\
        change
    
    grids.area[ year, cohort_config['cohort'] ] = current - change
