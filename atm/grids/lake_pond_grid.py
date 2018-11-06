"""
lake pond grid
--------------

"""
import numpy as np
# import pickle
import os

from constants import ROW, COL

try:
    from cohorts import find_canon_name, DISPLAY_COHORT_NAMES 
except ImportError:
    from ..cohorts import find_canon_name, DISPLAY_COHORT_NAMES 
    
    
    
try:
    from atm_io import binary, image, raster
except ImportError:
    from ..atm_io import binary, image, raster

from multigrids import TemporalMultiGrid, common
import copy

config_ex = {
    'pickle path': './pickles',
    'pond types': ['Ponds_WT_Y', 'Ponds_WT_M', 'Ponds_WT_O'],
    'lake types': [
        'SmallLakes_WT_Y', 'SmallLakes_WT_M', 'SmallLakes_WT_O',
        'MediumLakes_WT_Y', 'MediumLakes_WT_M', 'MediumLakes_WT_O',
        'LargeLakes_WT_Y', 'LargeLakes_WT_M', 'LargeLakes_WT_O',
    ],
    'grid_shape' : (10,10),
    'pond depth range' : (.3,.3),
    'lake depth range' : (.3, 5),
    
    'ice depth alpha range': (2.31, 2.55),
    'initialization year': 1900,
    'model length': 5
    
    
    
}


class LakePondNotFoundError (Exception):
    """Raised if lake/pond type not found"""


class LakePondGrid (TemporalMultiGrid):
    """Lake Pond Depth grid
    """
    
    def __init__ (self, *args, **kwargs):
        """Lake Pond Depth grid
        
        Parameters
        ----------
        
        
        Attributes
        ----------
        shape: tuple
            shape of object
        start_year: int
            star year 
        time_step: int
            offset from start year
        counts: dict
            counts for each type of lake/pond
        depths: dict
            lake/pond depth range grids
        pickel_path: path
            path to pickle file
        ice_depth_constatns: np.array
            array of alpha ice constatns for stephan equation
        """
        config = args [0]
        if type(config) is str:
            super(LakePondGrid , self).__init__(*args, **kwargs)
        else:

            lake_pond_types = config['pond types'] + config['lake types']
            grid_names = [lp + '_depth' for lp in lake_pond_types]
            grid_names += [lp + '_count' for lp in lake_pond_types]
            grid_names += \
                [lp + '_time_since_growth' for lp in config['pond types']]
            grid_names += [
                'ice_depth',
                # 'ice_depth_constants', ## constants don't change over time,
                                         ## so they are part of the config now
                'climate_expansion_lakes',
                'climate_expansion_ponds',
            ]
        
            args = [
                config['grid_shape'][ROW], config['grid_shape'][COL], 
                len(grid_names), config['model length']
            ]

            kwargs = copy.deepcopy(config) 
            kwargs['data_type'] = 'float'
            kwargs['mode'] = 'r+'
            kwargs['grid_names'] = grid_names
            super(LakePondGrid , self).__init__(*args, **kwargs)
            self.config['start_year'] = int(config['initialization year'])
            self.config['start_timestep'] = self.config['start_year']

             
            init_pond = config['pond depth range']
            init_lake = config['lake depth range']
            self.setup_random_range(
                [t + '_depth' for t in config['pond types']],
                self.grid_shape, 
                init_pond
            )
                
            self.setup_random_range(
                [t + '_depth' for t in config['lake types']], 
                self.grid_shape, 
                init_lake
            )

            alpha_range = config['ice depth alpha range']
            #############
            self.config['ice_depth_constants'] =  np.random.uniform(
                alpha_range[0], alpha_range[1], self.grid_shape
            )#.flatten()

            
        self.current_year = self.current_timestep
        

    def setup_random_range (self, types, shape, init_depth):
        """set up initial data for a grid given a random range
        
        Parameters
        ----------
        types: list
            list of cohorts 
        shape: tuple
            (row, col) shape of model
        init_depth: tuple
            (min,max) initial depth
            
            
        Returns
        -------
        dict:
            dictionary of depth grids
        """
        for t in types:
            self[ t ,self.start_year] = np.random.uniform(
                init_depth[0], init_depth[1], shape
            )
        
    def apply_lake_pond_mask (self, lake_pond_type, mask):
        """Apply Mask to cells, will set depth to 0 in cells with no lakes/ponds
        of lake_pond_type, at current timestep
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        mask: np.array
            mask with shape of shape attribute
            
        Raises
        ------
        LakePondNotFoundError
        """
        # if lake_pond_type in self.depths:
        try:
            self[lake_pond_type + '_depth', self.current_year()]\
                [np.logical_not(mask)] = 0
        except KeyError:
            msg = 'Lake/Pond type(' + lake_pond_type +\
                ') not found in LakePondGrid depth data'
            raise LakePondNotFoundError, msg

    def set_grid_at_current_timestep(self, grid_name, grid):
        """Set the grid at the current time step

        Parameters
        ----------
        grid_name: str
            a grid name
        grid: np.array like
            Grid data that can be reshaped to grid_shape
        """
        try:
            self[grid_name, self.current_year()] =\
                grid.reshape(self.shape)
        except KeyError:
            msg = 'Lake/Pond type(' + grid_name +\
                ') not found in LakePondGrid data'
            raise LakePondNotFoundError, msg

    def set_depth_grid (self, lake_pond_type, grid):
        """set a depth grid, at current timestep, for a lake or pond type
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        grid: np.array
            grid of depths that can be reshaped to shape
            
        Raises
        ------
        LakePondNotFoundError
        
        """
        self.set_grid_at_current_timestep(lake_pond_type + '_depth',grid)

    def set_count (self, lake_pond_type, count):
        """set a counts grid
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        count: np.array
            grid of count that can be reshaped to shape
            
        Raises
        ------
        LakePondNotFoundError
        """
        self.set_grid_at_current_timestep(lake_pond_type + '_count',count)
        
    def calc_ice_depth (self, fdd):
        """calculate current ICE depth, using a modified Stefan Equation as
        described in setup_ice_depth_constants. Sets current_timestep's data
        
        h     : ice thickness (m)
        alpha : Stefan coefficient (set in set_lake_ice_constant.py)
        FDD   : Freezing Degree days
        100   : Conversion from cm to m
        
        h = (alpha * sqrt(FDD))/100.0  
        
        Parameters
        ----------
        fdd: np.array
            freezing degree days
            
        
        """    
        fdd = fdd.reshape(self.grid_shape)
        self['ice_depth', self.current_year()] = ((
            self.ice_depth_constants * np.sqrt(-1. * fdd)
        )/100.)
            
    def depth_figure(self, cohort, filename, time_step = -1):
        """Save lake depth figures
        
        Parameters
        ----------
        cohort: str
            lake pond type
        filename: path
            file to save
        time_step: int 
            time step to save
        """
        if time_step == -1:
            time_step = self.current_year()
        title = 'Inital Depth \n' + DISPLAY_COHORT_NAMES[cohort] 
        cohort_data = self[cohort+'_depth', time_step]
        image.save_img(cohort_data, filename, title,  cbar_extend = 'max') 
        
        
