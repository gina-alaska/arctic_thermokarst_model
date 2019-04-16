"""
CUDA Lake To Pond Transition
----------------------------

CUDA Checks for transitions from lake to pond
"""
import numpy as np

from numba import cuda

from debug import DEBUG
if DEBUG:
    import llvmlite.binding as llvm
    llvm.set_option('', '--debug-only=loop-vectorize')

@cuda.jit
def update_depth(new, depth_grid, elapsed_ts, depth_factor, mask):
    """CUDA Update Depth for lake to pond

    Parameters
    ----------
    new:  np.array like (float) [m,n] <OUT>
        values to be calculated
    depth_grid: np.array like (float) [m,n] <IN>
        grid of current lake depths
    elapsed_ts: float
        number timesteps since start year
    depth_factor: float
    mask: np.array (bool) [m,n]
        true were lakes are presnet 
    """
    row, col = cuda.grid(2)
    if row < depth_grid.shape[0] and col < depth_grid.shape[1]:
        if mask[row,col] == True:
            new[row,col] = \
                depth_grid[row,col] + ((elapsed_ts ** .5) / depth_factor)    

@cuda.jit
def apply_change(transitions_to, transitions_from, freezes):
    """CUDA apply change for lake to pond transition

    if the lake freezes to bottom then it is a pond

    Parameters
    ----------
    transitions_to: np.array (float) [m,n] <IN/OUT>
    transitions_from: np.array (float) [m,n] <IN/OUT>
    freezes: np.array (bool) [m,n]
        true if the lake freezes to bottom
    """
    row, col = cuda.grid(2)
    if row < transitions_to.shape[0] and col < transitions_to.shape[1]:
        if freezes[row,col]:
            transitions_to[row, col] += transitions_from[row, col]
            transitions_from[row, col] = 0.0




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
    blocks  =  (32, 32)
    threads = (
        int(np.ceil(grids.shape[0] / blocks[0])),
        int(np.ceil(grids.shape[1] / blocks[1]))
    )

    model_area_mask = grids.area.area_of_interest()
    cohort_present_mask = grids.area[name, year] > 0
    
    current_cell_mask = np.logical_and(model_area_mask, cohort_present_mask)

    update_depth[blocks, threads](
        grids.lake_pond[name + '_depth', year],
        grids.lake_pond[name + '_depth', year], 
        year - control['start year']+1, 
        control['Lake_Pond_Control'][name + '_depth_control'],
        current_cell_mask
    )
    
    freezes = \
        grids.lake_pond[name + '_depth', year].reshape(grids.shape) <= \
        grids.lake_pond['ice_depth', year]
        
    freezes = np.logical_and(freezes, current_cell_mask)
       
    shifts_to = control['cohorts'][name + '_Control']['transitions_to']

    apply_change[blocks, threads](
        grids.area[shifts_to, year], grids.area[name, year], freezes
    )


# compile
update_depth(
    np.zeros([10,10]).astype(np.float32), 
    np.zeros([10,10]).astype(np.float32), 
    10, 1, 
    np.ones([10,10]).astype(np.bool)
)

apply_change(
    np.zeros([10,10]).astype(np.float32),
    np.zeros([10,10]).astype(np.float32), 
    np.ones([10,10]).astype(np.bool)
)
