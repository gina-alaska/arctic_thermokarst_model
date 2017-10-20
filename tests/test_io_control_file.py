"""test control file IO
"""
from context import atm
from atm.io import control_file

import unittest
from StringIO import StringIO


class TestIOControlFile_dict_style (unittest.TestCase):
    """test the POIGrid class
    """
    def setUp(self):
        """setup"""
        
        text = """
        ## exaple data
        first        1
        second       w
        third        7.7
        """
        
        self.data = {
            'first':'1',
            'second':'w',
            'third':'7.7'
        }
        
        self.in_fd = StringIO(text)
        
    def test_read(self):
        """ test read """
        control = control_file.read(self.in_fd)
        self.assertEqual(self.data, control)
        
    def test_write(self):
        """test write"""
        out_fd =  StringIO()
        with self.assertRaises(control_file.ControlWriteError):
            control_file.write(out_fd, self.data, order = [])
        out_fd.close()
        
        out_fd =  StringIO()
        control_file.write(out_fd, self.data)
        copy = control_file.read(StringIO(out_fd.getvalue()))
        self.assertEqual(self.data, copy)
        out_fd.close()
        
        out_fd =  StringIO()
        control_file.write(out_fd, self.data, order = self.data.keys())
        copy = control_file.read(StringIO(out_fd.getvalue()))
        self.assertEqual(self.data, copy)
        out_fd.close()

        

class TestIOControlFile_list_style (unittest.TestCase):
    """test the POIGrid class
    """
    def setUp(self):
        """setup"""
        
        text = """
        ## exaple data
        first
        second
        third
        """
        
        self.data = {
            0:'first',
            1:'second',
            2:'third',
        }
        
        self.in_fd = StringIO(text)
        
    def test_read(self):
        """ test read """
        control = control_file.read(self.in_fd)
        self.assertEqual(self.data, control)
        
    def test_write(self):
        """test write"""
        out_fd = StringIO()
        with self.assertRaises(control_file.ControlWriteError):
            control_file.write(out_fd, self.data, order = [], save_keys = False)
        out_fd.close()
        
        out_fd = StringIO()
        control_file.write(out_fd, self.data, save_keys = False)
        copy = control_file.read(StringIO(out_fd.getvalue()))
        self.assertEqual(self.data, copy)
        out_fd.close()
        
        out_fd = StringIO()
        control_file.write(
            out_fd, self.data, order = self.data.keys(), save_keys = False
        )
        copy = control_file.read(StringIO(out_fd.getvalue()))
        self.assertEqual(self.data, copy)
        out_fd.close()

if __name__ == '__main__':
    unittest.main()
