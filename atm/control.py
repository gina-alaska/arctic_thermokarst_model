"""
Control
-------

for manageing control confguration in the ATM

"""
# from atm.io import control_file
import os

try: 
    from .cohorts import find_canon_name
except(ImportError):
    from cohorts import find_canon_name

try:
    from .grids.ice_grid import ICE_TYPES
except(ImportError):
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


class ControlInitFailure (Exception):
    """Raised if control initialization fails"""

class Control(dict):
    """ Class doc """

    def __init__(self, arg, **kwargs):
        """Function Docs 
        Parameters
        ----------
        Returns
        -------
        """
        optional = {
            "logger": None,
        }
        optional.update(kwargs)

        self.logger = optional['logger']

        if type(arg) is str:
            with open(arg,'r') as in_file:
                arg = yaml.load(in_file, Loader=yaml.Loader)
        elif not type(arg) is dict:
            raise ControlInitFailure(
                "The main argument was not a file name, or a dictionary"
            )
        super(Control , self).__init__(arg, **kwargs)
        
        self.update(self.expand_sub_configs(self))
        self['cohorts'].update(self.expand_sub_configs(self['cohorts']))
        
        self['Initial_Area_data'] = [
            os.path.join(
                self['Input_dir'],tif
            ) 
            for tif in self['Initial_Area_data']
        ]
        
        self.find_model_length()

        try:
            self['start year']
        except KeyError:
            self['start year'] = self['initialization_year'] + 1
            if self.logger:
                self.logger.add('Set start year to initialization_year + 1')

        self.init_keys = self.keys()
        self.is_key = lambda k: k in self.keys()
        self.is_added_key = lambda k: (True if self.is_key(k) else None) \
            and not k in self.init_keys

        ## Fast Access Special Tags
        self.fast_table = {
            "_FAST_get_pl_factors": self.get_protective_layer_factors,
            "_FAST_get_cohorts": self.get_cohorts,
            "_FAST_get_ice_slope_coefficients": self.get_ice_slope_coefficients,
            "_FAST_get_pond_types": self.get_pond_types,
            "_FAST_get_lake_types": self.get_lake_types,
            "_FAST_get_pond_types": self.get_pond_types,
            "_FAST_get_pond_depth_range": self.get_pond_depth_range,
            "_FAST_get_lake_depth_range": self.get_lake_depth_range,
            "_FAST_get_ice_depth_alpha_range": self.get_ice_depth_alpha_range,
            "_FAST_get_climate_block_range": self.get_climate_block_size_range,
            "_FAST_get_get_porosities": self.get_porosities,
        }

    def __getitem__ (self, key):
        """
        """
        
        

        if "_FAST_" == key[:6]:
            return self.fast_table[key]()

        return super(Control , self).__getitem__(key)
    
    def __setitem__ (self, key, value):
        """
        """
        if "_FAST_" == key[:6]:
            raise KeyError("'_FAST_' keys are reserved, and read only")

        super(Control , self).__setitem__(key, value)

    def expand_sub_configs (self, to_expand):
        """if any dict key retruns a yaml file try to open it and expand the  
        config dict
        Parameters
        ----------
        Returns
        -------
        """
        
        control_dir = self['Control_dir']
        for key in to_expand.keys():
            val = to_expand[key]
            if type(val) is str and val.lower()[-4:] in ['yaml', '.yml']:
                
                fn = to_expand[key]

                # is it in the control_dir?
                if os.path.exists(os.path.join(control_dir, fn)):
                    in_file = open(os.path.join(control_dir, fn),'r')
                # is in cwd
                elif os.path.exists(os.path.join(fn)):
                    in_file = open(os.path.join(fn),'r')
                else:
                    if self.logger:
                        msg = (
                            "File: " + fn + " could not be found in "
                            "Control_dir, or current working directory"
                        )
                        self.logger.add(msg, "error", __file__, __name__ )
                    continue # FILE DNE
                    
                to_expand[key] = yaml.load(in_file, Loader=yaml.Loader)
                try:
                    to_expand[key].update(
                        self.expand_sub_configs(to_expand[key])
                    )
                except AttributeError as e:
                    pass
                
        return to_expand

    def find_model_length(self):
        """Function Docs 
        Parameters
        ----------
        Returns
        -------
        """
        try: 
            self['model length']
        except KeyError:
            self['model length'] = 'auto'


        if self['model length'] == 'auto':
            ## add other places where 'auto' should occuer like "no key"
            ## read FDD length. read TDD length, take minimum
            if self.logger:
                self.logger.add(
                    "model length not provided, attempting to calculate",
                    in_file= __file__
                    )
            met = self['Met_Control']
            files = [met['FDD_file'], met['TDD_file']]
            min_len = 1000000000  # really big
            data_limiting_file = 'Default Max'
            d_dir = self['Input_dir']
            for file in files:
                m_old = min_len
                try:
                    with open(os.path.join(d_dir,file), 'r') as fd:
                        met_cfg = yaml.load(fd, Loader=yaml.Loader)
                        min_len = min(met_cfg['num_timesteps'], min_len)
                except (IOError, TypeError):
                    if self.logger:
                        self.logger.add(
                            "Could not load a file: " + file,   
                            in_file= __file__, at = __name__
                        )
                        
                if m_old != min_len:
                    data_limiting_file = file
            
            self['model length'] = min_len
            if self.logger:
                self.logger.add(
                    "model length is determined to be " + str(min_len) +\
                    " because of num_timesteps in " + data_limiting_file,
                    in_file= __file__
                    )

    #     def get_target_resoloution (self):
#         """Get model target resoloution
        
#         Returns
#         -------
#         tuple, 
#             (y_resoloution, x_resoloution)
#         """
#         return (self.Y_model_resolution, self.X_model_resolution)
   
#     def get_initial_ald (self):
#         """Get init ald range
        
#         Returns
#         -------
#         tuple, 
#             (lower bound, upper bound)
#         """
#         return (self.Terrestrial_Control['ALD_Distribution_Lower_Bound'],
#                 self.Terrestrial_Control['ALD_Distribution_Upper_Bound'])
                
    def get_protective_layer_factors (self):
        """Gets protecetive layer factors
        
        Returns
        -------
        dict:
            dict of protecetive layer factors
        """
        keys = [
            key for key in self['Terrestrial_Control'] if key.find('PLF') != -1
        ]
        
        return {
            find_canon_name(key.replace('_PLF','')): 
                self['Terrestrial_Control'][key] for key in keys
        }
    
    def get_cohorts(self):
        """Return a list of cohort names
        
        Retruns
        -------
        list
            list of cannon cohort names
        """
        return [c.replace('_Control', '') for c in self['cohorts']]

    def get_ice_slope_coefficients (self):
        """Gets Ice slope coefficients for each cohort each type of ice 
        
        Returns
        -------
        Dict
        """
        cohorts = {}
        for key in self.get_cohorts():
            coeff = {}
            try:
                for ice in ICE_TYPES:
                    # print self['cohorts'][key+'_Control']
                    coeff[ice] = \
                        self['cohorts'][key+'_Control']['ice_slope_' + ice]
                cohorts[key] = coeff
            except TypeError:
                pass
            except KeyError:
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
        for key in self.get_cohorts():
            if key.lower() == 'lake_pond_control':
                continue
            name = key # + '_Control'
            if name.lower().find('pond') != -1:
                cohorts.append(name)
        return cohorts
        
    def get_lake_types (self):
        """gets lake types
        
        Returns
        -------
        list:
            list of all canon cohort names used with 'lake' present
        """
        cohorts = []
        for key in self.get_cohorts():
            if key.lower() == 'lake_pond_control':
                continue
            name = key #+ '_Control'
            if name.lower().find('lake') != -1:
                cohorts.append(name)
        return cohorts
        
    def get_pond_depth_range(self):
        """gets pond depth range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        #~ print self['Lake_Pond_Control']
        if self['Lake_Pond_Control']['Pond_Distribution'].lower() == 'uniform':
            return (
                self['Lake_Pond_Control']['Uniform_Pond_Depth'], 
                self['Lake_Pond_Control']['Uniform_Pond_Depth']
            )
        elif self['Lake_Pond_Control']['Pond_Distribution'].lower() == 'random':
            return (
                self['Lake_Pond_Control']['Lower_Pond_Depth'], 
                self['Lake_Pond_Control']['Upper_Pond_Depth']
            )
        else:
            raise ControlInvalidRequest("cannot get pond depth range")
            
    def get_lake_depth_range(self):
        """gets lake depth range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        if self['Lake_Pond_Control']['Lake_Distribution'].lower() == 'uniform':
            return (
                self['Lake_Pond_Control']['Uniform_Lake_Depth'], 
                self['Lake_Pond_Control']['Uniform_Lake_Depth']
            )
        elif self['Lake_Pond_Control']['Lake_Distribution'].lower() == 'random':
            return (
                self['Lake_Pond_Control']['Lower_Lake_Depth'], 
                self['Lake_Pond_Control']['Upper_Lake_Depth']
            )
        else:
            raise ControlInvalidRequest("cannot get lake depth range")

    def get_ice_depth_alpha_range(self):
        """gets ice depth coefficient range
        
        Returns
        -------
        tuple: (min,max)
            range, if the range is specified as uniform, sets min == max
        """
        if self['Lake_Pond_Control']['ice_thickness_distribution'].lower() ==\
            'uniform':
            return (
                self['Lake_Pond_Control']['ice_thickness_uniform_alpha'], 
                self['Lake_Pond_Control']['ice_thickness_uniform_alpha']
            )
        elif self['Lake_Pond_Control']['ice_thickness_distribution'].lower() ==\
            'random':
            return (
                self['Lake_Pond_Control']['Lower_ice_thickness_alpha'], 
                self['Lake_Pond_Control']['Upper_ice_thickness_alpha']
            )
        else:
            raise ControlInvalidRequest("cannot get ice depth alpha range")

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

    def get_porosities (self):
        """Gets porosities
        
        Returns
        -------
        List:
            dict of porosities
        """
        p = {}
        for key in self.get_cohorts():
            try:
                p[key] = self['cohorts'][key + '_Control']['porosity']
            except TypeError:
                pass
            except KeyError:
                pass
        return p
        