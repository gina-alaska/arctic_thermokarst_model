

from atm.io import raster
import gdal
import os
import numpy as np

def clip_raster (in_raster, out_raster, extent):
    """
    
    extent : [minX, maxY, maxX, minY]
    """
    return gdal.Translate(out_raster, in_raster, projWin = extent, format='GTiff', outputType=gdal.GDT_Float32 ) 

def clip_rasters (in_dir, out_dir, extent, ext = '.tif'):
    """
    """
    files = [f for f in os.listdir(in_dir) if f[-4:] == ext]
    print files
    for f in files:
        out_path = os.path.join(out_dir,f)
        in_path = os.path.join(in_dir,f)
        print in_path, out_path
        clip_raster(in_path, out_path, extent)


def load_and_stack (in_dir, ext = '.tif'):
    """
    """
    files = [f for f in os.listdir(in_dir) if f[-4:] == ext]
    for fdx in range(len(files)):
        f = files[fdx]
        print f
        ras = os.path.join(in_dir,f)
        
        if fdx ==0:
            data = raster.load_raster(ras)[0].flatten()
        else:
            data = np.vstack((data,  raster.load_raster(ras)[0].flatten()))
            print 'a'
       
            
        print data.shape
    return data
