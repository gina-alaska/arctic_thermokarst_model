"""
Functions
---------

Functions with a common interface for parameters
"""
import numpy as np

from numba import njit, prange, jit, float32
# import numpy as np

@jit(float32(float32, float32, float32, float32, float32), nopython=True, nogil=True)
def sigmoid (x, A1, A2, x0, dx):
    """Sigmoid function
    POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx))
    
    Parameters
    ----------
    x: float or array of floats
        variable
    parameters: dict
        dictionary containing 'sigmoid_A1','sigmoid_A2','sigmoid_x0',
        and 'sigmoid_dx'
        
    Returns
    -------
    float or array of floats:
        function  result
    """
    # A1 = parameters['sigmoid_A1']
    # A2 = parameters['sigmoid_A2']
    # x0 = parameters['sigmoid_x0']
    # dx = parameters['sigmoid_dx']
    
    return A2 + (A1 - A2)/(1.+ np.exp((x - x0)/dx))

@jit(float32(float32, float32, float32, float32, float32), nopython=True, nogil=True)
def sigmoid2 (x, K, C, A, B):
    """Sigmoid function
    POI = K / (C + (A*x**B))
    
    Parameters
    ----------
    x: float or array of floats or array of floats
        variable
    parameters: dict
        dictionary containing 'sigmoid2_K','sigmoid2_C','sigmoid2_A',
        and 'sigmoid2_B'
        
    Returns
    -------
    float or array of floats:
        function  result
    """
    # K = parameters['sigmoid2_K']
    # C = parameters['sigmoid2_C']
    # A = parameters['sigmoid2_A']
    # B = parameters['sigmoid2_B']
    return K / (C + (A * x**B))    

@jit(float32(float32, float32, float32), nopython=True, nogil=True)
def linear (x, a, b):
    """Sigmoid function
    POI = a + (b * x )
    
    Parameters
    ----------
    x: float or array of floats
        variable
    parameters: dict
        dictionary containing 'linear_a', and 'linear_b'
        
    Returns
    -------
    float or array of floats:
        function  result
    """
    # a = parameters['linear_a']
    # b = parameters['linear_b']
    return a + (b * x)

@jit(float32(float32, float32, float32), nopython=True, nogil=True)
def hill (x, B, N):
    """Sigmoid function
    POI = (B*(x^n))/(1+(x^n))
    
    Parameters
    ----------
    x: float or array of floats
        variable
    parameters: dict
        dictionary containing 'hill_B' and 'hill_N'
        
    Returns
    -------
    float or array of floats:
        function  result
    """
    # B = parameters['hill_B']
    # N = parameters['hill_N']
    # for n in range(x.size[0]):
    #     x[n] = (B * (x[n]**N))/(1. + (x[n]**N))
    return (B * (x**N))/(1. + (x**N))

# table of functions
table = {
    'sigmoid': sigmoid,
    'linear': linear,
    'sigmoid2': sigmoid2,
    'hill': hill,
}

def call_function(func_name, x, parameters):
    """set up the parameters to call the function
    """
    # fn = table[func_name]
    if 'sigmoid' == func_name:
        A1 = parameters['sigmoid_A1']
        A2 = parameters['sigmoid_A2']
        x0 = parameters['sigmoid_x0']
        dx = parameters['sigmoid_dx']
        return sigmoid(x, A1, A2, x0, dx)
    elif 'linear' == func_name:
        a = parameters['linear_a']
        b = parameters['linear_b']
        return linear (x, a, b)
    elif 'sigmoid2' == func_name:
        K = parameters['sigmoid2_K']
        C = parameters['sigmoid2_C']
        A = parameters['sigmoid2_A']
        B = parameters['sigmoid2_B']
        return K / (C + (A * x**B)) 
    elif 'hill' == func_name:
        B = parameters['hill_B']
        N = parameters['hill_N']
        return (B * (x**N))/(1. + (x**N))
    else:
        raise TypeError, func_name + " is not a valid function"



