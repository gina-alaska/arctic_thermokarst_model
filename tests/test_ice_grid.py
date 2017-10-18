"""test_ice_grid.py
"""
import unittest
from context import atm
from atm.grids import ice_grid

import numpy as np

class TestIceGridClass_random(unittest.TestCase):
    """test the IceGrid class with random ice types set
    """
    def setUp(self):
        """setup class for tests 
        """
        
        
        config = {
            'shape': (10,10),
            'cohort ice slopes': 
                {'HCP':{'poor':.25, 'pore':.5, 'wedge':.75, 'massive':1.0},
                 'FCP':{'poor':25, 'pore':5, 'wedge':75, 'massive':100},
                 'CLC':{'poor':1, 'pore':1, 'wedge':2, 'massive':3},
                 'LCP':{'poor':2, 'pore':4, 'wedge':6, 'massive':8},
                 'POND':{'poor':.2, 'pore':.4, 'wedge':.6, 'massive':.8}
                 },
            'init ice': ice_grid.ICE_TYPES,
            
        }
        config['AOI mask'] = \
            np.ones(config['shape']) == np.ones(config['shape'])
        config['AOI mask'][:5] = False
        
        
        self.ice = ice_grid.IceGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ice.shape )
        
    def test_aoi (self):
        """ test if aoi mask works """
        self.assertTrue((self.ice['HCP'][:5] == 0).all())
        self.assertTrue((self.ice['HCP'][5:] != 0).all())

        
 
class TestIceGridClass_uniform(unittest.TestCase):
    """test the IceGrid class with an ice type set"""
    
    def setUp(self):
        """setup class for tests
        """
        
        
        config = {
            'shape': (10,10),
            'cohort ice slopes': 
                {'HCP':{'poor':.25, 'pore':.5, 'wedge':.75, 'massive':1.0},
                 'FCP':{'poor':25, 'pore':5, 'wedge':75, 'massive':100},
                 'CLC':{'poor':1, 'pore':1, 'wedge':2, 'massive':3},
                 'LCP':{'poor':2, 'pore':4, 'wedge':6, 'massive':8},
                 'POND':{'poor':.2, 'pore':.4, 'wedge':.6, 'massive':.8}
                 },
            'init ice': ice_grid.ICE_TYPES[:1],
            
        }
        config['AOI mask'] = \
            np.ones(config['shape']) == np.ones(config['shape'])
        
        self.ice = ice_grid.IceGrid(config)

    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ice.shape )
        self.assertTrue( (ice_grid.ICE_TYPES[0] == self.ice.grid).all() )

    def test__getitem__ (self):
        """ Test get item function """
        self.assertEqual( (10,10), self.ice['HCP'].shape )
        self.assertEqual( np.float64, self.ice['HCP'].dtype.type )
        self.assertEqual( np.string_, self.ice.grid.dtype.type )
  
  
if __name__ == '__main__':
    unittest.main()

