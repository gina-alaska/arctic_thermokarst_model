"""
area_grid
---------

Contains objects to represent internal grid cohort data in ATM
"""
import numpy as np
import os
import sys

try:
    from cohorts import find_canon_name, DISPLAY_COHORT_NAMES 
except ImportError:
    from ..cohorts import find_canon_name, DISPLAY_COHORT_NAMES 
    

try:
    from tools import read_raster_layers
except ImportError:
    from ..tools import read_raster_layers

from .constants import ROW, COL, create_deepcopy

import copy

from multigrids import TemporalMultiGrid, common, TemporalGrid


try:
    import moviepy.editor as mpy
except StandardError:
    mpy = None







def get_example_config( data_dir ):
    """
    Patameters
    ----------
    data_dir: path
        path to input raster layers
    
    Returns
    -------
    dict
        example configs
    """
    files = [ os.path.join(data_dir, f) for f in os.listdir( data_dir )] 
    config_ex = {
        'Target_resolution': (1000,1000),
        'initialization_year': 1900,
        'Initial_Area_data': files,
        'model length': 100
    }
    return config_ex


class MassBalanceError (Exception):
    """Raised if there is a mass balance problem"""

class AreaGrid(TemporalMultiGrid):
    """ AreaGrid represents fractional areas of each cohort in a grid element
    """

    ## REDO DOCS
    def __init__ (self, *args, **kwargs):
        """This class represents model area grid as fractional areas of each
        cohort that make up a grid element. In each grid element all
        fractional cohorts should sum to one.
        
        
        .. note:: Note on grid coordinates
            Origin (Y,X) is top left. rows = Y, cols = X
            Object will store dimensional(resolution, dimensions) 
            metadata as a tuple (Y val, X val).
            
        Parameters
        ----------
        input_data: list
            list of tiff files to read
        target_resolution: tuple
            (Y, X) target grid size in (m, m)
            
        Attributes
        ----------
        input_data : list
            list of input files used
        shape : tuple of ints
            Shape of the grid (y,x) (rows,columns)
        resolution : tuple of ints
            resolution of grid elements in m (y,x)
        grid : array
                This 3d array is the grid data at each time step. 
            The first dimension is the time step with 0 being the initial data.
            The second dimension is the flat grid for given cohort, mapped using  
            key_to_index. The third dimension is the grid element. Each cohort
            can be reshaped using  shape to get the proper grid
        init_grid: np.ndarray 
                The initial data corrected to the target resolution. Each
            row is one cohort percent grid flattened to a 1d array. The 
            the index to get a given cohort can be looked up in the 
            key_to_index attribute.
        key_to_index : dict
                Maps canon cohort names to the index for that cohort in the 
            data object 
        raster_info : dict of RASTER_METADATA
            Metadata on each of the initial raster files read
        
        
        """
        config = args [0]
        if type(config) is str:
            super(AreaGrid , self).__init__(*args, **kwargs)
        else:
            input_rasters = config['Initial_Area_data'] 
            target_resolution = config['Target_resolution']

            logger = None
            if 'logger' in kwargs:
                logger = kwargs["logger"]
            layers, raster_metadata = read_raster_layers.read_layers(
                input_rasters, target_resolution, logger
            ) 

            # add in ages here
            # print layers.grids.shape
            layers_with_ages, grid_name_map_with_ages = \
                self.setup_cohort_ages(layers)
            # print layers_with_ages
            # print layers.grids.shape

            args = [
                layers.config["grid_shape"][ROW], 
                layers.config["grid_shape"][COL], 
                layers_with_ages.shape[0], 
                config['model length']
            ]

            kwargs = create_deepcopy(config) 
            # kwargs['data_type'] = 'float'
            kwargs['mode'] = 'r+'
            # kwargs['filename'] = 'test.mgdatatest'
            # kwargs['cfg_path'] = './'

            # kwargs['grid_names'] = layers.
            super(AreaGrid , self).__init__(*args, **kwargs)
            # print self.grids.shape
            # self.config['grid_names'] = layers.grid_names
            self.config['grid_name_map'] = grid_name_map_with_ages
            self.grids[0,:] = layers_with_ages.reshape(self.config['memory_shape'][1:])

            self.key_to_index = grid_name_map_with_ages
        
            self.config['start_year'] = int(config['initialization_year'])
            self.config['resolution'] = target_resolution

        self.config['start_timestep'] = self.config['start_year']
        
        self.shape = self.config['grid_shape']
        self.init_grid = self.grids[0]
        self.config['AOI mask'] = self.area_of_interest()
        # self.config['mask'] = self.area_of_interest()

    def setup_cohort_ages(self, layers):
        """ Function doc """
        layers_with_ages = [] 
        grid_name_map_with_ages = {}
        index = 0
        for layer in layers.config['layer_names']:
            layers_with_ages.append(layers[layer].flatten())
            grid_name_map_with_ages[layer + '--0'] = index
            slice_start = index
            index += 1
            num_years = 1 # < to be set based on cohort age range later, FOR TRACKING AGE OF COHORTS <<<<<<<<<<<<<
            for age in range(1, num_years):
                layers_with_ages.append(np.zeros(
                    layers.config["grid_shape"][0] *\
                    layers.config["grid_shape"][1]
                ))
                grid_name_map_with_ages[layer + '--' + str(age) ] = index
                index += 1
            slice_end = index
            grid_name_map_with_ages[layer] = slice(slice_start,slice_end)

        layers_with_ages = np.array(layers_with_ages)
        return layers_with_ages, grid_name_map_with_ages

    @staticmethod
    def is_grid_with_range(key):
        return type(key) is tuple and len(key) == 2 and \
            type(key[0]) in (str,slice) and type(key[1]) is slice

    @staticmethod
    def is_grid_with_index(key):
        return type(key) is tuple and len(key) == 2 and \
            type(key[0]) in (str,slice) and type(key[1]) is int

    ## REDO DOCS
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True, sum_age_grids = True):
        """Get a cohort at a given time step
        
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
            The cohorts fractional area grid at a given time step. 
        """
        if time_step == -1:
            time_step = self.config['timestep']

        grids = self.get_cohort(cohort, flat, sum_age_grids)

        return grids[time_step]
    
    ## REDO DOCS
    def get_cohort (self, cohort, flat = True, sum_age_grids = True):
        """Get a cohort at all time steps
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        flat: bool
            keep the data flat, or convert to 2d grid with correct dimensions
            
        Returns
        -------
        np.array
            The cohorts fractional area grid at all time steps. 
        """
        grids = self[cohort]

        if sum_age_grids and type(self.get_grid_number(cohort)) is slice:
            grids = grids.sum(1)

        if flat:
            grids = grids.reshape(self.config['num_timesteps'], np.prod(self.config['grid_shape']))
        
        return grids
                
    ## REDO DOCS
    def get_all_cohorts_at_time_step (self, time_step = -1, flat = True):
        """Get all cohorts at a given time step
        
        Parameters
        ----------
        time_step: int, defaults -1
            time step to retrieve, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with correct divisions
            
        Returns
        -------
        np.array
            all cohorts fractional area grids at a given time step in a 2d 
        array. 
        """
        if time_step == -1:
            time_step = self.config['timestep']
        grids = self[time_step + self.config['start_year'] ]
        if flat:
            grids = grids.reshape(self.config['num_grids'], np.prod(self.config['grid_shape']))
        return grids
          
    def total_fractional_area(self, time_step):
        """get total fractional area for each grid element at a time step 
        
        Parameters
        ----------
        time_step: int
        
        Returns
        -------
        np.array
            total fractional area array
        """            
        grid = self[time_step + self.config['start_year']]
        return np.round(grid.sum(0), decimals = 6 )
                
    def check_mass_balance (self, time_step=-1):
        """reruns true if mass balance is preserved. Raises an exception, 
        otherwise
        
        Parameters 
        ----------
        time_step : int, defaults -1
            time step to test
        
        Raises
        ------
        MassBalanceError
            if any grid element at time_step is <0 or >1
        
        Returns
        -------
        Bool
            True if no mass balance problem found.
        """
        if time_step == -1:
            time_step = self.config['timestep']
        ATTM_Total_Fractional_Area = self.total_fractional_area(time_step)
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) > 1.0).any():
            raise MassBalanceError(
                'Mass balance has become greater than 1. Mass was gained.'
            )
            ## write a check to locate mass balance error
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) < 0.0).any():
            raise MassBalanceError(
                'Mass balance has become greater less than 0. Mass was lost'
            )
            
        return True
        
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
        raise NotImplementedError(
            'AreaGrid cannot set a cohort at all time steps.'
        )
    
    ## REDO DOCS
    def set_cohort_at_time_step(self, cohort, time_step, data):
        """Set a cohort at a given time step
        
        Parameters
        ----------
        cohort: str
            canon name of cohort
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            2D array with shape matching shape attribute
        """
        self[cohort, time_step + self.config['start_year']] = data

    ## REDO DOCS 
    def set_all_cohorts_at_time_step(self, time_step, data):
        """Sets all cohorts at a time step
        
        
        Parameters
        ----------
        time_step: int
            0 <= # < len(grid)
        data: np.ndarray
            3D array with shape rebroadcastable to init_grid.shape())
            i.e [cohorts][ages][grid]
        """
        # shape = self.init_grid.shape
        # self.grid[time_step] = data.reshape(shape)
        self[time_step + self.config['start_year']] = data
        
            
    def area_of_interest (self, time_step = 0):
        """get area of interest at a time step
        
        Parameters
        ----------
        time_step: int, default 0
        
        Returns
        -------
        np.array
            a grid of booleans where true elements are in AOI, false are not
        """
        return (self.total_fractional_area(time_step) > 0.0).reshape(self.shape)
        
    def save_init_age_figure (self, cohort, path): 
        """save the init age figure
        
        Parameters
        ----------
        cohort: str
            cannon cohort name
        path: path
            path to output file at
        """
        file_name = cohort + '_age'
        title = DISPLAY_COHORT_NAMES[cohort] + ' - Initial Age'
        self.save_cohort_at_time_step(
            cohort, path, file_name, title,
            time_step = 0, bin_only=False, cbar_extend = 'max',
            colormap = 'bone', binary_pixels = True
        )
        
    def save_init_dist_figure (self, cohort, path): 
        """save the init distribution figure
        
        Parameters
        ----------
        cohort: str
            cannon cohort name
        path: path
            path to output file at
        """
        file_name = 'Initial_' +cohort
        title = DISPLAY_COHORT_NAMES[cohort] + ' - Initial Cohort Distribution'
        self.save_cohort_at_time_step(
            cohort, path, file_name, title,
            time_step = 0, bin_only=False, cbar_extend = 'max',
            colormap = 'spectral', binary_pixels = True
        )
        
    def save_init_normal_figure (self, cohort, path): 
        """save the init normalized Distribution figure (fractional area)
        
        Parameters
        ----------
        cohort: str
            cannon cohort name
        path: path
            path to output file at
        """
        file_name = cohort + '_fractional_cohorts'
        title = DISPLAY_COHORT_NAMES[cohort] + ' - Initial Fractional Area'
        self.save_cohort_at_time_step(
            cohort, path, file_name, title,
            time_step = 0, bin_only=False, cbar_extend = 'max',
            colormap = 'bone'
        )
        
    def save_cohort_timeseries( self, cohort, path, video = False ):
        """save a cohort time series
        
        Parameters
        ----------
        cohort: str
            a cannon cohort
        path: path
            path to save images at
        video: bool
            saves a video if true
        """
        idx = 0
        files = []
        while True:
            try:
                fname = cohort + '_Fractional_Area_'+ str(self.config['start_year'] + idx)
                try:
                    name = DISPLAY_COHORT_NAMES[cohort]
                except KeyError:
                    # raise KeyError("Cohort name invalid: " + cohort)
                    pass
                    
                title = name + str(self.config['start_year'] + idx)
                self.save_cohort_at_time_step( 
                    cohort, path, fname, title, time_step = idx, bin_only=False
                )
                files.append(fname+'.png')
                idx += 1
            except IndexError:
                break
        files = [os.path.join(path, f) for f in files]
        #~ print files
        if video and not mpy is None:
            
            
            clip = mpy.ImageSequenceClip(files, fps=5)
            clip.write_videofile(
                os.path.join(path,cohort+"_fraction.mp4"), 
                progress_bar=False, verbose = False
            )
            
    def get_cohort_list (self):
        """Gets list of cannon cohort names in model
        
        Returns
        -------
        list:
            cannon cohorts in model instance
        """
        return [key for key in self.key_to_index if key.find('--') == -1]

    def create_dominate_cohort_dataset (self):
        """
        """
        real_shape = self.config['real_shape']
        data = TemporalGrid(
            real_shape[2], real_shape[3], real_shape[0],
            start_timestep = self.config["start_timestep"]
        )
        

        for year in range(
            self.config["start_timestep"], 
            self.config["start_timestep"]+self.config["num_timesteps"]
        ):
            dom = np.zeros(self.config['grid_shape'])
            # this loop finds the max cohort for each cell per year
            for idx, grid in enumerate(sorted(self.get_cohort_list())):
                # print grid, idx
                
                dom[self[grid, year] > dom] = idx
            
            dom[np.logical_not(self.config['AOI mask'])] = np.nan
            
            data[year][:] = dom

        data.config['cohort list'] = sorted(self.get_cohort_list())
        data.config['cohort display names'] = [
            DISPLAY_COHORT_NAMES[n] for n in sorted(self.get_cohort_list())
        ]

        return data

def test (files):
    """
    """
    config = {
        'Target_resolution': (1000,1000),
        'initialization_year': 1900,
        'initial area data': files,
        'model length': 100
    }
    
    return AreaGrid(config)
