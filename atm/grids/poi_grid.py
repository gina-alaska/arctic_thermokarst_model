"""
POI_grid
--------

POI: probability of instantiation
"""

import numpy as np
import os

from constants import ROW, COL

import copy

from multigrids import TemporalMultiGrid

class POIGrid (TemporalMultiGrid):
    """ Class doc """

    def __init__ (self, *args, **kwargs):
        """This class represents each cohorts POI for the model grid at
        each time step
        
        
        .. note:: Note on grid coordinates
            Origin (Y,X) is top left. rows = Y, cols = X
            Object will store dimensional(resolution, dimensions) 
            metadata as a tuple (Y val, X val).
            
        Parameters
        ----------
        Config: Dict
            should have keys 'start year', 'cohort list', and 'shape'
            
        Attributes
        ----------
        shape : tuple of ints
            Shape of the grid (y,x) (rows,columns)
        grid : array
            This 3d array is the grid data at each time step. 
            The first dimension is the time step with 0 being the initial data.
            The second dimension is the flat grid for given cohort, mapped using  
            key_to_index. The third dimension is the grid element. Each cohort
            can be reshaped using  shape to get the proper grid
        init_grid: np.ndarray 
                starting POI grid
        key_to_index : dict
                Maps canon cohort names to the index for that cohort in the 
            data object 
        
        
        """
        config = args [0]
        if type(config) is str:
            super(POIGrid , self).__init__(*args, **kwargs)
        else: 
           
            grid_names = config['_FAST_get_cohorts']##['cohorts']

            args = [
                config['grid_shape'][ROW], config['grid_shape'][COL], 
                len(grid_names), config['model length']
            ]

            kwargs = copy.deepcopy(config) 
            kwargs['data_type'] = 'float32'
            kwargs['mode'] = 'r+'
            kwargs['grid_names'] = grid_names
            
            super(POIGrid , self).__init__(*args, **kwargs)

        self.config['start_timestep'] = config['start_year']

        # self.start_year = int(config['initialization year'])
        # self.shape = config['shape']

        