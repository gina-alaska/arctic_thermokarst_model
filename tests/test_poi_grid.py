"""test POI Grid class
"""
from context import atm
from atm.grids import poi_grid
from atm import control

import unittest
import numpy as np
from config_example import config_ex
  

class TestPOIGridClass(unittest.TestCase):
    """test the POIGrid class
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
        self.POI = poi_grid.POIGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.POI.config['grid_shape']  )
        self.assertTrue( 
            (np.zeros(self.POI.config['grid_shape'] ).flatten() == \
            self.POI.grids[0]).all()
        )
        
    
        

        

    

if __name__ == '__main__':
    unittest.main()
