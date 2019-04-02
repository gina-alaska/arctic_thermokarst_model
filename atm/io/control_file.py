"""
Control File
------------

control file IO
"""

class ControlWriteError (Exception):
    """Raised if there is an error wrtieing a control file"""
    
def read (in_file):
    """reads control file
    
    Parameters
    ----------
    in_file: file descriptor 
        open in 'r' mode
        
    Returns
    -------
    dict
        ditctionary of control values
    """
    text = in_file.read().replace('\r\n','\n').replace('\t', ' ').rstrip()
    control = {}
    non_key_idx = 0

    good_lines = []
    
    for line in text.split('\n'):
        if len(line) == 0:
            continue
        if line.lstrip()[0] == '#':
            continue
        good_lines.append(' '.join(line.split()))

    for line in good_lines:
        try:
            key, value = line.split(' ')
        except:
            key, value = non_key_idx, line
            non_key_idx += 1
        control[key] = value
    return control
    
def write (out_file, values, order = None, save_keys = True):
    """writes control values 
    
    Parameters
    ----------
    out_file: file descriptor 
        open file in write or append mode
    values: dict
        dict of values to write to control file
    order: list (optional)
        order to save values in, defaults to values.keys()
    save_keys: bool, (optional)
        if true (default) key value pairs are saved
    
    Raises
    ------
    ControlWriteError
    """
    if order is None:
        order = values.keys()
        
    if set(order) != set(values.keys()):
        raise ControlWriteError, "order does not match values.keys"
        
    text = ""
    
    for key in order:
        if save_keys:
            text += str(key) + ' ' * 12 + str(values[key]) + '\n'
        else:
            text += str(values[key]) + '\n'

    out_file.write(text)
        
        
