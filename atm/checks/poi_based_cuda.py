"""
CUDA POI Based transition
-------------------------

Transition functions for POI based changes in area with CUDA
"""
import numpy as np
import functions
import matplotlib.pyplot as plt
import math

from numba import  cuda

@cuda.jit
def calc_x(x, ALD,PL): ## jit works
    """CUDA version of the calc X function

    Find the ration of the active layer to the protective layer minus 1

    Parameters
    ----------
    x: np.array like (floats) [m,n] <OUT> 
        uninitialized x array same shape as ALD, and PL, This is what is 
        returned in the non CUDA version
    ALD: np.array like (floats) [m,n] <IN> 
        ALD grid for a year
    PL: np.array like (floats) [m,n] <IN> 
        Protective layer grid for a cohort in a year
    """

    row, col = cuda.grid(2)
    if row < ALD.shape[0] and col < ALD.shape[1]:
        if PL[row,col] != 0 :
            x[row,col] = (ALD[row,col] / PL[row,col]) - 1

@cuda.jit
def calc_new_sig2_poi(new_poi, params, x, above_idx):
    """CUDA sigmoid 2 poi calculation function 

    POI = K / C + A * x ^ B

    Parameters
    ----------
    new_poi: np.array like (floats) [m,n] <OUT> 
        the new_poi that is being calculated [
    params: list [8] <IN>
        list of sigmoid 2 parametes for above and below the draining threshold
        specified in above_idx. [K above, C above, A above, B above, 
        K below, C below, A below, B below]
    x: np.array like (floats) [m,n] <IN>
        calculated x values
    above_idx: np.array like (bools) [m,n] <IN>
        indcates if cells are above(true) or below(false) the drainage 
        threshold.
    """
    K_a = 0
    C_a = 1
    A_a = 2
    B_a = 3
    K_b = 4
    C_b = 5
    A_b = 6
    B_b = 7

    row, col = cuda.grid(2)
    if row < x.shape[0] and col < x.shape[1]:
        if above_idx[row,col] == True: 
            new_poi[row, col] = params[K_a] / \
                (params[C_a] + (params[A_a] * x[row, col] ** params[B_a]))
        else:
            new_poi[row, col] = params[K_b] / \
                (params[C_b] + (params[A_b] * x[row, col] ** params[B_b]))

@cuda.jit
def calc_new_sig_poi(new_poi, params, x, above_idx):
    """CUDA sigmoid poi calculation function 

    POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx))

    Parameters
    ----------
    new_poi: np.array like (floats) [m,n] <OUT> 
        the new_poi that is being calculated [
    params: list [8] <IN>
        list of sigmoid 2 parametes for above and below the draining threshold
        specified in above_idx. [A1 above, A2 above, x0 above, dx above, 
        A1 below, A2 below, x0 below, dx below]
    x: np.array like (floats) [m,n] <IN>
        calculated x values
    above_idx: np.array like (bools) [m,n] <IN>
        indcates if cells are above(true) or below(false) the drainage 
        threshold.
    """
    A1_a = 0
    A2_a = 1
    x0_a = 2
    dx_a = 3
    A1_b = 4
    A2_b = 5
    x0_b = 6
    dx_b = 7
    
    row, col = cuda.grid(2)
    if row < x.shape[0] and col < x.shape[1]:
        if above_idx[row,col] == True: 
            new_poi[row, col] = params[A2_a] + (params[A1_a] - params[A2_a]) \
                / (1.+ math.exp((x[row, col] - params[x0_a])/params[dx_a]))
        else:
            new_poi[row, col] = params[A2_b] + (params[A1_b] - params[A2_b]) \
                / (1.+ math.exp((x[row, col] - params[x0_b])/params[dx_b]))

@cuda.jit
def calc_new_hill_poi(new_poi, params, x, above_idx):
    """CUDA hill poi calculation function 

    POI = (B*(x^n))/(1+(x^n))

    Parameters
    ----------
    new_poi: np.array like (floats) [m,n] <OUT> 
        the new_poi that is being calculated [
    params: list [8] <IN>
        list of sigmoid 2 parametes for above and below the draining threshold
        specified in above_idx. [B above, N above, B below, N below]
    x: np.array like (floats) [m,n] <IN>
        calculated x values
    above_idx: np.array like (bools) [m,n] <IN>
        indcates if cells are above(true) or below(false) the drainage 
        threshold.
    """
    B_a = 0
    N_a = 1
    B_b = 2
    N_b = 3
    
    row, col = cuda.grid(2)
    if row < x.shape[0] and col < x.shape[1]:
        if above_idx[row,col] == True: 
            new_poi[row, col] = \
                params[B_a] * (x[row, col] ** params[N_a]) \
                / (1 + x[row, col] ** params[N_a])
        else:
            new_poi[row, col] = \
                params[B_b] * (x[row, col] ** params[N_b]) \
                / (1 + x[row, col] ** params[N_b])

@cuda.jit
def calc_new_linear_poi(new_poi, params, x, above_idx):
    """CUDA linear poi calculation function 

    POI = a + (b * x )

    Parameters
    ----------
    new_poi: np.array like (floats) [m,n] <OUT> 
        the new_poi that is being calculated [
    params: list [8] <IN>
        list of sigmoid 2 parametes for above and below the draining threshold
        specified in above_idx. [a above, b above, a below, b below]
    x: np.array like (floats) [m,n] <IN>
        calculated x values
    above_idx: np.array like (bools) [m,n] <IN>
        indcates if cells are above(true) or below(false) the drainage 
        threshold.
    """
    a_a = 0
    b_a = 1
    a_b = 2
    b_b = 3

    row, col = cuda.grid(2)
    if row < x.shape[0] and col < x.shape[1]:
        if above_idx[row,col] == True: 
            new_poi[row, col] = params[a_a] + (params[b_a] + x[row, col])
        else:
            new_poi[row, col] = params[a_b] + (params[b_b] + x[row, col])
@cuda.jit
def update_poi (POIn, POInm1, new, current_cell_mask):
    """CUDA update POI function

    where cell in in current_cell_mask 
        poi[n] = poi[n-1] + new

    Parameters
    ----------
    POIn: np.array like (floats) [m,n] <OUT> 
        the current years poi that is being calculated 
    POInm1: np.array like (floats) [m,n] <IN> 
        the last years poi 
    new: np.array like (floats) [m,n] <IN> 
        the new additions for the poi
    current_cell_mask: np.array like (bools) [m,n] <IN>
        indcates if cells are active
    """
    row, col = cuda.grid(2)

    if row < POIn.shape[0] and col < POIn.shape[1]:
        POIn[row,col] = 0 
        if current_cell_mask[row,col] == True:
            POIn[row,col] = POInm1[row,col] + new[row,col]

@cuda.jit
def calc_change (change_amnts, rate_of_transition, from_cohort, present):
    """CUDA calc change. Calculates cohort the change for each cell.

    Parameters
    ----------
    change_amnts: np.array like (floats) [m,n] <OUT> 
        the amount of change to be calculated
    rate_of_transition: np.array like (floats) [m,n] <IN>
        Rate of transition grid.
    from_cohort: np.array like (floats) [m,n] <IN> 
        Grid for the cohort that is being changed. 
    present: np.array like (bools) [m,n] <IN> 
        Gird indicating that cohort should change
    
    """
    row, col = cuda.grid(2)

    if row < from_cohort.shape[0] and col < from_cohort.shape[1]:
        change_amnts[row,col] = \
            rate_of_transition[row,col] * from_cohort[row,col] 
        if present[row, col] and change_amnts[row, col] > from_cohort[row, col]:
                change_amnts[row, col] = from_cohort[row,col]

@cuda.jit
def calc_rot(rot, POIn, ice_slope, max_rot):
    """CUDA calc rate of transition. Calculates rate of transition 
    the change for each cell.

    Parameters
    ----------
    rot: np.array like (floats) [m,n] <OUT> 
        the rate of transition to be calculated
    POIn: np.array like (floats) [m,n] <IN>
        Rate of transition grid.
    ice_slope: np.array like (floats) [m,n] <IN> 
        Grid of ice slope constants 
    max_rot: float <IN> 
        Maximum rate of change 0 < max_rot <= 1
    """
    row, col = cuda.grid(2)

    if row < POIn.shape[0] and col < POIn.shape[1]:
        rot[ row, col ] = POIn[ row, col ] * ice_slope[ row, col ] * max_rot
        
        if rot[row, col] > max_rot:
            rot[ row, col ] = max_rot

def transition(name, year, grids, control):
    """This checks for any area in the cohort 'name' that should be transitioned
    to the next cohort, and then transitions the area. Using Cuda sub functions.

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
    ## SETUP -------------------------------------------------
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

    present = from_cohort > 0
    pl_breach = ALD >= PL
    current_cell_mask = np.logical_and(np.logical_and(AOI, present),  pl_breach)

    ## work ---------------
    blocks  =  (32, 32)
    threads = (
        int(np.ceil(ALD.shape[0] / blocks[0])),
        int(np.ceil(ALD.shape[1] / blocks[1]))
    )
    
    X = np.zeros(ALD.shape)
    calc_x[blocks, threads](X, ALD,PL)#.astype(np.float32)

    
    new_poi = np.zeros(X.shape)
    poi_func(new_poi, params, X, above_idx)


    update_poi[blocks, threads](POIn, POInm1, new_poi, current_cell_mask)
    

    # not cuda'd
    ALD[current_cell_mask] = \
        ALD[current_cell_mask] + \
        (ALD[current_cell_mask] - PL[ current_cell_mask ] ) * porosity

    rate_of_transition = np.zeros(POIn.shape) 
    calc_rot[blocks, threads](rate_of_transition, POIn, ice_slope, max_rot)

    change = np.zeros(POIn.shape) 
    calc_change[blocks, threads](
        change, rate_of_transition, from_cohort, present
    )
    
    # not cuda'd
    to_cohort_a0[present] = to_cohort[present] + change[present]
    from_cohort_a0[present] =  from_cohort[present] - change[present]
  

def compile():
    """precompile functions
    """
    calc_x(
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32)
    )

    calc_new_sig2_poi(
        np.ones([10,10]).astype(np.float32),
        np.ones(8).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10])==np.ones([10,10])
    )


    calc_new_sig_poi(
        np.ones([10,10]).astype(np.float32),
        np.ones(8).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10])==np.ones([10,10])
    )

    calc_new_hill_poi(
        np.ones([10,10]).astype(np.float32),
        np.ones(8).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10])==np.ones([10,10])
    )

    calc_new_linear_poi(
        np.ones([10,10]).astype(np.float32),
        np.ones(8).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10])==np.ones([10,10])
    )


    update_poi(
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32), 
        np.ones([10,10])==np.ones([10,10])
    )


    calc_rot(
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32), 
        np.ones([10,10]).astype(np.float32), 
        .5
    )

    calc_change(
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.float32),
        np.ones([10,10]).astype(np.bool)
    )

