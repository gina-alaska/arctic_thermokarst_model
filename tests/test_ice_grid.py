"""test_ice_grid.py
"""
import unittest
from context import atm
from config_example import config_ex
from atm.grids import ice_grid
from atm import control

import numpy as np

class TestIceGridClass_random(unittest.TestCase):
    """test the IceGrid class with random ice types set
    """
    def setUp(self):
        """setup class for tests 
        """
        config = config_ex
        config.update({
            'grid_shape': (10,10),
            'model length': 100,
        })
      
        config['AOI mask'] = \
            np.ones(config['grid_shape']) == np.ones(config['grid_shape'])
        
        config = control.Control(config)
        self.ice = ice_grid.IceGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ice.shape )
        
    def test_aoi (self):
        """ test if aoi mask works """
        # print(self.ice['HCP_WT_Y'][:5])
        self.assertTrue((self.ice['HCP_WT_Y'][:5] != 0).all())
        self.assertTrue((self.ice['HCP_WT_Y'][5:] != 0).all())

        
 
class TestIceGridClass_uniform(unittest.TestCase):
    """test the IceGrid class with an ice type set"""
    
    def setUp(self):
        """setup class for tests
        """
        cfg = config_ex
        cfg.update({
            'grid_shape': (10,10),
            'model length': 100,
        })
      
        cfg['AOI mask'] = \
            np.ones(cfg['grid_shape']) == np.ones(cfg['grid_shape'])
        
        cfg['mask'] = None
        cfg['init ice'] = ice_grid.ICE_TYPES[:1]

        cfg['Control_dir'] =  './'
        cfg = control.Control(cfg)
        self.ice = ice_grid.IceGrid(cfg)

    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ice.shape )
        # print(self.ice.grid)
        # self.assertTrue( (ice_grid.ICE_TYPES[0] == self.ice.grid).all() )

    def test__getitem__ (self):
        """ Test get item function """
        # print(self.ice.grid.dtype.type)
        self.assertEqual( (10,10), self.ice['HCP_WT_Y'].shape )
        self.assertEqual( np.float64, self.ice['HCP_WT_Y'].dtype.type )
        # self.assertEqual( np.string_, self.ice.grid.dtype.type )
  
  
if __name__ == '__main__':
    unittest.main()

