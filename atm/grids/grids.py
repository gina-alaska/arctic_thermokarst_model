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
from climate_event_grid import ClimateEventGrid

from met_grid import DegreeDayGrids

class ModelGrids (object):
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
        lake_pond: LakePondGrid
            Lake Pond Object
        drainage: DrainageGrid
            drainage grid
        shape: tuple:
            shape of grid at model resoloution
        aoi: np.array
            a grid of booleans where true elements are in AOI, false are not
    """
    
    def __init__ (self, config):
        """Class containg all grid objects for the ATM model
        
        Parameters
        ----------
        config: dict
            configuration for grid objects
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
        self.climate_event = ClimateEventGrid(config)
        #~ print config['pond types'] + config['lake types']
        for lpt  in config['pond types'] + config['lake types']:
            print lpt
            mask = self.area[lpt][0] > 0 # all cells in first ts > 0
            self.lake_pond.apply_mask(lpt, mask)
        self.drainage = DrainageGrid(config)
        
        self.degreedays = DegreeDayGrids(config)
        
        self.ald.setup_ald_constants(
            self.degreedays.thawing[config['start year']]
        )
        
    def get_max_time_steps (self):
        """Get the max number of model timesteps possible
        
        Returns
        -------
        int:
            number timesteps, based on length of degree day arrays
        """
        return len(self.degreedays.thawing.history)
        
    def add_time_step(self, zeros = False):
        """add a time step for all grids where nessary/possible
        
        Parameters
        ----------
        zeros: bool
            if set to true data is set as all zeros
        """
        self.area.add_time_step(zeros)
        self.ald.add_time_step(zeros)
        self.poi.add_time_step(zeros)
        self.lake_pond.increment_time_step()
        self.climate_event.increment_time_step()
        
    
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
        if key.lower() == 'climate event':
            return self.climate_event
        
        raise KeyError, 'could not find grid'
        
        
        
    
