
import numpy as np


def check(name, year, grids, control):
    """
    """
    model_area_mask = grids.area.area_of_intrest()
    cohort_present_mask = grids.area[ year, name ] > 0
    
    current_cell_mask = np.logical_and(model_area_mask, cohort_present_mask)


    grids.lake_pond.depths[name][current_cell_mask.flatten()] = (
        grids.lake_pond.depths[name].reshape(grids.shape)[current_cell_mask] +\
        (np.sqrt(grids.lake_pond.counts[name])[
            current_cell_mask.flatten()
        ] / control['Lake_Pond_Control'][name + '_depth_control'])
    ).flatten()
    
    freezes = \
        grids.lake_pond.depths[name].reshape(grids.shape) <= \
        grids.lake_pond.ice_depth 
        
    freezes = np.logical_and(freezes, current_cell_mask)
       
    shifts_to = control[name + '_Control']['transitions_to']
        
    grids.area[year, shifts_to][ freezes ] = \
        grids.area[year, shifts_to][freezes] + \
        grids.area[year, name][freezes]
        
    grids.area[year, name][ freezes ] = 0.0
