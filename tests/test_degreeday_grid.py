"""tests Met and  Degree Day Grid class
"""
from context import atm
from atm.grids import met_grid

import unittest
import numpy as np
import os

  

class TestMetGridClass(unittest.TestCase):
    """test the POIGrid class
    """
    def setUp(self):
        """setup class for tests
        """
        
        config = {
            'shape': (10,10),
            'start year': 1901,
            'data path': './',
            'pickle path': './'
        }

        
        self.met = met_grid.MetGridBase(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.met.shape )
        self.assertTrue(self.met.history is None)
        self.assertEqual( self.met.met_type, 'base')
        self.assertEqual( self.met.source, 'none')
        
    def test_read_data(self):
        """
        """
        path = os.path.abspath(os.path.dirname(__file__))
        data, source = self.met.read_data(
            os.path.join(path,'example_met.data'),'test'
        )

        self.assertEqual( (10, 100), data.shape )
        self.assertEqual( source,  os.path.join(path,'example_met.data') )
        
class testDDgridCalass(unittest.TestCase):
    """"""
    def setUp(self):
        """setup class for tests
        """
        path = os.path.abspath(os.path.dirname(__file__))
        config = {
            'shape': (10,10),
            'start year': 1901,
            'data path': './',
            'Input_dir': './',
            'pickle path': './',
                
            'Met_Control': {
                'TDD_file': os.path.join(path,'example_met.data'),
                'FDD_file': os.path.join(path,'example_met.data'),
            },
        }

        self.ddg = met_grid.DegreeDayGrids(config)
        
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ddg.shape )
        self.assertTrue( type(self.ddg.freezing) is met_grid.FDDGrid)
        self.assertTrue( type(self.ddg.thawing) is met_grid.TDDGrid)
        self.assertEqual( self.ddg.freezing.met_type, 'Freezing Degree-Days')
        self.assertEqual( self.ddg.thawing.met_type, 'Thawing Degree-Days')


if __name__ == '__main__':
    unittest.main()
