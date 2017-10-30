"""
Generate Raster
---------------

tools for generating atm input rasters
"""
from osgeo import ogr


ACP_metadata = {
    'NoData': 0,
    'Coalescent low-center polygons': 2,
    'Low-center polygons': 3,
    'Meadow': 4,
    'Drained slope': 7,
    'Flat-center polygons': 8,
    'High-center polygons': 9,
    'Sandy Barrens': 10,
    'Sand Dunes':  11,
    'Ice': 12,
    'Saline coastal water': 13,
    'Rivers': 16,
    'Urban': 17,
    'Riparian shrub': 18,
    'Ponds': 20,
    'Small Lakes': 21,
    'Medium Lakes': 22,
    'Large Lakes': 23,
}


def from_shapefile(infile, metadata):
    """
    """
    filter_attr = '"GRIDCODE"'
    
    shapefile = ogr.Open(infile)
    layer = shapefile.GetLayer(0)
    extent = layer.GetExtent()
    
    for land_cover in metadata:
        val = metadata[ land_cover ]
        layer.SetAttributeFilter( filter_attr + ' = ' + str(val) )
        cmd = 'gdal_rasterize -a Area '
        cmd += '-tr 25 25 -te '
        cmd += ' '.join([str(i) for i in extent]) + ' '
        cmd += '-a_nodata -9999 '
        cmd += '
        exec(cmd)
        
    
    
    
    
    
