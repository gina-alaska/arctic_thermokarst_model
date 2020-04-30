"""
Raster Clip
-----------

clip out a sub raster from input file
"""
import gdal
import os
import numpy as np
import glob

def clip_raster (in_raster, out_raster, extent):
    """Clip a raster to extent
    
    Parameters:
    in_raster: path
        input raster file
    out_raster: path
        output raster file
    extent: tuple
        (minX, maxY, maxX, minY)
    """
    return gdal.Translate(
        out_raster, in_raster, projWin = extent, 
        format='GTiff', outputType=gdal.GDT_Float32 
    ) 

def clip_rasters (in_dir, out_dir, extent, ext = '.tif'):
    """clip all rasters in a directory
    
    Parameters:
    in_dir: path
        input raster directory
    out_dit: path
        output raster directory
    extent: tuple
        (minX, maxY, maxX, minY)
    ext: optional, (.tif)
        file extension to filter for in in_dir
    """
    files = glob.glob(in_dir+'/*' + ext)
    for f in files:
        print f
        out_f = os.path.split(f)[1]
        out_path = os.path.join(out_dir,out_f)
        in_path = f
        clip_raster(in_path, out_path, extent)

def tool():
    """Command line tool for calling clip_rasters
    """
    import CLILib
    try:
        arguments = CLILib.CLI([
            '--input-dir',
            '--output-dir',
            '--extent'
            ],
            ['--extension']
        )
    except (CLILib.CLILibHelpRequestedError, CLILib.CLILibMandatoryError):
        print tool.__doc__
        return

    in_dir = arguments['--input-dir']
    out_dir = arguments['--output-dir']
    extent = arguments['--extent']
    
    ext = 'tif' if arguments['--extension']  is None else arguments['--extension'] 

    try:
        extent = extent.replace('(','').replace(')','')
        extent = [float(n) for n in extent.split(',')]
        if len(extent) != 4:
            raise ValueError
    except ValueError:
        print 'Extent must be in format, (Upper,Left,Lower,Right)' +\
            ' or Upper,Left,Lower,Right'
        return
   
    clip_rasters(in_dir, out_dir, extent, ext)

if __name__ == '__main__':
    tool()
