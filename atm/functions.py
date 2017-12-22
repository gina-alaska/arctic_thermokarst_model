"""
"""
import numpy as np

def sigmoid (x, parameters):
    """
    """
    A1 = parameters['A1']
    A2 = parameters['A2']
    x0 = parameters['x0']
    dx = parameters['dx']
    
    return A2 + (A1 - A2)/(1.+ np.exp((x - x0)/dx))

def linear (x, parameters):
    """
    """
    a = parameters['a']
    b = parameters['b']
    return a + (b * x)
    
def sigmoid2 (x, parameters):
    """
    """
    K = parameters['K']
    C = parameters['C']
    A = parameters['A']
    B = parameters['B']
    return K / (C + (A * x**B))
    
def hill (x, parameters):
    """
    """
    B = parameters['hB']
    N = parameters['hN']
    return (B * (x**N))/(1. + (x**N))

# table of functions
table = {
    'sigmoid': sigmoid,
    'linear': linear,
    'sigmoid2': sigmoid2,
    'hill': hill,
}
