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
            'shape': (10,10),
            'cohort list': ['HCP','FCP','CLC','LCP','POND'], ## replace with canon names
            'start year': 1900,
        }
        config['AOI mask'] = \
            np.ones(config['shape']) == np.ones(config['shape'])
        
        self.POI = poi_grid.POIGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.POI.shape )
        self.assertTrue( 
            (np.zeros(self.POI.shape ).flatten() == \
            self.POI.init_grid).all()
        )
        
        
    def tests__getitem__(self):
        """ __getitem__  """
        
        ## add some data
        
        self.POI.grid[0] = self.POI.grid[0] +1
        
        self.POI.add_time_step(False)
        self.POI.add_time_step(True)
        
        self.assertTrue((self.POI[1900] == self.POI[1901]).all())
        self.assertTrue((self.POI[1900] != self.POI[1902]).all())
        
        self.assertEqual( (5, 10,10), self.POI[1900].shape)
        self.assertEqual( (10,10), self.POI[1900, 'LCP'].shape)
        self.assertEqual( (3, 10,10), self.POI['LCP'].shape)
        

        
    def test__setitem__ (self):
        """
        """
        self.POI[1901, 'LCP'] = np.zeros((10, 10)) + .5
        self.POI[1902, 'LCP'] = np.zeros((10, 10)) + .6
        self.POI[1903, 'LCP'] = np.zeros((10, 10)) + 1.6
        self.POI[1904, 'LCP'] = np.zeros((10, 10)) + -1.6
        
        self.assertTrue((self.POI[1901, 'LCP'] == .5).all())
        self.assertTrue((self.POI[1902, 'LCP'] == .6).all())
        self.assertTrue((self.POI[1903, 'LCP'] == 1).all())
        self.assertTrue((self.POI[1904, 'LCP'] == 0).all())
        self.assertFalse((self.POI[1901, 'LCP'] == self.POI[1902, 'LCP']).all())
        
        with self.assertRaises(NotImplementedError):
            self.POI[1901] = ''
            self.POI['LCP'] = ''
            
        with self.assertRaises(KeyError):
            self.POI[1910] =  ''
            self.POI[1805] =  ''
        
        
    def test_add_time_step (self):
        """
        """
        self.POI.add_time_step()
        self.assertTrue((self.POI[1900] == self.POI[ 1901]).all())
        
        self.POI.add_time_step(True)
        self.assertTrue((self.POI[1902] == 0).all())

if __name__ == '__main__':
    unittest.main()
