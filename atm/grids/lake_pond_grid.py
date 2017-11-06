"""
lake pond grid
--------------

"""
import numpy as np
import pickle
import os

from constants import ROW, COL


config_ex = {
    'pond types': ['Pond_WT_Y', 'Pond_WT_M', 'Pond_WT_O'],
    'lake types': [
        'SmallLakes_WT_Y', 'SmallLakes_WT_M', 'SmallLakes_WT_O',
        'MediumLakes_WT_Y', 'MediumLakes_WT_M', 'MediumLakes_WT_O',
        'LargeLakes_WT_Y', 'LargeLakes_WT_M', 'LargeLakes_WT_O',
    ],
    'shape' : (10,10),
    'pond depth' : (.3,.3),
    'lake depth' : (.3, 5)
    
}




class LakePondGrid (object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        
        self.shape = config['shape']
        
        self.pond_counts = self.setup_counts(config['pond types'])
        self.lake_counts = self.setup_counts(config['lake types'])
        
        
        init_pond = config['pond depth']
        init_lake = config['lake depth']
        
        self.pond_grids = self.setup_grids(
            config['pond types'], self.shape, init_pond
        )
        self.lake_grids = self.setup_grids(
            config['lake types'], self.shape, init_lake
        )
        
        self.pickle_path = 'lake_pond_history.pkl'
        
    def apply_mask (self, lake_pond_type, mask):
        """Apply Mask to cells, will set depth to 0 in cells with no lakes/ponds
        of lake_pond_type
        
        
        """
        if lake_pond_type in self.pond_grids:
            self.pond_grids[lake_pond_type][np.logical_not(mask)] = 0
        elif lake_pond_type in self.lake_grids:
            self.lake_grids[lake_pond_type][np.logical_not(mask)] = 0
        else:
            raise StandardError, 'Lake Pond type not in grids'
     
    def setup_counts (self, types):   
        """Function doc"""
        count = {}
        for t in types:
            count[t] = 0
        
        return count
        

    def setup_grids (self, types, shape, init_depth):
        """ Function doc """
        grids = {}
        for t in types:
            grids[t] = np.random.uniform(
                init_depth[0], init_depth[1], shape
            ).flatten()
        
        return grids
        
    def get_grid (self, lake_pond_type, flat = True):
        """ Function doc """
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        if lake_pond_type in self.pond_grids:
            return self.pond_grids[lake_pond_type].reshape(shape)
        elif lake_pond_type in self.lake_grids:
            return self.lake_grids[lake_pond_type].reshape(shape)
        else:
            raise StandardError, 'Lake Pond type not in grids'
        
    def get_grid_at_ts (self, lake_pond_type, ts = -1, flat = True):
        """ Function doc """
        if ts == -1:
            return self.get_grid(lake_pond_type)
        data = self.load_from_pickle(ts)   
        if data == False:
            raise IndexError, 'Time step not found'
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
        if lake_pond_type in self.pond_grids:
            return data['pond_grids'][lake_pond_type].reshape(shape)
        elif lake_pond_type in self.lake_grids:
            return data['lake_grids'][lake_pond_type].reshape(shape)
        else:
            raise StandardError, 'Lake Pond type not in grids'
        
        
    def get_grid_history (self, lake_pond_type, flat = True):
        """ Function doc """
        if lake_pond_type in self.pond_grids:
            key = 'pond_grids'
        elif lake_pond_type in self.lake_grids:
            key = 'lake_grids'
        else:
            raise StandardError, 'Lake Pond type not in grids'
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        data = self.load_from_pickle()
        data = [ ts[key][lake_pond_type].reshape(shape) for ts in data]
        return data
        
    
    def get_count (self, lake_pond_type):
        """ Function doc """
        if lake_pond_type in self.pond_counts:
            return self.pond_counts[lake_pond_type]
        elif lake_pond_type in self.lake_counts:
            return self.lake_counts[lake_pond_type]
        else:
            raise StandardError, 'Lake Pond type not in grids'
        
    def get_count_at_ts (self, lake_pond_type, ts = -1):
        """"""
        if ts == -1:
            return self.get_count(lake_pond_type)
        data = self.load_from_pickle(ts)   
        if data == False:
            raise IndexError, 'Time step not found'
        
        if lake_pond_type in self.pond_counts:
            return data['pond_counts'][lake_pond_type]
        elif lake_pond_type in self.lake_counts:
            return data['lake_counts'][lake_pond_type]
        else:
            raise StandardError, 'Lake Pond type not in grids'
        
    def get_count_history (self, lake_pond_type):
        """"""
        if lake_pond_type in self.pond_counts:
            key = 'pond_counts'
        elif lake_pond_type in self.lake_counts:
            key = 'lake_counts'
        else:
            raise StandardError, 'Lake Pond type not in grids'
            
        data = self.load_from_pickle()
        data = [ ts[key][lake_pond_type] for ts in data]
        return data
        
    def write_to_pickle (self, ts = 0, pickle_name = None ):
        """ Function doc """  
        if pickle_name is None:
            pickle_name = self.pickle_path
        data = {
            'ts': ts,
            'pond_counts': self.pond_counts,
            'lake_counts': self.lake_counts,
            'pond_grids':  self.pond_grids,
            'lake_grids':  self.lake_grids,
        }
        
        if ts == 0:
            mode = 'w'
        else:
            mode = 'a'
        
        with open(pickle_name, mode) as pkl:
            pickle.dump(data, pkl)
        
        
    def load_from_pickle (self, ts = None, pickle_name = None):
        """Function doc
        """
        if pickle_name is None:
            pickle_name = self.pickle_path
        
        archive = []
        with open(pickle_name, 'r') as pkl:
            while True:
                try:
                    archive.append(pickle.load(pkl))
                except EOFError:
                    break
        if ts == None: 
            return archive
        else:
            ## if the list item idx == item['ts']
            if archive[ts] == archive[ts]['ts']:
                return archive[ts]
            for item in archive:
                if ts == item['ts']:
                    return item
            return False
        
