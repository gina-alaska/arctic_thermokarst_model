"""
ald_grid
--------

for the purposes of this file ALD(or ald) refers to Active layer depth,
and PL (or pl) to Protective layer
"""
import numpy as np

from .constants import ROW, COL, create_deepcopy


import copy

from multigrids import TemporalMultiGrid

def random_grid (shape, minimum, maximum, mask = None):
        """create a random ALD grid
        
        Parameters
        ----------
        shape:  
        
        min:
        max:
        mask: np.array of bools( optional)
            if provided ALD is set where mask is true, other wise 0
        
        Returns
        -------
        np.array
            random ald grid
        """
        grid = np.random.uniform( minimum, maximum, shape ).flatten()
        if mask is None:
            mask = grid == grid
        
        grid[ mask.flatten() == False ] = 0
        
        return grid

class ALDGrid(TemporalMultiGrid):
    """ALD, and PL object """
    
    def __init__ (self, *args, **kwargs):
        """Represents ALD, and PL for each cohort for the model
        
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
        config = args[0]

        grid_names = self.setup_grid_info(config)

        args = [
            config['grid_shape'][ROW], config['grid_shape'][COL], 
            len(grid_names), config['model length']
        ]

        kwargs = create_deepcopy(config) 
        # kwargs['data_type'] = 'float'
        kwargs['mode'] = 'r+'
        kwargs['grid_names'] = grid_names
        super(ALDGrid , self).__init__(*args, **kwargs)

        init_grids = self.setup_grids(config)

        self.grids[0,:] = init_grids
        self.config['start_year'] = int(config['initialization year'])
        self.config['start_timestep'] = self.config['start_year']

        # shape = config['shape']
        # cohort_list = config['cohort list']
        # init_ald = config ['init ald']
        # self.start_year = config ['initialization year']
        
        # ## setup soil properties
        self.porosity = config['_FAST_get_get_porosities']
        # self.protective_layer_factor = config['PL factors']
        # self.aoi_mask = config['AOI mask']
        
        # ald, pl, pl_map = self.setup_grid ( 
        #     shape, 
        #     cohort_list, 
        #     init_ald, 
        #     self.aoi_mask, 
        #     self.protective_layer_factor 
        # )
        self.init_ald_grid = self.grids[0,0]
        self.init_pl_grid =self.grids[0,1:]
        # self.timestep = 0
        # self.pl_key_to_index = pl_map
        
       
        # self.shape = shape
        # self.ald_grid = [ self.init_ald_grid ]
        # self.pl_grid = [ self.init_pl_grid ]
        
        self.ald_constants = np.zeros(self.config['grid_shape'])
    
    def setup_grids(self, config):
        """ Function doc """
        
        grids = np.zeros(
            [self.config['num_grids'], self.config['grid_shape'][0]* self.config['grid_shape'][1]]
        )

        # print config['Terrestrial_Control']['Initial ALD']
        if type(config['Terrestrial_Control']['Initial ALD']) in [tuple, list]:
            grids[0] = random_grid(
                self.config['grid_shape'], 
                config['Terrestrial_Control']['Initial ALD'][0],
                config['Terrestrial_Control']['Initial ALD'][1], 
                config['AOI mask']
            )
        else:
            grids[0] = self.read_grid(
                config['Terrestrial_Control']['Initial ALD']
            )

        pl_factors = config['_FAST_get_pl_factors']#.get_protective_layer_factors()#['PL factors']

        # print pl_factors

        if pl_factors == {}:
            pl_factors = {key: 1 for key in cohorts}
        
        # print config['cohorts'].keys()
        # print self.grid_name_map
        for cohort in config['_FAST_get_cohorts']:
            grids[self.get_grid_number(cohort)] = grids[0] * pl_factors[cohort]
        return grids

    def setup_grid_info (self, config):
        """ Function doc """
        
        ## count number of grids needed for multigrid
        grid_names = ['ALD']
        for cohort in config['_FAST_get_cohorts']:
            #~ print cohort
            grid_names.append(cohort)
        
        return grid_names



        
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
        if key == 'PL' or 'PL' in key:
            raise NotImplementedError('get all PL timesteps not implemented')
        return super(ALDGrid , self).__getitem__(key)
        
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
            raise NotImplementedError('Cannot set layers for entire timeframe')
        if type(key) is str and 'PL' in key:
            raise NotImplementedError('PL key not implemented')
        return super(ALDGrid , self).__setitem__(key, value)
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
        
        self.ald_constants = (
            self.init_ald_grid.flatten() / degree_days
        ).reshape(self.config['grid_shape'])
    
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
        if time_step == -1:
            time_step = self.timestep
        return self.get_grid('ALD', time_step, flat)
        
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
        # shape = tuple([len(self.ald_grid)] + list(self.ald_grid[0].shape))
        # if not flat:
        #     shape = tuple([len(self.ald_grid)] + list(self.shape))
            
        # return np.array(self.ald_grid).reshape(shape)
        return self.get_grid_over_time('ALD',None,None,flat=flat)
        
    def set_ald_at_time_step (self, time_step, grid):
        """Sets the ALD grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            2D array with shape matching shape attribute
        """
        if grid.shape != self.config['grid_shape']:
            raise StandardError('grid shapes do not match')
        self['ALD', time_step+self.start_year] = grid.flatten()
        
    def get_pl_at_time_step (self, time_step, cohort = None, flat = True):
        """gets All PL layers at at a time step
        
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
        raise NotImplementedError('Cannot set all PL layers all at time steps')
        
    def set_pl_at_time_step (self, time_step, data):
        """Sets the PL grid at a time step
        
        Parameters
        ----------
        time_step: int
            time step to set
        grid: np.array
            3D array that can be reshaped to match initial_l_grid shape
        """
        raise NotImplementedError('Cannot set all PL layers all at time steps')

    def set_pl_cohort_at_time_step (self, cohort, time_step, data):
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
        if data.shape != self.config['grid_shape']:
            raise StandardError('grid shapes do not match')
        self[cohort, time_step+self.start_year] = data.flatten()
        
        
    def add_time_step (self, zeros = False):
        """adds a time step for ald_grid and pl_grid
        
        Parameters
        ----------
        zeros: bool
            if set to true data is set as all zeros
        
        """
        # self..append(copy.deepcopy(self.ald_grid[-1]))
        # self.pl_grid.append(copy.deepcopy(self.pl_grid[-1]))
        
        self.timestep += 1
        self.grids[self.timestep, : ] = self.grids[self.timestep - 1, : ] 
        if zeros:
            self.grids[self.timestep, : ]  = 0
            
    
    def calc_ald(self, init_tdd, current_tdd, flat = True):
        """calculates the ald from thawing degreedays for all cells
        
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
        shape = self.config['grid_shape']
        if flat:
            shape = shape[0] * shape[1]
        return (self.init_ald_grid.flatten() * \
            np.sqrt(current_tdd / init_tdd).flatten()).reshape(shape)

def test (files):
    """
    """
    mask = np.ones([5, 10])
    mask[:,5:] = 0
    config = {
        'target resolution': (1000,1000),
        'grid_shape': [5, 10],
        'initialization year': 1900,
        'area data': files,
        'model length': 100,
        'Initial ALD': (.9, 1),
        'AOI mask': mask,
        'cohorts':[ 
            'Meadow_WT_Y',
            'Meadow_WT_M',     
            'Meadow_WT_O'
        ],
        'PL factors': {
            'Meadow_WT_Y':.25,
            'Meadow_WT_M':.5,     
            'Meadow_WT_O':.75
        }

    }
    
    return ALDGrid(config)
