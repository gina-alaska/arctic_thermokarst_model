"""
POI Based transition
--------------------

Transition functions for POI based changes in area
"""
import numpy as np
import functions
import matplotlib.pyplot as plt

from numba import njit, prange, jit, float32

## time for acp was   0:03:00.623743

import llvmlite.binding as llvm
llvm.set_option('', '--debug-only=loop-vectorize')

@jit(nopython=True, nogil=True)
def calc_x(ALD,PL): ## jit works
    x = np.zeros(ALD.shape)
    for row in range(x.shape[0]):
        for col in range(x.shape[1]):
            if PL[row,col] != 0:
                x[row,col] = (ALD[row,col] / PL[row,col]) - 1
    return x

calc_x(np.ones([10,10]).astype(float),np.ones([10,10]).astype(float))

# # @jit(nopython=True, nogil=True) ## jit does not work
# def apply_change(to_cohort, to_cohort_a0, from_cohort, from_cohort_a0, change, present):
#     # present = from_cohort > 0
#     for row in range(from_cohort.shape[0]):
#         for col in range(from_cohort.shape[1]):
#             if present[row, col]:
#                 to_cohort_a0[ row, col ] = to_cohort[ row, col] + change[ row, col]
#                 from_cohort_a0[row, col] = from_cohort[ row, col] - change[ row, col]

@jit(nopython=True, nogil=True) ## jit works?
def calc_new_poi(params, x, above_idx):
    K_a = 0
    C_a = 1
    A_a = 2
    B_a = 3
    K_b = 4
    C_b = 5
    A_b = 6
    B_b = 7
    
    new_poi = np.zeros(x.shape)
    above = params[K_a] / (params[C_a] + (params[A_a] * x**params[B_a])) 
    below = params[K_b] / (params[C_b] + (params[A_b] * x**params[B_b]))
    for row in range(above_idx.shape[0]):
        for col in range(above_idx.shape[1]):

            if above_idx[row,col] == True: 
                new_poi[row, col] = above[row,col]
            else:
                new_poi[row, col] = below[row,col]
    return new_poi

@jit(nopython=True, nogil=True) ## jit works?
def update_poi (POIn, POInm1, new, current_cell_mask):
    POIn = POInm1 + new
    for row in range(POIn.shape[0]):
        for col in range(POIn.shape[1]):
            if current_cell_mask[row,col] == False: 
                POIn[row, col] = 0.0

calc_new_poi(np.ones(8).astype(float), np.ones([10,10]).astype(float), np.ones([10,10])==np.ones([10,10]) )
update_poi(np.ones([10,10]).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10])==np.ones([10,10]) )

@jit(nopython=True, nogil=True) ## jit works?
def calc_change (rate_of_transition, from_cohort, present):
    """
    """
    change = rate_of_transition * from_cohort

    
    # if change is bigger than area available
    # TODO: handle age buckets
    for row in range(change.shape[0]):
        for col in range(change.shape[1]):
            if present[row, col] and change[row, col] > from_cohort[row, col]:
                change[row, col] = from_cohort[row,col]
    return change

calc_change(np.ones([10,10]).astype(float),np.ones([10,10]).astype(float),np.ones([10,10]).astype(float)==np.ones([10,10]).astype(float) )


@jit(nopython=True, nogil=True) ## jit works?
def calc_rot(POIn, ice_slope, max_rot):
    ## rot = rate of transition
    rot = POIn * ice_slope * max_rot
    for row in range(rot.shape[0]):
        for col in range(rot.shape[1]):
            if rot[row, col] > max_rot:
                rot[ row, col ] = max_rot
    return rot

# print(np.ones([10,10]).astype(float).dtype, np.ones([10,10]).astype(float).dtype, type(.5))
calc_rot(np.ones([10,10]).astype(np.float32), np.ones([10,10]).astype(np.float32), .5)

# @jit(nopython=True, nogil=True) ## jit not working?
# def update_ald(ALD,PL, porosity, current_cell_mask):
#     for row in range(ALD.shape[0]):
#         for col in range(ALD.shape[1]):
#             if current_cell_mask[row,col]: 
#                 ALD[ row, col ] = (ALD + (ALD - PL) * porosity)[ row, col ]

# @jit(nopython=True, nogil=True)
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

    ## x = (ALD / PL) - 1
    x = calc_x(ALD,PL)


    present = from_cohort > 0
    pl_breach = ALD >= PL
    current_cell_mask = np.logical_and(np.logical_and(AOI, present),  pl_breach)




    # update cumulative POI
    # above_idx = drainage == 'above'

    # K_a = 0
    # C_a = 1
    # A_a = 2
    # B_a = 3
    # K_b = 4
    # C_b = 5
    # A_b = 6
    # B_b = 7
    
    # above = params[K_a] / (params[C_a] + (params[A_a] * x**params[B_a])) 
    # below = params[K_b] / (params[C_b] + (params[A_b] * x**params[B_b]))
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if above_idx[row,col] == False: 
    #             above[row, col] = below[row, col]
 
    new = calc_new_poi(params, x, above_idx).astype(np.float32)
    # POIn = POInm1 + new
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if current_cell_mask[row,col] == False: 
    #             POIn[row, col] = 0.0
    # print(POIn.dtype,POInm1.dtype,new.dtype,current_cell_mask.dtype)
    update_poi(POIn,POInm1,new,current_cell_mask)
    

    # change PL[year] if ALD > PL
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if current_cell_mask[row,col]: 
    #             ALD[ row, col ] = (ALD + (ALD - PL) * porosity)[ row, col ]
    ALD[ current_cell_mask ] = ALD[current_cell_mask] + (ALD[current_cell_mask] - PL[ current_cell_mask ] ) * porosity



    # update_ald(ALD,PL, porosity, current_cell_mask)

    # rate_of_transition = POIn * ice_slope * max_rot
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if rate_of_transition [row, col] > max_rot:
    #             rate_of_transition[ row, col ] = max_rot
    # print (POIn.dtype,ice_slope.dtype, type(max_rot))
    rate_of_transition = calc_rot(POIn, ice_slope, max_rot)
    # calculate chage
    # change = rate_of_transition * from_cohort

    
    # # if change is bigger than area available
    # # TODO: handle age buckets
    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if present[row, col] and change[row, col] > from_cohort[row, col]:
    #             change[row, col] = from_cohort[row,col]

    change = calc_change(rate_of_transition, from_cohort, present)
    
    # change[np.logical_and(present, change > from_cohort )] = \
    #     from_cohort[np.logical_and(present, change > from_cohort )]

    
    # apply change

    # for row in range(above_idx.shape[0]):
    #     for col in range(above_idx.shape[1]):
    #         if present[row, col]:
    #             to_cohort_a0[ row, col ] = to_cohort[ row, col] + change[ row, col]


    #             from_cohort_a0[row, col] = from_cohort[ row, col] - change[ row, col]
    # apply_change(to_cohort, to_cohort_a0, from_cohort, from_cohort_a0, change, present)

    to_cohort_a0[present ] = to_cohort[present ] + change[present ]

    from_cohort_a0[present ] =  from_cohort[present ] - change[present ]
  

    

