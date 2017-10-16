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
        """
        
        
        config = {
            'shape': (10,10),
            'cohort list': ['HCP','FCP','CLC','LCP','POND'], ## replace with canon names
            'init ald': (.3,.3),
            'start year': 1900,
        }
        
        config['porosities'] = {k: 1 for k in config['cohort list']}
        config['PL factors'] = {k: 1 for k in config['cohort list']}
        
        self.ALD = ald_grid.ALDGrid(config)
    
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
        """ test other get functions """ 
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
        
    def tests__getitem__(self):
        """ __getitem__  """
        
        
        
        self.ALD.add_time_step(True)
        self.assertTrue((self.ALD['ALD',1900] != self.ALD['ALD', 1901]).all())
        self.assertTrue((self.ALD['PL',1900] != self.ALD['PL', 1901]).all())
        
        self.assertEqual((2, 10, 10), self.ALD['ALD'].shape)
        self.assertEqual((10, 10), self.ALD['ALD',1900].shape)
        
        self.assertEqual(( 5, 10, 10), self.ALD['PL', 1900].shape)
        self.assertEqual(( 10, 10), self.ALD['FCP', 1900].shape)
        
        
        with self.assertRaises(NotImplementedError):
            self.ALD['PL']
        
        with self.assertRaises(KeyError):
            self.ALD['BAD KEY']
            
        with self.assertRaises(KeyError):
            self.ALD[1]
        
        with self.assertRaises(KeyError):
            self.ALD['ADL', 'BAD']
        
        with self.assertRaises(KeyError):
            self.ALD['PL', 'BAD']
            
        with self.assertRaises(KeyError):
            self.ALD['HCP', 'BAD']
        
        with self.assertRaises(KeyError):
            self.ALD[1, 'BAD']
            
        
        
    def test_setters(self):
        """test setters"""
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
            
    def test__setitem__ (self):
        """
        """
        self.ALD['ALD', 1901] = np.ones((10,10))
        self.ALD['PL', 1901] = np.ones((5,10,10))
        
        self.assertTrue((self.ALD['ALD',1901] == 1).all())
        self.assertTrue((self.ALD['PL',1901] == 1).all())
        
        self.ALD['LCP', 1901] = np.zeros((10,10)) + 5
        
        self.assertTrue((self.ALD['LCP', 1901] == 5).all())
        self.assertFalse((self.ALD['PL',1901] == 1).all())
        
        with self.assertRaises(NotImplementedError):
            self.ALD['PL'] = np.zeros((5, 10,10))
        
        with self.assertRaises(NotImplementedError):
            self.ALD['ALD'] = np.zeros((10,10))
            
        with self.assertRaises(KeyError):
            self.ALD[1] = np.zeros((10,10))
        
        with self.assertRaises(KeyError):
            self.ALD['ADL', 'BAD'] = np.zeros((10,10))
        
        with self.assertRaises(KeyError):
            self.ALD['PL', 'BAD'] = np.zeros((10,10))
            
        with self.assertRaises(KeyError):
            self.ALD['HCP', 'BAD'] = np.zeros((10,10))
        
        with self.assertRaises(KeyError):
            self.ALD[1, 'BAD']
        
        
            
    def test_add_time_step (self):
        """
        """
        self.ALD.add_time_step()
        self.assertTrue((self.ALD['ALD',1900] == self.ALD['ALD', 1901]).all())
        self.assertTrue((self.ALD['PL',1900] == self.ALD['PL', 1901]).all())
        
        self.ALD.add_time_step(True)
        self.assertTrue((self.ALD['ALD',1902] == 0).all())
        self.assertTrue((self.ALD['PL',1902] == 0).all())

if __name__ == '__main__':
    unittest.main()
