import os
import numpy as np
from ..tools import stack_rasters

class MetGridShapeError(Exception):
    """Raised if data shape is not correct"""

class MetGridBase (object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        if type(config) is str:
            ## read from existing pickle
            self.load_from_pickle(config)
            return
        
        
        self.start_year = config['start year']
        self.shape = config['shape']
        self.history, self.met_type = self.setup(config)
        
        
        
    def setup (self):
        """ Function doc """
        return None, 'base'
        
    def __getitem__ (self, key):
        """
        """
        if key < self.start_year:
            raise IndexError, 'index should be after '+ str(self.start_year)
        
        return self.get_grid(key - self.start_year, True)
    
    def read_data(self, source, data_type = 'spatial'):
        """
        """
        if data_type.lower() == 'spatial':
            
            ## if mm data DNE create it 
            if type(source) is list:
                mm_file = os.path.join(
                    config['data path'], self.met_type + '_history.data'
                )
                data, shape = self.read_spatial_from_files(
                    source, self.met_type, mm_file
                )
                if shape[0] != self.shape[0] * self.shape[1] :
                    raise MetGridShapeError, 'loaded met data has wrong shape'
                del data
                source = mm_file
                
            
            ## load data as read only
            data = self.read_spatial_from_memory_map(source)
            years = data.shape[0] / (self.shape[0] * self.shape[1])
            data = data.reshape(
                years, (self.shape[0] * self.shape[1])
            )
        else:
            msg = 'non spatial data handeling not implmented'
            raise NotImplementedError, msg
        return data
        
    def read_spatial_from_files (self, files, bin_name):
        """
        """
        return tools.load_and_stack_memory_mapped(files, bin_name)
        
    def read_spatial_from_memory_map (self, met_file):
        """
        """
        return np.memmap(met_file, dtype='float32', mode='r')
        
    ## spatial data takes precdence
    #~ def read_met_point (self):
        #~ """
        #~ """
        
    def get_grid (self, time_step, flat = True):
        """get grid at ts
        """
        shape = self.shape
        if flat:
            shape = self.shape[0] * self.shape[1]
        return self.history[time_step].reshape(shape)
        
    def save_to_pickle(self):
        """
        """
        data = {
            'start year', self.star_year,
            'history', self.history,
            'type', self.met_type,
            'shape', self.shape,
            'data', self.history
        }
        brine(filename, data)
        
    
    def load_from_pickle(self):
        """
        """
        data = load(pickle_name)
        
        self.start_year = data['start year']
        self.history = data['history']
        self.met_type = data['type']
        self.shape = data['shape'],
        self.history = data['data']
        
        
    def figure (self, filename, ts):
        """
        """
        pass
        
    def binary (self, filename, ts):
        """
        """
        pass
        
## Not Implemented at this point. use the preprocessing tool to convert to 
## degree day data
#~ class AirTempGrid (MetGridBase):
    #~ """Air temerature grid. Not implmenting functionality at this
    #~ time use preprocessing utility to convert data to degree days
    #~ """
    #~ def setup(config):
        #~ return grid, 'Air Temp'

class TDDGrid (MetGridBase):
    """ Class doc """
    
    def setup (self, config):
        """ Class initialiser """
        data = self.read_data( config['TDD_file'] )
        return data, 'TDD'
        

class FDDGrid (MetGridBase):
    """ Class doc """
    
    def setup (self, config):
        """ Class initialiser """
        data = self.read_data( config['FDD_file'] )
        return data, 'FDD'

class DegreeDayGrids (object):
    """
    """
    def __init__ (self, config):
        """ Class initialiser """
        self.thawing = TDDGrid(config)
        #~ #self.thawing.setup()
        
        self.freezing = FDDGrid(config)
        #~ #self.freezing.setup()
        
        
    def __getitem__ (self, key):
        """
        """
        freeze_or_thaw = key[0]
        year = key[1]
        
        if freeze_or_thaw.lower() in ['freeze', 'fdd']:
            return self.freezing[year]
        elif freeze_or_thaw.lower() in ['thaw', 'tdd', 'heating']:
            return self.thawing[year]
        else:
            raise KeyError, "key did not match tdd of fdd"
        
        
            
    
    


