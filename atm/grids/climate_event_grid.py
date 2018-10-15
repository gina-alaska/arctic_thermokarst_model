"""
"""

import os
# import pickle
import numpy as np
from constants import ROW, COL
import matplotlib.pyplot as plt

from multigrids import TemporalGrid, figures, common

try:
    from atm_io import image
except ImportError:
    from ..atm_io import image

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

            kwargs = copy.deepcopy(config) 
            kwargs['data_type'] = 'bool'
            kwargs['mode'] = 'r+'
            kwargs['start_timestep'] = int(config['start year'])
            super(ClimateEventGrid , self).__init__(*args, **kwargs)

            self.config['start_year'] = int(config['start year'])

            self.config['probability'] = float(
                config['Met_Control']['climate_event_probability']
            )
            self.config['climate_block_range'] = config['climate block range']
        self.grid = self.grids[self.timestep]
        
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
            time_step = self.start_year + self.timestep
        # shape = self.shape
        grid = self[time_step]
        if flat:
            return grid.flatten()
        return grid

    def create_climate_events (self):
        """Creates climate events 
        """
        block_size = np.random.randint(
            self.climate_block_range[0],
            self.climate_block_range[1]
        )
        
        for row in range(0, self.grid_shape[ROW], block_size):
            for col in range(0, self.grid_shape[COL], block_size):
                climate_event = np.random.uniform(0.0, 1.0)
                
                if not climate_event <= self.probability:
                    continue
                ## climate envent occuts in block
                print "climate event occured"
                self.grid.reshape(self.grid_shape)\
                    [row:row+block_size, col:col+block_size] = True
        return block_size

    def figure (self, filename, grid_id, **kwargs):
        """Save a figure for a climate_event_grid
        
        Parameters
        ----------
        filename: path
            path to save image at
        grid_id: int or str
            if an int, it should be the grid number.
            if a str, it should be a grid name.
        **kwargs: dict
            dict of key word arguments
            'cmap': str, defaults 'seismic'
                matplotlib colormap
            'cbar_extend': str, defaults 'neither'
                'neither', 'min' or 'max' 
        """
        data = self[grid_id].astype(float)
        data[np.logical_not(self.mask)] = np.nan

        figure_name = self.dataset_name + ' ' + str( grid_id )

        # limits = load_or_use_default(kwargs, 'limits', (None,None))
        cmap = common.load_or_use_default(kwargs, 'cmap', 'seismic')
        # cbar_extend = load_or_use_default(kwargs, 'cbar_extend', 'neither')
        
        figures.save_categorical_figure(
            data.reshape(self.grid_shape) , 
            filename, 
            figure_name ,
            categories = ['no climate event', 'climate event'],
            cmap = plt.get_cmap(cmap, 2)
        )
