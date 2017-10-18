"""test_ice_grid.py
"""
import unittest
from context import atm
from atm.grids import grids, terraingrid, ald_grid, poi_grid, ice_grid

import os
import numpy as np

class TestGrids(unittest.TestCase):
    """test the IceGrid class with random ice types set
    """
    def setUp(self):
        """setup class for tests 
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
            ## cohort grid
            'target resolution': (1000,1000),
            'start year': 1900,
            'input data': files,
            
            ## ald & poi
            'cohort list': ['HCP','FCP','CLC','LCP','POND'], ## replace with canon names
            'init ald': (.3,.3),
            
            ## ice
            'cohort ice slopes': 
                {'HCP':{'poor':.25, 'pore':.5, 'wedge':.75, 'massive':1.0},
                 'FCP':{'poor':25, 'pore':5, 'wedge':75, 'massive':100},
                 'CLC':{'poor':1, 'pore':1, 'wedge':2, 'massive':3},
                 'LCP':{'poor':2, 'pore':4, 'wedge':6, 'massive':8},
                 'POND':{'poor':.2, 'pore':.4, 'wedge':.6, 'massive':.8}
                 },
            'init ice': ice_grid.ICE_TYPES,
        }
    
        ## ald & poi & ice
        config['porosities'] = {k: 1 for k in config['cohort list']}
        config['PL factors'] = {k: 1 for k in config['cohort list']}
        #~ config['AOI mask'] = \
            #~ np.ones(config['shape']) == np.ones(config['shape'])
        
        self.grids = grids.ModelGrids(config)
    
    def test_init(self):
        """test init results are correct
        """
        self.assertEqual( (50,67), self.grids.shape )
        self.assertEqual( self.grids.area.shape, self.grids.shape )
        self.assertEqual( self.grids.area.shape, self.grids.shape )
        self.assertEqual( self.grids.area.shape, self.grids.shape )
        self.assertEqual( self.grids.area.shape, self.grids.shape )
        
    def test__getitem__ (self):
        """ test if items """
        self.assertIs(type(self.grids['AREA']), terraingrid.CohortGrid)
        self.assertIs(type(self.grids['ALD']), ald_grid.ALDGrid)
        self.assertIs(type(self.grids['POI']), poi_grid.POIGrid)
        self.assertIs(type(self.grids['ICE']), ice_grid.IceGrid)
        
        with self.assertRaises(KeyError):
            self.grids['abcdef']
        

  
  
if __name__ == '__main__':
    unittest.main()




