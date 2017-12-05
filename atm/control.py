"""
Control
-------

for manageing control confguration in the ATM

"""
from atm_io import control_file
import os

from cohorts import find_canon_name
from grids.ice_grid import ICE_TYPES

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
        with open(in_file, 'r') as fd:
            inputs = control_file.read(fd)
        
        is_list = True
        for k in inputs.keys():
            if type(k) is int:
                continue
            is_list = False
            break
            
        if is_list: 
            return inputs.values()
        
        for key in inputs:
            val = inputs[key]
            
            ## can val convert to # 
            try: 
                val = int(val)
            except ValueError:
                try: 
                    val = float(val)
                except ValueError:
                    pass
            
            if key in control.keys():
                raise ControlKeyError, key + ' is in the control file already'
            
            control[key] = val
            
        # main control 
        if 'Simulation_area' in control.keys():
            
            if not os.path.exists(control['Run_dir']):
                if control['Run_dir'][:2] == './':
                    control['Run_dir'] = control['Run_dir'][2:]
                root = os.path.abspath(os.path.split(in_file)[0])
                pth = os.path.join(root, control['Run_dir']) 
                if os.path.exists(pth):
                    control['Run_dir'] = pth
                else:
                    raise ControlPathError, "Input Path Invalid: " + pth
            
            run_dir = control['Run_dir']
            
            if not os.path.exists(control['Input_dir']):
                pth = os.path.join(run_dir, control['Input_dir']) 
                if os.path.exists(pth):
                    control['Input_dir'] = pth
                else:
                    raise ControlPathError, "Input Path Invalid: " + pth
            
            if not os.path.exists(control['Output_dir']):
                pth = os.path.join(run_dir, control['Output_dir']) 
                if os.path.exists(pth):
                    control['Output_dir'] = pth
                else:
                    raise ControlPathError, "Output Path Invalid: " + pth
                
            if not os.path.exists(control['Control_dir']):
                pth = os.path.join(run_dir, control['Control_dir']) 
                if os.path.exists(pth):
                    control['Control_dir'] = pth
                else:
                    raise ControlPathError, "Control Path Invalid: " + pth
              
            in_path = control['Control_dir']
            for key in [k for k in control if type(control[k]) is str]:
                pth = os.path.join(in_path, control[key])
                #~ print pth
                if not os.path.isfile(pth):
                    continue
                control[key] = self.load({}, pth)
        
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
        for key in self.init_control:
            try:
                p[find_canon_name(key.replace('_Control', ''))] = \
                    self.init_control[key]['porosity']
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
        for key in self.init_control:
            coeff = {}
            try:
                
                for ice in ICE_TYPES:
                    coeff[ice] = self.init_control[key]['ice_slope_' + ice]
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
        for key in self.init_control:
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
        for key in self.init_control:
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
        
        
        
