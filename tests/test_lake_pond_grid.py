"""test_ice_grid.py
"""
import unittest
from context import atm
from atm.grids import lake_pond_grid

import os
import numpy as np

class TestLakePondGridClass_random(unittest.TestCase):
    """test the IceGrid class with random ice types set
    """
    def setUp(self):
        """setup class for tests 
        """
        config = lake_pond_grid.config_ex
        
        config['pickle path'] = 'test_pickles'
        try:
            os.makedirs(config['pickle path'])
        except:
            pass
        
        self.lake_pond = lake_pond_grid.LakePondGrid(config)
    
    def tearDown(self):
        """
        """
        try:
            pass
            os.remove(self.lake_pond.pickle_path)
            os.removedirs('test_pickles')
        except:
            pass
        
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (10,10), self.lake_pond.grid_shape )
        self.assertEqual( 1900, self.lake_pond.start_year )
        
        keys = self.lake_pond.grid_name_map.keys() 
        count_keys = [k for k in keys if k.find('_count') != -1]
        self.assertEqual( 12, len(count_keys))
        
        for item in count_keys:
            self.assertEqual( 0, 
                self.lake_pond[item, self.lake_pond.current_year()].flatten()[0]
            )
        
        depth_keys = [k for k in keys if k.find('_depth') != -1]
        for item in depth_keys:
            self.assertEqual( (5,10,10), self.lake_pond[item].shape)
            self.assertEqual('float64', self.lake_pond[item].dtype)
        
        tsg_keys = [k for k in keys if k.find('_time') != -1]
        for item in tsg_keys:
            self.assertEqual( (5,10,10), self.lake_pond[item].shape)
        
        cy = self.lake_pond.current_year()
        for item in lake_pond_grid.config_ex['lake types']:
            self.assertTrue(
                np.logical_and(
                    lake_pond_grid.config_ex['lake depth range'][0] <=\
                        self.lake_pond[item + '_depth', cy ],
                    lake_pond_grid.config_ex['lake depth range'][1] >=\
                        self.lake_pond[item + '_depth', cy ],
                ).all()
            )
            
        for item in lake_pond_grid.config_ex['pond types']:
            self.assertTrue(
                np.logical_and(
                    lake_pond_grid.config_ex['pond depth range'][0] <=\
                        self.lake_pond[item + '_depth', cy ],
                    lake_pond_grid.config_ex['pond depth range'][1] >=\
                        self.lake_pond[item + '_depth',  cy ],
                ).all()
            )
            
        self.assertTrue(
            np.logical_and(
                lake_pond_grid.config_ex['ice depth alpha range'][0] <=\
                    self.lake_pond.ice_depth_constants,
                lake_pond_grid.config_ex['ice depth alpha range'][1] >=\
                    self.lake_pond.ice_depth_constants
            ).all()
        )
            
        self.assertEqual( (5,10,10), self.lake_pond['ice_depth'].shape)
        self.assertEqual( 
            (5,10,10), self.lake_pond['climate_expansion_lakes'].shape
        )
        self.assertEqual(
            (5,10,10), self.lake_pond['climate_expansion_ponds'].shape
        )
     
    def test_current_year (self):
        """ Function doc """
        self.assertEqual(1900, self.lake_pond.current_year())
        self.lake_pond.increment_time_step()
        self.assertEqual(1901, self.lake_pond.current_year())
        
    def test_apply_lake_pond_mask (self):
        """"""
        mask = np.ones(100)
        mask[:50] = 0
        mask = mask == 1
        self.lake_pond.apply_lake_pond_mask('Ponds_WT_Y', mask)
        
        test = np.zeros(100) + .3
        test[:50] = 0
        

        self.assertTrue(
            (test == self.lake_pond['Ponds_WT_Y_depth', 1900].flatten()
        ).all())
        
    def test_increment_time_step (self):
        """ test increment time step, load history"""
        self.assertEqual(1900, self.lake_pond.current_year())
        self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year()] = 0
        self.lake_pond.increment_time_step()
        self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year()] = 1
        self.assertEqual(1901, self.lake_pond.current_year())
        
        self.assertTrue(
            (
                1 == self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year()]
            ).all()
        )
        self.lake_pond.increment_time_step()
        self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year()] = \
            self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year() - 1] + 1
        self.assertTrue(
            (
                2 == self.lake_pond['Ponds_WT_Y_depth', self.lake_pond.current_year()]
            ).all()
        )

        self.assertTrue((0 == self.lake_pond['Ponds_WT_Y_depth', 1900]).all())
        self.assertTrue((1 == self.lake_pond['Ponds_WT_Y_depth', 1901]).all())
        self.assertTrue((2 == self.lake_pond['Ponds_WT_Y_depth', 1902]).all())
            
    def test_count_feature (self):
        cy = self.lake_pond.current_year()
        self.assertEqual(0, self.lake_pond['Ponds_WT_Y_count',cy][0][0])
        self.lake_pond.set_count('Ponds_WT_Y', np.zeros((10,10))+10)
        cy = self.lake_pond.current_year()
        self.assertEqual(10, self.lake_pond['Ponds_WT_Y_count',cy][0][0])
        
        self.lake_pond.increment_time_step()
        self.lake_pond.increment_time_step()
        cy = self.lake_pond.current_year()
        self.lake_pond.set_count('Ponds_WT_Y', np.zeros((10,10))+20)
        self.assertEqual(20, self.lake_pond['Ponds_WT_Y_count',cy][0][0])

        


if __name__ == '__main__':
    unittest.main()
