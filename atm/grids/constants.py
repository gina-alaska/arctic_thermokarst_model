"""
constants
---------

constants used in grid objects
"""
import copy

# index names for rows and columns to make code easier to read/update
#
ROW, Y = 0, 0 ## index for dimensions 
COL, X = 1, 1 ## index for dimensions 

def create_deepcopy(old_dict):
    """create a deep copy of dictionary key by key as python 3 doesn't do this 
    """
    new_dict = {}
    for key in old_dict:
        try:
            new_dict[key] = copy.deepcopy(old_dict[key])
        except TypeError: # the item its self is a dict
            new_dict[key] = create_deepcopy(old_dict[key])
    
    return new_dict
