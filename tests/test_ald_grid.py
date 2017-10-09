"""test ald Grid class
"""
from context import atm
from atm import ald_grid

import unittest
import numpy as np

  

class TestALDGridClass(unittest.TestCase):
    """test the ALDGrid class
    """
    def setUp(self):
        """setup class for tests
        
        Make a pickle for faster loading?
        """
        print 'a'
        shape = (10,10)
        cohort_list = ['HCP','FCP','CLC','LCP','POND'] ## replace with canon names
        
        init_ald = (.3,.3)
        self.ALD = ald_grid.ALDGrid(shape, cohort_list, init_ald)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.ALD.shape )
        self.assertTrue( 
            (np.random.uniform(.3,.3, self.ALD.shape ).flatten() == \
            self.ALD.init_ald_grid).all()
        )
        self.assertTrue( 
            (np.random.uniform(.3,.3, self.ALD.shape ).flatten() == \
            self.ALD.init_pl_grid[0]).all()
        )

if __name__ == '__main__':
    unittest.main()
