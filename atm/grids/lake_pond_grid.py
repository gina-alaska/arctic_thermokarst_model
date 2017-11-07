"""
lake pond grid
--------------

"""
import numpy as np
import pickle
import os

from constants import ROW, COL


config_ex = {
    'pickle path': './pickles',
    'pond types': ['Pond_WT_Y', 'Pond_WT_M', 'Pond_WT_O'],
    'lake types': [
        'SmallLakes_WT_Y', 'SmallLakes_WT_M', 'SmallLakes_WT_O',
        'MediumLakes_WT_Y', 'MediumLakes_WT_M', 'MediumLakes_WT_O',
        'LargeLakes_WT_Y', 'LargeLakes_WT_M', 'LargeLakes_WT_O',
    ],
    'shape' : (10,10),
    'pond depth' : (.3,.3),
    'lake depth' : (.3, 5),
    'start year': 1900,
    
}


class LakePondNotFoundError (Exception):
    """Raised if lake/pond type not found"""


class LakePondGrid (object):
    """Lake Pond Depth grid
    
    """
    
    def __init__ (self, config):
        """Lake Pond Depth grid
        
        """
        
        self.shape = config['shape']
        self.start_year = config['start year']
        self.time_step = 0
        
        self.counts = self.setup_counts(config['pond types'])
        self.counts.update(self.setup_counts(config['lake types']))
        
        
        init_pond = config['pond depth']
        init_lake = config['lake depth']
        
        self.grids = self.setup_grids(
            config['pond types'], self.shape, init_pond
        )
        self.grids.update(
            self.setup_grids(config['lake types'], self.shape, init_lake)
        )
        
        self.pickle_path = os.path.join(
            config['pickle path'], 'lake_pond_history.pkl'
        )
        
    def set_pickle_path (self, path):
        """overrided default pickle path"""
        self.pickle_path = path
        
    def __setitem__ (self, key, grid):
        """sets a grid, can only set grids in current ts
        """
        self.set_grid(key, grid)
    
    def __getitem__ (self, key):
        """gets a grid
        """
        if type(key) is str: ## cohort at all ts
            get_type = 'history' 
            ts = None
            lake_pond_type = key
        elif type(key) is int: ## all cohorts at a ts
            get_type = 'snap_shot' 
            ts = key -self.start_year
            lake_pond_type = None
        else: # tuple ## a cohort at a ts
            get_type = 'item_at_time' 
            lake_pond_type = key[0]
            ts = key[1] - self.start_year 
            
            
        if get_type == 'item_at_time':
            return self.get_grid_at_ts(lake_pond_type, ts, False)
        elif get_type == 'snap_shot':
            return self.get_all_grids_at_ts(ts, flat=False)
        elif get_type == 'history':
            return self.get_grid_history(lake_pond_type, flat=False)
        
    def current_year (self):
        """get current year
        """
        return self.start_year + self.time_step
        
    def increment_time_step (self, archive_results = True):
        """saves records to pickle
        """
        if archive_results:
            self.write_to_pickle(self.time_step, self.pickle_path)
        self.time_step += 1
        return self.current_year()
        
    def apply_mask (self, lake_pond_type, mask):
        """Apply Mask to cells, will set depth to 0 in cells with no lakes/ponds
        of lake_pond_type
        
        """
        if lake_pond_type in self.grids:
            self.grids[lake_pond_type][np.logical_not(mask)] = 0
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
     
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
        
    def set_grid (self, lake_pond_type, grid):
        """ Function doc """
        
        if lake_pond_type in self.grids:
            self.grids[lake_pond_type] = grid.reshape(self.shape).flatten()
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
    
    def set_count (self, lake_pond_type, count):
        """ Function doc """
        if lake_pond_type in self.counts:
            self.counts[lake_pond_type] = count
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
        
    def get_grid (self, lake_pond_type, flat = True):
        """ Function doc """
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        if lake_pond_type in self.grids:
            return self.grids[lake_pond_type].reshape(shape)
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
        
    def get_grid_at_ts (self, lake_pond_type, ts = -1, flat = True):
        """ Function doc """
        if ts == -1 or ts == self.time_step:
            return self.get_grid(lake_pond_type, flat)
            
        data = self.load_from_pickle(ts)   
       
        if data == False:
            raise IndexError, 'Time step not found'
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
        if lake_pond_type in self.grids:
            return data['grids'][lake_pond_type].reshape(shape)
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
            
    def get_all_grids (self):
        """
        """
        return self.grids
            
    def get_all_grids_at_ts (self, ts = -1, flat = True):
        """ Function doc """
        if ts == -1 or ts == self.time_step:
            return self.get_all_grids()
            
        data = self.load_from_pickle(ts)   
        if data == False:
            raise IndexError, 'Time step not found'
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
       
        return {t:data['grids'][t].reshape(shape) for t in data['grids']}
        
        
    def get_grid_history (self, lake_pond_type, flat = True):
        """ Function doc """
        if not (lake_pond_type in self.grids.keys()):
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg
                
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        data = self.load_from_pickle()
        data = [ ts['grids'][lake_pond_type].reshape(shape) for ts in data ]
        
        #missing current ?
        if len(data) == self.time_step:
            data.append(self.grids[lake_pond_type].reshape(shape))
            
        return data
        
        
    def get_count (self, lake_pond_type):
        """ Function doc """
        if lake_pond_type in self.counts:
            return self.counts[lake_pond_type]
        else:
            raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
    
    ## don't really need next two for now so not fixing at this time
    #~ def get_count_at_ts (self, lake_pond_type, ts = -1):
        #~ """"""
        #~ if ts == -1:
            #~ return self.get_count(lake_pond_type)
        #~ data = self.load_from_pickle(ts)   
        #~ if data == False:
            #~ raise IndexError, 'Time step not found'
        
        #~ if lake_pond_type in self.pond_counts:
            #~ return data['pond_counts'][lake_pond_type]
        #~ elif lake_pond_type in self.lake_counts:
            #~ return data['lake_counts'][lake_pond_type]
        #~ else:
            #~ raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
        
    #~ def get_count_history (self, lake_pond_type):
        #~ """"""
        #~ if lake_pond_type in self.pond_counts:
            #~ key = 'pond_counts'
        #~ elif lake_pond_type in self.lake_counts:
            #~ key = 'lake_counts'
        #~ else:
            #~ raise LakePondNotFoundError, 'Lake/Pond type not found in LakePondGrid data'
            
        #~ data = self.load_from_pickle()
        #~ data = [ ts[key][lake_pond_type] for ts in data]
        #~ return data
        
    def write_to_pickle (self, ts = 0, pickle_name = None ):
        """ Function doc """  
        if pickle_name is None:
            pickle_name = self.pickle_path
        data = {
            'ts': ts,
            'counts': self.counts,
            'grids':  self.grids,
        }
        
        if ts == 0:
            mode = 'w'
        else:
            mode = 'a'
        
        with open(pickle_name, mode) as pkl:
            pickle.dump(data, pkl)
        
        
    def load_from_pickle (self, ts = None, pickle_name = None, set_current = False):
        """Function doc
        """
        if pickle_name is None:
            pickle_name = self.pickle_path
        
        if not os.path.exists(pickle_name):
            return {}
        
        archive = []
        with open(pickle_name, 'r') as pkl:
            while True:
                try:
                    archive.append(pickle.load(pkl))
                except EOFError:
                    break
        if ts == None: 
            
            if set_current:
                self.grids = archive[-1]['grids']
                self.counts = archive[-1]['counts']
                self.time_step = archive[-1]['ts']
            
            return archive
        else:
            ## if the list item idx == item['ts']
            if archive[ts] == archive[ts]['ts']:
                return archive[ts]
            for item in archive:
                if ts == item['ts']:
                    return item
            return {}
        
