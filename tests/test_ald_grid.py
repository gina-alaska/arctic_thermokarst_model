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

    def test_getters(self):
        """ test __getitem__ and other get functions """ 
        flat = self.ALD.get_ald_at_time_step()
        grid = self.ALD.get_ald_at_time_step(flat=False)
        self.assertEqual( (10 * 10,), flat.shape)
        self.assertEqual( (10, 10), grid.shape)
        self.assertTrue((flat.reshape((10,10)) == grid).all())
        self.assertTrue((grid == .3).all())
        
        # add some scratch data
        self.ALD.ald_grid.append(self.ALD.ald_grid[0] + 1)
        self.ALD.ald_grid.append(self.ALD.ald_grid[0] + 2)
        
        flat_all = self.ALD.get_ald()
        grid_all = self.ALD.get_ald(False)
        self.assertEqual( (3, 10 * 10), flat_all.shape)
        self.assertEqual( (3, 10, 10), grid_all.shape) 
        
        self.assertTrue((flat != self.ALD.get_ald_at_time_step(2)).all())
        
    def test_setters(self):
        """"""
         # add some scratch data
        self.ALD.ald_grid.append(np.zeros(10*10))
        self.ALD.ald_grid.append(np.zeros(10*10))
        new_grid = np.ones((10,10))
        
        
        self.ALD.set_ald_at_time_step(1, new_grid)
        self.assertTrue(
            (new_grid == self.ALD.get_ald_at_time_step(1, False)).all()
        )
        
        self.assertTrue(
            (new_grid != self.ALD.get_ald_at_time_step(0, False)).all()
        )
        
        with self.assertRaises(StandardError):
            self.ALD.set_ald_at_time_step(2, np.ones((2,2)))
        
        with self.assertRaises(IndexError):
            self.ALD.set_ald_at_time_step(3, new_grid)

if __name__ == '__main__':
    unittest.main()
