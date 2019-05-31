"""
Scale Layer
-----------

Resize elements in a grid
"""

import numpy as np
import os
import sys

import math

from multigrids import MultiGrid

try:
    from images import  raster
except ImportError:
    from ..images import raster

# try:
from atm.grids.constants import ROW,COL
# except (ValueError, ImportError) as e:
#     ROW,COL = 0, 1

try:
    from cohorts import find_canon_name, DISPLAY_COHORT_NAMES 
except ImportError:
    from ..cohorts import find_canon_name, DISPLAY_COHORT_NAMES 


def read_layers(input_rasters, target_resolution, logger = None):
    """Read cohort layers from raster files
    
    Parameters
    ----------
    Input_layers
    target_resolution: tuple of ints
        target resolution of each grid element (y,x)
        
    Returns
    -------
    Layers : np.ndarray
        2d array of flattened cohort grids, corrected to the proper
    resolution, and normalized. First dimension is layer index, which can be 
    found with the keys_to_index dict. The second dimension is gird element 
    index.
    raster_metadata : dict
        metadata for each raster loaded. Keys being canon name of layer
    """
    layers = []
    raster_metadata = {}
    layer_names = []
    
    for f in input_rasters:
        if logger:
            logger.add("LOADING RASTER:" + f )
        path = f
        try:
            data, metadata = raster.load_raster (path)
        except AttributeError:
            if logger:
                logger.add('Could Not Load Raster File'+ path, 'fatal')
            else:
                print('Could Not Load Raster File', path, 'fatal error')
            sys.exit(0)
        
        shape = (metadata.nY,metadata.nX)
        resolution = (abs(metadata.deltaY),abs(metadata.deltaX))
        
        try:
            filename = os.path.split(f)[-1]
            name = find_canon_name(filename.split('.')[0])
        except KeyError as e:
            print(e)
            continue
    
        raster_metadata[name] = metadata
        cohort_year_0, new_dimensions = scale_layer_down(
            data, resolution, target_resolution
        )

        layers.append( cohort_year_0 ) 
        layer_names.append( name)
        
        flat_grid_size = len(cohort_year_0) 
        
    layers = normalize_layers(
        np.array(layers), resolution, target_resolution
    )
    layer_mg = MultiGrid(
        new_dimensions[0],new_dimensions[1],len(layers),
        grid_names = layer_names,
        initial_data = layers
    )
    layer_mg.config['layer_names'] = layer_names
    return layer_mg, raster_metadata

def normalize_layers( layers, current_resolution, target_resolution):
    """Normalize Layers. Ensures that the fractional cohort areas in each 
    grid element sums to one. 
    """
    total = layers.sum(0) #sum fractional cohorts at each grid element
    cohorts_required = \
        (float(target_resolution[ROW])/(current_resolution[ROW])) * \
        (float(target_resolution[COL])/(current_resolution[COL]))

    cohort_check = total / cohorts_required
    ## the total is zero in non study cells. Fix warning there
    adjustment = float(cohorts_required)/total

    check_mask = cohort_check > .5
    new_layers = []
    for layer in layers:
        
        layer_mask = np.logical_and(check_mask,(layer > 0))
        layer[layer_mask] = np.multiply(
            layer,adjustment, where=layer_mask)[layer_mask]
        
        layer = np.round((layer) / cohorts_required, decimals = 6)
        new_layers.append(layer)
    new_layers = np.array(new_layers)
    return new_layers
    

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
    dimensions = (
        int(math.ceil(abs(shape[ROW] * current_resolution[ROW] /target_resolution[ROW]))),
        int(math.ceil(abs(shape[COL] * current_resolution[COL] /target_resolution[COL])))
    )
    ## regroup at new resolution
    for row in range(0, int(shape[ROW]), resize_num[ROW]):
        for col in range(0, int(shape[COL]), resize_num[COL]):
            A = layer[row : row+resize_num [ROW], col:col + resize_num[COL]]
            b = A > 0
            resized_layer.append(len(A[b]))
    
    return np.array(resized_layer), dimensions    
