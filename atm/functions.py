"""
Functions
---------

Functions with a common interface for parameters
"""
import numpy as np

def sigmoid (x, parameters):
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
    A1 = parameters['sigmoid_A1']
    A2 = parameters['sigmoid_A2']
    x0 = parameters['sigmoid_x0']
    dx = parameters['sigmoid_dx']
    
    return A2 + (A1 - A2)/(1.+ np.exp((x - x0)/dx))
    
def sigmoid2 (x, parameters):
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
    K = parameters['sigmoid2_K']
    C = parameters['sigmoid2_C']
    A = parameters['sigmoid2_A']
    B = parameters['sigmoid2_B']
    return K / (C + (A * x**B))    


def linear (x, parameters):
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
    a = parameters['linear_a']
    b = parameters['linear_b']
    return a + (b * x)
    
def hill (x, parameters):
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
    B = parameters['hill_B']
    N = parameters['hill_N']
    return (B * (x**N))/(1. + (x**N))

# table of functions
table = {
    'sigmoid': sigmoid,
    'linear': linear,
    'sigmoid2': sigmoid2,
    'hill': hill,
}
