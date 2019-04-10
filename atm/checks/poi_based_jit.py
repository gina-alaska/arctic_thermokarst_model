"""
POI Based transition
--------------------

Transition functions for POI based changes in area
"""
import numpy as np
import functions
import matplotlib.pyplot as plt

from numba import jit

from debug import DEBUG
if DEBUG:
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

calc_x(np.ones([10,10]).astype(np.float32),np.ones([10,10]).astype(np.float32))

# # @jit(nopython=True, nogil=True) ## jit does not work
# def apply_change(to_cohort, to_cohort_a0, from_cohort, from_cohort_a0, change, present):
#     # present = from_cohort > 0
#     for row in range(from_cohort.shape[0]):
#         for col in range(from_cohort.shape[1]):
#             if present[row, col]:
#                 to_cohort_a0[ row, col ] = to_cohort[ row, col] + change[ row, col]
#                 from_cohort_a0[row, col] = from_cohort[ row, col] - change[ row, col]

@jit(nopython=True, nogil=True) ## jit works?
def calc_new_sig2_poi(params, x, above_idx):
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
def calc_new_sig_poi(params, x, above_idx):
    A1_a = 0
    A2_a = 1
    x0_a = 2
    dx_a = 3
    A1_b = 4
    A2_b = 5
    x0_b = 6
    dx_b = 7
    
    new_poi = np.zeros(x.shape)

    # A2 + (A1 - A2)/(1.+ np.exp((x - x0)/dx))
    above = \
        params[A2_a] + \
        (params[A1_a] - params[A2_a]) / \
        (1.+ np.exp((x - params[x0_a])/params[dx_a]))
    below = \
        params[A2_b] + \
        (params[A1_b] - params[A2_b]) / \
        (1.+ np.exp((x - params[x0_b])/params[dx_b]))
    
    for row in range(above_idx.shape[0]):
        for col in range(above_idx.shape[1]):

            if above_idx[row,col] == True: 
                new_poi[row, col] = above[row,col]
            else:
                new_poi[row, col] = below[row,col]
    return new_poi

@jit(nopython=True, nogil=True) ## jit works?
def calc_new_linear_poi(params, x, above_idx):
    a_a = 0
    b_a = 1
    a_b = 2
    b_b = 3

    
    new_poi = np.zeros(x.shape)

    # a = parameters['linear_a']
    # b = parameters['linear_b']
    # return a + (b * x)
    above = params[a_a] + (params[b_a] + x)
    below = params[a_b] + (params[b_b] + x)
    
    for row in range(above_idx.shape[0]):
        for col in range(above_idx.shape[1]):

            if above_idx[row,col] == True: 
                new_poi[row, col] = above[row,col]
            else:
                new_poi[row, col] = below[row,col]
    return new_poi

@jit(nopython=True, nogil=True) ## jit works?
def calc_new_hill_poi(params, x, above_idx):
    B_a = 0
    N_a = 1
    B_b = 2
    N_b = 3

    
    new_poi = np.zeros(x.shape)

    # B = parameters['hill_B']
    # N = parameters['hill_N']
    # return (B * (x**N))/(1. + (x**N))
    above = (params[B_a] * (x ** params[N_a]) / (1 + x ** params[N_a]))
    below = (params[B_b] * (x ** params[N_b]) / (1 + x ** params[N_b]))

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

calc_new_sig2_poi(np.ones(8).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10])==np.ones([10,10]) )
calc_new_sig_poi(np.ones(8).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10])==np.ones([10,10]) )
calc_new_linear_poi(np.ones(8).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10])==np.ones([10,10]) )
calc_new_hill_poi(np.ones(8).astype(np.float32), np.ones([10,10]).astype(np.float32), np.ones([10,10])==np.ones([10,10]) )
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

calc_change(np.ones([10,10]).astype(np.float32),np.ones([10,10]).astype(np.float32),np.ones([10,10]).astype(np.float32)==np.ones([10,10]).astype(np.float32) )


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
    # year = current_year
    cc = control['cohorts'][name + '_Control']
    from_cohort_a0 = grids.area[name + '--0', year]
    from_cohort = grids.area[name, year]
    transitions_to = cc['transitions_to']
    to_cohort_a0 = grids.area[transitions_to + '--0', year]
    to_cohort = grids.area[transitions_to + '--0', year]
    ice_slope = \
        grids.ice.get_ice_slope_grid( name )\
        .reshape(grids.shape).astype(np.float32)
    ALD, PL = grids.ald['ALD', year], grids.ald[name ,year] 
    AOI = grids.area.area_of_interest()
    POIn = grids.poi[name, year]
    POInm1 = grids.poi[name, year-1]
    drainage = grids.drainage.grid.reshape(grids.shape)
    above_idx = drainage == 'above'
    porosity = grids.ald.porosity[name]

    max_rot = cc['max_terrain_transition']

    x = calc_x(ALD,PL).astype(np.float32)


    present = from_cohort > 0
    pl_breach = ALD >= PL
    current_cell_mask = np.logical_and(np.logical_and(AOI, present),  pl_breach)

    if cc['POI_Function'] == 'Sigmoid2':
        params = np.array([
            cc['Parameters']['above']['sigmoid2_K'],
            cc['Parameters']['above']['sigmoid2_C'],
            cc['Parameters']['above']['sigmoid2_A'],
            cc['Parameters']['above']['sigmoid2_B'],
            cc['Parameters']['below']['sigmoid2_K'],
            cc['Parameters']['below']['sigmoid2_C'],
            cc['Parameters']['below']['sigmoid2_A'],
            cc['Parameters']['below']['sigmoid2_B'],
        ]).astype(np.float32)
        poi_func = calc_new_sig2_poi
    elif cc['POI_Function'] == 'Sigmoid':
        params = np.array([
            cc['Parameters']['above']['sigmoid_A1'],
            cc['Parameters']['above']['sigmoid_A2'],
            cc['Parameters']['above']['sigmoid_x0'],
            cc['Parameters']['above']['sigmoid_dx'],
            cc['Parameters']['below']['sigmoid_A1'],
            cc['Parameters']['below']['sigmoid_A2'],
            cc['Parameters']['below']['sigmoid_x0'],
            cc['Parameters']['below']['sigmoid_dx'],
        ]).astype(np.float32)
        poi_func = calc_new_sig_poi
        # new = calc_new_sig_poi(params, x, above_idx).astype(np.float32)

    elif cc['POI_Function'] == 'Hill':
        params = np.array([
            cc['Parameters']['above']['hill_B'],
            cc['Parameters']['above']['hill_N'],
            cc['Parameters']['below']['hill_B'],
            cc['Parameters']['below']['hill_N'],
        ]).astype(np.float32)
        poi_func = calc_new_hill_poi
    elif cc['POI_Function'] == 'Linear':
        params = np.array([
            cc['Parameters']['above']['linear_a'],
            cc['Parameters']['above']['linear_b'],
            cc['Parameters']['below']['linear_a'],
            cc['Parameters']['below']['linear_b'],
        ]).astype(np.float32)
        poi_func = calc_linear_linear_poi
    else:
        raise KeyError("Not a valid function type")
    
    
    new = poi_func(params, x, above_idx).astype(np.float32)
    update_poi(POIn,POInm1,new,current_cell_mask)
    

  
    ALD[ current_cell_mask ] = ALD[current_cell_mask] + (ALD[current_cell_mask] - PL[ current_cell_mask ] ) * porosity



    rate_of_transition = calc_rot(POIn, ice_slope, max_rot).astype(np.float32)
  
    change = calc_change(rate_of_transition, from_cohort, present)
    

    to_cohort_a0[present ] = to_cohort[present ] + change[present ]

    from_cohort_a0[present ] =  from_cohort[present ] - change[present ]
  

    

