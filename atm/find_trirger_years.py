"""
Initialization Areas 
--------------------

initialization_areas.py

Tools to help find areas were thermokarst initialization is likely 

"""
from atm.images import raster
from multigrids import temporal_grid
import glob
import numpy as np
import os 
import re
         
def show(data, title='fig'):  
    """Unility Function to show a figure
    """
    import matplotlib.pyplot as plt

    plt.imshow(data, cmap='viridis', vmin=0,vmax=4)
    plt.title(title, wrap = True)
    cb = plt.colorbar(ticks =range( 4), orientation = 'vertical')
    cb.set_ticklabels(['below', 'above', '>1 std', '>2 std'])
    #plt.imshow(data, cmap='seismic')
    #plt.colorbar()
    plt.show()


def load_precip_data(precip_dir, start_year, end_year):
    """Loads monthly precipitation data from raster files in a given directory,
    for a given range of years(inclusive range).

    Parameters
    ----------
    precip_dir: path
        directory contains the raster files in the format "**MM_YYYY.tif"
    start_year: int
        start year of rasters to load
    end_year: int
        end year of rasters to load

    Returns
    -------
    multigrids.temporal_gird.TemporalGrid
        The monthly precipitation data for the range of years. Grid names are 
        in the format "YYYY-MM."
    """
    files = glob.glob(precip_dir+'/*.tif')

    num_ts = (end_year+1-start_year)*12
    data, metadata = raster.load_raster(files[0])

    precip = temporal_grid.TemporalGrid(data.shape[0], data.shape[1], num_ts)

    grid_names={}                                       
    c = 0
    for year in range(start_year,end_year+1):
        for mon in range(1,13):
            fm = '000'+str(mon)
            tsn = str(year) +'-' + fm[-2:]
            grid_names[tsn] = c
            c += 1

    # # print grid_names
    precip.config['grid_name_map'] = grid_names

    mm_yyyy = re.compile(r'\d\d_\d\d\d\d')
    
    for file_with_path in sorted(files):
        file = os.path.split(file_with_path)[1]
        mon, year = mm_yyyy.findall(file)[0].split('_')
        if not (start_year <= int(year) <= end_year):
            continue


        data, metadata = raster.load_raster(file_with_path)
        data[data==-9999] = np.nan
        idx = year +'-'+ mon
        
        precip[idx] = data

    precip.config['grid_name_map'] = grid_names  
    precip.config['raster_metadata'] = metadata
    precip.config['dataset_name'] = \
        "Monthly-Precipitation-" + str(start_year) + "-" + str(end_year)
    precip.config['description'] = \
        "Monthly Precipitation from" + str(start_year) + " to " +\
        str(end_year) + ". Grid names are in the format 'YYYY-MM'."

    return precip


def calc_early_winter_precip_avg (precip, years='all'):
    """Calculate the average and standard diveation for early winter 
    precipitation. Early winter consists of October and November

    Parameters
    ----------
    precip: multigrids.temporal_gird.TemporalGrid
    years: str
        Range of years to calculate average over. 
        'all' or 'start-end' ie '1901-1950'.
    
    Returns
    ------- 
    winter_avg: np.array [M x N]
        map early winter precipitation averages 
    winter_std: np.array [M x N]
        map early winter precipitation standard diveations 
    winter_precip: np.array [M x N x Num_Years]
        maps of early winter precipitation for each year
    """
    keys = precip.config['grid_name_map'].keys()
    oct_keys = sorted([k for k in keys if k[-2:]=='10'])
    nov_keys = sorted([k for k in keys if k[-2:]=='11'])
    # # print nov_keys
    if years != 'all':
        start, end = years.split('-')
        oct_filtered = []
        nov_filtered = []
        for year in range(int(start),int(end)+1):
            oct_filtered += [ok for ok in oct_keys if ok[:4] == str(year)]
            nov_filtered += [nk for nk in nov_keys if nk[:4] == str(year)]

        oct_keys = sorted(oct_filtered)
        nov_keys = sorted(nov_filtered)
            
    # # print oct_keys
    # # print nov_keys

    oct_precip = precip.get_grids_at_keys(oct_keys)
    nov_precip = precip.get_grids_at_keys(nov_keys)

    winter_precip = oct_precip + nov_precip
    # print winter_precip.shape
    winter_avg =  winter_precip.mean(0)
    winter_std =  winter_precip.std(0)
    return winter_avg, winter_std, winter_precip


def calc_winter_precip_avg (precip, years='all'):
    """Calculate the average and standard diveation for winter 
    precipitation. Winter consists of October - March

    Parameters
    ----------
    precip: multigrids.temporal_gird.TemporalGrid
    years: str
        Range of years to calculate average over. 
        'all' or 'start-end' ie '1901-1950'.
    
    Returns
    ------- 
    winter_avg: np.array [M x N]
        map winter precipitation averages 
    winter_std: np.array [M x N]
        map winter precipitation standard diveations 
    winter_precip: np.array [M x N x Num_Years]
        maps of winter precipitation for each year
    """
    keys = precip.config['grid_name_map'].keys()
    oct_keys = sorted([k for k in keys if k[-2:]=='10'])
    nov_keys = sorted([k for k in keys if k[-2:]=='11'])
    dec_keys = sorted([k for k in keys if k[-2:]=='12'])
    jan_keys = sorted([k for k in keys if k[-2:]=='01'])
    feb_keys = sorted([k for k in keys if k[-2:]=='02'])
    mar_keys = sorted([k for k in keys if k[-2:]=='03'])

    if years != 'all':
        start, end = years.split('-')
        oct_filtered = []
        nov_filtered = []
        dec_filtered = []
        jan_filtered = []
        feb_filtered = []
        mar_filtered = []
        for year in range(int(start),int(end)):
            oct_filtered += [ok for ok in oct_keys if ok[:4] == str(year)]
            nov_filtered += [nk for nk in nov_keys if nk[:4] == str(year)]
            dec_filtered += [dk for dk in dec_keys if dk[:4] == str(year)]
            jan_filtered += [jk for jk in jan_keys if jk[:4] == str(year + 1)]
            feb_filtered += [fk for fk in feb_keys if fk[:4] == str(year + 1)]
            mar_filtered += [mk for mk in mar_keys if mk[:4] == str(year + 1)]

        oct_keys = sorted(oct_filtered)
        nov_keys = sorted(nov_filtered)
        dec_keys = sorted(dec_filtered)
        jan_keys = sorted(jan_filtered)
        feb_keys = sorted(feb_filtered)
        mar_keys = sorted(mar_filtered)
            

    oct_precip = precip.get_grids_at_keys(oct_keys)
    nov_precip = precip.get_grids_at_keys(nov_keys)
    dec_precip = precip.get_grids_at_keys(dec_keys)
    jan_precip = precip.get_grids_at_keys(jan_keys)
    feb_precip = precip.get_grids_at_keys(feb_keys)
    mar_precip = precip.get_grids_at_keys(mar_keys)


    winter_precip = oct_precip + nov_precip + dec_precip +\
                    jan_precip + feb_precip + mar_precip
    winter_avg =  winter_precip.mean(0)
    winter_std =  winter_precip.std(0)
    return winter_avg, winter_std, winter_precip



def find_initialization_areas (precip, tdd, fdd, directory, years = 'all', 
        winter_precip_func = calc_winter_precip_avg
    ):
    """Creates raster outputs of the Initialization Areas.

    These initialization areas rasters are calculated based on a given winter
    and the following summer. Basically if the winter is warmer than average
    with high precipitation (early or full) is higher than average, followed 
    by a warmer than average summer then the likelihood for initialization is
    higher.

    Parameters
    ----------
    precip: multigrids.temporal_gird.TemporalGrid 
        Full monthly precipitation dataset
    tdd: multigrids.temporal_gird.TemporalGrid
        Thawing Degree Days dataset 
    fdd: multigrids.temporal_gird.TemporalGrid
        Freezing Degree Days dataset 
    directory: path
        directory to save raster files(.tif) to.
    years: str
        Range of years to calculate averages over. 
        'all' or 'start-end' ie '1901-1950'.
    winter_precip_func: function
        The function to use for calculating the winter precipitation.
        Either calc_winter_precip_avg or calc_early_winter_precip_avg
        

    Returns
    ------
    winter_precip_avg, winter_precip_std, 
    tdd_avg, tdd_std, fdd_avg, fdd_std: np.array [M x N]
        maps of the average and standard diveation. 
    """

    # Fist line gets the average and standard diveation for the desired range
    # of years. The second and third lines gets the full winter 
    # precipitation data.
    winter_precip_avg, winter_precip_std, winter_precip = \
        winter_precip_func(precip, years) 
    winter_precip  = winter_precip_func(precip, 'all') 
    winter_precip = winter_precip[2] 
    

    ## get the degree day averages and standard dilations. 
    if years == 'all':
        start = 1901
        fdd_avg = fdd.grids.reshape(fdd.config['real_shape'])
        tdd_avg = tdd.grids.reshape(tdd.config['real_shape'])
    else:
        start, end = years.split('-')
        fdd_avg = fdd.get_grids_at_keys(range(int(start),int(end)+1))
        tdd_avg = tdd.get_grids_at_keys(range(int(start),int(end)+1))
    fdd_std = fdd_avg.std(0)
    tdd_std = tdd_avg.std(0)
    fdd_avg = fdd_avg.mean(0)
    tdd_avg = tdd_avg.mean(0)

    # raster metadata 
    transform = precip.config['raster_metadata'].transform
    projection = precip.config['raster_metadata'].projection

    raster.save_raster(
        os.path.join(directory, years + '_precip_winter_avg.tif'), 
        winter_precip_avg, transform, projection)
    raster.save_raster(
        os.path.join(directory, years + '_fdd_avg.tif'),
        fdd_avg, transform, projection
    )
    raster.save_raster(
        os.path.join(directory, years + '_tdd_avg.tif'), 
        tdd_avg, transform, projection
    )

    ## find the areas
    shape = tdd.config['grid_shape']
    fdd_grid = np.zeros(shape)  
    fdd_grid[::] = np.nan
    # show(fdd_grid)

    tdd_grid = np.zeros(shape)  
    tdd_grid[::] = np.nan

    precip_grid = np.zeros(shape)  
    precip_grid[::] = np.nan

    warm_winter = np.zeros(shape)  
    warm_winter[::] = np.nan

    os.makedirs(os.path.join(directory, years))
    
    for idx in range(fdd.grids.shape[0]):
        c_fdd = fdd.grids[idx].reshape(shape)
        c_tdd = tdd.grids[idx].reshape(shape)
        c_precip = winter_precip[idx].reshape(shape)

        fdd_grid[::] = c_fdd - c_fdd
        tdd_grid[::] = c_tdd - c_tdd
        precip_grid[::] = c_precip - c_precip
        for s in [0, 1, 2]:
            fdd_grid[c_fdd > (fdd_avg + s * fdd_std)] = s + 1  
            tdd_grid[c_tdd > (tdd_avg + s * tdd_std)] = s + 1 
            precip_grid[
                c_precip > (winter_precip_avg + s * winter_precip_std)
            ] = s + 1 
            # show(fdd_grid)
            # show(tdd_grid)
            # show(precip_grid)
            # show(trigger)

        trigger = warm_winter + (tdd_grid)
        
        # show(fdd_grid, str(1901 + idx) + 'fdd')
        # show(tdd_grid, str(1901 + idx) +'tdd')
        # show(precip_grid, str(1901 + idx) +'winter precip')
        # show(trigger, str(1901 + idx) +'trigger')


        yr = str(int(start)+idx)
        raster.save_raster(os.path.join(directory, years, yr + '_initialization_areas.tif'), trigger, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_precip_gtavg.tif'), precip_grid, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_fdd_gtavg.tif'), fdd_grid, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_tdd_gtavg.tif'), tdd_grid, transform, projection)

        warm_winter = (fdd_grid)+ precip_grid

    return winter_precip_avg, winter_precip_std, tdd_avg, tdd_std, fdd_avg, fdd_std

   



# precip = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_precip_monthly/cliped-precip-loaded-data-1901-2015.yml')
# fdd = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_fdd/fdd.yml')
# tdd = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_tdd/tdd.yml')


## 0 = precip <= avg, fdd <= avg, fdd <= avg
## 1 = precip > avg, fdd <= avg, fdd <= avg
## 2 = precip > 1 std, fdd <= avg, fdd <= avg
## 3 = precip > 2 std, fdd <= avg, fdd <= avg
## 4 = precip <= avg std, fdd > avg, fdd <= avg
## 5 = precip <= avg std, fdd > avg, fdd <= avg
## 6 = precip <= avg std, fdd > avg, fdd <= avg
## 7 = precip <= avg std, fdd > avg, fdd <= avg


