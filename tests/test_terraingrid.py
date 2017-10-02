from context import atm
#~ import context
from atm import terraingrid

import numpy as np
import unittest
import os 


class TestTerrainGridFunctions(unittest.TestCase):
    pass

class TestCohortGridClass(unittest.TestCase):

    def setUp(self):
        """setup class for tests
        
        Make a pickle for faster loading?
        """
        path = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(path,'example_data')
        files = [ os.path.join(data_dir, f) for f in os.listdir( data_dir )] 
        
        config = {
            'target resoloution': (1000,1000),
            'start year': 1900,
            'input data': files,
        }
    
        self.tg_class =  terraingrid.CohortGrid(config)
    
    def test_check_mass_balance_error_gt1 (self):
        """test failure if a grid elements sum is greater > 1
        """
        self.tg_class.grid[-1][0] = 1000
        self.assertRaises(
            terraingrid.MassBalaenceError, 
            self.tg_class.check_mass_balance 
        )
        pass
        
    def test_check_mass_balance_error_lt0 (self):
        """test failure if a grid elements sum is greater < 0
        """
        self.tg_class.grid[-1][0] = -1000
        self.assertRaises(
            terraingrid.MassBalaenceError, 
            self.tg_class.check_mass_balance 
        )
        pass
        
    def test_check_mass_balance_pass (self):
        """test check_mass_balance no failure
        """
        self.assertTrue(self.tg_class.check_mass_balance())
      
    def test_shape(self):
        """test shape
        for test data should be (50, 67)
        """
        self.assertEqual((50,67), self.tg_class.shape)
                
    def test_getitem (self):
        """
        """
        # str mode
        lcp = self.tg_class['LCP_WT_O']
        hcp = self.tg_class['HCP_WT_O']
        
        ## type
        self.assertIs(np.ndarray, type(lcp))
        ## shape
        self.assertEqual((1, 50, 67), lcp.shape)
        self.assertEqual(self.tg_class.shape, lcp[0].shape)
        ## gets different things
        self.assertFalse((lcp == hcp).all())
        
        # int mode
        _1900 = self.tg_class[1900]
        
        ## type
        self.assertIs(np.ndarray, type(_1900))
        
        ## shape
        self.assertEqual((len(self.tg_class.key_to_index), 50, 67), _1900.shape)
        
        
        # tuple mode
        lcp =self.tg_class[1900,'LCP_WT_O']
        hcp = self.tg_class[1900,'HCP_WT_O']
        ## type
        self.assertIs(np.ndarray, type(lcp))
        ## shape
        self.assertEqual(self.tg_class.shape, lcp.shape)
        ## gets different things
        self.assertFalse((lcp == hcp).all())
        

if __name__ == '__main__':
    unittest.main()
