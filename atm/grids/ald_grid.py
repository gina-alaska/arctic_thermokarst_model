"""
ald_grid
--------

for the purposes of this file ALD(or ald) refers to Active layer depth,
and PL (or pl) to Protective layer
"""
import numpy as np

from constants import ROW, COL

try:
    from atm_io import binary, image, raster
except ImportError:
    from ..atm_io import binary, image, raster

import copy

class ALDGrid(object):
    """ALD, and PL object """
    
    def __init__ (self, config):
        """Represnts ALD, and PL for each cohort for the model
        
        Parameters
        ----------
        config: dict
        
        Attributes
        ----------
        start_year: int
            year of init data
        porosity: dict
            porosity values for each cohort
        protective_layer_factor: dict
            PL factor for each cohort
        aoi_mask: np.array
            Boolean array where true elemets are in model domain
        init_ald_grid: np.array
            initial ALD gird
        init_pl_grid: np.array
            initial PL gird
        pl_key_to_index: dict
            maps canon cohort names to index used in internal pl_grid
        shape: tuple
            (rows, columns)
        ald_grid: list
            array or ALD grids for each timestep
        pl_grid: list
            array or PL grids for each timestep
        ald_constants: np.array
            starts as zeros, this should be updated once the met values 
            are loaded with setup_ald_constants, and then changed
        """
        shape = config['shape']
        cohort_list = config['cohort list']
        init_ald = config ['init ald']
        self.start_year = config ['initilzation year']
        
        ## setup soil properties
        self.porosity = config['porosities']
        self.protective_layer_factor = config['PL factors']
        self.aoi_mask = config['AOI mask']
        
        ald, pl, pl_map = self.setup_grid ( 
            shape, 
            cohort_list, 
            init_ald, 
            self.aoi_mask, 
            self.protective_layer_factor 
        )
        self.init_ald_grid = ald
        self.init_pl_grid = pl
        self.pl_key_to_index = pl_map
        
       
        self.shape = shape
        self.ald_grid = [ self.init_ald_grid ]
        self.pl_grid = [ self.init_pl_grid ]
        
        self.ald_constants = np.zeros(self.shape)
    
        
    def __getitem__ (self, key):
        """Gets ALD or PL or PL for a cohort
        
        Parameters
        ----------
        key: str, tuple (str, int)
        
        Raises
        ------
        NotImplementedError:
            get ALD or PL at all time steps functions not implemented
        KeyError:
            if key is does not meet key requirements
        
        Returns
        -------
        np.array
            requested grid, each grid will match the shape attribute
        """
        if type(key) is str:
            if key == 'ALD':
                return self.get_ald(flat = False)
            elif key == 'PL':
                #return self.get_pl()
                raise NotImplementedError, 'get all PL ts not implemented'
            else:
                raise KeyError, 'String key must be ALD, or PL'
               
        elif type(key) is tuple:
            if key[0] == 'ALD':
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_ald_at_time_step(ts, False)
                else:
                    raise KeyError, 'Tuple key(ALD) index 1 must be an int'
                
            elif key[0] == 'PL':
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_pl_at_time_step(ts, flat = False)
                else:
                    raise KeyError, 'Tuple key(PL) index 1 must be an int'
            
            elif key[0] in self.pl_key_to_index.keys():
                if type(key[1]) is int:
                    ts = key[1] - self.start_year
                    return self.get_pl_at_time_step(ts,
                        cohort = key[0], flat = False)
                else:
                    raise KeyError, 'Tuple key(cohort) index 1 must be an int'
            
            else:
                msg = ('Tuple keys first item must be ALD,'
                        ' or PL, or a cohort in pl_grid')
                raise KeyError, msg

        else:
            raise KeyError, 'Key is not a str or tuple.'
        
    def __setitem__ (self, key, value):
        """Set ALD or PL data. 
        
        
        Parameters
        ----------
        key: Str, or tuple(str, int)
            if key is a string, raises NotImplementedError
            if key is tuple, the str should be ALD, PL, or a cohort in the 
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
        if type(key) is str:
            raise NotImplementedError, 'cannot set whole ALD or PL array'
            
        elif type(key) is tuple:
            if type(key[1]) is int:
                year = key[1]
                if year == self.start_year + len(self.ald_grid):
                ## year == end year + 1 
                ## (I.e start_year == 1900, len(grid) =10, year = 1910)
                ## time steps from 0 - 9, (1900 - 1909)
                ## year - star_year = 10, no 10 as a time,
                ## but 10 == year - star_year, or 1910 == start_year+len(grid)
                ## so, will add a new grid year, because it is end +1, and set 
                ## values to 0
                    self.add_time_step(True)
                elif year > self.start_year + len(self.ald_grid):
                    raise KeyError, 'Year too far after current end'
                elif year < self.start_year:
                    raise KeyError, 'Year before start year'
            else:
                raise KeyError, 'tuple index 1 should be int'
            
            ts = year - self.start_year
            
            if key[0] is 'ALD':
                self.set_ald_at_time_step(ts, value)
            elif key[0] == 'PL':
                self.set_pl_at_time_step(ts, value)
            elif key[0] in self.pl_key_to_index.keys():
                self.set_pl_cohort_at_time_step(ts, key[0], value)
            else: 
                msg = ('Tuple keys first item must be ALD,'
                        ' or PL, or a cohort in pl_grid')
                raise KeyError, msg
        else:
            raise KeyError, 'Key is not a str or tuple.'
        
        
    def setup_grid (self, shape, cohorts, init_ald, aoi_mask, pl_factors = {}):
        """
        
        Parameters
        ----------
        dimensions: tuple of ints
            size of grid
        cohorts: list 
            list of cohorts in model domain
        init_ald: tuple, 2d array, of filename
            if it is as tuple it should have 2 elements (min, max)
        """
        ## TODO READ pl_modifiers from config
        
        if type(init_ald) is tuple:
            ald_grid = self.random_grid(shape, init_ald, aoi_mask)
        else:
            ald_grid = self.read_grid(init_ald)
        
        if pl_factors == {}:
            pl_factors = {key: 1 for key in cohorts}
        
        ## protective layer (pl)
        pl_grid = []
        pl_key_to_index = {}
        index = 0 
        for cohort in cohorts:
            pl_grid.append(ald_grid * pl_factors[cohort]) 
            pl_key_to_index[ cohort ] = index
            index += 1
            
        return ald_grid, np.array(pl_grid), pl_key_to_index
        ## need to add random chance + setup for future reading of values
        
    def setup_ald_constants (self, degree_days):
        """Initialize the ALD constant array
        
        Parameters
        ----------
        degree_days: float or np.array
            a thawing Degree Day value or grid of thawing Degree Day values
        """
        try:
            degree_days = degree_days.flatten()
        except AttributeError:
            pass
        
        self.ald_constants = self.init_ald_grid.flatten() / degree_days
        
        

    def random_grid (self, shape, init_ald, aoi_mask = None):
        """create a random ALD grid
        
        Parameters
        ----------
        shape:  
        
        init_ald: tuple (2 floats)
            (min, max) ald in each element is set to min <= ald < max
        aoi_mask: np.array of bools( optional)
            if provided ALD is set where mask is true, other wise 0
        
        Returns
        -------
        np.array
            random ald grid
        """
        grid = np.random.uniform(init_ald[0], init_ald[1], shape ).flatten()
        if aoi_mask is None:
            aoi_mask = grid == grid
        
        grid[ aoi_mask.flatten() == False ] = 0
        
        
        return grid
    
    def read_grid (self, init_ald):
        """Read init ald from file or object"""
        raise NotImplementedError
        
    def get_ald_at_time_step (self, time_step = -1, flat = True):
        """returns ald at a given time step
        
        Parameters
        ----------
        time_step: int, default -1
            timestep to get ald at
        flat: bool
            if true returns 1d array, else reshapes to shape
            
        Returns
        -------
        np.array
            ald at time step
        """
        shape = self.ald_grid[time_step].shape
        if not flat:
            shape = self.shape
        return self.ald_grid[time_step].reshape(shape)
        
    def get_ald (self, flat = True):
        """gets ald grid
        
         Parameters
        ----------
        flat: bool
            if true each year is a 1d array, else each year reshapes to shape
        
        Returns
        -------
        np.array
            the ald grid at all time steps
        """
        shape = tuple([len(self.ald_grid)] + list(self.ald_grid[0].shape))
        if not flat:
            shape = tuple([len(self.ald_grid)] + list(self.shape))
            
        return np.array(self.ald_grid).reshape(shape)
        
    def set_ald_at_time_step (self, time_step, grid):
        """Sets the ALD grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            2D array with shape matching shape attribute
        """
        if grid.shape != self.shape:
            raise StandardError('grid shapes do not match')
        self.ald_grid[time_step] = grid.flatten()
        
    def get_pl_at_time_step (self, time_step, cohort = None, flat = True):
        """gets the ALD grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to get
        cohort: Str or None
            cohort to return
        flat: bool
            keeps grid flat if true
            
        Returns
        -------
        np.array
            the grid of the cohort, if a cohort is provided, other wise
            returns all cohorts. Data is reshaped to grid shape if flat is
            false
        """
        if cohort is None:
            if flat:
                return pl_self.grid[time_step] 
            else:
                return self.pl_grid[time_step].reshape(
                    len(self.init_pl_grid),
                    self.shape[ROW],
                    self.shape[COL]
                )
        # else get cohort
        cohort = self.pl_key_to_index[cohort]
        r_val = self.pl_grid[time_step][cohort]
        if flat:
            return r_val
        else: 
            return r_val.reshape(self.shape[ROW], self.shape[COL])
        
        
    def set_pl_at_time_step (self, time_step, data):
        """Sets the PL grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            3D array that can be reshaped to match initial_l_grid shape
        """
        shape = self.init_pl_grid.shape
        self.pl_grid[time_step] = data.reshape(shape)

    def set_pl_cohort_at_time_step (self, time_step, cohort, data):
        """Sets the PL grid for a cohort at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        cohort: str
            cohort to set
        grid: np.array
            2d array that can has shape equal to  self.shape
        """
        idx = self.pl_key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        self.pl_grid[time_step][idx] = data.flatten()
        
    def add_time_step (self, zeros = False):
        """adds a time step for ald_grid and pl_grid
        
        Parameters
        ----------
        zeros: bool
            if set to true data is set as all zeros
        
        """
        self.ald_grid.append(copy.deepcopy(self.ald_grid[-1]))
        self.pl_grid.append(copy.deepcopy(self.pl_grid[-1]))
        if zeros:
            self.ald_grid[-1] = self.ald_grid[-1]*0
            self.pl_grid[-1] = self.pl_grid[-1]*0
            
    
    def calc_ald(self, init_tdd, current_tdd, flat = True):
        """caclulates the ald from thawing degreedays for all cells
        
        Parameters
        ----------
        init_tdd: np.array
            initial Thawing Degree-days
        current_tdd: np.array
            Thawing  Degree-days for the current time step
        flat: bool, defaults True
            if true array is kept flat, else reshaped to shape
        
        Returns
        -------
        np.array
            the ald grid
        """ 
        shape = self.shape
        if flat:
            shape = self.shape[0] * self.shape[1]
        return (self.init_ald_grid.flatten() * \
            np.sqrt(current_tdd / init_tdd).flatten()).reshape(shape)
        
        
    def init_ald_figure (self, filename):
        """ save initilal ald figure
        
        Parameters
        ----------
        filename: path
            file to save
        """
        title = 'Initial Active Layer Depth'
        data = self.init_ald_grid.reshape(self.shape) 
        image.save_img(data, filename, title,
            cbar_extend = 'max', cmap='bone'
        ) 
        
    def init_ald_binary (self, filename):
        """ save initial ald as binary np array 
        
        Parameters
        ----------
        filename: path
            file to save
        """
        binary.save_bin(self.init_ald_grid.reshape(self.shape), filename)
    
    def ald_constants_figure (self, filename):
        """ save initilal  ald constants figure
        
        Parameters
        ----------
        filename: path
            file to save
        """
        title = 'Initial Active Layer Depth'
        data = self.ald_constants.reshape(self.shape) 
        image.save_img(data, filename, title,
            cbar_extend = 'max', cmap='bone'
        ) 
        
    
        
    def ald_constants_binary (self, filename):
        """ save initial ald constants as binary np array 
        
        Parameters
        ----------
        filename: path
            file to save
        """
        binary.save_bin(self.ald_constants.reshape(self.shape), filename)
        
