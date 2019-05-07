"""
Met Grid
--------

Grids for meterological stuff
"""
import os
import numpy as np

from multigrids import TemporalGrid, common

# try:
from atm.tools import stack_rasters
# except ImportError:
#     from ..tools import stack_rasters
    



class MetGridShapeError(Exception):
    """Raised if data shape is not correct"""

MetGridBase = TemporalGrid
        
def load_degree_days(*args, **kwargs):
    """
    """
    # rows, cols, timesteps, data
    degree_days = MetGridBase(*args, **kwargs)
    if len(args) > 1:
        dt = kwargs['data_type'] if 'data_type' in kwargs else 'float32'
        mm = np.memmap(args[3], dtype=dt, mode='r') 
        degree_days.grids = mm.reshape(degree_days.memory_shape)

    return degree_days

class DegreeDayGrids (object):
    """Degree-days grids
    
    Parameters
    ----------
    config: dict or atm.control
        configuration for object
    """
    def __init__ (self, *args, **kwargs):
        """ Class initialiser 
        
        Parameters
        ----------
        args: tuple
            must be (rows, cols, timesteps, fdd_data, tdd_data) or
            (saved_fdd_temporal_grid, saved_tdd_temporal_grid)
        """

        if len(args) == 5:
            rows, cols, timesteps = args[:3]
            self.thawing = load_degree_days(
                rows, cols, timesteps, args[4], **kwargs
            )
            self.freezing = load_degree_days(
                rows, cols, timesteps, args[3], **kwargs
            )
        # elif len(args) == 2:
        else:
            self.thawing = MetGridBase(args[1], **kwargs)
            self.freezing = MetGridBase(args[0], **kwargs)
        
    def save(self, path, filename_start):
        """save the fdd and tdd , in the tempoal_grid output format

        Parameters
        ----------
        path: path
            path to save at
        filename_start: str
            used to create file names, (i.e. 'test' becomes 'test_fdd.*', and
            'test_tdd.*')
        """
        self.freezing.save(os.path.join(path, filename_start + '_fdd.yaml'))
        self.thawing.save(os.path.join(path, filename_start + '_tdd.yaml'))

    def __getitem__ (self, key):
        """get grid for thawing or freezing degree-days
        
        Parameters
        ----------
        key: tuple
            (str, year). str should be freeze, fdd, thaw, tdd, or heating. 
            the year is an int
        
        Raises
        ------
        KeyError
        
        Returns
        -------
        np.array
            thawing or freezing gird for a year
        """
        freeze_or_thaw = key[0]
        year = key[1]
        
        if freeze_or_thaw.lower() in ['freeze', 'fdd']:
            return self.freezing[year]
        elif freeze_or_thaw.lower() in ['thaw', 'tdd', 'heating']:
            return self.thawing[year]
        else:
            raise KeyError, "key did not match tdd of fdd"
        
        
            
    
    


