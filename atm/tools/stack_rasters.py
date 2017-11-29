
from atm.atm_io import raster
import numpy as np

def load_and_stack (files):
    """
    """
   
    for fdx in range(len(files)):
        
        f = files[fdx]
        
        if fdx == 0:
            data, md = raster.load_raster(f)
            shape = data.shape
            data = data.flatten()
        else:
            data = np.vstack((data,  raster.load_raster(f)[0].flatten()))
       
            
        #~ print data.shape
    return data, shape


def load_and_stack_memory_mapped (files, filename = 'temp.data'):
    """ 
    """
    for fdx in range(len(files)):
        f = files[fdx]
        
        if fdx == 0:
           
            r, md = raster.load_raster(f)
            
            shape = (len(files), r.shape[0] * r.shape[1])
            data = np.memmap(filename, dtype='float32', mode='w+', shape=shape)
            
            shape = r.shape
            data[0] = r.flatten()
        else:
            data[fdx] = raster.load_raster(f)[0].flatten()

       
            
        #~ print data.shape
    return data, shape
    
    
def stack_np_arrays_from_file (files, out_filename):
    """Loads and stacks data from nparrays that have been written to a file
    
    Parameters
    ----------
    files: list
        sorted list of files to load
    out_filename: path
        file to create stacked data in
        
    Returns
    -------
    data:
        mameory mapped data, fist index is timestep, second is flattened array
    index.
    shape:
        flattened shape for the firest array read
    """
    for fdx in range(len(files)):
        f = files[fdx]
        
        if fdx == 0:
           
            init = np.fromfile(f).flatten()
        
            
            shape = (len(files), init.shape[0] )
            data = np.memmap(
                out_filename, dtype='float32', mode='w+', shape=shape
            )
            
            shape = init.shape
            data[0] = init
        else:
            data[fdx] = np.fromfile(f).flatten()

       
            
        #~ print data.shape
    return data, shape
