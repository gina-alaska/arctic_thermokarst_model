

from terraingrid import CohortGrid
from ald_grid import ALDGrid
from poi_grid import POIGrid
from ice_grid import IceGrid


class ModelGrids (object):
    """Model Grids Class"""
    
    def __init__ (self, config):
        """Class containg all grid objects for the ATM model
        
        Parameters
        ----------
        config: dict
            configuration for grid objects
            
        Attributes
        ----------
        area: CohortGrid
            object representing fractional area grids for each cohort
        ald: ALDGrid
            ALD, and PL grid object
        poi: POIGird 
            POI grid object
        ice: IceGrid
            ice grid object
        shape: tuple:
            shape of grid at model resoloution
        aoi: np.array
            a grid of booleans where true elements are in AOI, false are not
        
        """
        self.area = CohortGrid(config)
        
        self.shape = self.area.shape
        self.aoi = self.area.area_of_intrest()
        # set for other objects
        config['shape'] = self.shape
        config['AOI mask'] = self.aoi
        self.ald = ALDGrid(config)
        self.poi = POIGrid(config)
        self.ice = IceGrid(config)
    
    def __getitem__ (self, key):
        """get item
        
        Parameters
        ----------
        key: str
            string 'area', 'ald', 'poi', or 'ice'. case does not matter
            
        Raises:
        -------
        KeyError
        
        Returns
        -------
            an atm.grids object 
        """
        if key.lower() == 'area':
            return self.area
        if key.lower() == 'ald':
            return self.ald
        if key.lower() == 'poi':
            return self.poi
        if key.lower() == 'ice':
            return self.ice
        
        raise KeyError, 'could not find grid'
        
        
        
    
