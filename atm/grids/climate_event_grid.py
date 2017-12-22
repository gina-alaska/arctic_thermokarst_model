"""
"""

import os
import pickle
import numpy as np
from constants import ROW, COL

class GetGridError (Exception):
    """Raised if grid timestep not found"""


class ClimateEventGrid (object):
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
    
        self.start_year = config['start year']
        self.shape = config['shape']
        ## grid initilzed assuming no climate events
        self.grid = np.zeros(self.shape).astype(bool)
        
        ## current time step
        self.ts = 0
        
        self.climate_block_range = config['climate block range']
        self.probability = float(
            config['Met_Control']['climate_event_probability']
        )
        
        self.pickle_path = os.path.join(
            config['data path'], 'climate_event_records.pkl'
        )
        
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
            self.write_to_pickle(self.pickle_path)
        self.ts += 1
        self.grid = np.zeros(self.shape).astype(bool)
        return self.start_year + self.ts
        
    def get_grid (self, time_step = -1, flat = True):
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
           
        if time_step == -1:
            grid = self.grid
        else:
            data = self.read_from_pickle(self.pickle_path, time_step)
            #~ print time_step
            if len(data) == 0:
                raise GetGridError, 'invalid time step requested'
            grid = data['grid']
            
        return grid.reshape(shape)
        
    def create_climate_events (self):
        """Creates climate events 
        """
        block_size = np.random.randint(
            self.climate_block_range[0],
            self.climate_block_range[1]
        )
        
        
        for row in range(0, self.shape[ROW], block_size):
            for col in range(0, self.shape[COL], block_size):
                climate_event = np.random.uniform(0.0, 1.0)
                
                if not climate_event <= self.probability:
                    continue
                ## climate envent occuts in block
                print "climate event occured"
                self.grid[row:row+block_size, col:col+block_size] = True
        return block_size
        
    def write_to_pickle(self, pickle_name = None):
        """Save Met object to pickle file
        
        Parameters
        ----------
        pickle_name:
            name of pickle file
        """
        data = {
            'start year': self.start_year,
            'ts': self.ts,
            'shape': self.shape,
            'grid': self.grid,
            'climate block range': self.climate_block_range,
            'probablity': self.probability,
        }
        
        if pickle_name is None:
            pickle_name = self.pickle_path
       
        if self.ts == 0:
            mode = 'wb'
        else:
            mode = 'ab'

        with open(pickle_name, mode) as pkl:
            pickle.dump(data, pkl)
        
    
    def read_from_pickle(self, pickle_name, ts = -1):
        """load state from pickle
        
        Parameters
        ----------
        pickle_name: str
            pickle file with state
        """
        data = []
        with open(pickle_name, 'rb') as pkl:
            while True:
                try:
                    data.append(pickle.load(pkl))
                except EOFError:
                    break
                    
        if ts == -1:
            return data[ts]
        else:
            c = 0 
            while c < len(data):
                if data[c]['ts'] == ts:
                    return data[c]
                c += 1
        
        return {}
        
    def load_from_pickle(self, pickle_name):
        """
        """
        # get last ts from pickle and set state
        data = self.read_from_pickle(pickle_name, -1)
        
        self.start_year = data['start year']
        self.grid = data['grid']
        self.shape = data['shape']
        self.climate_block_range = data['climate block range']
        self.probability = data['probability']
        self.pickle_path = pickle_name
        self.data_path = os.path.split(pickle_name)[0]
        
        
        
    def figure (self, filename, year ):
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
            self[year].astype(int).reshape(self.shape) , 
            filename, 
            self.met_type + '-' + str(year) ,
            cmap = 'viridis',
            vmin = 0,
            vmax = 1
        )
        
    def figures(self, dirname ):
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
                self.met_type.replace(' ', '_') + '_' + str(year) + '.jpg'
            )
            self.figure(filename, year)
