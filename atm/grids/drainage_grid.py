"""
Drainage Grid
-------------

Grid for drainage efficiency
"""
import os
import numpy as np

try:
    from atm_io import binary, image
except ImportError:
    from ..atm_io import binary, image

from multigrids import Grid, common
from constants import ROW, COL
import copy

import matplotlib.pyplot as plt

config_ex = {
    'Terrestrial_Control': {
        'Drainage_Efficiency_Distribution': 'random',
        'Drainage_Efficiency_Random_Value': 	0.85,
        'Drainage_Efficiency_Figure':		'Yes' ,
    },
    'pickle path': './pickles',
    'grid_shape': (10,10),
    'mask': np.random.choice([True,False],(10,10))
}

class DrainageTypeInvalid(Exception):
    """Raised if lake/pond type not found"""

class DrainageGrid (Grid):
    """ DrainageGrid """
    
    def __init__ (self, *args, **kwargs):
        """Drainage Efficiency Grid 
        
        Parameters
        ----------
        *args: list
            List of required arguments, containing exactly 1 argument
            the config dictionary or string file name of yaml file
            containing config
        **kwargs: dict
            Dictionary of key word arguments. Place holder for later extension.
            
        Attributes
        ----------
        shape: tuple
            shape of grid
        grid: np.array
            drainage grid
        pickle_path: path
            path to pickle file
        """
        config = args[0]    
        if type(args[0]) is str:
            super(DrainageGrid , self).__init__(*args, **kwargs)
        else:
            args = [
                config['grid_shape'][ROW], 
                config['grid_shape'][COL]
            ]

            kwargs = copy.deepcopy(config) 
            kwargs['data_type'] = 'object'
            kwargs['dataset_name'] = 'Drainage efficiency'
            kwargs['mode'] = 'r+'
            super(DrainageGrid , self).__init__(*args, **kwargs)

            threshold = config['Terrestrial_Control']\
                ['Drainage_Efficiency_Random_Value']
            eff = config['Terrestrial_Control']\
                ['Drainage_Efficiency_Distribution']
            self.grids = self.initialize_grid(
                eff, self.shape, threshold, self.config['mask']
            )
        self.grid = self.grids

            
        # self.shape = config['shape']
        # aoi = config['AOI mask']
        
        # threshold = config['Terrestrial_Control']\
        #     ['Drainage_Efficiency_Random_Value']
        
        
        # self.grid = self.setup(eff, self.shape, threshold, aoi)
        # self.pickle_path = os.path.join(
        #     config['pickle path'], 'drainage_grid.pkl'
        # )

    def initialize_grid (
            self, efficiency, shape, threshold = .5, aoi = None
        ):
        """setup grid
        
        Parameters
        ----------
        efficiency: str
            ['above', 'below', 'random']
        shape: tuple
            (rows, columns)
        threshold: float, defaults .5
            when randomizing values > threshold become above, <= below
        aoi: np.array, optional
            area of interest mask
            grid cells that are in AOI == True, False other wise
        
        Returns
        -------
        np.array:
            flattened drainage grid with values ['above', 'below', 'none']
        """
        efficiency = efficiency.lower()
        valid_input = ['above', 'below', 'random']
        if not efficiency in valid_input:
            msg = 'Efficiency Type not in ' + str(valid_input)
            raise DrainageTypeInvalid, msg
        
        grid = np.random.random(shape).flatten()
        
        if efficiency == 'random':
            grid[grid > threshold] = 1
            grid[grid <= threshold] = 0
            
            grid = grid.astype(int).astype(str)
            grid[grid == '1'] = 'above'
            grid[grid == '0'] = 'below'
            
            
        else:
            grid = grid.astype(str)
            grid[:] = efficiency
            
        if not aoi is None:
            grid[ aoi.flatten() == False ] = 'none'
            
        return grid
        
    def as_numbers(self):
        """converts grid to a numerical representaion.
        
        Returns
        -------
        np.array:
            shpae is shape, 0 is substituted for 'none', 1 for 'above', and
            2 for 'below'
        """
        grid = copy.deepcopy(self.get_grid(False))
        
        grid[grid == 'none'] = np.nan
        grid[grid == 'above'] = 1
        grid[grid == 'below'] = 2
        return grid.astype(float)
        
        
    def figure (self, filename, **kwargs):
        """save a figure
        
        Parameters
        ----------
        filename: path
            file to save
        """
        temp = copy.deepcopy(self.grids)
        self.grid = self.as_numbers()
        limits = common.load_or_use_default(kwargs,'limits',(1,2))
        cmap = common.load_or_use_default(kwargs,'cmap','bone')
        dtype = common.load_or_use_default(kwargs, 'type', float)
        kwargs['limits'] = limits
        kwargs['cmap'] = plt.get_cmap(cmap, 2)
        kwargs['dtype'] = dtype 
        super(DrainageGrid , self).figure(filename, **kwargs)
        self.grid = temp
        
    # def binary (self, filename):
    #     """save a binary representation
        
    #     Parameters
    #     ----------
    #     filename: path
    #         file to save
    #     """
    #     binary.save_bin(self.as_numbers(), filename)
        
        
        
