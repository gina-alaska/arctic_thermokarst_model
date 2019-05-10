"""test POI Grid class
"""
from context import atm
from atm.grids import poi_grid

import unittest
import numpy as np

  

class TestPOIGridClass(unittest.TestCase):
    """test the POIGrid class
    """
    def setUp(self):
        """setup class for tests
        """
        
        
        config = {
            'grid_shape': (10,10),
            'cohorts': ['HCP','FCP','CLC','LCP','POND'], ## replace with canon names
            'model length': 100,
            'initialization year': 1900
        }
        config['AOI mask'] = \
            np.ones(config['grid_shape']) == np.ones(config['grid_shape'])
        
        self.POI = poi_grid.POIGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.POI.grid_shape )
        self.assertTrue( 
            (np.zeros(self.POI.grid_shape ).flatten() == \
            self.POI.grids[0]).all()
        )
        
    
        

        

    

if __name__ == '__main__':
    unittest.main()
