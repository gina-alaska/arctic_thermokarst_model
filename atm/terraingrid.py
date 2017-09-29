"""Contains objests to represent internal grid cohort data in ATM
"""
import numpy as np
import gdal


from collections import namedtuple

class MassBalaenceError (Exception):
    """Raised if there is a mass balance problem"""

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

ROW, Y = 0, 0 ## index for dimenisons 
COL, X = 1, 1 ## index for dimenisons 

class TerrainGrid(object):
    """ Concept Class for atm TerrainGrid that represents the data  """
    
   
    
    def __init__ (self, input_data = [], target_resoloution = (1000,1000) ):
        """This class represents model area grid as fractional areas of each
        cohort that make up a grid element. In each grid element all
        fractional cohorts should sum to one.
        
        
        .. note:: Note on grid coordinates
            Origin (Y,X) is top left. rows = Y, cols = X
            Object will store diminsional(resoloution, dimensions) 
            metadata as a tuple (Y val, X val).
            
        Parameters
        ----------
        input_data: list
            list of tiff files to read
        target_resoloution: tuple
            (Y, X) target grid size in (m, m)
            
        Attributes
        ----------
        input_data : list
            list of input files used
        shape : tuple of ints
            Shape of the grid (y,x) (rows,columns)
        resoloution : tuple of ints
            resoloution of grid elements in m (y,x)
        data : array
                This 3d array is the grid data at each time step. 
            The first diminison is the time setp with 0 being the inital data.
            The second dimision is the flat grid for given cohort, mapped using  
            key_to_index. The third dimision is the grid element. Each cohort
            can be reshaped using  shape to get the proper grid
        init_data: np.ndarray 
                The initial data corrected to the target resoloution. Each
            row is one cohort precent grid flattened to a 1d array. The 
            the index to get a given cohort can be looked up in the 
            key_to_index attribute.
        key_to_index : dict
                Maps canon cohort names to the index for that cohort in the 
            data object 
        raster_info : dict of RASTER_METADATA
            Metadata on each of the initial raster files read
        
        
        """
        self.input_data = input_data
        ## read input
        ## rename init_grid??
        self.init_data, self.raster_info, self.key_to_index = \
            self.read_layers(target_resoloution)
        
        ## rename grid_history?
        self.data = [self.init_data]
        
        self.check_mass_balance() ## check mass balance at inital time_step
        
        #get resoloution, andshape of gird data as read in
        original = self.raster_info.values()[0]
        o_shape = (original.nY, original.nX) 
        o_res = (original.deltaY, original.deltaX) 
        self.shape = (
            abs(int(o_shape[ROW] *o_res[ROW] /target_resoloution[ROW])),
            abs(int(o_shape[COL] *o_res[COL] /target_resoloution[COL])),
        )
        self.resoloution = target_resoloution
        
    def read_layers(self, target_resoloution):
        """Read cohort layers from raster files
        
        Parameters
        ----------
        target_resoloution: tuple of ints
            target resoloutin of each grid element (y,x)
            
        Returns
        -------
        Layers : np.ndarray
            2d array of flattend cohort grids, corrected to the proper
        resoloution, and normailzed. First dimision is layer index, which can be 
        found with the keys_to_index dict. The second diminison is gird element 
        index.
        metadata_dict : dict
            metadata for each raster loaded. Keys being canon name of layer
        keys_to_index : dict
            Maps each canon cohort name to the int index used in layer grid 
        """
        layers = []
        metadata_dict = {}
        key_to_index = {}
        idx = 0
        shape, resoloution = None, None
        
        for f in self.input_data:
            ## add path here
            path = f
            data, metadata = load_raster (path)
            
            ## set init shape and resoloution
            ## TODO maybe do this differently 
            if shape is None:
                shape = (metadata.nY,metadata.nX)
            elif shape != (metadata.nY,metadata.nX):
                raise StandardError, 'Raster Size Mismatch'
                
            if resoloution is None:    
                resoloution = (abs(metadata.deltaY),abs(metadata.deltaX))
            elif resoloution != (abs(metadata.deltaY), abs(metadata.deltaX)):
                raise StandardError, 'Resoloution Size Mismatch'
            
            try:
                name = find_canon_name(f.split('.')[0])
            except KeyError as e:
                print e
                continue
            ## update key to index map, metadata dict, layers, 
            ## and increment index
            key_to_index[name] = idx
            metadata_dict[name] = metadata
            layers.append(
                self.resize_grid_elements(data, resoloution, target_resoloution)
            )
            idx += 1
        
        layers = self.normalize_layers(
            np.array(layers), resoloution, target_resoloution
        )
        
        return layers, metadata_dict, key_to_index
       
    ## make a static method?
    def normalize_layers(self, layers, current_resoloution, target_resoloution):
        """Normalize Layers. Ensures that the fractional cohort areas in each 
        grid element sums to one. 
        """
        total = layers.sum(0) #sum fractional cohorts at each grid element
        cohorts_required = \
            (float(target_resoloution[ROW])/(current_resoloution[ROW])) * \
            (float(target_resoloution[COL])/(current_resoloution[COL]))

        cohort_check = total / cohorts_required
        ## the total is zero in non study cells. Fix warning there
        adjustment = float(cohorts_required)/total

        check_mask = cohort_check > .5
        new_layers = []
        for layer in layers:
            
            layer_mask = np.logical_and(check_mask,(layer > 0))
            layer[layer_mask] = np.multiply(
                layer,adjustment, where=layer_mask)[layer_mask]
            
            layer = np.round((layer) / cohorts_required, decimals = 6)
            new_layers.append(layer)
        new_layers = np.array(new_layers)
        return new_layers
        
    
    ## make a static method?
    def resize_grid_elements (self, 
        layer, current_resoloution, target_resoloution):
        """resize cells to target resoloution
        
        Parameters
        ----------
        layer : np.ndarray
            2d raster data
        current_resoloution: tuple of ints
            current resoloutin of each grid element (y,x)
        target_resoloution: tuple of ints
            target resoloutin of each grid element (y,x)
            
        Returns 
        -------
        np.ndarray
            flatened representation of resized layer
        """
        ## check that this is correct
        if target_resoloution == current_resoloution:
            layer[layer<=0] = 0
            layer[layer>0] = 1
            return layer.flatten()
        
        resize_num = (
            abs(int(target_resoloution[ROW]/current_resoloution[ROW])),
            abs(int(target_resoloution[COL]/current_resoloution[COL]))
        )
        resized_layer = []
        
        shape = layer.shape
        
        ## regroup at new resoloution
        for row in range(0, int(shape[ROW]), resize_num[ROW]):
            for col in range(0, int(shape[COL]), resize_num[COL]):
                A = layer[row : row+resize_num [ROW], col:col + resize_num[COL]]
                b = A > 0
                resized_layer.append(len(A[b]))
        
        return np.array(resized_layer)
        
        
    def get_cohort_at_time_step (self, cohort, time_step = -1, flat = True):
        """Get a cohort at a given time step
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        time_step: int, defaults -1
            time step to retrive, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with corret dimisions
            
        Returns
        -------
        np.array
            The cohorts fractional area grid at a given time step. 
        """
        cohort = self.key_to_index[cohort]
        
        if flat:
            return self.data[time_step][cohort]
        else: 
            return self.data[time_step][cohort].reshape(
                self.shape[ROW], self.shape[COL]
            )
    
    ## NEED TO TEST
    def get_cohort (self, cohort, flat = True):
        """Get a cohort at all time steps
        
        Parameters
        ----------
        cohort: str
            canon cohort name
        flat: bool
            keep the data flat, or convert to 2d grid with corret dimisions
            
        Returns
        -------
        np.array
            The cohorts fractional area grid at all time steps. 
        """
        cohort = self.key_to_index[cohort]
        if flat:
            return np.array(self.data)[:,cohort]
        else:
            return np.array(self.data)[:,cohort].reshape(len(self.data),
                self.shape[0], self.shape[1])
                
    def get_all_cohorts_at_time_step (self, time_step = -1, flat = True):
        """Get all cohorts at a given time step
        
        Parameters
        ----------
        time_step: int, defaults -1
            time step to retrive, default is last time step
        flat: bool
            keep the data flat, or convert to 2d grid with corret dimisions
            
        Returns
        -------
        np.array
            all cohorts fractional area grids at a given time step in a 2d 
        array. 
        """
        if flat:
            return self.data[time_step]
        else:
            return self.data[time_step].reshape(len(self.init_data),
                self.shape[0], self.shape[1])
                
    def check_mass_balance (self, time_step=-1):
        """retruns true if mass balance is preserved. Raises an exception, 
        otherwise
        
        Parameters 
        ----------
        time_step : int, defaults -1
            time step to test
        
        Raises
        ------
        MassBalaenceError
            if any grid elemnt at time_step is <0 or >1
        
        Returns
        -------
        Bool
            True if no mass balence problem found.
        """
        grid = self.data[time_step]
        
        ATTM_Total_Fractional_Area = np.round(grid.sum(0), decimals = 6 )
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) > 1.0).any():
            raise MassBalaenceError, 'mass balence problem 1'
            ## write a check to locate mass balance error
        if (np.round(ATTM_Total_Fractional_Area, decimals = 4) < 0.0).any():
            raise MassBalaenceError, 'mass balence problem 2'
            
        return True
    
    def save (self):
        """various save functions should be created to save, reports, images, 
        or videos
        """
        pass
        
        
def test (files):
    """
    """
    return TerrainGrid(files)
