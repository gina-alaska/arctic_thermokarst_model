"""Contains objests to represent internal grid cohort data in ATM
"""
import numpy as np
import gdal


from collections import namedtuple


RASTER_METADATA = namedtuple('RASTER_METADATA', 
    ['transform', 'projection', 
        'nX', 'nY', 'deltaX', 'deltaY', 'originX', 'originY'
    ]
)

def load_raster (filename):
    """
    """
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    (X, deltaX, rotation, Y, rotation, deltaY) = dataset.GetGeoTransform()

    metadata = RASTER_METADATA(
        transform = (X, deltaX, rotation, Y, rotation, deltaY),
        projection = dataset.GetProjection(),  
        nX = dataset.RasterXSize,
        nY = dataset.RasterYSize,
        deltaX = deltaX,
        deltaY = deltaY,
        originX = X,
        originY = Y
    )
    ## assumes one band, also gdal uses one based indexing here 
    data = dataset.GetRasterBand(1).ReadAsArray()
    return data, metadata

### CANON NAMES
CANON_COHROT_NAMES = {
    ('CoalescentLowCenterPolygon_WetlandTundra_Medium',): 'CLC_WT_M',
    ('CoalescentLowCenterPolygon_WetlandTundra_Old',): 'CLC_WT_O',
    ('CoalescentLowCenterPolygon_WetlandTundra_Young',): 'CLC_WT_Y',
    
    ('CoastalWaters_WetlandTundra_Old',): 'CoastalWaters_WT_O',
    
    ('DrainedSlope_WetlandTundra_Medium',): 'DrainedSlope_WT_M',
    ('DrainedSlope_WetlandTundra_Old',): 'DrainedSlope_WT_O',
    ('DrainedSlope_WetlandTundra_Young',): 'DrainedSlope_WT_Y',
    
    ('FlatCenterPolygon_WetlandTundra_Medium',): 'FCP_WT_M',
    ('FlatCenterPolygon_WetlandTundra_Old',): 'FCP_WT_O',
    ('FlatCenterPolygon_WetlandTundra_Young',): 'FCP_WT_Y',
    
    ('HighCenterPolygon_WetlandTundra_Medium',): 'HCP_WT_M',
    ('HighCenterPolygon_WetlandTundra_Old',): 'HCP_WT_O',
    ('HighCenterPolygon_WetlandTundra_Young',): 'HCP_WT_Y',
    
    ('LargeLakes_WetlandTundra_Medium',): 'LargeLakes_WT_M',
    ('LargeLakes_WetlandTundra_Old',): 'LargeLakes_WT_O',
    ('LargeLakes_WetlandTundra_Young',): 'LargeLakes_WT_Y',
    
    ('LowCenterPolygon_WetlandTundra_Medium',): 'LCP_WT_M',
    ('LowCenterPolygon_WetlandTundra_Old',): 'LCP_WT_O',
    ('LowCenterPolygon_WetlandTundra_Young',): 'LCP_WT_Y',
    
    ('Meadow_WetlandTundra_Medium',): 'Meadow_WT_M',
    ('Meadow_WetlandTundra_Old',): 'Meadow_WT_O',
    ('Meadow_WetlandTundra_Young',): 'Meadow_WT_Y',
    
    ('MediumLakes_WetlandTundra_Medium',): 'MediumLakes_WT_M ',
    ('MediumLakes_WetlandTundra_Old',): 'MediumLakes_WT_O',
    ('MediumLakes_WetlandTundra_Young',): 'MediumLakes_WT_Y' ,
    
    ('NoData_WetlandTundra_Old', ): 'NoData_WT_O',
    
    ('Ponds_WetlandTundra_Medium',): 'Ponds_WT_M',
    ('Ponds_WetlandTundra_Old',): 'Ponds_WT_O',
    ('Ponds_WetlandTundra_Young',): 'Ponds_WT_Y',
    
    ('Rivers_WetlandTundra_Medium',): 'Rivers_WT_M',
    ('Rivers_WetlandTundra_Old',): 'Rivers_WT_O',
    ('Rivers_WetlandTundra_Young',): 'Rivers_WT_Y',
    
    ('SandDunes_WetlandTundra_Medium',): 'SandDunes_WT_M',
    ('SandDunes_WetlandTundra_Old',): 'SandDunes_WT_O',
    ('SandDunes_WetlandTundra_Young',): 'SandDunes_WT_Y',
    
    ('SaturatedBarrens_WetlandTundra_Medium',): 'SaturatedBarrens_WT_M',
    ('SaturatedBarrens_WetlandTundra_Old',): 'SaturatedBarrens_WT_O',
    ('SaturatedBarrens_WetlandTundra_Young',): 'SaturatedBarrens_WT_Y',
    
    ('Shrubs_WetlandTundra_Old',): 'Shrubs_WT_O',
    
    ('SmallLakes_WetlandTundra_Medium',): 'SmallLakes_WT_M',
    ('SmallLakes_WetlandTundra_Old',): 'SmallLakes_WT_O',
    ('SmallLakes_WetlandTundra_Young',): 'SmallLakes_WT_Y',
    
    ('Urban_WetlandTundra_Old',): 'Urban_WetlandTundra_Old',
    
    ## barrow NO AGE STUFF ?? ask bob.
    ('Rivers',): 'Rivers',
    ('Ponds',): 'Ponds',
    ('Lakes',): 'Lakes',
    ('FlatCenter',): 'FCP',
    ('Urban',): 'Urban',
    ('Medows',): 'Medows',
    ('CoalescentLowCenter',): 'CLC',
    ('HighCenter',) : 'HCP',
    
    ## Tanana flats
    ('OldBog',): 'TF_OB',
    ('OldFen',): 'TF_OF',
    ('Coniferous_PermafrostPlateau',): 'TF_Con_PP',
    ('Deciduous_PermafrostPlateau',): 'TF_Dec_PP',
    ('ThermokarstLake',): 'TF_TL',
    ('YoungBog',): 'TF_YB',
    ('YoungFen',): 'TF_YF',
    
    ## Yukon Flats
    ('Barren_Yukon',): 'Barren_Yukon',
    ('Bog_Yukon',): 'Bog_Yukon',
    ('DeciduousForest_Yukon',): 'DeciduousForest_Yukon',
    ('DwarfShrub_Yukon',): 'DwarfShrub_Yukon',
    ('EvergreenForest_Yukon',): 'EvergreenForest_Yukon',
    ('Fen_Yukon',): 'Fen_Yukon',
    ('Lake_Yukon',): 'Lake_Yukon',
    ('Pond_Yukon',): 'Pond_Yukon',
    ('River_Yukon',): 'River_Yukon',
    ('ShrubScrub_Yukon',): 'ShrubScrub_Yukon',
    ('Unclassified_Yukon',): 'Unclassified_Yukon',
}

def find_canon_name (name):
    """find canonical name of cohort given an alterate name
    
    Parameters
    ----------
    name: str
        the alternative name
        
    Raises
    ------
    KeyError
        if canon name not found
    
    Returns
    -------
    Str
        Canon name of cohort
    """
    ## is name a canon name
    if name in CANON_COHROT_NAMES.values():
        return name
    
    ## loop to find canon name
    for alt_names in CANON_COHROT_NAMES:
        if name in alt_names:
            return CANON_COHROT_NAMES[alt_names]
    raise KeyError, 'No canon cohort name for exists ' + name 

class TerrainGrid(object):
    """ Concept Class for atm TerrainGrid that represents the data  """
    
    def __init__ (self, input_data = [], target_resoloution = (1000,1000) ):
        """ Class initialiser 
        
        rows = Y
        cols = X
        
        target resoloution (row size m, col size m)
        
        """
        self.start = (0,0) # (X,Y) position of first grid element, keep track in case data is split
        #~ self.shape = (2,5) # (X,Y) shape of data 
        self.input_data = input_data
        
        ## read input
        self.init_data, self.raster_info, self.key_to_index = \
            self.read_layers(target_resoloution)
        
        
        self.shape = (
            abs(int(self.shape[0] *self.resoloution[0] /target_resoloution[0])),
            abs(int(self.shape[1] *self.resoloution[1] /target_resoloution[1])),
        )
        self.resoloution = target_resoloution
        

        self.data = [self.init_data]
        
    def read_layers(self, target_resoloution):
        """
        """
        layers = []
        metadata_dict = {}
        key_to_index = {}
        idx = 0
        for f in self.input_data:
            ## add path here
            path = f
            data, metadata = load_raster (path)
            
            ## set init shape and resoloution
            try:
                if self.shape != (metadata.nY,metadata.nX):
                    raise StandardError, 'Raster Size Mismatch'
            except AttributeError:
                self.shape = (metadata.nY,metadata.nX)
                
            try:
                if self.resoloution != \
                        (abs(metadata.deltaY), abs(metadata.deltaX)):
                    raise StandardError, 'Resoloution Size Mismatch'
            except AttributeError:
                self.resoloution = (abs(metadata.deltaY),abs(metadata.deltaX))
                
            
                 
            
            try:
                name = find_canon_name(f.split('.')[0])
            except KeyError as e:
                print e
                continue
            ## update key to index map, metadata dict, layers, 
            ## and increment index
            key_to_index[name] = idx
            metadata_dict[name] = metadata
            layers.append(self.resize_cells(data, target_resoloution))
            idx += 1
        
        layers = self.normalize_layers(np.array(layers), target_resoloution)
        
        return layers, metadata_dict, key_to_index
        
    def normalize_layers (self, layers, target_resoloution):
        """ 
        """
        total = layers.sum(0)#sum each cell 
        cohorts_required = \
            (float(target_resoloution[0])/(self.resoloution[0])) * \
            (float(target_resoloution[1])/(self.resoloution[1]))

        cohort_check = total / cohorts_required
        adjustment = float(cohorts_required)/total

        check_mask = cohort_check > .5
        new_layers = []
        for layer in layers:
            
            layer_mask = np.logical_and(check_mask,(layer > 0))
            layer[layer_mask] = np.multiply(layer, adjustment, where=layer_mask)[layer_mask]
            
            layer = np.round((layer) / cohorts_required, decimals = 6)
            new_layers.append(layer)
        new_layers = np.array(new_layers)
        ATTM_Total_Fractional_Area = np.round(new_layers.sum(0), decimals = 6 )
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) > 1.0).any():
            print 'mass balence problem 1'
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) < 0.0).any():
            print 'mass balence problem 2'
        return new_layers
        
    def resize_cells (self, data, target_resoloution):
        """"""
        ## check thati is is correct
        if target_resoloution == self.resoloution:
            data[data<=0] = 0
            data[data>0] = 1
            return data.flatten()
        
        resize_num = (
            abs(int(target_resoloution[0]/self.resoloution[0])),
            abs(int(target_resoloution[1]/self.resoloution[1]))
        )
        new_data = []
        ## regroup at neresoloution
        #~ print resize_num
        for i in range(0, int(self.shape[0]), resize_num[0]):
            for j in range(0, int(self.shape[1]), resize_num[1]):
                A = data[i:i+resize_num [0],j:j+resize_num[1]]
                b = A > 0
                new_data.append(len(A[b]))
        
        return new_data
        
        
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True):
        """Get a cohort at a given time step
        
        Note: cohort, would be passed as strings, and converted to index using
        a well defined maping structure (i.e lakes->0, lcp_wt_y -> 1,...)
        
        cohort: int (enentually string)
        time_step: int, (add ability to retrive slice
        flat: bool, keep the data flat, or convert to 2d grid
        """
        cohort = self.key_to_index[cohort]
        
        if flat:
            return self.data[time_step][cohort]
        else: 
            return self.data[time_step][cohort].reshape(
                self.shape[0], self.shape[1])
        
    def get_cohort (self, cohort, flat = True):
        """Get a cohort at all time steps
        
        Note: cohort, would be passed as strings, and converted to index using
        a well defined maping structure (i.e lakes->0, lcp_wt_y -> 1,...)
        
        cohort: int (enentually string)
        flat: bool, keep the data flat, or convert to 2d grid
        """
        cohort = self.key_to_index[cohort]
        if flat:
            return np.array(self.data)[:,cohort]
        else:
            return np.array(self.data)[:,cohort].reshape(len(self.data),
                self.shape[0], self.shape[1])
                
    def get_all_cohorts_at_time_step (self, time_step = -1, flat = True):
        """get all cohort data at a single time step
        """
        if flat:
            return self.data[time_step]
        else:
            return self.data[time_step].reshape(len(self.init_data),
                self.shape[0], self.shape[1])
                
    def check_balance (self, time_step):
        """checks to ensure that no mass was added or removed
        """
        pass
    
    def save (self):
        """various save functions should be created to save, reports, images, 
        or videos
        """
        pass
        
        
def test (files):
    """
    """
    return TerrainGrid(files)
