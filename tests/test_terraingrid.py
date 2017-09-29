from context import atm
#~ import context
from atm import terraingrid


import unittest
import os 


class TestTerrainGridFunctions(unittest.TestCase):
    pass

class TestTerrainGridClass(unittest.TestCase):

    def setUp(self):
        """setup class for tests"""
        path = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(path,'example_data')
        files = [ os.path.join(data_dir, f) for f in os.listdir( data_dir )] 
        self.tg_class =  terraingrid.TerrainGrid(files)
    
    def test_check_mass_balance_error_gt1 (self):
        """test failure if a grid elements sum is greater > 1
        """
        self.tg_class.data[-1][0] = 1000
        self.assertRaises(
            terraingrid.MassBalaenceError, 
            self.tg_class.check_mass_balance 
        )
        pass
        
    def test_check_mass_balance_error_lt0 (self):
        """test failure if a grid elements sum is greater < 0
        """
        self.tg_class.data[-1][0] = -1000
        self.assertRaises(
            terraingrid.MassBalaenceError, 
            self.tg_class.check_mass_balance 
        )
        pass
        
    def test_check_mass_balance_pass (self):
        """test check_mass_balance no failure
        """
        self.assertEqual(True, self.tg_class.check_mass_balance())
        

if __name__ == '__main__':
    unittest.main()
