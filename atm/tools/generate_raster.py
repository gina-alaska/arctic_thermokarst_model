"""
Generate Raster
---------------

tools for generating atm input rasters
"""
from osgeo import ogr, gdal


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


def from_shapefile(in_shape, out_raster, metadata):
    """
    
    adatabed from 
        https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#convert-an-ogr-file-to-a-raster
        and 
        http://ceholden.github.io/open-geo-tutorial/python/chapter_4_vector.html#Pure-Python-version----gdal.RasterizeLayer
    """
    # important coefficients
    filter_attr = '"GRIDCODE"'
    pixel_size = 25
    NoData_value = -9999
    rasterize_attr = 'Shape_Area'

    # Open the data source and read in the extent
    source = ogr.Open(in_shape)
    layer = source.GetLayer(0)
    x_min, x_max, y_min, y_max = layer.GetExtent()

    # Create Raster
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    dest = gdal.GetDriverByName('GTiff').Create(out_raster, x_res, y_res, 1, gdal.GDT_Byte)
    dest.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    
    
    
    band_num = 1
    for attr in metadata:
        val = metadata[attr]
        layer.SetAttributeFilter( filter_attr + ' = ' + str(val) )
        band = dest.GetRasterBand(band_num)
        band.SetNoDataValue(NoData_value)
        gdal.RasterizeLayer(
            dest, 
            [band_num], 
            layer, 
            None, 
            None, 
            [0], 
            ['ATTRIBUTE=Shape_Area']
        )
        

## simple test, need to be moved.
#~ import sys
#~ from_shapefile(sys.argv[1], 'rasterize_test.tif',ACP_metadata)
    
        
    
    
    
    
    
