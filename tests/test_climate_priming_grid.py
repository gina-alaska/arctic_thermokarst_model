"""test_ice_grid.py
"""

import unittest
from context import atm
from config_example import config_ex


from atm.grids import climate_priming_grid
from atm import control

from atm.images import raster

import os
import numpy as np
import shutil

class TestClimatePrimingGridClass(unittest.TestCase):
    """test the DrainageGrid class"""
    
    def setUp(self):
        """setup class for tests 
        """
        self.data_dir = './cp_test_data'
        os.makedirs(self.data_dir)


        y0 = (np.arange(100) - 50).reshape([10,10])   
        self.comparison_data = []
        for NN in range(15):
            yN = np.roll(y0, NN*5)
            self.comparison_data.append(yN)
            raster.save_raster(
                os.path.join(self.data_dir, 'year_%04i.tif' % (1901 + NN)), 
                yN, None, None
            )
        self.comparison_data = np.array(self.comparison_data)


        config = config_ex
        config.update({
            'grid_shape': (10,10),
            'model length': 15,
            'climate_priming_input_directory': self.data_dir,
            'initiation_threshold': 25, 
            'termination_threshold': -25, 
            'preload_climate_priming': False, 
        })
        config['AOI mask'] = \
            np.ones(config['grid_shape']) == np.ones(config['grid_shape'])
    

        
        config['Control_dir'] =  './'
        config = control.Control(config)
        self.climate_priming = climate_priming_grid.ClimatePrimingGrid(config)
    
    def tearDown(self):
        shutil.rmtree(self.data_dir)


    def test_load_climate_priming_from_directory(self):
        """Tests loading of climate priming data
        """
        self.climate_priming.load_climate_priming_from_directory(self.data_dir)
        self.assertTrue(
            (self.climate_priming['climate_priming_values'].flatten() == \
                self.comparison_data.flatten()).all()
        )


    def test_load_predisposition_map(self):
        """tests loading of predisposition data
        """
        predisp_file = '.test_predisp.tif'
        ex_predisp = np.zeros([10,10]) + 50
        raster.save_raster(predisp_file, ex_predisp, None, None)

        self.climate_priming.load_predisposition_map(predisp_file)

        predisp_map = self.climate_priming.config['predisposition_map']
        self.assertTrue(
            np.logical_and(0 <=predisp_map, predisp_map  <= 1).all()
        )
        
        with self.assertRaises(IOError):
            self.climate_priming.load_predisposition_map(predisp_file)
        
        self.climate_priming.config['predisposition_map'] = None 
        raster.save_raster(predisp_file, ex_predisp, None, None)

        self.climate_priming.load_predisposition_map(predisp_file)
        
        predisp_map = self.climate_priming.config['predisposition_map']
        self.assertTrue(
            np.logical_and(0 <=predisp_map, predisp_map  <= 1).all()
        )

        os.remove(predisp_file)

    def test_load_stable_climate_averages(self):

        averages = {
            "fdd": np.zeros([10,10]),
            "tdd": np.zeros([10,10]),
            "ewp": np.zeros([10,10]),
            "ewp": np.zeros([10,10]),
            "tdd+1": np.zeros([10,10])
        }

        self.climate_priming.config['preload_climate_priming'] = False
        self.climate_priming.load_stable_climate_averages(averages)

        self.assertIsInstance(
            self.climate_priming.config['stable_climate_averages'], dict
        )

        self.climate_priming.config['preload_climate_priming'] = True

        with self.assertRaises(climate_priming_grid.StaticClimatePrimingError):
            self.climate_priming.load_stable_climate_averages(averages)


    def test_get_active_map(self):
        """
        """
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue((self.climate_priming.get_active_map() == False).all() )
        self.assertTrue((self.climate_priming.get_active_map(1900) == False).all())

        

        cp_variables = {
            "fdd": np.arange(-48,52).reshape([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = np.zeros([10,10])
        comp_val[5:]=1

        self.assertTrue(
            (self.climate_priming.get_active_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_active_map(1901) == comp_val).all()
        )
        




    def test_get_stable_map(self):
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue((self.climate_priming.get_stable_map() == True).all() )
        self.assertTrue((self.climate_priming.get_stable_map(1900) == True).all())

        

        cp_variables = {
            "fdd": np.arange(-48,52).reshape([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = np.zeros([10,10])
        comp_val[:5]=1

        self.assertTrue(
            (self.climate_priming.get_stable_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_stable_map(1901) == comp_val).all()
        )

    def test_get_initiation_map(self):
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue((self.climate_priming.get_initiation_map() == False).all() )
        self.assertTrue((self.climate_priming.get_initiation_map(1900) == False).all())

        

        cp_variables = {
            "fdd": np.arange(-48,52).reshape([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = np.zeros([10,10])
        comp_val[5:]=1

        self.assertTrue(
            (self.climate_priming.get_initiation_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_initiation_map(1901) == comp_val).all()
        )

    def test_get_termination_map(self):
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue((self.climate_priming.get_termination_map() == False).all() )
        self.assertTrue((self.climate_priming.get_termination_map(1900) == False).all())

        

        cp_variables = {
            "fdd": np.arange(-50,50).reshape([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = np.zeros([10,10])
        comp_val[:5]=1

        # print (self.climate_priming['climate_priming_values',1901])

        self.assertTrue(
            (self.climate_priming.get_termination_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_termination_map(1901) == comp_val).all()
        )

    def test_get_categorical_map(self):
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue((self.climate_priming.get_categorical_map() == 0).all() )
        self.assertTrue((self.climate_priming.get_categorical_map(1900) == 0).all())

        

        cp_variables = {
            "fdd": np.arange(-50,50).reshape([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = np.zeros([10,10])
        comp_val[5:]=1
        comp_val[:5]=0
        comp_val[5, :2]=0
        # print(comp_val)
        # print(self.climate_priming.get_categorical_map())

        # print (self.climate_priming['climate_priming_values',1901])

        self.assertTrue(
            (self.climate_priming.get_categorical_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_categorical_map(1901) == comp_val).all()
        )

    def test_get_predisposition_value_map(self):
        averages = {
            "fdd": np.ones([10,10]),
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.load_stable_climate_averages(averages)
        self.assertTrue(np.isnan(self.climate_priming.get_predisposition_value_map()).all() )
        self.assertTrue(np.isnan(self.climate_priming.get_predisposition_value_map(1900)).all())

        

        cp_variables = {
            "fdd": np.ones([10,10]), 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )
        
        comp_val = 0

        # print (self.climate_priming['climate_priming_values',1901])

        self.assertTrue(
            (self.climate_priming.get_predisposition_value_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_predisposition_value_map(1901) == comp_val).all()
        )

        cp_variables = {
            "fdd": np.ones([10,10])+1, 
            "tdd": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "ewp": np.ones([10,10]),
            "tdd+1": np.ones([10,10])
        }

        comp_val = 25

        self.climate_priming.increment_time_step(carry_data_forward=False)
        self.climate_priming.calculate_climate_priming(
            cp_variables=cp_variables
        )

        self.assertTrue(
            (self.climate_priming.get_predisposition_value_map() == comp_val).all()
        )
        self.assertTrue(
            (self.climate_priming.get_predisposition_value_map(1902) == comp_val).all()
        )


    def test_calculate_climate_priming(self):

        # test_get_predisposition_value_map does necessary testing
        self.test_get_predisposition_value_map()

        with self.assertRaises(
                climate_priming_grid.CalculateClimatePrimingError
                ):
            self.climate_priming.increment_time_step(carry_data_forward=False)
            self.climate_priming.calculate_climate_priming(
                {}
            )

       

        
        

if __name__ == '__main__':
    unittest.main()
