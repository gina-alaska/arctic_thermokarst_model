"""
Drainage Grid
-------------

Grid for drainage efficiency
"""
import os
import numpy as np
import pickle

try:
    from atm_io import binary, image
except ImportError:
    from ..atm_io import binary, image

config_ex = {
    'Terrestrial_Control': {
        'Drainage_Efficiency_Distribution': 'random',
        'Drainage_Efficiency_Random_Value': 	0.85,
        'Drainage_Efficiency_Figure':		'Yes' ,
    },
    'pickle path': './pickles',
    'shape': (10,10),
    'AOI mask': np.random.choice([True,False],(10,10))
}

class DrainageTypeInvalid(Exception):
    """Raised if lake/pond type not found"""

class DrainageGrid (object):
    """ DrainageGrid """
    
    def __init__ (self, config):
        """Drainage Efficiency Grid 
        
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
            
        Attributes
        ----------
        shape: tuple
            shape of grid
        grid: np.array
            drainage grid
        pickle_path: path
            path to pickle file
        """
        if type(config) is str:
            ## read from existing pickle
            self.load_from_pickle(config)
            return
            
        self.shape = config['shape']
        aoi = config['AOI mask']
        eff = config['Terrestrial_Control']['Drainage_Efficiency_Distribution']
        threshold = config['Terrestrial_Control']\
            ['Drainage_Efficiency_Random_Value']
        
        
        self.grid = self.setup(eff, self.shape, threshold, aoi)
        self.pickle_path = os.path.join(
            config['pickle path'], 'drainage_grid.pkl'
        )

    def setup (self, efficiency, shape, threshold = .5, aoi = None):
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
        
    def get_grid (self, flat = True):
        """gets the gird
        
        Parameters
        ----------
        flat: bool, Default True
            if False, retruned grid is reshaped to shape
        
        Returns
        -------
        np.array
            the grid
        """
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        return self.grid.reshape(shape)
        

    def load_from_pickle(self, pickle_name):
        """load state from pickle file. sets shape, and grid to values
        in file, and pickle_path to pickle_name
    
        Parameters
        ----------
        pickel_name: path
            path to pickle file
        """
        with open(pickle_name, 'rb') as pkl:
            data = pickle.load(pkl)
            
        self.shape = data['shape']
        self.grid = data['grid']
        self.pickle_path = pickle_name
        
    def write_to_pickle (self, pickle_name = None):
        """Write to pickle, object are serialized as a python dictionary 
        with shape, and grid as keys
        
        Parameters
        ----------
        pickle_name: path, optional
            path to write to.
        """
        if pickle_name is None:
            pickle_name = self.pickle_path
        
        data = {
            'shape': self.shape,
            'grid': self.grid
        }    
        
        mode = 'wb'

        with open(pickle_name, mode) as pkl:
            pickle.dump(data, pkl)
        
    def as_numbers(self):
        """converts grid to a numerical representaion.
        
        Returns
        -------
        np.array:
            shpae is shape, 0 is substituted for 'none', 1 for 'above', and
            2 for 'below'
        """
        grid = self.get_grid(False)
        
        grid[grid == 'none'] = 0
        grid[grid == 'above'] = 1
        grid[grid == 'below'] = 2
        return grid.astype(int)
        
        
    def figure (self, filename):
        """save a figure
        
        Parameters
        ----------
        """
        image.save_img(
            self.as_numbers(), 
            filename, 
            'Drainage efficiency',
            cmap = 'bone',
            vmin = 0,
            vmax = 2
        )
        
    def binary (self, filename):
        """save a binary representation
        
        Parameters
        ----------
        """
        binary.save_bin(self.as_numbers(), filename)
        
        
        
