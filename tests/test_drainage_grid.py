"""test_ice_grid.py
"""

import unittest
from context import atm
from atm.grids import drainage_grid

import os
import numpy as np

class TestDrainageGridClass(unittest.TestCase):
    """test the DrainageGrid class"""
    def setUp(self):
        """setup class for tests 
        """
        config = drainage_grid.config_ex
        
        config['pickle path'] = 'test_pickles'
        try:
            os.makedirs(config['pickle path'])
        except:
            pass
        
        self.drainage = drainage_grid.DrainageGrid(config)
    
    def tearDown(self):
        """
        """
        try:
            pass
            os.remove(self.drainage.pickle_path)
            os.removedirs('test_pickles')
        except:
            pass
            
    def test_init (self):
        """ Function doc """
        self.assertEqual( (10,10), self.drainage.shape )
                
        grid = self.drainage.get_grid()
        grid[grid == 'none'] = 0 
        grid[grid == 'above'] = 1
        grid[grid == 'below'] = 2
        self.assertTrue( 
            grid.astype(int).all() in [0,1,2]
        )
        
        
    def test_get_item (self):
        """ Function doc """
        self.assertEqual( (10*10,), self.drainage.get_grid().shape )
        self.assertEqual( (10,10), self.drainage.get_grid(False).shape )
        
    def test_load_pickle (self):
        """ Function doc """
        self.drainage.write_to_pickle()
        
        new = drainage_grid.DrainageGrid(self.drainage.pickle_path)
        self.assertTrue((new.get_grid() == self.drainage.get_grid()).all())
        
    #~ def test_to_numbers (self):
        #~ """
        #~ """
        #~ nums = self.drainage.as_numbers()
        
        #~ print nums
        
        
    def test_figures (self):
        """ test figure out put
        """
        path = './'
        
        self.drainage.figure(os.path.join(path,'drainage.png'))
        self.drainage.binary(os.path.join(path,'drainage.bin'))
        
        self.assertTrue(os.path.isfile(os.path.join(path,'drainage.png')))
        self.assertTrue(os.path.isfile(os.path.join(path,'drainage.bin')))
        
        os.remove(os.path.join(path,'drainage.png'))
        os.remove(os.path.join(path,'drainage.bin'))
        

if __name__ == '__main__':
    unittest.main()
