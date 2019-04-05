"""Preprocess area input into properly scaled/normalized data
"""
import os 
import glob
from atm.io import raster as rio
from atm.cohorts import find_canon_name, DISPLAY_COHORT_NAMES 

from collections import namedtuple
import numpy as np

from atm.logger import Logger

GEORASTER = namedtuple('GEORASTER', ["data", "metadata"])

def load_rasters(directory, target_resolution=[1000,1000], log = Logger(None)):
    log.add("Loading started.")
    input_rasters = glob.glob(os.path.join(directory, "*.tif"))
    # raster_metadata = {}
    raster_data = {}
    for f in input_rasters:
        path = f
        filename = os.path.split(f)[-1]
        try:
            name = find_canon_name(filename.split('.')[0])
        except KeyError as e:
            log.add("could not find canon name for: " + filename + ". Using filename")
            name = filename 


        log.add("Loading raster: " + f)
        try:
            
            data, metadata = rio.load_raster (path)
            source_resolution = (abs(metadata.deltaY),abs(metadata.deltaX))
            log.add("Scaling: " + name)
            data = rio.scale_layer_down(data, source_resolution, target_resolution)
        
        except AttributeError:
            log.add('FATAL: Could Not Load Raster File: ' + path, 'FATAL')
            print "uh oh"
            sys.exit(0)

        # log.add("Creating GEORASTER")
        log.add("Storing data")
        raster_data[name] = data

    log.add("Loading finished.")
    return raster_data, metadata

# def check_rasters (rasters):
#     """ensure all rasters have same shape/resolution
#     """
#     log.add("Loading started.")
#     resolution = None
#     shape = None
#     for name in rasters:
#         r=rasters[name]
#         if resolution is None:
#             resolution = (abs(r.metadata.deltaY),abs(r.metadata.deltaX))
#         if shape is None:
#             shape = (r.metadata.nY,r.metadata.nX)
        
#         if shape != (r.metadata.nY,r.metadata.nX):
#             raise AttributeError("Raster shape does not match: " + name)
#         if resolution != (abs(r.metadata.deltaY),abs(r.metadata.deltaX)):
#             raise AttributeError("Raster resolution does not match: " + name)
#     return True

def scale_and_normalize (rasters, target_resolution, metadata, log = Logger(None)):
    log.add("scale_and_normalize started.")
    # log.add("Checking Rasters.")
    # if not check_rasters(rasters):
    #     raise AttributeError("Bad raster input")
    # log.add("Checking complete.")
    # metadata = rasters[rasters.keys()[0]].metadata
    source_resolution = (abs(metadata.deltaY),abs(metadata.deltaX))
    shape = (metadata.nY,metadata.nX)

    
    new_data = []
    new_data_order = []
    for name in rasters:
        # log.add("Scaling: " + name)
        # scaled_data = rio.scale_layer_down(
        #     rasters[name].data, source_resolution, target_resolution
        # )
        new_data.append(rasters[name])
        new_data_order.append(name)

    # new_data = rasters

    log.add("Normalizing data.")
    normalized = rio.normalize_layers(
        new_data, source_resolution, target_resolution
    )

    new_rasters = {}
    print metadata
    for  idx, name in enumerate(new_data_order):
        log.add("Updating metadata: " + name)
        meta = metadata
        # 'transform', 'projection', 
        # 'nX', 'nY', 'deltaX', 'deltaY', 'originX', 'originY'
        transform = (
            meta.transform[0], target_resolution[1] * np.sign([meta.deltaX])[0], meta.transform[2],
            meta.transform[3], meta.transform[4], target_resolution[0] * np.sign([meta.deltaY])[0]
        )
        new_meta = rio.RASTER_METADATA(
            transform, meta.projection, 
            normalized[idx].shape[1],  normalized[idx].shape[0],
            target_resolution[1], target_resolution[0],
            meta.originX, meta.originY
        )
        new_rasters[name] = GEORASTER(normalized[idx], new_meta )

    log.add("Finised Scale and Normalize")
    return new_rasters

def preprocess(in_dir, out_dir, target_resolution=[1000,1000]):
    log = Logger("log.csv", True)
    init_data, metadata = load_rasters(in_dir, log=log)
    s_and_n_data = scale_and_normalize(init_data, target_resolution, metadata, log=log)

    for name in s_and_n_data:
        log.add("Saving: " + name)
        raster = s_and_n_data[name]
        path = os.path.join(out_dir,name+"_scaled_and_normalized.tif")
        rio.save_raster(path, raster.data, raster.metadata.transform, raster.metadata.projection)


# (-530818.761000000056811,2373989.086000000126660)
# (-530818.761399999260902,2374001.250700000673532)
# (-530818.761000000056811,2373989.086000000126660)
