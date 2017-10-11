"""ald_grid.py

for the puproses of this file ALD(or ald) refers to Active layer depth,
and PL (or pl) to Protective layer
"""
import numpy as np

from terraingrid import ROW, COL


class ALDGrid(object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        
        shape = config['shape']
        cohort_list = config['cohort list']
        init_ald = config ['init ald']
        
        ## setup soil properites
        self.porosity = config['porosity map']
        self.protective_layer_factor = ['PL factor map']
       
        ald, pl, pl_map = self.setup_grid ( shape, cohort_list, init_ald)
        self.init_ald_grid = ald
        self.init_pl_grid = pl
        self.pl_key_to_index = pl_map
        
       
        self.shape = shape
        self.ald_grid = [ self.init_ald_grid ]
        self.pl_grid = [ self.init_pl_grid ]
    
        
    def __getitem__ (self, key):
        """ Function doc """
        pass
        
    def __setitem__ (self, key, value):
        """ Function doc """
        pass
        
    def setup_grid (self, shape, cohorts, init_ald, pl_modifiers = {}):
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
            ald_grid = self.random_grid(shape, init_ald)
        else:
            ald_grid = self.read_grid(init_ald)
        
        if pl_modifiers == {}:
            pl_modifiers = {key: 1 for key in cohorts}
        
        ## protective layer (pl)
        pl_grid = []
        pl_key_to_index = {}
        index = 0 
        for cohort in cohorts:
            pl_grid.append(ald_grid * pl_modifiers[cohort]) 
            pl_key_to_index[ cohort ] = index
            index += 1
            
        return ald_grid, pl_grid, pl_key_to_index
        ## need to add random chance + setup for future reading of values

    def random_grid (self, shape, init_ald):
        """ Function doc """
        return np.random.uniform(init_ald[0],init_ald[1], shape ).flatten()
    
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
        
    def get_pl_at_time_step (self, time_step, cohort = None):
        """ Function doc """
        if cohort is None:
            if flat:
                return pl_self.grid[time_step] 
            else:
                return self.pl_grid[time_step].reshape(
                    len(self.init_grid),
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
        """ Function doc """
        shape = self.init_pl_grid.shape
        self.pl_grid[time_step] = data.reshape(shape)

    def set_pl_cohort_at_time_step (self, time_step, cohort, data):
        """ Function doc """
        idx = self.key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        self.grid[time_step][idx] = data.flatten()
        
    def add_time_step (self, zeros = False):
        """adds a time step for ald_grid and pl_grid"""
        self.ald_grid.append(self.ald_grid[-1])
        self.pl_grid.append(self.pl_grid[-1])
        if zeros:
            self.ald_grid[-1] = self.ald_grid[-1]*0
            self.pl_grid[-1] = self.pl_grid[-1]*0
        
        
        
    def save_ald (self, time_step):
        """ save ald at time step """
        pass
        
