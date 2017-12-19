"""
Control
-------

for manageing control confguration in the ATM

"""
from atm_io import control_file
import os

from cohorts import find_canon_name
from grids.ice_grid import ICE_TYPES

import yaml

class ControlKeyError (Exception):
    """Raised if key being set is in control dict"""
    
class ControlPathError (Exception):
    """Raised if control path is invalid"""
    
class ControlSetError (Exception):
    """Raised if control path is invalid"""

class ControlInvalidRequest (Exception):
    """Raised if control value requested is bad"""

class Control(object):
    """ Class doc """
    
    def __init__ (self, main_control_file):
        """class for managing  control configuration
        
        Parameters
        ----------
        main_control_file: path
            path to main control file
            
        Attributes
        ----------
        init_control: dict
            initial control values read from the Control files
        new_control:
            control values set at runtime
        """
        self.init_control = self.load({}, main_control_file)
        
        from pprint import pprint
        pprint(self.init_control)
        
        self.new_control = {}
        
        if not os.path.exists(self['data path']):
            os.makedirs(self['data path'])
        
    def load (self, control, in_file):
        """Reads control files, recursivly
        
        Parameters
        ----------
        control: dict
            control dict to update
        in_file:
            file to read values from
            
        Raises
        ------
        ControlPathError
            if paths are not found
            
        Returns
        -------
        dict or list
        """
        with open(in_file, 'r') as cf:
            control = yaml.load(cf)
            
        control_dir = control['Control_dir']
        
        with open(os.path.join(
            control_dir, control['Archive_data']
        )) as cf:
            control['Archive_data'] = yaml.load(cf)
        
        with open(os.path.join(
            control_dir, control['Initialize_Control']
        )) as cf:
            control['Initialize_Control'] = yaml.load(cf)
        
        with open(os.path.join(
            control_dir, control['Initial_Cohort_List']
        )) as cf:
            control['Initial_Cohort_List'] = yaml.load(cf)
        
        with open(os.path.join(
            control_dir, control['Met_Control']
        )) as cf:
            control['Met_Control'] = yaml.load(cf)
        
        with open(os.path.join(
            control_dir, control['Terrestrial_Control']
        )) as cf:
            control['Terrestrial_Control'] = yaml.load(cf)
       
        with open(os.path.join(
            control_dir, control['Lake_Pond_Control']
        )) as cf:
            control['Lake_Pond_Control'] = yaml.load(cf)
        
        for key in control['Cohorts']:
            try:
                with open(
                    os.path.join(control_dir, control['Cohorts'][key])
                ) as cf:
                    control['Cohorts'][key] = yaml.load(cf)
            except IOError:
                pass
        
        return control
        
        
    def __getitem__ (self, key):
        """get item function
        
        Parameters
        ----------
        key: str or other
        
        Raises
        ------
        KeyError
            key not found in init_control or new_control
        
        Returns
        -------
        returns value
        """
        if key.replace(' ', '_') in self.init_control.keys():
            return self.init_control[key.replace(' ', '_')]
        elif key.replace(' ', '_') in self.new_control.keys():
            return self.new_control[key.replace(' ', '_')]
        
        ## special cases
        elif key == 'target resolution':
            return self.get_target_resoloution()
        ## special cases
        elif key == 'area data':
            return self.get_area_rasters()
        elif key == 'init ald':
            return self.get_initial_ald()
        elif key == 'init ice':
            return self.get_initial_ice_content()
        elif key == 'porosities':
            return self.get_porosities()
        elif key == 'PL factors':
            return self.get_pl_factors()
        elif key == 'cohort ice slopes':
            return self.get_ice_slope_coefficients()
        elif key == 'pond types':
            return self.get_pond_types()
        elif key == 'lake types':
            return self.get_lake_types()
        elif key == 'pond depth range':
            return self.get_pond_depth_range()
        elif key == 'ice depth alpha range':
            return self.get_ice_depth_alpha_range()
        elif key == 'lake depth range':
            return self.get_lake_depth_range()
        elif key == 'pickle path':
            return os.path.join(self['Output_dir'], 'runtime_data')
        elif key == 'data path':
            return os.path.join(self['Output_dir'], 'runtime_data')
        elif key == 'climate block range':
            return self.get_climate_block_size_range()
        else:
            raise KeyError, 'Key "' + str(key) + '" is invalid'
            
    __getattr__ = __getitem__
    
    def __setitem__ (self, key, value):
        """sets an item in new_control
        
        Parameters
        ----------
        key:
            key in new control
        value:
            value to set
        
        Raises
        ------
        ControlSetError
        """
        if key in self.init_control.keys():
            raise ControlSetError, "cannot overwrite initial control values"
        else:
            self.new_control[key.replace(' ','_')] = value
        
    def get_target_resoloution (self):
        """Get model target resoloution
        
        Returns
        -------
        tuple, 
            (y_resoloution, x_resoloution)
        """
        return (self.Y_model_resolution, self.X_model_resolution)
   
    def get_initial_ald (self):
        """Get init ald range
        
        Returns
        -------
        tuple, 
            (lower bound, upper bound)
        """
        return (self.Terrestrial_Control['ALD_Distribution_Lower_Bound'],
                self.Terrestrial_Control['ALD_Distribution_Upper_Bound'])
    
    def get_initial_ice_content (self):
        """Get init ice contet, currently returns types of ice
        
        Returns
        -------
        tuple, 
            types of ice 
        """
        return ICE_TYPES 
        
    def get_area_rasters (self):
        """Gets input area raster file paths
        
        Returns
        -------
        List:
            paths to input rasters
        """
        print self.Initial_Cohort_List
        return [
            os.path.join(self.Input_dir, f) for f in self.Initial_Cohort_List
        ]
        

    def get_porosities (self):
        """Gets porosities
        
        Returns
        -------
        List:
            dict of porosities
        """
        p = {}
        for key in self.init_control['Cohorts']:
            try:
                p[find_canon_name(key.replace('_Control', ''))] = \
                    self.init_control['Cohorts'][key]['porosity']
            except:
                pass
        return p
        
    def get_pl_factors (self):
        """Gets protecetive layer factors
        
        Returns
        -------
        dict:
            dict of protecetive layer factors
        """
        keys = [
            key for key in self.Terrestrial_Control if key.find('PLF') != -1
        ]
        
        return {
            find_canon_name(key.replace('_PLF','')): 
                self.Terrestrial_Control[key] for key in keys
        }
        
    def get_ice_slope_coefficients (self):
        """Gets Ice slope coefficients for each cohort each type of ice 
        
        Returns
        -------
        Dict
        """
        cohorts = {}
        for key in self.init_control['Cohorts']:
            coeff = {}
            try:
                
                for ice in ICE_TYPES:
                    coeff[ice] = self.init_control['Cohorts'][key]['ice_slope_' + ice]
                cohorts[find_canon_name(key.replace('_Control', ''))] = coeff
            except:
                pass
        return cohorts
        
    def get_pond_types (self):
        """gets pond types
        
        Returns
        -------
        list:
            list of all canon cohort names used with 'pond' present
        """
        cohorts = []
        for key in self.init_control['Cohorts']:
            if key.lower() == 'lake_pond_control':
                continue
            try:
                name = find_canon_name(key.replace('_Control', ''))
                if name.lower().find('pond') != -1:
                    cohorts.append(name)
            except:
                pass
        return cohorts
        
    def get_lake_types (self):
        """gets lake types
        
        Returns
        -------
        list:
            list of all canon cohort names used with 'lake' present
        """
        cohorts = []
        for key in self.init_control['Cohorts']:
            if key.lower() == 'lake_pond_control':
                continue
            try:
                name = find_canon_name(key.replace('_Control', ''))
                if name.lower().find('lake') != -1:
                    cohorts.append(name)
            except:
                pass
        return cohorts
        
    def get_pond_depth_range(self):
        """gets pond depth range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        print self.Lake_Pond_Control
        if self.Lake_Pond_Control['Pond_Distribution'].lower() == 'uniform':
            return (
                self.Lake_Pond_Control['Uniform_Pond_Depth'], 
                self.Lake_Pond_Control['Uniform_Pond_Depth']
            )
        elif self.Lake_Pond_Control['Pond_Distribution'].lower() == 'random':
            return (
                self.Lake_Pond_Control['Lower_Pond_Depth'], 
                self.Lake_Pond_Control['Upper_Pond_Depth']
            )
        else:
            raise ControlInvalidRequest , "cannot get pond depth range"
            
    def get_lake_depth_range(self):
        """gets lake depth range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        if self.Lake_Pond_Control['Lake_Distribution'].lower() == 'uniform':
            return (
                self.Lake_Pond_Control['Uniform_Lake_Depth'], 
                self.Lake_Pond_Control['Uniform_Lake_Depth']
            )
        elif self.Lake_Pond_Control['Lake_Distribution'].lower() == 'random':
            return (
                self.Lake_Pond_Control['Lower_Lake_Depth'], 
                self.Lake_Pond_Control['Upper_Lake_Depth']
            )
        else:
            raise ControlInvalidRequest, "cannot get lake depth range"
    
    def get_ice_depth_alpha_range(self):
        """gets ice depth coefficient range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        if self.Lake_Pond_Control['ice_thickness_distribution'].lower() ==\
            'uniform':
            return (
                self.Lake_Pond_Control['ice_thickness_uniform_alpha'], 
                self.Lake_Pond_Control['ice_thickness_uniform_alpha']
            )
        elif self.Lake_Pond_Control['ice_thickness_distribution'].lower() ==\
            'random':
            return (
                self.Lake_Pond_Control['Lower_ice_thickness_alpha'], 
                self.Lake_Pond_Control['Upper_ice_thickness_alpha']
            )
        else:
            raise ControlInvalidRequest, "cannot get ice depth alpha range"
            
    def get_climate_block_size_range (self):
        """
        """
        if self['Met_Control']['climate_blocks'].lower() == 'random':
            return (
                int(self['Met_Control']['climate_block_lower_bound']),
                int(self['Met_Control']['climate_block_upper_bound'])
            )
        else:
            return (
                int(self['Met_Control']['climate_blocks']),
                int(self['Met_Control']['climate_blocks'])
            )
        
        
        
