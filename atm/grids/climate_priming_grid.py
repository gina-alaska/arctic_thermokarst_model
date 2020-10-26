"""
Climate Priming Grid
--------------------

Grid for managaging climate priming thermokarst initiation values
"""
import os
import numpy as np

from multigrids import TemporalMultiGrid, common, tools

from atm.tools import stack_rasters, initiation_areas

from .constants import ROW, COL, create_deepcopy

from atm.images import raster




class StaticClimatePrimingError (Exception):
    """Raised when a method attempts to change climate priming gird if
    config['preload_climate_priming'] is True, or when attemting to preload
    data if config['preload_climate_priming'] is False.
    """

class CalculateClimatePrimingError (Exception):
    """Raised if error occurs while calculating climate priming values
    """

CLIMATE_PRIMING_UNINITALIZED_VALUE = np.nan

class ClimatePrimingGrid (TemporalMultiGrid):
    """Lake Pond Depth grid
    """
    
    def __init__ (self, *args, **kwargs):
        """climate priming grid
        
        Parameters
        ----------
        
        
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
        ice_depth_constatns: np.array
            array of alpha ice constatns for stephan equation
        """
        config = args [0]
        if type(config) is str: # existing multigrid 
            super(ClimatePrimingGrid , self).__init__(*args, **kwargs)
            self.config['start_timestep'] = self.config['start_year']
        else: # new multigrid
            args = [
                config['grid_shape'][ROW], 
                config['grid_shape'][COL],  
                2,
                config['model length']
            ]

            kwargs = create_deepcopy(config) 

            kwargs['data_type'] = 'float32'
            kwargs['mode'] = 'r+'
            kwargs['grid_names'] = ['climate_priming_values', 'active_areas']

            super(ClimatePrimingGrid , self).__init__(*args, **kwargs)
            self.config['start_year'] = int(config['initialization_year'])
            self.config['start_timestep'] = self.config['start_year']

            self.config['preload_climate_priming'] = config['preload_climate_priming']
            if config['preload_climate_priming'] == True:
                self.load_climate_priming_from_directory(
                    config['climate_priming_input_directory']
                )
            else:
                self.grids[:] = CLIMATE_PRIMING_UNINITALIZED_VALUE

            self.config['predisposition_map'] = None

            self.config['initiation_threshold'] = config['initiation_threshold']
            self.config['termination_threshold'] = \
                                                 config['termination_threshold']

            self.config['stable_climate_averages'] = None


    def load_climate_priming_from_directory(self, in_dir):
        """
        """
        # if self.config['preload_climate_priming'] == True:
        #     msg = "cannot preload climate priming data "
        #     msg += "'preload_climate_priming' is False"
        #     raise StaticClimatePrimingError(msg)
        # pass
        data = tools.tiffs_to_array(
            in_dir
            # file_name_structure='*.tif', 
            # sort_func=sorted, 
            # verbose=False
        )

        self.grids[:,0,:] = data[:].reshape(self.grids[:,0,:].shape )

    def load_predisposition_map(self, map_raster):
        """
        """
        if not self.config['predisposition_map'] is None:
            # return False
            raise IOError('predisposition_map is already loaded')
        data, md = raster.load_raster(map_raster)
        # print(np.logical_and(0 <= data, data <= 1))
        if (np.logical_and(0 <= data, data <= 1)).all():
            self.config['predisposition_map'] = data
        elif (np.logical_and(0 <= data, data <= 100)).all():
            self.config['predisposition_map'] = data / 100
        else: 
            raise ValueError (
                'Predisposition data should be between 0 and 1 or 0 and 100'
            )
        # return True


    def load_stable_climate_averages(self, climate_average_dict):
        """
        """
        if self.config['preload_climate_priming'] == True:
            msg = "cannot load stable_climate_averages when "
            msg += "'preload_climate_priming' is True"
            raise StaticClimatePrimingError(msg)

        self.config['stable_climate_averages'] = climate_average_dict

    def get_active_map(self, year=None):
        """
        """
        if year is None:
            year = self.current_timestep()

        if year > self.config['start_timestep']:
            return self['active_areas', year].astype(bool)
        else:
             
            return np.zeros(self.config['grid_shape']) != 0

    def get_stable_map(self, year=None):
        """
        """
        return np.logical_not( self.get_active_map(year) )
        

        
    def get_initiation_map(self, year=None):
        """
        """
        if year is None:
            year = self.current_timestep()

        current = self.get_predisposition_value_map(year)
        return current >= self.config['initiation_threshold']
    
    def get_termination_map(self, year=None):
        """
        """
        if year is None:
            year = self.current_timestep()

        current = self.get_predisposition_value_map(year)
        return current < self.config['termination_threshold']
    
    def get_categorical_map(self, year=None):
        """Gets a map showing regions that are: 
            0: are not changing (stable)
            1: climate is primied for initialization (initialized)
            2: are still changing (active)
            3: have stopped changing (termiated)
        """
        if year is None:
            year = self.current_timestep()

        current = np.zeros(self.config['grid_shape']) + np.nan
        
       
        current[self.get_active_map(year)] = 2
        current[self.get_initiation_map(year)] = 1
        current[self.get_termination_map(year)] = 3
        current[self.get_stable_map(year)] = 0

        return current         

    def get_predisposition_value_map(self, year=None):
        """
        """
        if year is None:
            year = self.current_timestep()

        current = self['climate_priming_values', year]
        if not self.config['predisposition_map'] is None:
            current *= self.config['predisposition_map']
        
        return current 
            
    def calculate_climate_priming(self, year = None, cp_variables = {}):

        if year is None:
            year = self.current_timestep()

        # print(year)
        if self.config['preload_climate_priming'] == False:
            if len(cp_variables.keys()) == 0:
                raise CalculateClimatePrimingError(
                    'No data provided to calculate climate priming values'
                )
            ## need to calculate cp value firest
            # self['climate_priming_values', year] = ...
            values = initiation_areas._calc_vpdm_cptki_for_year(
                cp_variables,
                self.config['stable_climate_averages'],
                self.config['grid_shape']
            )
            # print (values)
            self['climate_priming_values', year] = values
            
        # print(self['climate_priming_values',1901])
        current_i = self.get_initiation_map(year) # initialized 

        current_t = self.get_termination_map(year) # terminated
        last_a = self.get_active_map(year - 1) # last year active
        

        a_or_i = np.logical_or(last_a, current_i)
        not_t = np.logical_not(current_t)
        current_a = np.logical_and(a_or_i, not_t) # new current active


        # print (current_i)

        # import matplotlib.pyplot as plt
        # if year % 10 == 0:
        #     fig, axes = plt.subplots(2,3)

        #     axes[0,0].imshow(current_i, vmin=0, vmax=1)
        #     axes[0,1].imshow(current_t, vmin=0,vmax=1)
        #     axes[0,2].imshow(current_a, vmin=0,vmax=1)

        #     axes[1,0].imshow(current_a_or_i, vmin=0,vmax=1)
        #     axes[1,1].imshow(current_not_t, vmin=0,vmax=1)
        #     axes[1,2].imshow(current_active, vmin=0,vmax=1)
        #     fig.show()


        # print (current_a)
        self['active_areas', year]= 0
        self['active_areas', year][current_a] = 1
       