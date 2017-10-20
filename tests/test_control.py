"""test control file IO
"""
from context import atm
from atm import control

import unittest
import os

class TestIOControlFile_dict_style (unittest.TestCase):
    """test the Control class, uses example barrow uniform
    """
    def setUp(self):
        """setup"""
        
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        dname =  os.path.dirname(dname)
        pth = os.path.join(dname,
                'example_control_files','Barrow_uniform_control'
                )
        self.control = control.Control(pth)
        
            
    def test_object (self):
        """
        """
        self.assertIs(type(self.control.init_control), dict)
        self.assertIs(type(self.control['Initial_Cohort_List'] ), list)
        
            
    def test_get(self):
        """test get items"""
        
        self.assertIs(type(self.control['Initial_Cohort_List'] ), list)
        self.assertIs(type(self.control.Initial_Cohort_List ), list)
        self.assertIs(
            type(self.control['SaturatedBarrens_WT_Y_Control'] ), dict
        )
        self.assertIs(
            type(self.control['SaturatedBarrens_WT_Y_Control']['A1_below'] ),
            float
        )
        self.assertIs(
            type(self.control.SaturatedBarrens_WT_Y_Control['A1_below'] ),
            float
        )
        
        
        
        with self.assertRaises(KeyError):
            self.control['z']
            
        self.control['z'] = 10
        self.assertEqual(10, self.control['z'])
            
    def test_set(self):
        """ test set items """
        with self.assertRaises(control.ControlSetError):
            self.control['Initial_Cohort_List'] = 10
            
        self.control['z'] = 10
        self.assertEqual(10, self.control['z'])
    
        
    

if __name__ == '__main__':
    unittest.main()
