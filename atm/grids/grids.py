

from terraingrid import CohortGrid
from ald_grid import ALDGrid
from poi_grid import POIGrid
from ice_grid import IceGrid


class ModelGrids (object):
    """ Class doc """
    
    def __init__ (self, config):
        """ Class initialiser """
        
        self.area = CohortGrid(config)
        self.ald = ALDGrid(config)
        self.poi = POIGrid(config)
        self.ice = IceGrid(config)
        
        self.shape = config['Shape']
        
        pass 
    
    def __getitem__ (self, key):
        """ Function doc """
        if key.lower() is 'area':
            return self.area
        if key.lower() is 'ald':
            return self.area
        if key.lower() is 'poi':
            return self.area
        if key.lower() is 'ice':
            return self.area
        
        raise KeyError, 'could not find grid'
        
        
        
    
