"""
Scale Layer
-----------

Resize elements in a grid
"""

import numpy as np

from ..grids.constants import ROW,COL


def scale_layer_down (layer, current_resolution, target_resolution):
    """Increases the size of grid elements by combining adjecent elements
    
    Parameters
    ----------
    layer: np.array
        layer to resize
    current_resoloution: tuple
        (row, col) resoloution in m of current layer
    target_resoloution: tuple
        (row, col) resoloution in m of desired layer
    
    Returns
    -------
    np.array
        a rescaled layer
    """
    if target_resolution == current_resolution:
        layer[layer<=0] = 0
        layer[layer>0] = 1
        return layer.flatten()
    
    resize_num = (
        abs(int(target_resolution[ROW]/current_resolution[ROW])),
        abs(int(target_resolution[COL]/current_resolution[COL]))
    )
    resized_layer = []
    
    shape = layer.shape
    
    ## regroup at new resolution
    for row in range(0, int(shape[ROW]), resize_num[ROW]):
        for col in range(0, int(shape[COL]), resize_num[COL]):
            A = layer[row : row+resize_num [ROW], col:col + resize_num[COL]]
            b = A > 0
            resized_layer.append(len(A[b]))
    
    return np.array(resized_layer)
    
