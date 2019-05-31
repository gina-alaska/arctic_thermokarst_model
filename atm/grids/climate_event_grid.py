"""
"""

import os
# import pickle
import numpy as np
from .constants import ROW, COL, create_deepcopy
import matplotlib.pyplot as plt
import copy
from multigrids import TemporalGrid, figures, common


class GetGridError (Exception):
    """Raised if grid timestep not found"""

class ClimateEventGrid (TemporalGrid):
    """Base class for met grids
        
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
            
        Attributes
        ----------
        start_year: int 
            year data starts at, should be year model will start at
        shape: tuple
            shape of grid
        history: np.array
            drainage grid
        met_type: str
            type of met data
        pickle_path: path
            path to pickle file
        source: path
           path to memory mapped history file 
    """
    
    def __init__ (self, *args, **kwargs):
        """
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
        """
        config = args[0]       
        
        # if type(config) is str:
        #     ## read from existing pickle
        #     self.load_from_pickle(config)
        #     return
        # if type()
        if type(args[0]) is str:
            super(ClimateEventGrid , self).__init__(*args, **kwargs)
        else:
            args = [
                config['grid_shape'][ROW], 
                config['grid_shape'][COL], 
                config['model length']
            ]

            kwargs = create_deepcopy(config) 
            kwargs['data_type'] = 'bool'
            kwargs['mode'] = 'r+'
            kwargs['start_timestep'] = int(config['start year'])
            super(ClimateEventGrid , self).__init__(*args, **kwargs)

            self.config['start_year'] = int(config['start year'])

            self.config['probability'] = float(
                config['Met_Control']['climate_event_probability']
            )
            self.config['climate_block_range'] = \
                config['_FAST_get_climate_block_range']
        self.grid = self.grids[self.config['timestep']]
        
    def get_grid (self, time_step = -1, flat = True):
        """Get met grid at ts
        
        Parameters
        ----------
        time_step: int
            time step to get data at
        flat: bool, defaults True
            reshapes data to shape if False
            
        Returns
        -------
        np.array
            Met gird for given time step
        """
        if time_step == -1:
            time_step = self.config['start_year'] + self.config['timestep']
        # shape = self.shape
        grid = self[time_step]
        if flat:
            return grid.flatten()
        return grid

    def create_climate_events (self, logger = None, log_ce=False):
        """Creates climate events 
        """
        block_size = np.random.randint(
            self.config['climate_block_range'][0],
            self.config['climate_block_range'][1]
        )
        
        for row in range(0, self.config['grid_shape'][ROW], block_size):
            for col in range(0, self.config['grid_shape'][COL], block_size):
                climate_event = np.random.uniform(0.0, 1.0)
                
                if not climate_event <= self.config['probability']:
                    continue
                ## climate envent occuts in block
                if logger and log_ce:
                    logger.add("     A climate event occurred")
                self.grid.reshape(self.config['grid_shape'])\
                    [row:row+block_size, col:col+block_size] = True
        return block_size
