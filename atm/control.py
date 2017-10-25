"""
Control
-------

for manageing control confguration in the ATM

"""
from atm_io import control_file
import os

class ControlKeyError (Exception):
    """Raised if key being set is in control dict"""
    
class ControlPathError (Exception):
    """Raised if control path is invalid"""
    
class ControlSetError (Exception):
    """Raised if control path is invalid"""

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
              
            in_path = control['Input_dir']
            for key in [k for k in control if type(control[k]) is str]:
                pth = os.path.join(in_path, control[key])
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
        if key in self.init_control.keys():
            return self.init_control[key]
        elif key in self.new_control.keys():
            return self.new_control[key]
        else:
            raise KeyError
            
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
            self.new_control[key] = value
        
