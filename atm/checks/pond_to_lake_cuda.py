"""
Pond To Lake Transition
-----------------------

Checks for transitions from ponds to lakes
"""
import numpy as np

from numba import cuda

from debug import DEBUG
if DEBUG:
    import llvmlite.binding as llvm
    llvm.set_option('', '--debug-only=loop-vectorize')


@cuda.jit
def update_depth(new, depth_grid, elapsed_ts, depth_factor, mask):
    row, col = cuda.grid(2)
    if row < depth_grid.shape[0] and col < depth_grid.shape[1]:
        if mask[row,col] == True:
            new[row,col] = depth_grid[row,col] + ((elapsed_ts[row,col] ** .5) / depth_factor)


update_depth(np.zeros([10,10]).astype(np.float32), np.zeros([10,10]).astype(np.float32), np.zeros([10,10]).astype(np.float32), 1,np.ones([10,10]).astype(np.bool))

@cuda.jit
def apply_change(transitions_to, transitions_from, depth, no_grown, grown, freezes):
    """
    """
    row, col = cuda.grid(2)
    if row < transitions_to.shape[0] and col < transitions_to.shape[1]:
        if freezes[row,col]:
            transitions_to[row, col] += transitions_from[row, col]
            transitions_from[row, col] = 0.0
            depth[row, col]= 0
            no_grown[row, col] +=1
            
        else:
            grown[row, col] = 0

apply_change(
    np.zeros([10,10]).astype(np.float32),
    np.zeros([10,10]).astype(np.float32),
    np.zeros([10,10]).astype(np.float32),
    np.zeros([10,10]).astype(np.float32),
    np.zeros([10,10]).astype(np.float32),
    np.ones([10,10]).astype(np.bool)
    )


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
    
    blocks  =  (32, 32)
    threads = (
        int(np.ceil(grids.shape[0] / blocks[0])),
        int(np.ceil(grids.shape[1] / blocks[1]))
    )

    
    model_area_mask = grids.area.area_of_interest()
    cohort_present_mask = grids.area[name, year] > 0
    
    current_cell_mask = np.logical_and(model_area_mask, cohort_present_mask)

    ## had current TDD, TDD max
    TDD_max = grids.degreedays.thawing.grids[
        :year+1 - control['start year'] + 1
    ] 
    TDD_max = TDD_max.max(0).reshape(grids.shape)
    
    ## updated pond counts
    if year != control['start year']:
        new_max = TDD_max == grids.degreedays.thawing[year]
        
        new_max[np.logical_not(model_area_mask)] = False
    
        grids.lake_pond[name + '_count', year] += \
            len(np.where(new_max.flatten())[0])
    else:
        ## needed later
        new_max = TDD_max == TDD_max
        new_max[np.logical_not(model_area_mask)] = False
    
    ## NEW MAX DEGREE DAY(pond depth chages)
    update_pond_depth = np.logical_and(new_max, current_cell_mask)
    
    # print 'aa', grids.lake_pond.grid_name_map
    # print grids.lake_pond[name + '_depth', year].shape
    # print grids.lake_pond[name + '_depth', year][update_pond_depth].shape
    # print  control['Lake_Pond_Control'][name + '_depth_control']
    # print np.sqrt(grids.lake_pond[name + '_count', year][update_pond_depth]).shape

    # print (grids.lake_pond[name + '_depth', year].dtype,np.sqrt(grids.lake_pond[name + '_count', year]).dtype)
    # grids.lake_pond[name + '_depth', year][update_pond_depth]= (
    #     grids.lake_pond[name + '_depth', year].reshape(grids.shape)[update_pond_depth] +\
    #     (np.sqrt(grids.lake_pond[name + '_count', year].reshape(grids.shape))[
    #         update_pond_depth
    #     ] / control['Lake_Pond_Control'][name + '_depth_control'])
    # )
    update_depth[blocks, threads](
        grids.lake_pond[name + '_depth', year],
        grids.lake_pond[name + '_depth', year],
        grids.lake_pond[name + '_count', year],
        control['Lake_Pond_Control'][name + '_depth_control'],
        update_pond_depth
    )
    
        
    ## POND DEEPER THAN ICE BECOMES LAKE
    deeper_than_ice = \
        grids.lake_pond[name + '_depth', year].reshape(grids.shape) >= \
        grids.lake_pond['ice_depth', year]
    
    growth_time = control['Lake_Pond_Control'][name + '_growth_time_required']
    time_to_grow = grids.lake_pond[name + '_time_since_growth', year] >= growth_time
    
    to_lakes = np.logical_and(deeper_than_ice,time_to_grow.reshape(grids.shape))
    
    lake_shift = control['cohorts'][name + '_Control']['transitions_to']
    
    # ## convert to lakes
    # grids.area[lake_shift, year][to_lakes] = \
    #     grids.area[lake_shift, year][to_lakes] + \
    #     grids.area[name, year][to_lakes]
    
    # ## zero out ponds
    # grids.area[name, year][to_lakes] = 0.0
    apply_change[blocks, threads](
        grids.area[lake_shift, year],
        grids.area[name, year],
        grids.lake_pond[name + '_depth', year],
        grids.lake_pond[name + '_time_since_growth', year],
        grids.lake_pond[name + '_time_since_growth', year],
        to_lakes
    )

