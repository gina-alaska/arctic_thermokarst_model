"""test control file IO
"""
from context import atm
from atm import control

import unittest
import os

from config_example import config_ex

class TestIOControlFile_dict_style (unittest.TestCase):
    """test the Control class, uses example barrow uniform
    """
    def setUp(self):
        """setup"""
        
        # abspath = os.path.abspath(__file__)
        # dname = os.path.dirname(abspath)
        # dname =  os.path.dirname(dname)
        # pth = os.path.join(dname,
        #         'example_control_files','Control_barrow.yaml'
        #         )
        self.control = control.Control(config_ex)
        
            
    def test_object (self):
        """
        """
        self.assertIs(type(self.control['Initial_Area_data'] ), list)
        #~ print self.control['Met_Control']
            
    def test_get(self):
        """test get items"""
        
        self.assertIs(type(self.control['Initial_Area_data'] ), list)
        self.assertIs(
            type(self.control['cohorts']['CLC_WT_Y_Control'] ), 
            dict
        )
        self.assertIs(
            type(self.control[
                'cohorts']['CLC_WT_Y_Control']['Parameters'
            ] ),
            dict
        )
        #~ self.assertIs(
            #~ type(self.control['Cohorts']SaturatedBarrens_WT_Y_Control['A1_below'] ),
            #~ float
        #~ )
        
        
        
        with self.assertRaises(KeyError):
            self.control['z']
            
        self.control['z'] = 10
        self.assertEqual(10, self.control['z'])
            
    def test_set(self):
        """ test set items """
        # with self.assertRaises(control.ControlSetError):
        #     self.control['Initial_Area_data'] = 10
            
        self.control['z'] = 10
        self.assertEqual(10, self.control['z'])
    
        
    

if __name__ == '__main__':
    unittest.main()
