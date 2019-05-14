"""
grids
-----

object to manage all grid objects
"""

import numpy as np
from area_grid import AreaGrid
from ald_grid import ALDGrid
from poi_grid import POIGrid
from ice_grid import IceGrid
from lake_pond_grid import LakePondGrid
from drainage_grid import DrainageGrid
from climate_event_grid import ClimateEventGrid

from met_grid import DegreeDayGrids
import os

class ModelGrids (object):
    """Class containing all grid objects for the ATM model
        
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
    
    def __init__ (self, config, logger):
        """Class containg all grid objects for the ATM model
        
        Parameters
        ----------
        config: dict
            configuration for grid objects
        """
        self.logger = logger
        self.logger.add('loading AREA')
        config['data_type'] = np.float32
        self.area = AreaGrid(config,logger = self.logger)
        self.area.config['dataset_name'] = 'Area Data'
        self.area.config['description'] = \
            """Area Data contains fractional cohort data for each year the ATM
            was run. 
            """
        self.logger.add('performing post AREA setup')
        self.shape = self.area.grid_shape
        self.aoi = self.area.area_of_interest()
        config['shape'] = self.shape
        config['grid_shape'] = self.area.grid_shape
        config['AOI mask'] = self.aoi
        config['cohort list'] = self.area.get_cohort_list()
        self.logger.add('loading ALD')
        self.ald = ALDGrid(config,logger = self.logger)
        self.ald.config['dataset_name'] = 'ALD Data'
        self.ald.config['description'] = \
            """ALD Data contains ALD, and Protective Layer data for each year 
            the ATM was run.
            """
        self.logger.add('loading POI')
        self.poi = POIGrid(config,logger = self.logger)
        self.poi.config['dataset_name'] = 'POI Data'
        self.poi.config['description'] = \
            """POI Data contains Poi data for each year the ATM was run. 
            """
        self.logger.add('loading ICE')
        self.ice = IceGrid(config,logger = self.logger)
        self.ice.config['dataset_name'] = 'Ice Data'
        self.ice.config['description'] = \
            """
            Ice Data contains the ice content grid for the ATM model run
            """
        self.logger.add('loading LAKE POND')
        self.lake_pond = LakePondGrid(config,logger = self.logger)
        self.lake_pond.config['dataset_name'] = 'Lake Pond Data'
        self.lake_pond.config['description'] = \
            """Lake-Pond Data contains Lake and Pond depth and count data for 
            each year the ATM was run. 
            """
        self.logger.add('loading CLIMATE EVENT')
        self.climate_event = ClimateEventGrid(config,logger = self.logger)
        self.climate_event.config['dataset_name'] = 'Climate Event Data'
        self.climate_event.config['description'] = \
            """Climate Event Data contains climate event data for each 
            year the ATM was run. 
            """
        ## TODO:redo masks here
        # for lpt  in config['pond types'] + config['lake types']:
        #     #~ print lpt
        #     mask = self.area[lpt][0] > 0 # all cells in first ts > 0
        #     self.lake_pond.apply_mask(lpt, mask)
        self.logger.add('loading DRAINGAGE')
        self.drainage = DrainageGrid(config,logger = self.logger)
        self.drainage.config['dataset_name'] = 'Drainage Data'
        self.drainage.config['description'] = """
        Drainage contains the drainage grid for the ATM model run
        """
        
        self.logger.add('loading DEGREE DAY')
        self.degreedays = DegreeDayGrids(
            os.path.join(
                config['Input_dir'], config['Met_Control']['FDD_file']),
            os.path.join(
                config['Input_dir'], config['Met_Control']['TDD_file'])
        )
        
        ## what does this do?
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
        return self.degreedays.thawing.num_timesteps
        
    def increment_time_step(self):
        """Increment time step for all temporal grids
        """
        for grid in self.get_grid_list():
            try:
                self[grid].increment_time_step()
            except AttributeError:
                pass

    def get_grid_list (self):
        """
        Returns
        -------
        list
            list of grids in object
        """
        return [
            'area', 'ald', 'poi', 'ice', 'lake pond',
            'drainage', 'degree-day','climate event'
        ]
    
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
        
    def save_grids(self, out_path, new_options={}):
        """save all grids

        Parameters
        ----------
        out_path: path
            directory to save grids in
        new_options: dict
            keys are "area", "ald", "climate_event", "drainage", "ice", 
            "lake_pond", "poi", "met"
            Values are boolean and indicate which grids to save, all are saved
            by default.


        
        """
        options = {
            "area": True,
            "ald": True,
            "climate_event": True,
            "drainage": True,
            "ice": True,
            "lake_pond": True,
            "poi": True,
            # "met": True,
        }
        options.update(new_options)

        self.logger.add('Saving Grid Data')

        if options['area']:
            self.logger.add('   Saving AreaGrid')
            self.area.save(os.path.join(out_path, 'area.yaml'))
        if options['ald']:
            self.logger.add('   Saving ALDGrid')
            self.ald.save(os.path.join(out_path, 'ald.yaml'))
        if options['climate_event']:
            self.logger.add('   Saving ClimateEventGrid')
            self.climate_event.save(
                os.path.join(out_path, 'climate_event.yaml')
            )
        if options['drainage']:
            self.logger.add('   Saving DrainageGrid')
            self.drainage.save(os.path.join(out_path, 'drainage.yaml'))
        if options['ice']:
            self.logger.add('   Saving IceGrid')
            self.ice.save(os.path.join(out_path, 'ice.yaml'))
        if options['lake_pond']:
            self.logger.add('   Saving LakePondGrid')
            self.lake_pond.save(os.path.join(out_path, 'lake_pond.yaml'))
        if options['poi']:
            self.logger.add('   Saving POIGrid')
            self.poi.save(os.path.join(out_path, 'poi.yaml'))
        # if options['met']:
        #     self.logger.add('   Saving Met girds')
        #     self.degreedays.freezing.save(
        #         os.path.join(out_path, 'met_freezing.yaml')
        #     )
        #     self.degreedays.thawing.save(
        #         os.path.join(out_path, 'met_thawing.yaml')
        #     )
        
        
    
