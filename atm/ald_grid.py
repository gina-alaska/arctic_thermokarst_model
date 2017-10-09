"""ald_grid.py

for the puproses of this file ALD(or ald) refers to Active layer depth,
and PL (or pl) to Protective layer
"""
import numpy as np



class ALDGrid(object):
    """ Class doc """
    
    def __init__ (self, shape, cohort_list, init_ald):
        """ Class initialiser """
        
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
        
    def get_ald_at_time_step (self, time_step):
        """ Function doc """
        pass
        
    def set_ald_at_time_step (self, time_step):
        """ Function doc """
        pass
        
    def get_pl_at_time_step (self, time_step, cohort = None):
        """ Function doc """
        if cohort is None:
            ## get all
            pass
        # else get cohort
        pass
        
    def set_pl_at_time_step (self, time_step, cohort = None):
        """ Function doc """
        if cohort is None:
            ## set all
            pass
        # else set cohort
        pass
        
        
    def save_ald (self, time_step):
        """ save ald at time step """
        pass
        
