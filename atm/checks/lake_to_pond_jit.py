"""
Lake To Pond Transition
-----------------------

Checks for transitions from lake to pond
"""
import numpy as np

from numba import jit

from debug import DEBUG
if DEBUG:
    import llvmlite.binding as llvm
    llvm.set_option('', '--debug-only=loop-vectorize')

@jit(nopython=True, nogil=True)
def update_depth(depth_grid, elapsed_ts, depth_factor):
    new = np.zeros(depth_grid.shape)
    for row in range(depth_grid.shape[0]):
        for col in range(depth_grid.shape[0]):
            # if mask[row, col]:
            new[row,col] = depth_grid[row,col] + (np.sqrt(elapsed_ts) / depth_factor)
    return new

update_depth(np.zeros([10,10]).astype(np.float32), 10, 1)
    
@jit(nopython=True, nogil=True)
def apply_change(transitions_to, transitions_from):
    """
    """
    transitions_to += transitions_from
    transitions_from[:] = 0.0

# print(np.zeros([10]).astype(np.float32).dtype,np.zeros([10]).astype(np.float32).dtype)

apply_change(np.zeros([10]).astype(np.float32),np.zeros([10]).astype(np.float32))


def transition (name, year, grids, control):
    """This checks for any area in the lake cohort 'name' that should be 
    transitioned to a pond cohort

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
        See https://github.com/gina-alaska/arctic_thermokarst_model/wiki/Lake-to-Pond-Transition
        Lake_Pond_Control should match the lake pond control specs:
        See [add link]

    """
    # return
    # # print grids.lake_pond.grid_name_map
    model_area_mask = grids.area.area_of_interest()
    cohort_present_mask = grids.area[name, year] > 0
    
    current_cell_mask = np.logical_and(model_area_mask, cohort_present_mask)


    # grids.lake_pond[name + '_depth', year][current_cell_mask] = (
    #     grids.lake_pond[name + '_depth', year].reshape(grids.shape)[current_cell_mask] +\
    #     (np.sqrt(year - control['start year']+1)\
    #     / control['Lake_Pond_Control'][name + '_depth_control'])
    # )
    # print  grids.lake_pond[name + '_depth', year].dtype, type(year - control['start year']+1), type(control['Lake_Pond_Control'][name + '_depth_control'])
    grids.lake_pond[name + '_depth', year][current_cell_mask] = update_depth(
        grids.lake_pond[name + '_depth', year], 
        year - control['start year']+1, 
        control['Lake_Pond_Control'][name + '_depth_control']
    )[current_cell_mask] 
    
    freezes = \
        grids.lake_pond[name + '_depth', year].reshape(grids.shape) <= \
        grids.lake_pond['ice_depth', year]
        
    freezes = np.logical_and(freezes, current_cell_mask)
       
    shifts_to = control['cohorts'][name + '_Control']['transitions_to']

    # print grids.area[shifts_to, year][freezes].dtype , grids.area[name, year][freezes].dtype
    apply_change(grids.area[shifts_to, year][freezes], grids.area[name, year][freezes] )
    # grids.area[shifts_to, year][ freezes ] = \
    #     grids.area[shifts_to, year][freezes] + \
    #     grids.area[name, year][freezes]
        
    # grids.area[name, year][ freezes ] = 0.0
