"""POI_grid.py

POI: probablity of instantiation
"""

import numpy as np
import os

from constants import ROW, COL


class POIGrid (object):
    """ Class doc """

    def __init__ (self, config):
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
        self.start_year = int(config['start year'])

        shape = config['shape']
        cohorts = config['cohort list']

        ## read input
        ## rename init_grid??
        self.init_grid, self.key_to_index = self.setup_grid(shape, cohorts)
        
        ## rename grid_history?
        self.grid = [self.init_grid]

        self.shape = config['shape']
        
    def setup_grid (self, shape, cohorts):
        """sets up poi grid for each cohort
        
        
        Parameters
        ----------
        shpae: tuple of ints
            shape( (row,col) dimensions) of grid
        cohorts: list 
            list of cohorts in model domain
            
        Returns
        -------
        np.array
            2d array of each cohorts flattended POI grid
        dict
            map of each cohort to an index
        """
        
        poi_grid = np.zeros(shape).flatten()
        
        grid = []
        key_to_index = {}
        index = 0 
        for cohort in cohorts:
            grid.append( poi_grid ) 
            key_to_index[ cohort ] = index
            index += 1
        
        return  np.array(grid), key_to_index
        
        
    def __getitem__ (self, key):
        """Gets cohort data.
        
        Can get data for a cohort at all time steps, all cohorts at a ts, 
        or a cohort at a given ts
        
        Parameters
        ----------
        key: Str, int, or tuple(int,str)
            if key is a string, it should be a canon cohort name.
            if key is an int, it should be a year >= start_year, 
            but < start_year + len(grid)
            if key is tuple, the int should fit the int requirements, and the 
            string the string requirements. 
            
        Returns
        -------
        np.array
            if key is a string, 3D, dimension are [timestep][grid row][grid col],
            timestep is year(key) - start year
            if key is a int, 3D, dimension are [cohort #][grid row][grid col],
            use key_to_int to find cohort #
            if key is tuple, 2D, [grid row][grid col]
        """
        if type(key) is str: ## cohort at all ts
            get_type = 'cohort' 
        elif type(key) is int: ## all cohorts at a ts
            get_type = 'ts' 
        else: # tuple ## a cohort at a ts
            get_type = 'cohort at ts' 
            
            
        if 'cohort' == get_type: 
            return self.get_cohort(key, False)
        elif 'ts' == get_type:
            year = key - self.start_year
            return self.get_all_cohorts_at_time_step(year, False)
        elif 'cohort at ts' == get_type:
            year, cohort = key
            year = year-self.start_year
            return self.get_cohort_at_time_step(cohort, year, False)
            
    def __setitem__ (self, key, data):
        """Set cohort data. 
        
        Can set a grid for a cohort(or all cohorts) at a timestep. Will add 
        time step id desired time step == len(grid)
        
        Parameters
        ----------
        key: Str, int, or tuple(int,str)
            if key is a string, raises NotImplementedError
            if key is an int, it should be a year >= start_year, 
            but <= start_year + len(grid)
            if key is tuple, the int should fit the int requirements, and the 
            string should be a canon cohort name
        data: np.ndarray
            data of the proper shape. for tuple key shape = shape attribute, 
            else rebroadcastable to shape of init_grid
            
        Raises
        ------
        NotImplementedError
            if key is str, 'cannot set a cohort at all time steps'
        KeyError, 
            if key's year value < star_year or > star_year + len(grid)
        """
        if type(key) is str: ## cohort at all ts
            #~ get_type = 'cohort' 
            raise NotImplementedError, 'cannot set a cohort at all time steps'
        elif type(key) is int: ## all cohorts at a ts
            get_type = 'ts' 
            year = key
        else: # tuple ## a cohort at a ts
            get_type = 'cohort at ts' 
            year, cohort = key
            
        if year == self.start_year + len(self.grid):
            ## year == end year + 1 
            ## (I.e start_year == 1900, len(grid) =10, year = 1910)
            ## time steps from 0 - 9, (1900 - 1909)
            ## year - star_year = 10, no 10 as a time,
            ## but 10 == year - star_year, or 1910 == start_year+len(grid)
            ## so, will add a new grid year, because it is end +1, and set 
            ## values to 0
            self.add_time_step(True)
        elif year > self.start_year + len(self.grid):
            raise KeyError, 'Year too far after current end'
        elif year < self.start_year:
            raise KeyError, 'Year before start year'
        
            
        if  'ts' == get_type:
            ts = year - self.start_year
            self.set_all_cohorts_at_time_step(ts, data)
        elif  'cohort at ts' == get_type:
            ts = year - self.start_year
            self.set_cohort_at_time_step(cohort, ts, data)
        
        
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True):
        """Get a cohorts POI grid at a given time step
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        time_step: int, defaults -1
            time step to retrieve, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with correct dimension
            
        Returns
        -------
        np.array
            The cohorts POI grid at a given time step. 
        """
        cohort = self.key_to_index[cohort]
        
        
        r_val = self.grid[time_step][cohort]
       
        if flat:
            return r_val
        else: 
            return r_val.reshape(
                self.shape[ROW], self.shape[COL]
            )
            
    def get_cohort (self, cohort, flat = True):
        """Get a cohorts POI grid at all time steps
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        flat: bool
            keep the data flat, or convert to 2d grid with correct dimensions
            
        Returns
        -------
        np.array
            The cohorts POI grids at all time steps. 
        """
        cohort = self.key_to_index[cohort]
        
        
        r_val = np.array(self.grid)[:,cohort]
        
        if flat:
            # sum all age buckets for cohort(check1)
            return r_val
        else:
            return r_val.reshape(len(self.grid),
                self.shape[ROW], self.shape[COL])
                
    def get_all_cohorts_at_time_step (self, time_step = -1, flat = True):
        """Get all cohort POI grids at a given time step
        
        Parameters
        ----------
        time_step: int, defaults -1
            time step to retrieve, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with correct divisions
            
        Returns
        -------
        np.array
            all cohorts POI grids at a given time step in a 2d 
        array. 
        """
        ## do we want this to sum the age buckets
        if flat:
            # sum all age buckets for cohort
            return self.grid[time_step] 
        else:
            return self.grid[time_step].reshape(len(self.init_grid),
                self.shape[ROW], self.shape[COL])
                
        
    ## don't need a set_cohort, because we only want to set one ts at a time
    ## really only the most recent time_step.
    def set_cohort (self, cohort, data):
        """If implemented should set a cohort at all time steps
        
        Parameters
        ----------
        cohort: str
            canon name of cohort
        data: array like
        """
        raise NotImplementedError, 'cannot set POI grid at all time steps'
    
    def set_cohort_at_time_step(self, cohort, time_step, data):
        """Set a cohort POI grid at a given time step, ensures the max
        value is 1 and the min value is 0.
        
        Parameters
        ----------
        cohort: str
            canon name of cohort
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            2D array with shape matching shape attribute
            
        Raises
        ------
        StandardError
            bad shape
        """
        idx = self.key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        d = data.flatten()
        d[ d>1 ] = 1.0
        d[ d<0 ] = 0.0
        self.grid[time_step][idx] = d
        
    def set_all_cohorts_at_time_step(self, time_step, data):
        """Sets all POI cohorts at a time step
        
        Raises
        ------
        NotImplmentedError
            Setting all cohorts POI is not a thing to do
        
        Parameters
        ----------
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            3D array with shape rebroadcastable to init_grid.shape())
            i.e [cohorts][ages][grid]
        """
        raise NotImplementedError, \
            'cannot set all cohort POI grids at all time steps'
        #~ shape = self.init_grid.shape
        #~ self.grid[time_step] = data.reshape(shape)
        
    def add_time_step (self, zeros=False):
        """adds a new grid timestep and exact copy of the previous timestep
        
        Parameters
        ----------
        zeros : bool
            set new years data to 0 if true
        """
        self.grid.append(self.grid[-1])
        if zeros:
            self.grid[-1] = self.grid[-1]*0
    
    def save_cohort_at_time_step (self, cohort, path,
            time_step = -1, bin_only = True, binary_pixels = False):
        """various save functions should be created to save, reports, images, 
        or videos
        
        returns base file name
        """
        cohort_data = self.get_cohort_at_time_step(
            cohort, time_step, flat = False
        )
        
        if binary_pixels:
            ## see if cohort is present or not
            cohort_data[cohort_data>0] = 1
        #~ self.ts_to_year(time_step)
        year = 'TEMP_YEAR'
        filename = cohort+ "_POI_" + str(year)
        bin_path = os.path.join(path, filename + '.bin')
        save_bin(cohort_data, bin_path)
        if not bin_only:
            img_path = os.path.join(path, filename + '.png')
            save_img(cohort_data, img_path, filename) # pretty names
            
        return filename
            


