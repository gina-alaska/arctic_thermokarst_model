"""ice_grid.py


"""
import numpy as np

from terraingrid import ROW, COL


ICE_TYPES = ('poor', 'pore', 'wedge', 'massive')

class IceGrid(object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        
        shape = config['shape']
        cohort_list = config['cohort list']
        init_ice = config ['init ice']
        self.start_year = config ['start year']
        
        ## setup soil properties
        self.aoi_mask = config['AOI mask']
        
        self.grid = self.setup_grid ( 
            shape, 
            cohort_list, 
            init_ice, 
            self.aoi_mask, 
        )
        
        self.shape = shape
        
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
            requested Ice grid
        """
        return self.grid[key].reshape(self.shape)
        
        
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
        
        
    def setup_grid (self, shape, cohorts, init_ice, aoi_mask):
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
        ## TODO READ pl_modifiers from config
        
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
        
    def save_ice (self, time_step):
        """ save ice at time step """
        pass
        
