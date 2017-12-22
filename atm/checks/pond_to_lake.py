"""
Pond To Lake Transition
-----------------------

Checks for transitions from ponds to lakes
"""
import numpy as np


def transition (name, year, grids, control):
    """This checks for any area in the pond cohort 'name' that should be 
    transitioned to a lake cohort

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
        An object containg the control keys(type): name + '_Control' (Dict),
        Lake_Pond_Control (Dict), 'start year' (int).
        name + '_Control' should contain keys(type): 
        Transition_check_type (str), transitions_to (str)
        See https://github.com/gina-alaska/arctic_thermokarst_model/wiki/Ponds-to-Lake-Transition
        Lake_Pond_Control should match the lake pond control specs:
        See [add link]

    """
    model_area_mask = grids.area.area_of_intrest()
    cohort_present_mask = grids.area[ year, name ] > 0
    
    current_cell_mask = np.logical_and(model_area_mask, cohort_present_mask)

    ## had current TDD, TDD max
    TDD_max = grids.degreedays.thawing.history[
        :year+1 - control['start year']+1
    ] 
    TDD_max = TDD_max.max(0).reshape(grids.shape)
    
    ## updated pond counts
    if year != control['start year']:
        new_max = TDD_max == grids.degreedays.thawing[year]
        
        new_max[np.logical_not(model_area_mask)] = False
    
        grids.lake_pond.counts[name] += len(np.where(new_max.flatten())[0])
    else:
        ## needed later
        new_max = TDD_max == TDD_max
        new_max[np.logical_not(model_area_mask)] = False
    
    ## NEW MAX DEGREE DAY(pond depth chages)
    update_pond_depth = np.logical_and(new_max, current_cell_mask)
    
    grids.lake_pond.depths[name][update_pond_depth.flatten()] = (
        grids.lake_pond.depths[name].reshape(grids.shape)[update_pond_depth] +\
        (np.sqrt(grids.lake_pond.counts[name].reshape(grids.shape))[
            update_pond_depth
        ] / control['Lake_Pond_Control'][name + '_depth_control'])
    ).flatten()
        
    ## POND DEEPER THAN ICE BECOMES LAKE
    deeper_than_ice = \
        grids.lake_pond.depths[name].reshape(grids.shape) >= \
        grids.lake_pond.ice_depth 
    
    growth_time = control['Lake_Pond_Control'][name + '_growth_time_required']
    time_to_grow = grids.lake_pond.time_since_growth[name] >= growth_time
    
    to_lakes = np.logical_and(deeper_than_ice,time_to_grow.reshape(grids.shape))
    
    lake_shift = control['Cohorts'][name + '_Control']['transitions_to']
    
    ## convert to lakes
    grids.area[year, lake_shift][to_lakes] = \
        grids.area[year, lake_shift][to_lakes] + \
        grids.area[year, name][to_lakes]
    
    ## zero out ponds
    grids.area[year, name][to_lakes] = 0.0
    grids.lake_pond.depths[name][to_lakes.flatten()] = 0.0
   
    # Update pond growth array
    grids.lake_pond.time_since_growth[name][to_lakes.flatten()] += 1
    
    
    grids.lake_pond.time_since_growth[name][np.logical_not(to_lakes).flatten()]\
        = 0
    
    
    
   
