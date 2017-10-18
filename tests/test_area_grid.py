"""
testing code for area_grid.py
-------------------------------
"""
from context import atm
from atm.grids import area_grid
from atm import io

import numpy as np
import unittest
import os 
import tarfile

class TestTerrainGridFunctions(unittest.TestCase):
    pass

class TestAreaGridClass(unittest.TestCase):
    """test the AreaGrid class
    """

    def setUp(self):
        """setup class for tests
        
        Make a pickle for faster loading?
        """
        path = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(path,'example_data')
        
        if not os.path.exists(data_dir):
            with tarfile.open(os.path.join(path, 'example_data.tar')) as tar:
                tar.extractall(path)
            for f in [f for f in os.listdir( data_dir ) if f.find('._')!=-1 ]:
                os.remove(os.path.join(data_dir, f))
            
            
        files = [ os.path.join(data_dir, f) for f in os.listdir( data_dir )] 
        #~ print files
        config = {
            'target resolution': (1000,1000),
            'start year': 1900,
            'input data': files,
        }
    
        self.tg_class =  area_grid.AreaGrid(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (1000,1000), self.tg_class.resolution )
        self.assertEqual( ( 50, 67 ), self.tg_class.shape )
        self.assertEqual( 1900, self.tg_class.start_year )
        self.assertIs( np.ndarray, type(self.tg_class.init_grid) )
        self.assertEqual( (43, 50 * 67 ), self.tg_class.init_grid.shape )
        self.assertEqual( 1, len(self.tg_class.grid) )
        self.assertEqual( (1, 43, 50 * 67 ), 
            np.array(self.tg_class.grid).shape)
       
    def test_read_layers (self):
        """test read_layers
        """
        res_target = self.tg_class.resolution
        data, meta, key_map = self.tg_class.read_layers(res_target)
        self.assertIs( np.ndarray, type(data) )
        self.assertEqual (data.shape[0],
            len([k for k in key_map.keys() if k.find('--') == -1])
        )
        
    def test_resize_grid_elements (self):
        """test resize
        """
        path = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(path,'example_data')
        files = [ os.path.join(data_dir, f) for f in os.listdir( data_dir )] 
        raster, metadata = io.raster.load_raster(files[0])
        
        ## test resize 
        res_0 = (abs(metadata.deltaY), abs(metadata.deltaX))
        res_1 = self.tg_class.resolution
        resized = self.tg_class.resize_grid_elements(raster, res_0, res_1) 
        self.assertEqual(resized.shape, self.tg_class[1900][0].flatten().shape)
        
        ## test resize to same size
        resized = self.tg_class.resize_grid_elements(raster, res_0, res_0) 
        self.assertEqual(resized.shape, raster.flatten().shape)
     
    @unittest.skip('tested elsewhere')   
    def test_normalize_layers (self):
        """tested elsewhere """
        ## don't really know how to test this, if test_init, 
        ## and test_read_layers are passing, it should be good. maybe 
        ## refactor read_layers to not use this
        pass
    
    def test_check_mass_balance_error_gt1 (self):
        """test failure if a grid elements sum is greater > 1
        """
        self.tg_class.grid[-1][0] = 1000
        self.assertRaises(
            area_grid.MassBalanceError, 
            self.tg_class.check_mass_balance 
        )
        pass
        
    def test_check_mass_balance_error_lt0 (self):
        """test failure if a grid elements sum is greater < 0
        """
        self.tg_class.grid[-1][0] = -1000
        self.assertRaises(
            area_grid.MassBalanceError, 
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
        num_cohorts = [c for c in self.tg_class.key_to_index \
            if c.find('--') == -1]
        self.assertEqual((len(num_cohorts), 50, 67), _1900.shape)
        
        
        # tuple mode
        lcp = self.tg_class[1900,'LCP_WT_O']
        hcp = self.tg_class[1900,'HCP_WT_O']
        ## type
        self.assertIs(np.ndarray, type(lcp))
        ## shape
        self.assertEqual(self.tg_class.shape, lcp.shape)
        ## gets different things
        self.assertFalse((lcp == hcp).all())
        
    def test_getter_flat (self):
        """test flat == True feature of get_...

        flat == False tested in test_getitem
        """
        self.assertEqual( 1, 
            len(self.tg_class.get_cohort_at_time_step('LCP_WT_O', 0).shape)
        )
        self.assertIs( np.ndarray, 
            type (self.tg_class.get_cohort_at_time_step('LCP_WT_O', 0))
        )
        
        self.assertEqual( (43, 50*67),
            self.tg_class.get_all_cohorts_at_time_step(0).shape
        )
        self.assertIs( np.ndarray, 
           type( self.tg_class.get_all_cohorts_at_time_step(0) )
        )
        
        self.assertEqual( (1, 50*67),
            self.tg_class.get_cohort('LCP_WT_O').shape
        )
        self.assertIs( np.ndarray, 
            type(self.tg_class.get_cohort('LCP_WT_O'))
        )
        
    def test_setitem (self):
        """ Function doc """
        cohort_ex = np.zeros([50,67])
        all_cohort_ex = np.zeros([43,50,67])
        
        with self.assertRaises(StandardError):
            self.tg_class.set_cohort_at_time_step(
                'LCP_WT_O', 0, cohort_ex.flatten()
            )
        
        self.tg_class[1900, 'LCP_WT_O--0'] = cohort_ex
        self.assertTrue( (cohort_ex == self.tg_class[1900, 'LCP_WT_O']).all() )
        
        self.tg_class[1900] = all_cohort_ex
        
        self.assertTrue( (all_cohort_ex == self.tg_class[1900]).all() )
        
        cohort_ex += 1
        all_cohort_ex += 1
        
        self.tg_class[1901, 'LCP_WT_O--0'] = cohort_ex
        self.assertTrue( (cohort_ex == self.tg_class[1901, 'LCP_WT_O']).all() )
        
        self.tg_class[1901] = all_cohort_ex
        
        self.assertTrue( (all_cohort_ex == self.tg_class[1901]).all() )
        
        with self.assertRaises(NotImplementedError):
            self.tg_class.__setitem__('LCP_WT_O', '')
        with self.assertRaises(KeyError):
            self.tg_class.__setitem__(1905, '')
            self.tg_class.__setitem__(1805, '')
        #~ self.assertRaises(KeyError, self.tg_class.__setitem__(1805, ''))
        
    def test_append_grid_year (self):
        """test_append_grid_year
        """ 
        self.tg_class.append_grid_year()
        self.tg_class.append_grid_year(True)
        self.assertTrue((self.tg_class.grid[0] == self.tg_class.grid[1]).all())
        self.assertTrue((self.tg_class.grid[-1] == 0).all())
       
    @unittest.skip('Tested with test_setitem')
    def test_setters (self):
        """Tested with test_setitem
        """
        pass
        
    def test_save (self):
        """test save functions
        """
        path = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(path, 'example_data')
        filename = self.tg_class.save_cohort_at_time_step(
            'LCP_WT_O', data_dir, bin_only = False
        )
        
        f1 = os.path.join(data_dir, filename + '.png')
        f2 = os.path.join(data_dir, filename + '.bin')
        self.assertTrue(os.path.exists(f1))
        self.assertTrue(os.path.exists(f2))
        
        os.remove(f1)
        os.remove(f2)
        
        
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()
