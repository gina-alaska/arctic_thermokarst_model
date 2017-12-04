"""
grids
-----

object to manage all grid objects
"""

from area_grid import AreaGrid
from ald_grid import ALDGrid
from poi_grid import POIGrid
from ice_grid import IceGrid
from lake_pond_grid import LakePondGrid
from drainage_grid import DrainageGrid

from met_grid import DegreeDayGrids

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
        area: AreaGrid
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
        self.area = AreaGrid(config)
        
        self.shape = self.area.shape
        self.aoi = self.area.area_of_intrest()
        # set for other objects
        config['shape'] = self.shape
        config['AOI mask'] = self.aoi
        config['cohort list'] = self.area.get_cohort_list()
        self.ald = ALDGrid(config)
        self.poi = POIGrid(config)
        self.ice = IceGrid(config)
        self.lake_pond = LakePondGrid(config)
        for lpt  in config['pond types'] + config['lake types']:
            mask = self.area[lpt][0] > 0 # all cells in first ts > 0
            self.lake_pond.apply_mask(lpt, mask)
        self.drainage = DrainageGrid(config)
        
        self.degreedays = DegreeDayGrids(config)
    
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
        if key.lower() in ['lake pond','lake/pond','lakepond', 'lake', 'pond']:
            return self.lake_pond
        if key.lower() == 'drainage':
            return self.drainage
        if key.lower() == 'degree-day':
            return self.degreedays
        
        raise KeyError, 'could not find grid'
        
        
        
    
