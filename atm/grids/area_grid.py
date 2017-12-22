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
    from atm_io import binary, image, raster
except ImportError:
    from ..atm_io import binary, image, raster

from constants import ROW, COL

import copy

import  moviepy.editor as mpy

class MassBalanceError (Exception):
    """Raised if there is a mass balance problem"""

class AreaGrid(object):
    """ AreaGrid represents fractional areas of each cohort in a grid element
    """
    def __init__ (self, config):
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
        input_data = config['area data'] 
        target_resolution = config['target resolution']
        self.start_year = int(config['initilzation year'])
        
        self.input_data = input_data
        ## read input
        ## rename init_grid??
        self.init_grid, self.raster_info, self.key_to_index = \
            self.read_layers(target_resolution)
        
        ## rename grid_history?
        self.grid = [self.init_grid]
        
        self.check_mass_balance() ## check mass balance at initial time_step
        
        #get resolution, and shape of gird data as read in
        original = self.raster_info.values()[0]
        o_shape = (original.nY, original.nX) 
        o_res = (original.deltaY, original.deltaX) 
        self.shape = (
            abs(int(o_shape[ROW] * o_res[ROW] /target_resolution[ROW])),
            abs(int(o_shape[COL] * o_res[COL] /target_resolution[COL])),
        )
        
        ## some times new shape may be off by one
        try:
            self.get_cohort_at_time_step(
                self.key_to_index.keys()[0], flat = False)
        except ValueError:
            self.shape = (self.shape[0]+1,self.shape[1]+1)
            
        self.resolution = target_resolution
        
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
            if key is a string, 3D, dimension are[timestep][grid row][grid col],
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
        
        
    def read_layers(self, target_resolution):
        """Read cohort layers from raster files
        
        Parameters
        ----------
        target_resolution: tuple of ints
            target resolution of each grid element (y,x)
            
        Returns
        -------
        Layers : np.ndarray
            2d array of flattened cohort grids, corrected to the proper
        resolution, and normalized. First dimension is layer index, which can be 
        found with the keys_to_index dict. The second dimension is gird element 
        index.
        metadata_dict : dict
            metadata for each raster loaded. Keys being canon name of layer
        keys_to_index : dict
            Maps each canon cohort name to the int index used in layer grid 
        """
        layers = []
        metadata_dict = {}
        key_to_index = {}
        idx = 0
        shape, resolution = None, None
        
        for f in self.input_data:
            ## add path here
            #~ print f
            path = f
            try:
                data, metadata = raster.load_raster (path)
            except AttributeError:
                print 'FATAL ERROR: Could Not Load Raster File', path
                sys.exit(0)
            
            ## set init shape and resolution
            ## TODO maybe do this differently 
            if shape is None:
                shape = (metadata.nY,metadata.nX)
            elif shape != (metadata.nY,metadata.nX):
                raise StandardError, 'Raster Size Mismatch'
                
            if resolution is None:    
                resolution = (abs(metadata.deltaY),abs(metadata.deltaX))
            elif resolution != (abs(metadata.deltaY), abs(metadata.deltaX)):
                raise StandardError, 'Resolution Size Mismatch'
            
            try:
                filename = os.path.split(f)[-1]
                name = find_canon_name(filename.split('.')[0])
            except KeyError as e:
                print e
                continue
            ## update key to index map, metadata dict, layers, 
            ## and increment index
            key_to_index[name + '--0'] = idx
            slice_start = idx
            idx += 1 # < moved here because of the loop in a bit
        
            metadata_dict[name] = metadata

            
            cohort_year_0 = self.resize_grid_elements(
                data, resolution, target_resolution
            )
            layers.append( cohort_year_0 ) 
            
            flat_grid_size = len(cohort_year_0) 
            num_years = 1 # < to be set based on cohort age range later, FOR TRACKING AGE OF COHORTS <<<<<<<<<<<<<
            for age in range(1, num_years):
                layers.append(np.zeros(flat_grid_size))
                key_to_index[name + '--' + str(idx) ] = idx
                idx += 1
            slice_end = idx
            key_to_index[name] = slice(slice_start,slice_end)
           
        layers = self.normalize_layers(
            np.array(layers), resolution, target_resolution
        )
        #~ print layers
        return layers, metadata_dict, key_to_index
       
    ## make a static method?
    def normalize_layers(self, layers, current_resolution, target_resolution):
        """Normalize Layers. Ensures that the fractional cohort areas in each 
        grid element sums to one. 
        """
        total = layers.sum(0) #sum fractional cohorts at each grid element
        cohorts_required = \
            (float(target_resolution[ROW])/(current_resolution[ROW])) * \
            (float(target_resolution[COL])/(current_resolution[COL]))

        cohort_check = total / cohorts_required
        ## the total is zero in non study cells. Fix warning there
        adjustment = float(cohorts_required)/total

        check_mask = cohort_check > .5
        new_layers = []
        for layer in layers:
            
            layer_mask = np.logical_and(check_mask,(layer > 0))
            layer[layer_mask] = np.multiply(
                layer,adjustment, where=layer_mask)[layer_mask]
            
            layer = np.round((layer) / cohorts_required, decimals = 6)
            new_layers.append(layer)
        new_layers = np.array(new_layers)
        return new_layers
    
    ## make a static method?
    def resize_grid_elements (self, 
        layer, current_resolution, target_resolution):
        """resize cells to target resolution
        
        Parameters
        ----------
        layer : np.ndarray
            2d raster data
        current_resolution: tuple of ints
            current resolution of each grid element (y,x)
        target_resolution: tuple of ints
            target resolution of each grid element (y,x)
            
        Returns 
        -------
        np.ndarray
            flattened representation of resized layer
        """
        ## check that this is correct
        if target_resolution == current_resolution:
            layer[layer<=0] = 0
            layer[layer>0] = 1
            return layer.flatten()
        
        resize_num = (
            abs(int(target_resolution[ROW]/current_resolution[ROW])),
            abs(int(target_resolution[COL]/current_resolution[COL]))
        )
        #~ print resize_num
        resized_layer = []
        
        shape = layer.shape
        
        ## regroup at new resolution
        for row in range(0, int(shape[ROW]), resize_num[ROW]):
            for col in range(0, int(shape[COL]), resize_num[COL]):
                A = layer[row : row+resize_num [ROW], col:col + resize_num[COL]]
                b = A > 0
                resized_layer.append(len(A[b]))
        
        return np.array(resized_layer)
        
        
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True):
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
        cohort = self.key_to_index[cohort]
        
        
        r_val = self.grid[time_step][cohort]
        if type(cohort) is slice:
            # sum all age buckets for cohort      
            r_val = r_val.sum(0)
       
        if flat:
            return r_val
        else: 
            return r_val.reshape(
                self.shape[ROW], self.shape[COL]
            )
    
    ## NEED TO TEST
    def get_cohort (self, cohort, flat = True):
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
        cohort = self.key_to_index[cohort]
        
        
        r_val = np.array(self.grid)[:,cohort]
        if type(cohort) is slice:
            # sum all age buckets for cohort      
            r_val = r_val.sum(1)
        
        if flat:
            # sum all age buckets for cohort(check1)
            return r_val
        else:
            return r_val.reshape(len(self.grid),
                self.shape[ROW], self.shape[COL])
                
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
        ## do we want this to sum the age buckets
        if flat:
            # sum all age buckets for cohort
            return self.grid[time_step] 
        else:
            return self.grid[time_step].reshape(len(self.init_grid),
                self.shape[ROW], self.shape[COL])
                
    def total_franctonal_area(self, time_step):
        """get total fractional area for each grid element at a time step 
        
        Parameters
        ----------
        time_step: int
        
        Returns
        -------
        np.array
            total fractional area array
        """            
        grid = self.grid[time_step]
        
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
        ATTM_Total_Fractional_Area = self.total_franctonal_area(time_step)
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
        if cohort.find('--') == -1:
            raise StandardError, 'needs the age set'
        idx = self.key_to_index[cohort]
        if data.shape != self.shape:
            raise StandardError, 'Set shape Error'
        
        self.grid[time_step][idx] = data.flatten()
        
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
        shape = self.init_grid.shape
        self.grid[time_step] = data.reshape(shape)
        
         
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
            self.append_grid_year(True)
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
            
        
    def add_time_step (self, zeros=False):
        """adds a new grid timestep and exact copy of the previous timestep
        
        Parameters
        ----------
        zeros : bool
            set new years data to 0 if true
        """
        self.grid.append(copy.deepcopy(self.grid[-1]))
        if zeros:
            self.grid[-1] = self.grid[-1]*0
            
    def area_of_intrest (self, time_step = 0):
        """get area of interest at a time step
        
        Parameters
        ----------
        time_step: int, default 0
        
        Returns
        -------
        np.array
            a grid of booleans where true elements are in AOI, false are not
        """
        return (self.total_franctonal_area(time_step) > 0.0).reshape(self.shape)
        
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
        if video:
            
            
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
            
        dom[np.logical_not(self.area_of_intrest())] = np.nan
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
        
def test (files):
    """
    """
    config = {
        'target resolution': (1000,1000),
        'start year': 1900,
        'input data': files,
    }
    
    return CohortGrid(config)
