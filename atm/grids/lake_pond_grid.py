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
    'pond depth range' : (.3,.3),
    'lake depth range' : (.3, 5),
    
    'ice depth alpha range': (2.31, 2.55),
    'start year': 1900,
    
    
    
}


class LakePondNotFoundError (Exception):
    """Raised if lake/pond type not found"""


class LakePondGrid (object):
    """Lake Pond Depth grid
    """
    
    def __init__ (self, config):
        """Lake Pond Depth grid
        
        Parameters
        ----------
        config: dict or atm.control or path to pickle file
            configuration for object
        
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
        if type(config) is str:
            ## read from existing pickle
            self.load_from_pickle(config)
            return
        
        self.shape = config['shape']
        self.start_year = config['start year']
        self.time_step = 0
        
        self.pond_types = config['pond types']
        self.lake_types = config['lake types']
        
        self.counts = self.setup_counts(config['pond types'], self.shape)
        self.counts.update(self.setup_counts(config['lake types'], self.shape))
        
        
        init_pond = config['pond depth range']
        init_lake = config['lake depth range']
        
        self.depths = self.setup_depths(
            config['pond types'], self.shape, init_pond
        )
        self.depths.update(
            self.setup_depths(config['lake types'], self.shape, init_lake)
        )
        
        self.pickle_path = os.path.join(
            config['pickle path'], 'lake_pond_history.pkl'
        )
        
        
        alpha_range = config['ice depth alpha range']
        self.ice_depth_constants = self.setup_ice_depth_constants(
            self.shape, alpha_range
        )
        
        ## current ice depth starts as zeros
        self.ice_depth = np.zeros(self.shape).flatten()
        
        ## climate expansion expansion
        self.climate_expansion_lakes = np.zeros(self.shape).flatten()
        self.climate_expansion_ponds = np.zeros(self.shape).flatten()
        
        
        ## can cheat and use setup depths
        self.time_since_growth = self.setup_depths(
            config['pond types'], self.shape, (0,0)
        )
        #~ self.growth.update(
            #~ self.setup_depths(config['lake types'], self.shape, (0,0))
        #~ )
        
        
    def __setitem__ (self, key, grid):
        """Sets a grid, can only set depths in current time step
        
        Parameters
        ----------
        key: str
            canon cohort name for a lake or pond type present in object
        grid: np.array
            data to set. should re shepe to shape attribute
        """
        self.set_depth_grid(key, grid)
    
    def __getitem__ (self, key):
        """gets a grid
        
        Parameters
        ----------
        key: Str, int, or tuple(int,str)
            if key is a string, it should be a canon cohort(lake/pond) name.
            if key is an int, it should be a year >= start_year, 
            but < current_year()
            if key is tuple, the int should fit the int requirements, and the 
            string the string requirements. 
            
        Returns
        -------
        np.array
            if key is a string, 3D, dimension are [timestep][grid row][grid col],
            timestep is year(key) - start year
            if key is a int, 3D, dimension are [cohort #][grid row][grid col],
            use key_to_int to find cohort #
            if key is tuple, 2D, [grid row][grid col]
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
            return self.get_depth_grid_at_ts(lake_pond_type, ts, False)
        elif get_type == 'snap_shot':
            return self.get_all_depths_at_ts(ts, flat=False)
        elif get_type == 'history':
            return self.get_depth_grid_history(lake_pond_type, flat=False)
            
    def setup_counts (self, types, shape):   
        """set up counts grids
        
        Parameters
        ----------
        types: list
            list of cohorts 
        shape: tuple
            (row, col) shape of model
            
        Returns
        -------
        dict:
            dictioanry of count grids
        """
        count = {}
        for t in types:
            count[t] = np.zeros(shape).flatten()
        return count
        

    def setup_depths (self, types, shape, init_depth):
        """set up depth grids
        
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
            dictioanry of depth grids
        """
        depths = {}
        for t in types:
            depths[t] = np.random.uniform(
                init_depth[0], init_depth[1], shape
            ).flatten()
        return depths
    
    def setup_ice_depth_constants (self, shape, init_alpha):
        """set up depth costant(alpha) grids
        
         Lake ice thickness is calculated using a modified Stefan Equation.
        alpha-coefficients range from 1.7-2.4 for average lake with snow and 2.7
        for windy lake with no snow.

        The Stefan equation that will be used is:
        h = alpha * sqrt(FDD)
    
        where: h is ice thickness (cm)
           alpha is Stefan Equation Coefficent
           FDD are the freezing degree days
        
        Parameters
        ----------
        shape: tuple
            (row, col) shape of model
        init_depth: tuple
            (min,max) initial depth
            
            
        Returns
        -------
        np.array:
            flatened Ice depth constat grid
        """
        
        return np.random.uniform(
                init_alpha[0], init_alpha[1], shape
            ).flatten()
    
    def current_year (self):
        """get current year
        
        Returns
        -------
        int
            year of last time step in model
        """
        return self.start_year + self.time_step
        
    def increment_time_step (self, archive_results = True):
        """increment time_step, and by default save records to pickle
        
        Parameters
        ----------
        archive_results: bool, default True
            archive results to pickle if true
            
        Returns 
        -------
        int 
            year for the new time step
        """
        if archive_results:
            self.write_to_pickle(self.time_step, self.pickle_path)
        self.time_step += 1
        return self.current_year()
        
    def apply_mask (self, lake_pond_type, mask):
        """Apply Mask to cells, will set depth to 0 in cells with no lakes/ponds
        of lake_pond_type
        
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
        if lake_pond_type in self.depths:
            self.depths[lake_pond_type][np.logical_not(mask.flatten())] = 0
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg
        
    def set_pickle_path (self, path):
        """overrided default pickle path
        
        Parameters
        ----------
        path: str
            set the pickle path
        """
        self.pickle_path = path

    def set_depth_grid (self, lake_pond_type, grid):
        """set a depth grid
        
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
        
        if lake_pond_type in self.depths:
            self.depths[lake_pond_type] = grid.reshape(self.shape).flatten()
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg
    
    def set_count (self, lake_pond_type, count):
        """set a counts grid
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        grid: np.array
            grid of count that can be reshaped to shape
            
        Raises
        ------
        LakePondNotFoundError
        """
        
        if lake_pond_type in self.counts:
            self.counts[lake_pond_type] = count.reshape(self.shape).flatten()
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg   
                 
    def get_depth_grid (self, lake_pond_type, flat = True):
        """get most recent depth grid
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        flat: bool, default True
            reshaps to shape if false
            
        Raises
        ------
        LakePondNotFoundError
        
        Returns
        -------
        dict:
            name grid at most recent time step
        """
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        if lake_pond_type in self.depths:
            return self.depths[lake_pond_type].reshape(shape)
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg     
                  
    def get_depth_grid_at_ts (self, lake_pond_type, ts = -1, flat = True):
        """get a depth grid
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        ts: int, -1
            time step to get
        flat: bool, default True
            reshaps to shape if false
            
        Raises
        ------
        LakePondNotFoundError
        
        Returns
        -------
        dict:
            name grid at most recent time step
        """
        if ts == -1 or ts == self.time_step:
            return self.get_depth_grid(lake_pond_type, flat)
            
        data = self.read_from_pickle(ts)   
       
        if data == False:
            raise IndexError, 'Time step not found'
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
        if lake_pond_type in self.depths:
            return data['depths'][lake_pond_type].reshape(shape)
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg    
                       
    def get_all_depths (self):
        """Gets all depths at most recent timestep
        
        Returns
        -------
        dict:
            depths at most recent time step
        """
        return self.depths
            
    def get_all_depths_at_ts (self, ts = -1, flat = True):
        """Gets all depths at most recent timestep
        
         Parameters
        ----------
        ts: int, -1
            time step to get
        flat: bool, default True
            reshaps to shape if false
        
        Raises
        ------
        IndexError
        
        Returns
        -------
        dict:
            depths at time step
        """
        if ts == -1 or ts == self.time_step:
            return self.get_all_depths()
            
        data = self.read_from_pickle(ts)   
        if data == False:
            raise IndexError, 'Time step not found'
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
       
        return {t:data['depths'][t].reshape(shape) for t in data['depths']}
        
        
    def get_depth_grid_history (self, lake_pond_type, flat = True):
        """Get grid at all time steps
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        flat: bool, default True
            reshaps to shape if false
        
        Raises
        ------
        LakePondNotFoundError
        
        Returns
        -------
        np.array
            3d array [timestep][row][col]
        """
        if not (lake_pond_type in self.depths.keys()):
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg
                
       
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
            
        data = self.read_from_pickle()
        data = [ ts['depths'][lake_pond_type].reshape(shape) for ts in data ]
        
        #missing current ?
        if len(data) == self.time_step:
            data.append(self.depths[lake_pond_type].reshape(shape))
            
        return np.array(data)
        
        
    def get_count (self, lake_pond_type, flat = True):
        """Get count at current grid
        
        Parameters
        ----------
        lake_pond_type: str
            canon cohort lake pond type
        flat: bool, default True
            reshaps to shape if false
            
        Returns
        -------
        np.array
            a count grid
        """
        shape = self.shape[0]*self.shape[1] if flat == True else self.shape
        
        if lake_pond_type in self.counts:
            return self.counts[lake_pond_type].reshape(shape)
        else:
            msg = 'Lake/Pond type not found in LakePondGrid data'
            raise LakePondNotFoundError, msg
    
    ## don't really need next two for now so not fixing at this time
    #~ def get_count_at_ts (self, lake_pond_type, ts = -1):
        #~ """"""
        #~ if ts == -1:
            #~ return self.get_count(lake_pond_type)
        #~ data = self.read_from_pickle(ts)   
        #~ if data == False:
            #~ raise IndexError, 'Time step not found'
        
        #~ if lake_pond_type in self.pond_counts:
            #~ return data['pond_counts'][lake_pond_type]
        #~ elif lake_pond_type in self.lake_counts:
            #~ return data['lake_counts'][lake_pond_type]
        #~ else:
            #~ raise LakePondNotFoundError,
            # 'Lake/Pond type not found in LakePondGrid data'
        
    #~ def get_count_history (self, lake_pond_type):
        #~ """"""
        #~ if lake_pond_type in self.pond_counts:
            #~ key = 'pond_counts'
        #~ elif lake_pond_type in self.lake_counts:
            #~ key = 'lake_counts'
        #~ else:
            #~ raise LakePondNotFoundError, 
            #'Lake/Pond type not found in LakePondGrid data'
            
        #~ data = self.read_from_pickle()
        #~ data = [ ts[key][lake_pond_type] for ts in data]
        #~ return data
        
    def calc_ice_depth (self, fdd):
        """calculate current ICE depth, using a modified Stefan Equation as
        described in setup_ice_depth_constants
        
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
        self.ice_depth = ((
            self.ice_depth_constants * np.sqrt(-1. * fdd).flatten()
        )/100.).reshape(self.shape)
        
    def write_to_pickle (self, ts, pickle_name = None ):
        """ Write a time stpe to a pickle, if ts is 0, a new file will be 
        created and metadata will also be written. All time steps != 0 will be 
        appended.
        
        Parameters
        ----------
        ts: int
            time step to savee
        pickle_name: path, or None(default)
            path to pickle file, if None will use pickle_path
            
        """  
        if pickle_name is None:
            pickle_name = self.pickle_path
        data = {
            'ts': ts,
            'counts': self.counts,
            'depths':  self.depths,
            'ice depth': self.ice_depth,
            'climate expansion lakes': self.climate_expansion_lakes,
            'climate expansion ponds': self.climate_expansion_ponds,
            'growth': self.time_since_growth,
            
        }
        if ts == 0:
            mode = 'wb'
        else:
            mode = 'ab'
        
        with open(pickle_name, mode) as pkl:
            if mode == 'wb':
                metadata = {
                    'shape':self.shape,
                    'start year': self.start_year,
                    'ice depth constants': self.ice_depth_constants,
                    'pond types': self.pond_types,
                    'lake types': self.lake_types,
                }
                pickle.dump(metadata, pkl)
            
            pickle.dump(data, pkl)
            
    def load_from_pickle (self, pickle_name):
        """load a final state from a pickle file, can be used to reset 
        object to a state
        
        Parametes
        ---------
        pickle_name: path
            path to pickle representation of object
        """
        
        
        archive = []
        with open(pickle_name, 'r') as pkl:
            while True:
                try:
                    archive.append(pickle.load(pkl))
                except EOFError:
                    break
                    
        self.start_year = archive[0]['start year']
        self.shape = archive[0]['shape']
        self.ice_depth_constants = archive[0]['ice depth constants']
        self.pond_types = archive[0]['pond types']
        self.lake_types = archive[0]['lake types']
        
        
        self.depths = archive[-1]['depths']
        self.counts = archive[-1]['counts']
        self.time_step = archive[-1]['ts']
        
        self.ice_depth = archive[-1]['ice depth']
        self.climate_expansion_lakes = archive[-1]['climate expansion lakes']
        self.climate_expansion_ponds = archive[-1]['climate expansion ponds']
        
        self.time_since_growth = archive[-1]['growth'] 
        
        
    
        self.pickle_path = pickle_name

        
    def read_from_pickle (self, ts = None, pickle_name = None, 
            set_current = False):
        """Read some data from a pickle file
        
        Parameters
        ----------
        ts: int or None
            time step to load, if none all are loaded
        pickle_name: path
            path to pickle representation of object
        set_current: bool
            if true set current state from file
            
        Returns
        -------
        dict or list of dicts 
            read from pickle
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
        archive = archive[1:] ## strip metadata
        
        if ts == None: 
            
            if set_current:
                self.depths = archive[-1]['depths']
                self.counts = archive[-1]['counts']
                self.time_step = archive[-1]['ts']
                
                self.ice_depth = archive[-1]['ice depth']
                self.climate_expansion_lakes = \
                    archive[-1]['climate expansion lakes']
                self.climate_expansion_ponds = \
                    archive[-1]['climate expansion ponds']
                
                self.time_since_growth = archive[-1]['growth'] 
            
            return archive
        else:
            ## if the list item idx == item['ts']
            if archive[ts] == archive[ts]['ts']:
                return archive[ts]
            for item in archive:
                if ts == item['ts']:
                    return item
            return {}
        
