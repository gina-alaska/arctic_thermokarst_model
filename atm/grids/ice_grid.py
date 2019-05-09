"""
ice_grid
--------

"""
import numpy as np
import copy
from constants import ROW, COL

# try:
from atm.images import binary
# except ImportError:
#     from ..io import binary, image

from multigrids import Grid, common, figures
import matplotlib.pyplot as plt

ICE_TYPES = ('poor', 'pore', 'wedge', 'massive')

config_ex = {
    'grid_shape': (10,10),
    'cohort ice slopes': 
        {'HCP':{'poor':.25, 'pore':.5, 'wedge':.75, 'massive':1.0},
            'FCP':{'poor':25, 'pore':5, 'wedge':75, 'massive':100},
            'CLC':{'poor':1, 'pore':1, 'wedge':2, 'massive':3},
            'LCP':{'poor':2, 'pore':4, 'wedge':6, 'massive':8},
            'POND':{'poor':.2, 'pore':.4, 'wedge':.6, 'massive':.8}
            },
    'init ice': ICE_TYPES,
    'AOI mask': np.ones((10,10)) == np.ones((10,10))
}
config_ex['AOI mask'][:5] = False


class IceGrid(Grid):
    """ Ice grid object """
    
    def __init__ (self, *args, **kwargs):
        """Represents Ice quality for each grid element
        
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
        AOI_mask: np.array
            boolean array where True elements are part of model domain
        cohort_coeffs: dict
            Dictionary with key for each cohort in model, and values 
            that are a dict of ice slope coefficients
        grid: np.array
            model ice slope grid
        shape: tuple
            (row dimension, column dimension)
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
            kwargs['dataset_name'] = 'Ice Grid'
            kwargs['mode'] = 'r+'
            super(IceGrid , self).__init__(*args, **kwargs)

            # threshold = config['Terrestrial_Control']\
            #     ['Drainage_Efficiency_Random_Value']
            # eff = config['Terrestrial_Control']\
            #     ['Drainage_Efficiency_Distribution']
            init_ice = ICE_TYPES##config['init ice']
            self.config['cohort_coeffs'] = \
                config['_FAST_get_ice_slope_coefficients']
            # print self.config['cohort_coeffs']
            self.config['AOI mask'] = config['AOI mask']
            self.config['ice types'] = ICE_TYPES
            self.grids = self.initialize_grid(
                self.shape, init_ice, self.config['AOI mask']
            )
        self.grid = self.grids
        
        # shape = config['shape']
        #~ cohort_list = config['cohort list']
        # init_ice = config ['init ice']
        
        # ## setup soil properties
        # self.aoi_mask = config['AOI mask']
        
        # self.cohort_coeffs = config['cohort ice slopes']
        
        # self.grid = self.setup_grid ( 
        #     shape, 
        #     init_ice, 
        #     self.aoi_mask, 
        # )
        
        # self.shape = shape
        
    def __getitem__ (self, key):
        """Gets ICE or PL or PL for a cohort
        
        Parameters
        ----------
        key: str, tuple (str, int)
        
        Raises
        ------
        KeyError:
            if key is does not meet key requirements
        
        Returns
        -------
        np.array
            requested Ice slope grid
        """
        return self.get_ice_slope_grid(key, False)
        
        
    def __setitem__ (self, key, value):
        """Set ICE or PL data. 
        
        
        Parameters
        ----------
        key: Str, or tuple(str, int)
            if key is a string, raises NotImplementedError
            if key is tuple, the str should be ICE, PL, or a cohort in the 
            PL grid. the int should start_year <= int <= start_year + len(grid)
        data: np.ndarray
            data of the proper shape, for key provided
            
            
        Raises
        ------
        KeyError: 
            if key does not match key parameters
        NotImplementedError:
            if key is str
        """
        raise NotImplementedError, 'cannot set ICE arrays once initilized'
        
        
    def initialize_grid (self, shape, init_ice, aoi_mask):
        """
        
        Parameters
        ----------
        dimensions: tuple of ints
            size of grid
        cohorts: list 
            list of cohorts in model domain
        init_ice: tuple, 2d array, of filename
            if it is as tuple it should have 2 elements (min, max)
        """
        
        if type(init_ice) is tuple:
            ice_grid = self.random_grid(shape, init_ice, aoi_mask)
        else:
            ice_grid = self.read_grid(init_ice)
            
        return ice_grid
        ## need to add random chance + setup for future reading of values

    def random_grid (self, shape, init_ice, aoi_mask = None):
        """create a random ICE grid
        
        Parameters
        ----------
        shape:  
        
        init_ice: tuple (2 floats)
            (min, max) ice in each element is set to min <= ice < max
        aoi_mask: np.array of bools( optional)
            if provided ICE is set where mask is true, other wise 0
        
        Returns
        -------
        np.array
            random ice grid
        """
        grid = np.random.choice(init_ice, shape ).flatten()
        if aoi_mask is None:
            aoi_mask = grid == grid
        
        grid[ aoi_mask.flatten() == False ] = 'none'
        return grid
    
    def read_grid (self, init_ice):
        """Read init ice from file or object"""
        raise NotImplementedError
        
    def get_ice_slope_grid(self, cohort, flat = True):
        """Get the ice content coefficient values for a cohort
        
        Parameters
        ----------
        cohort: str
            cannon cohort name
        flat: bool
            reshaps grid to shape if False
        """
        coeffs = self.cohort_coeffs[cohort]
        coeffs['none'] = 0
        grid = copy.deepcopy(self.grid)
        for c in coeffs:
            grid[ grid == c ] = coeffs[c]
        
        shape = grid.shape if flat else self.shape
    
        return grid.astype(float).reshape(shape)
    
    def as_numbers(self):
        """converts grid to a numerical representaion.
        
        Returns
        -------
        np.array:
            shpae is shape, 0 is substituted for 'none', 1 for 'above', and
            2 for 'below'
        """
        grid = self.grid.reshape(self.shape)
        grid[grid == 'none'] = 0
        grid[grid == 'poor'] = 1
        grid[grid == 'pore'] = 2
        grid[grid == 'wedge'] = 3
        grid[grid == 'massive'] = 4
        return grid.astype(int)  

    def save_figure (
            self, filename, figure_func=figures.default, figure_args={}
        ):
        """
        """
        super(Grid , self).save_figure(None, filename, figure_func, figure_args, data = self.as_numbers())


    def show_figure (self, figure_func=figures.default, figure_args={}):
        """
        """
        super(Grid , self).show_figure(None, figure_func, figure_args, data = self.as_numbers()) 

    # def figure (self, filename, **kwargs):
    #     """save a figure
        
    #     Parameters
    #     ----------
    #     filename: path
    #         file to save
    #     """
    #     temp = copy.deepcopy(self.grids)
    #     self.grid = self.as_numbers()
    #     limits = common.load_or_use_default(kwargs,'limits',(0,4))
    #     cmap = common.load_or_use_default(kwargs,'cmap','jet')
    #     dtype = common.load_or_use_default(kwargs, 'type', float)
    #     kwargs['limits'] = limits
    #     kwargs['cmap'] = plt.get_cmap(cmap, 5)
    #     kwargs['dtype'] = dtype 
    #     super(IceGrid , self).figure(filename, **kwargs)
    #     self.grid = temp
    
    # def binary (self, filename):
    #     """save a binary representation
        
    #     Parameters
    #     ----------
    #     filename: path
    #         file to save
    #     """
    #     binary.save_bin(self.as_numbers(), filename)
        
