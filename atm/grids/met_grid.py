"""
Met Grid
--------

Grids for meterological stuff
"""
import os
import numpy as np

try:
    from tools import stack_rasters
except ImportError:
    from ..tools import stack_rasters
    

try:
    from atm_io import image
except ImportError:
    from ..atm_io import image


class MetGridShapeError(Exception):
    """Raised if data shape is not correct"""

class MetGridBase (object):
    """Base class for met grids
        
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
            
        Attributes
        ----------
        start_year: int 
            year data starts at, should be year model will start at
        shape: tuple
            shape of grid
        history: np.array
            drainage grid
        met_type: str
            type of met data
        pickle_path: path
            path to pickle file
        source: path
           path to memory mapped history file 
    """
    
    def __init__ (self, config):
        """
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
        """
        if type(config) is str:
            ## read from existing pickle
            self.load_from_pickle(config)
            return
        
        self.data_path = config['data path']
        self.start_year = config['start year']
        self.shape = config['shape']
        self.history, self.met_type, self.source = self.setup(config)
        
        
        
        self.pickle_path = os.path.join(
            config['pickle path'], self.met_type + '_history.pkl'
        )
        
        
        
    def setup (self, config):
        """Function to setup met histroy should be over loaded by child classes
        Parameters
        ----------
        config: dict or atm.control
            config for met history
        
        Returns
        -------
        None, str
        """
        return None, 'base', 'none'
        
    def __getitem__ (self, key):
        """Get item function
        
        Parameters
        ----------
        key: int 
            a year >= start_year
            
        Raises
        ------
        index error
        
        Returns
        -------
        np.array
            grid for year with shape self.shape
        """
        if key < self.start_year:
            raise IndexError, 'index should be after '+ str(self.start_year)
        
        return self.get_grid(key - self.start_year, False)
    
    def read_data(self, source, met_type, data_type = 'spatial'):
        """Read the met history from file
        
        Parameters
        ----------
        source: list, or path:
            list of paths or path to read data from
        data_type: str, defaults spatial
            'point' or 'spatial'
            
        Raises
        ------
        MetGridShapeError:
            grid shape mismatch
        NotImplementedError:
            point data handeling not impmented 
            
        Returns
        -------
        np.memorymap
            memory mapped history data
        source: path
            path to memory mapped file
        """
        if data_type.lower() == 'spatial':
            
            with open(source, 'r') as s:
                i = s.read().rstrip().split('\n')
                
            try:
                if os.path.isfile(os.path.join(os.path.split(source)[0], i[0])):
                    source = [
                        os.path.join(os.path.split(source)[0],f) for f in i
                    ]
            except TypeError:
                pass
            
            ## if mm data DNE create it 
            if type(source) is list:
                mm_file = os.path.join(
                    self.data_path, met_type.replace(' ','_') + '_history.data'
                )
                data, shape = self.read_spatial_from_files(
                    source, mm_file
                )
                if shape[0] != self.shape[0] * self.shape[1] :
                    raise MetGridShapeError, 'loaded met data has wrong shape'
                del data
                source = mm_file
                
        
            ## load data as read only
            data = self.read_spatial_from_memory_map(source)
            #~ print data.shape
            #~ print data
            years = data.shape[0] / (self.shape[0] * self.shape[1])
            data = data.reshape(
                years, (self.shape[0] * self.shape[1])
            )
        else:
            msg = 'non spatial data handeling not implmented'
            raise NotImplementedError, msg
        return data, source
        
    def read_spatial_from_files (self, files, mm_name):
        """read spatial data from files in a list and build memory maped history 
        
        Parameters
        ----------
        files: list
            sorted list of files to load, first file in list is stored 
            as first item in history
        mm_name: path
            memory mapped file name
            
        Returns 
        -------
        np.memorymap
            met history memory mapped array 
        """
        return stack_rasters.stack_np_arrays_from_file (files, mm_name)
        
    def read_spatial_from_memory_map (self, met_file):
        """
        Parameters
        ----------
        met_file: path
            memory mapped file to read
            
        Returns 
        -------
        np.memorymap
            met history memory mapped array 
        """
        return np.memmap(met_file, dtype='float32', mode='r')
        
    ## spatial data takes precdence
    #~ def read_met_point (self):
        #~ """
        #~ """
        
    def get_grid (self, time_step, flat = True):
        """Get met grid at ts
        
        Parameters
        ----------
        time_step: int
            time step to get data at
        flat: bool, defaults True
            reshapes data to shape if False
            
        Returns
        -------
        np.array
            Met gird for given time step
        """
        shape = self.shape
        if flat:
            shape = self.shape[0] * self.shape[1]
        return self.history[time_step].reshape(shape)
        
    def save_to_pickle(self):
        """Save Met object to pickle file
        """
        data = {
            'start year': self.star_year,
            #~ 'history', self.history,
            'type': self.met_type,
            'shape': self.shape,
            'source': self.source
        }
        
        if pickle_name is None:
            pickle_name = self.pickle_path
        mode = 'wb'

        with open(pickle_name, mode) as pkl:
            pickle.dump(data, pkl)
        
    
    def load_from_pickle(self, pickle_name):
        """load state from pickle
        
        Parameters
        ----------
        pickle_name: str
            pickle file with state
        """
        with open(pickle_name, 'rb') as pkl:
            data = pickle.load(pkl)
        
        self.start_year = data['start year']
        self.history = self.read_spatial_from_memory_map(data['source'])
        self.met_type = data['type']
        self.shape = data['shape'],
        self.pickle_path = pickle_name
        self.data_path = os.path.split(pickle_name)[0]
        self.source = data['source']
        
        
    def figure (self, filename, year, limits = (None, None) ):
        """Save a figure for a year
        
        Parameters
        ----------
        filename: path
            path to save image at
        year: int
            year to save grid for
        limits: tuple, defaults (None, None)
            min, max limits for data
        """
        image.save_img(
            self[year].reshape(self.shape) , 
            filename, 
            self.met_type + '-' + str(year) ,
            cmap = 'viridis',
            vmin = limits[0],
            vmax = limits[1]
        )
        
    def figures(self, dirname, limits = (None, None) ):
        """Save figures for every year
        
        Parameters
        ----------
        dirname: path
            path to save images at
        limits: tuple, defaults (None, None)
            min, max limits for data
        """
        for year in range(self.start_year, self.start_year + len(self.history)):
            filename = os.path.join(
                dirname, 
                self.met_type.replace(' ', '_') + '_' + str(year) + '.png'
            )
            self.figure(filename, year, limits)
            
    
    ## not really nessary with the data being stored as a memory mapped array
    #~ def binary (self, filename, ts):
        #~ """
        #~ """
        #~ pass
        
## Not Implemented at this point. use the preprocessing tool to convert to 
## degree day data
#~ class AirTempGrid (MetGridBase):
    #~ """Air temerature grid. Not implmenting functionality at this
    #~ time use preprocessing utility to convert data to degree days
    #~ """
    #~ def setup(config):
        #~ return grid, 'Air Temp'

class TDDGrid (MetGridBase):
    """Thawing Degree-day history grid
    
    Parameters
    ----------
    config: dict or atm.control or path to pickle file
        configuration for object
    """
    
    def setup (self, config):
        """Setup function
        
        Parameters
        ----------
        config: dict or atm.control
            configuration for object
        
        Returns
        -------
        data: np.memorymap
            history of met gird
        str:
            Thawing Degree-Days'
        path:
            path to memory maped array file
        """
        
        
        data_path = os.path.join(config['Input_dir'],
            config['Met_Control']['TDD_file']
        )
        data, source = self.read_data( data_path, 'Thawing Degree-Days' )
        return data, 'Thawing Degree-Days', source
        

class FDDGrid (MetGridBase):
    """Thawing Degree-day history grid
    
    Parameters
    ----------
    config: dict or atm.control or path to pickle file
        configuration for object
    """
    
    def setup (self, config):
        """Setup function
        
        Parameters
        ----------
        config: dict or atm.control
            configuration for object
        
        Returns
        -------
        data: np.memorymap
            history of met gird
        str:
            Freezing Degree-Days'
        path:
            path to memory maped array file
        """
        data_path = os.path.join(config['Input_dir'],
            config['Met_Control']['FDD_file']
        )
        data, source = self.read_data( data_path, 'Freezing Degree-Days' )
        return data, 'Freezing Degree-Days', source

class DegreeDayGrids (object):
    """Degree-days grids
    
    Parameters
    ----------
    config: dict or atm.control
        configuration for object
    """
    def __init__ (self, config):
        """ Class initialiser 
        
        Parameters
        ----------
        config: dict or atm.control
            configuration for object
        """
        self.thawing = TDDGrid(config)
        self.freezing = FDDGrid(config)
        self.shape = self.freezing.shape
        
        #~ import matplotlib.pyplot as plt
        
        #~ plt.imshow(self.thawing.history[0].reshape(self.shape))
        #~ plt.show()

        
        
    def __getitem__ (self, key):
        """get grid for thawing or freezing degree-days
        
        Parameters
        ----------
        key: tuple
            (str, year). str should be freeze, fdd, thaw, tdd, or heating. 
            the year is an int
        
        Raises
        ------
        KeyError
        
        Returns
        -------
        np.array
            thawing or freezing gird for a year
        """
        freeze_or_thaw = key[0]
        year = key[1]
        
        if freeze_or_thaw.lower() in ['freeze', 'fdd']:
            return self.freezing[year]
        elif freeze_or_thaw.lower() in ['thaw', 'tdd', 'heating']:
            return self.thawing[year]
        else:
            raise KeyError, "key did not match tdd of fdd"
        
        
            
    
    


