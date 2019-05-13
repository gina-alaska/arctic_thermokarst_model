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

from constants import ROW, COL

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
        'target resolution': (1000,1000),
        'initialization year': 1900,
        'initial area data': files,
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
            input_rasters = config['initial area data'] 
            target_resolution = config['target resolution']

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
                layers.grid_shape[ROW], layers.grid_shape[COL], 
                layers_with_ages.shape[0], config['model length']
            ]

            kwargs = copy.deepcopy(config) 
            # kwargs['data_type'] = 'float'
            kwargs['mode'] = 'r+'
            # kwargs['filename'] = 'test.mgdatatest'
            # kwargs['cfg_path'] = './'

            # kwargs['grid_names'] = layers.
            super(AreaGrid , self).__init__(*args, **kwargs)
            # print self.grids.shape
            # self.config['grid_names'] = layers.grid_names
            self.config['grid_name_map'] = grid_name_map_with_ages
            self.grids[0,:] = layers_with_ages.reshape(self.memory_shape[1:])

            self.key_to_index = grid_name_map_with_ages
        
            self.config['start_year'] = int(config['initialization year'])
            self.config['resolution'] = target_resolution

        self.config['start_timestep'] = self.config['start_year']
        
        self.shape = self.grid_shape
        self.init_grid = self.grids[0]
        self.config['AOI mask'] = self.area_of_interest()
        # self.config['mask'] = self.area_of_interest()

    def setup_cohort_ages(self, layers):
        """ Function doc """
        layers_with_ages = [] 
        grid_name_map_with_ages = {}
        index = 0
        for layer in layers.layer_names:
            layers_with_ages.append(layers[layer].flatten())
            grid_name_map_with_ages[layer + '--0'] = index
            slice_start = index
            index += 1
            num_years = 1 # < to be set based on cohort age range later, FOR TRACKING AGE OF COHORTS <<<<<<<<<<<<<
            for age in range(1, num_years):
                layers_with_ages.append(
                    np.zeros(layers.grid_shape[0] * layers.grid_shape[1])
                )
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
        
    # ## REDO DOCS
    # def __getitem__ (self, key):
    #     """Gets cohort data.

    #     AreaGrid[]
        
    #     Can get data for a cohort at all time steps, all cohorts at a ts, 
    #     or a cohort at a given ts
        
    #     # Parameters
    #     # ----------
    #     # key: Str, int, or tuple(int,str)
    #     #     if key is a string, it should be a canon cohort name.
    #     #     if key is an int, it should be a year >= start_year, 
    #     #     but < start_year + len(grid)
    #     #     if key is tuple, the int should fit the int requirements, and the 
    #     #     string the string requirements. 
            
    #     # Returns
    #     # -------
    #     # np.array
    #     #     if key is a string, 3D, dimension are[timestep][grid row][grid col],
    #     #     timestep is year(key) - start year
    #     #     if key is a int, 3D, dimension are [cohort #][grid row][grid col],
    #     #     use key_to_int to find cohort #
    #     #     if key is tuple, 2D, [grid row][grid col]
    #     """
    #     # print key
    #     access_key = [slice(None,None) for i in range(3)]
    #     if self.is_grid(key):
    #         access_key[1] = self.get_grid_number(key)
    #     elif self.is_grid_with_range(key) or self.is_grid_with_index(key):
    #         access_key[0] = key[1] - self.start_year
    #         access_key[1] = self.get_grid_number(key[0])
    #     else:
    #         access_key = key - self.start_year
    #     # print 'key', access_key, type(access_key)
    #     return self.grids.reshape(self.real_shape)[access_key]

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
            grids = grids.reshape(self.num_timesteps, np.prod(self.grid_shape))
        
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
            time_step = self.timestep
        grids = self[time_step + self.start_year ]
        if flat:
            grids = grids.reshape(self.num_grids, np.prod(self.grid_shape))
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
        grid = self[time_step + self.start_year]
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
            time_step = self.timestep
        ATTM_Total_Fractional_Area = self.total_fractional_area(time_step)
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) > 1.0).any():
            raise MassBalanceError, 'mass balance problem 1'
            ## write a check to locate mass balance error
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) < 0.0).any():
            raise MassBalanceError, 'mass balance problem 2'
            
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
        raise NotImplementedError, 'cannot set a cohort at all time steps'
    
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
            
        Raises
        ------
        StandardError
            bad shape
        """
        self[cohort, time_step + self.start_year] = data

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
        self[time_step + self.start_year] = data
        
    ## REDO DOCS
    # def __setitem__ (self, key, data):
    #     """Set cohort data. 
        
    #     Can set a grid for a cohort(or all cohorts) at a timestep. Will add 
    #     time step id desired time step == len(grid)
        
    #     Parameters
    #     ----------
    #     key: Str, int, or tuple(int,str)
    #         if key is a string, raises NotImplementedError
    #         if key is an int, it should be a year >= start_year, 
    #         but <= start_year + len(grid)
    #         if key is tuple, the int should fit the int requirements, and the 
    #         string should be a canon cohort name
    #     data: np.ndarray
    #         data of the proper shape. for tuple key shape = shape attribute, 
    #         else rebroadcastable to shape of init_grid
            
    #     Raises
    #     ------
    #     NotImplementedError
    #         if key is str, 'cannot set a cohort at all time steps'
    #     KeyError, 
    #         if key's year value < star_year or > star_year + len(grid)
    #     """
    #     access_key = [slice(None,None) for i in range(3)]
    #     if common.is_grid(key) or self.is_grid_with_range(key):
    #         raise NotImplementedError, 'cannot set a cohort at multiple time steps'
    #     elif self.is_grid_with_index(key):
    #         if type(self.get_grid_number(key[0])) is slice:
    #             raise NotImplementedError, 'cannot set a cohorts age grids as a group, try setting each age one at a time'
    #         access_key[0] = key[1] - self.start_year
    #         access_key[1] = self.get_grid_number(key[0])
    #     else:
    #         access_key = key - self.start_year
    #     # print 'key', access_key, type(access_key)
    #     shape = self.grids[access_key].shape
    #     self.grids[access_key] = data.reshape(shape)
            
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
        
    def save_cohort_at_time_step (self, cohort, path, filename, title = '', 
            time_step = -1, bin_only = True, binary_pixels = False, 
            cbar_extend = 'neither', colormap = 'viridis'
        ):
        """save a in image representing a cohort at a time step
        
        Parameters
        ----------
        cohort: str
            cannon cohort name
        path: path
            path to save figures at
        filename: str
            name of file without extension
        title: str, optional
            title for png figure
        timestep: int, optional
            timestep to save defaults to -1
        bin_only: bool, defaults True
            only saves numpy binary image represntation if true 
        binary_pixels: Bool, defaults False
            if true converts all pixels > 0 to 1.
        cbar_extend: str
            max, min, or neither
        colormap: str
            matplotlib color map
        
        
        returns 
        -------
        str:
            base file name
        """
        cohort_data = self.get_cohort_at_time_step(
            cohort, time_step, flat = False
        )
        #~ print binary_pixels
        if binary_pixels:
            ## see if cohort is present or not
            cohort_data = copy.deepcopy(cohort_data)
            cohort_data[cohort_data>0] = 1
            #~ print cohort_data
        #~ self.ts_to_year(time_step)
        year = 'TEMP_YEAR'
        #~ filename = f
        bin_path = os.path.join(path, filename + '.bin')
        binary.save_bin(cohort_data, bin_path)
        if not bin_only:
            img_path = os.path.join(path, filename + '.png')
            image.save_img(
                cohort_data, img_path, title, cmap = colormap,
                cbar_extend = cbar_extend
                ) 
            
        return filename
        
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
                fname = cohort + '_Fractional_Area_'+ str(self.start_year + idx)
                try:
                    name = DISPLAY_COHORT_NAMES[cohort]
                except KeyError:
                    print cohort + ' not Found'
                    return
                    #~ name = cohort
                    
                title = name + str(self.start_year + idx)
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
          
    def find_dominate_cohort_at_time_step (self, time_step = -1):
        """Create the dominate cohort map at a time step
        
        Parameters
        ----------
        time_step: int
            time step to create
            
        Returns
        -------
        np.array:
            grid
        dict:
            metadata
        """
        
        dom = np.zeros(self.shape).flatten()
        
        metadata = {}
        count = 0
        
        for grid in sorted(self.get_cohort_list()):
            metadata[count] = grid
            temp = self.get_cohort_at_time_step(grid,time_step)
            idx = temp > dom
            dom[idx] = count
            count += 1
            
        dom = dom.reshape(self.shape)
            
        dom[np.logical_not(self.area_of_interest())] = np.nan
        return dom , metadata
        
    def dominate_cohort_figure (self, path, filename, title = '', 
            time_step = -1, colormap = 'tab20', bin_only=False
        ):
        """save dominate cohort image at a time step
        
         Parameters
        ----------
        path: path
            path to save figures at
        filename: str
            name of file without extension
        title: str, optional
            title for png figure
        timestep: int, optional
            timestep to save defaults to -1
        bin_only: bool, defaults True
            only saves numpy binary image represntation if true 
        colormap: str
            matplotlib color map
            
        """
        grid, md = self.find_dominate_cohort_at_time_step(time_step)
        
        bin_path = os.path.join(path, filename + '.bin')
        binary.save_bin(grid, bin_path)
        if not bin_only:
            img_path = os.path.join(path, filename + '.png')
            image.save_categorical_img(
                grid, img_path, title, sorted(self.get_cohort_list()),
                cmap = colormap
                ) 
                
    def dominate_cohort_timeseries( self, path, video = False,
            colormap = 'tab20' 
        ):
        """save dominate cohort time series
        
        Parameters
        ----------
        path: path
            path to save images at
        video: bool
            saves a video if true
        colormap: str
            color map to use
        """
        idx = 0
        files = []
        while True:
            try:
                fname = 'Dominant_Cohort_'+ str(self.start_year + idx)
                title = 'Dominant Cohort - ' + str(self.start_year + idx)
                self.dominate_cohort_figure ( 
                    path, fname, title, time_step = idx, bin_only=False
                )
                files.append(fname+'.png')
                idx += 1
            except IndexError:
                break
        files = [os.path.join(path, f) for f in files]
        #~ print files
        if video:
            
            
            clip = mpy.ImageSequenceClip(files, fps=5)
            clip.write_videofile(
                os.path.join(path, "Dominant_Cohort.mp4"), 
                progress_bar=False, verbose = False
            )   

    def create_dominate_cohort_dataset (self):
        """
        """
        data = TemporalGrid(
            self.real_shape[2], self.real_shape[3], self.real_shape[0],
            start_timestep = self.start_timestep
        )
        

        for year in range(
            self.start_timestep, self.start_timestep+self.num_timesteps
        ):
            dom = np.zeros(self.grid_shape)
            # this loop finds the max cohort for each cell per year
            for idx, grid in enumerate(sorted(self.get_cohort_list())):
                # print grid, idx
                
                dom[self[grid, year] > dom] = idx
            
            dom[np.logical_not(self.AOI_mask)] = np.nan
            
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
        'target resolution': (1000,1000),
        'initialization year': 1900,
        'initial initial area data': files,
        'model length': 100
    }
    
    return AreaGrid(config)
