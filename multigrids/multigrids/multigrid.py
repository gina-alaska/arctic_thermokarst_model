"""
Multigrid
---------

multigrid.py

This file contains the MultiGrid class

"""
import numpy as np
import os
from tempfile import mkdtemp
import yaml
import copy
import sys

from . import figures

from .common import load_or_use_default, GridSizeMismatchError

def open_or_create_memmap_grid(filename, mode, dtype, shape):
    """Initialize or open a memory mapped np.array.
    
    Parameters
    ----------
    filename: str
        Path to file to create or open
    mode: str
        Mode to open file in: 'r', 'r+' or 'w+'.
    dtype: str
        Data type of array. Must be a type suppored by numpy.
    shape: tuple
        Shape of array to create 

    Returns
    -------
    Opened memory mapped array.
    
    """
    if not os.path.exists(filename) and mode in ('r','r+'):
        ## if file dne initialize and delete
        grids = np.memmap(filename, dtype=dtype, mode='w+', shape=shape)           
        del grids
    return np.memmap(filename, dtype=dtype, mode=mode, shape=shape)
    

class MultiGrid (object):
    """
        A class to represent a set of multiple related grids of the same 
        dimensions. Implemented usin gnumpy arrays.

    Parameters
    ----------
    *args: list
        List of required arguments, containing exactly 3 items: # rows, 
        # columns, # grids.
        Example call: mg = MultiGrid(rows, cols, n_grids)
    **kwargs: dict
        Dictionary of key word arguments. The following options are valid
        'data_type': data type to use for grid values, defaults 'float'
        'mode': Mode to open memmap file in. Can be 'r+', 'r', 'w+', or 'c'
        'dataset_name': Name of data set, defaults 'Unknown'
        'mask': Mask for the area of interest(AOI) in the MultiGrid.
            Should be a np.array of type bool where true values are
            in the AOI.
            Defaults to None, which generates a mask that sets all 
            grid cells to be part of the AOI
        'grid_names': list of names for each grid in the MultGird, 
            Defaults None.
        'filename': name of file if using memmap as data_model.
            Defaults to None, which will create a temp file.
        'data_model': how to internally represent data, memmap or array.
            Defaults  Memmap.
        'initial_data': Initial data for MultiGrid. Defaults to None. 
    
    Attributes 
    ----------
    config: dict
        'grid_shape': 2 tuple, grid shape (rows, cols)
        'real_shape': 3 tuple, (num_grids, rows, cols)
        'memory_shape': 2 tuple, (num_grids, rows * cols)
        'data_type': data type of grid values
        'mode': Mode memory mapped file is open in. 
        'dataset_name': Name of data set.
        'mask': Mask for the area of interest(AOI) in the MultiGrid grids. 
        'filename': name of memory mapped file.
        'data_model': model of data in memory, 'array', or 'memmap'
        'grid_name_map': map of grid names to gird ids
    grids: np.memmap or np.ndarray 
    """

    def __init__ (self, *args, **kwargs):
        """ Class initializer """
        # print( args )
        # print( kwargs )
        
        if type(args[0]) is int:
            # print('new')
            init_func = self.new

        if type(args[0]) is str:
            # print('load')
            init_func = self.load
        self.config, self.grids = init_func(*args, **kwargs)

    def __del__ (self):
        """deconstructor for class"""
        del(self.config)
        del(self.grids)

    def __getattr__(self, attr):
        """get attribute, allows access to config dictionary values
        as class attributes 

        Paramaters
        ----------
        attr: str
            attribute. spaces in this paramater are replaced with '_' if 
            the space version of the attribute is not found.

        Raises
        ------
        AttributeError:
            if Attribute is not found.

        Returns
        -------
        value of attribute
        """
        # if not hasattr(self, 'config'):
        #     sys.exit(1)
        try:
            if attr == 'config':
                return self.config
            elif attr in self.config and attr != 'config'  and attr != 'config':
                return self.config[attr]
            elif attr.replace('_',' ') in self.config and attr != 'config':
                return self.config[attr.replace('_',' ')]
            else:
                s = "'" + self.__class__.__name__ + \
                    "' object has no attribute '" + attr + "'"
                return s
        except(AttributeError) as e:
            return 'not attr'
        
    def __repr__ (self):
        """Get string representation of object
        
        Returns
        -------
        string
        """
        return str(self.grids.reshape(self.real_shape))
        
    def __getitem__(self, key): 
        """Get item function
        
        Parameters
        ----------
        key: str or int
            A grid named in the grid_names list, and grid_name_map, or
        A int index for one of the grids.

        Returns
        -------
        np.array like
            Grid from the multigrid with the shape self.grid_shape
        
        """
        if type(key) in (str,):
            key = self.get_grid_number(key)
        return self.grids.reshape(self.real_shape)[key].reshape(self.grid_shape)

    def __setitem__(self, key, value):
        """Set item function
        
        Parameters
        ----------
        key: str or int
            A grid named in the grid_names list, and grid_name_map, or
        A int index for one of the grids.
        value: np.array like
            Grid that is set. Should have shape of self.grid_shape.
        """
        if type(key) in (str,):
            key = self.get_grid_number(key)
        # if type(key) in (tuple, int, slice):
        self.grids[key] = value.flatten()
    
    def __eq__(self, other):
        """Equality Operator for MultiGrid object 

        Returns
        -------
        Bool:
            True if intreal grids are equal
        """
        if other is self:
            return True
        return (self.grids == other.grids).all()

    def new(self, *args, **kwargs):
        """Does setup for a new MultGrid object
        
        Parameters
        ----------
        *args: list
            Variable length list of arguments. Needs 3 itmes.
            where the first is the number of rows in each grid, the
            second is the number of columns, and the third is the 
            number of grids in the MultiGrid. All other values are
            ignored. 
        **kwargs: dict
            Dictionary of key word arguments. The following options are valid
            'data_type': data type to use for grid values, defaults 'float'
            'mode': Mode to open memmap file in. Can be 'r+', 'r', 'w+', or 'c'
            'dataset_name': Name of data set, defaults 'Unknown'
            'mask': Mask for the area of interest(AOI) in the MultiGrid.
                Should be a np.array of type bool where true values are
                in the AOI.
                Defaults to None, which generates a mask that sets all 
                grid cells to be part of the AOI
            'grid_names': list of names for each grid in the MultGird, 
                Defaults None.
            'filename': name of file if using memmap as data_model.
                Defaults to None, which will create a temp file.
            'data_model': how to internally represent data, memmap or array.
                Defaults  Memmap.
            'initial_data': Initial data for MultiGrid. Defaults to None. 

        Returns
        -------
        Config: dict
            dict to be used as config attribute.
        Grids: np.array like
            array to be used as internal memory.
        """

        config = {}
        config['grid_shape']= (args[0], args[1])
        config['num_grids'] = args[2]
        config['memory_shape'] = self.get_memory_shape(config)
        config['real_shape'] = self.get_real_shape(config)
        config['data_type'] = load_or_use_default(
            kwargs, 'data_type', 'float32'
        )
        config['mode'] = load_or_use_default(kwargs, 'mode', 'r+')
        config['dataset_name'] = load_or_use_default(
            kwargs, 'dataset_name', 'Unknown'
        )

        config['mask'] = load_or_use_default(kwargs, 'mask', None)

        if config['mask'] is None:
            config['mask'] = \
                np.ones(config['grid_shape']) == \
                np.ones(config['grid_shape'])

        grid_names = load_or_use_default(kwargs, 'grid_names', [])
        
        if len(grid_names) > 0 and config['num_grids'] != len(grid_names):
            raise GridSizeMismatchError( 'grid name size mismatch' )
        config['grid_name_map'] = self.create_name_map(grid_names)
            

        config['filename'] = load_or_use_default(kwargs, 'filename', None)
        config['data_model'] = load_or_use_default(
            kwargs, 'data_model', 'memmap'
        )
        if config['data_model'] != 'memmap':
            config['data_model'] = 'array'

        grids = self.setup_internal_memory(config)
        
        init_data = load_or_use_default(kwargs, 'initial_data', None)
        if not init_data is None:
            grids = init_data.reshape(config['memory_shape'])
        
        return config, grids 

    def load(self, file):
        """Load a MultiGird object from yaml metadata file and data file
        
        Parameters
        ----------
        file: path
            Path to the metadata file for the MultiGrid object.

        Returns
        -------
        Config: dict
            dict to be used as config attribute.
        Grids: np.array like
            array to be used as internal memory.
        """
        with open(file) as conf_text:
            config = yaml.load(conf_text)

        config['cfg_path'] = os.path.split(file)[0]
        config['memory_shape'] = self.get_memory_shape(config)
        config['real_shape'] = self.get_real_shape(config)
        grids = self.setup_internal_memory(config)

        return config, grids

    def save(self, file, grid_file_ext = '.mgdata'):
        """Save MiltiGrid Object to metadata file and data file
        The metadata file cantinas the config info, and the data file
        contains the grids. 

        Parameters
        ----------
        file: path
            Path to the metadata file (yaml) to save. The data file name will
            be genetated from metadata name if a data file does not all ready
            exist. 
        grid_file_ext: str, defaults: '.mgdata' 
            The extension to save the data file as if the datafile does not
            already exist. The data is saved as a memory mapped Numpy array,
            so the extension is more for description than any thing else.
        """
        s_config = copy.deepcopy(self.config)
        if s_config['data_model'] is 'array' or s_config['filename'] is None:
            try:
                path, grid_file = os.path.split(file)
            except ValueError:
                path, grid_file = './', file
            if grid_file[0] == '.':
                grid_file = '.' + grid_file[1:].split('.')[0] + grid_file_ext
            else:
                grid_file = grid_file.split('.')[0] + grid_file_ext
            data_file = os.path.join(path,grid_file) 
            save_file = np.memmap(
                data_file, 
                mode = 'w+', 
                dtype = s_config['data_type'], 
                shape = self.grids.shape 
            )
            save_file[:] = self.grids[:]
            del save_file
            s_config['filename'] = os.path.split(data_file)[1]
        
        del s_config['memory_shape']
        del s_config['real_shape']

        s_config['mode'] = 'r+'
        with open(file, 'w') as sfile:
            sfile.write('#Saved ' + self.__class__.__name__ + " metadata\n")
            yaml.dump(s_config, sfile, default_flow_style=False)
        
    def create_name_map(self, grid_names):
        """Creates a dictionary to map string grid names to their 
        interger index values. Used to initialize gird_name_map
        
        Paramaters
        ----------
        grid_names: list of strings
            List of grid names. Length == num_grids

        Returns
        -------
        Dict:
            String: int, key value pairs
        """
        return {grid_names[i]: i for i in range(len(grid_names))}   

    def setup_internal_memory(self, config):
        """Setup the internal memory representation of grids

        Parameters
        ----------
        config: dict
            Should have keys 'filename', 'data_model', 'data_type', 
        and 'memory_shape'. 
            'filename': name of file to write or None
            'data_model': Model for data representation: 'array' or 'memmap'
            'data_type': 
                String type of data. Must be type supported by np.arrays.
            'memory_shape': Tuple
                shape of grids as represented in memory 

        Returns
        -------
        grids: np.array or np.memmap
        """
        filename = config['filename']
        if config['filename'] is None and config['data_model'] == 'memmap':
            filename = os.path.join(mkdtemp(), 'temp.dat')
        elif not os.path.exists(filename):
            filename = os.path.split(filename)[1]
            filename = os.path.join(config['cfg_path'], filename)
            
        if config['data_model'] == 'memmap':
           
            
            # print filename
            grids = open_or_create_memmap_grid(
                filename, 
                config['mode'], 
                config['data_type'], 
                config['memory_shape']
            )
        else: # array
            grids = np.zeros(config['memory_shape'])
        return grids 
    
    def get_memory_shape (self, config):
        """Construct the shape needed for multigrid in memory from 
        configuration. 

        Parameters
        ----------
        config: dict
            Must have keys 'num_grids' an int, 'grid_shape' a tuple of 2 ints

        Returns
        -------
        Tuple
            (num_grids, flattened shape of each grid )
        """
        return (config['num_grids'], 
            config['grid_shape'][0] * config['grid_shape'][1])

    def get_real_shape (self, config):
        """Construct the shape that represents the real shape of the 
        data for the MultiGird.

        Parameters
        ----------
        config: dict
            Must have keys 'num_grids' an int, 'grid_shape' a tuple of 2 ints

        Returns
        -------
        Tuple
            ('num_grids', 'rows', 'cols')
        """
        return (config['num_grids'], 
            config['grid_shape'][0], config['grid_shape'][1])

    def get_grid_number(self, grid_id):
        """Get the Grid number for a grid id
        
        Parameters
        ----------
        grid_id: int or str
            if an int, it should be the grid number.
            if a str, it should be a grid name.

        Returns
        -------
        int
            gird id
        """
        return grid_id if type(grid_id) is int else self.grid_name_map[grid_id]
    
    def get_grid(self, grid_id, flat = True):
        """Get a grid
        
        Parameters
        ----------
        grid_id: int or str
            if an int, it should be the grid number.
            if a str, it should be a grid name.
        flat: bool, defaults true
            returns the grid as a flattened array.

        Returns
        -------
        np.array
            1d if flat, 2d otherwise.
        """
        if flat:
            return self[grid_id].flatten()
        return self[grid_id]

    def set_grid(self, grid_id, new_grid):
        """Set a grid
         Parameters
        ----------
        grid_id: int or str
            if an int, it should be the grid number.
            if a str, it should be a grid name.
        new_grid: np.array like
            Grid to set. must be able to reshape to grid_shape.
        """
        self[grid_id] = new_grid.reshape(self.grid_shape)

    def figure (self, filename, grid_id, **kwargs):
        """Save a figure for a grid
        
        Parameters
        ----------
        filename: path
            path to save image at
        grid_id: int or str
            if an int, it should be the grid number.
            if a str, it should be a grid name.
        **kwargs: dict
            dict of key word arguments
            'limits': tuple, defaults (None, None)
                min, max limits for data
            'cmap': str, defaults 'viridis'
                matplotlib colormap
            'cbar_extend': str, defaults 'neither'
                'neither', 'min' or 'max' 
        """
        data = self[grid_id].astype(float)
        data[np.logical_not(self.mask)] = np.nan

        figure_name = self.dataset_name + ' ' + str( grid_id )

        limits = load_or_use_default(kwargs, 'limits', (None,None))
        cmap = load_or_use_default(kwargs, 'cmap', 'viridis')
        cbar_extend = load_or_use_default(kwargs, 'cbar_extend', 'neither')

        figures.save_figure(
            data.reshape(self.grid_shape) , 
            filename, 
            figure_name ,
            cmap = cmap,
            vmin = limits[0], 
            vmax = limits[1],
            cbar_extend = cbar_extend
        )
        
    def figures(self, dirname, **kwargs):
        """Save figures for every grid
        
        Parameters
        ----------
        dirname: path
            path to save images at
        **kwargs: dict
            dict of key word arguments
            'limits': tuple, defaults (None, None)
                min, max limits for data
            'cmap': str, defaults 'viridis'
                matplotlib colormap
            'cbar_extend': str, defaults 'neither'
                'neither', 'min' or 'max' 
        """
        grids = self.grid_name_map
        if grids == {}:
            grids = range(self.num_grids)

        for grid in grids:
            filename = os.path.join(
                dirname, 
                (self.dataset_name + '_' + grid + '.jpg').replace(' ','_')
            )
            self.figure(filename, grid, **kwargs)


def create_example():
    """create and return an example MultiGrid

    Returns
    -------
    MultiGrid
    """
    g_names = ['first', 'second']

    init_data = np.ones([2,5,10])
    init_data[1] += 1

    t1 = MultiGrid(5, 10, 2, grid_names = g_names, initial_data = init_data)
    
    return t1

