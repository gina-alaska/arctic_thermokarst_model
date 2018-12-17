
from atm_io import raster
from multigrids import temporal_grid
import glob
import numpy as np
import os 
import re

# def show(data):
#     import matplotlib.pyplot as plt
#     plt.imshow(data)
#     plt.show()
         
def show(data, title='fig'):  
    import matplotlib.pyplot as plt

    plt.imshow(data, cmap='viridis', vmin=0,vmax=4)
    plt.title(title, wrap = True)
    cb = plt.colorbar(ticks =range( 4), orientation = 'vertical')
    cb.set_ticklabels(['below', 'above', '>1 std', '>2 std'])
    #plt.imshow(data, cmap='seismic')
    #plt.colorbar()
    plt.show()


def load_precips(precip_dir, start_year, end_year):
    """"""
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

    # print grid_names
    precip.grid_name_map = grid_names   

    mm_yyyy = re.compile(r'\d\d_\d\d\d\d')
    
    for file in sorted(files):
        data, metadata = raster.load_raster(file)
        data[data==-9999] = np.nan
        mon, year = mm_yyyy.findall(file)[0].split('_')
        idx = year+'-'+mon
        # print precip.grid_name_map[idx], idx
        precip[idx] = data

    precip.config['grid_name_map'] = grid_names  
    precip.config['raster_metadata'] = metadata

    return precip


def calc_winter_precip_avg (precip, years='all'):
    """
    years: 'all' or 'start-end' ie '1901-1950'
    """
    keys = precip.grid_name_map.keys()
    oct_keys = sorted([k for k in keys if k[-2:]=='10'])
    nov_keys = sorted([k for k in keys if k[-2:]=='11'])
    # print nov_keys
    if years != 'all':
        start, end = years.split('-')
        oct_filtered = []
        nov_filtered = []
        for year in range(int(start),int(end)+1):
            oct_filtered += [ok for ok in oct_keys if ok[:4] == str(year)]
            nov_filtered += [nk for nk in nov_keys if nk[:4] == str(year)]

        oct_keys = sorted(oct_filtered)
        nov_keys = sorted(nov_filtered)
            
    # print oct_keys
    # print nov_keys

    oct_precip = precip.get_grids_at_keys(oct_keys)
    nov_precip = precip.get_grids_at_keys(nov_keys)

    winter_precip = oct_precip + nov_precip
    print winter_precip.shape
    winter_avg =  winter_precip.mean(0)
    winter_std =  winter_precip.std(0)
    return winter_avg, winter_std, winter_precip



def create_avgs (precip, tdd, fdd, directory, years = 'all'):
    wavg, wstd, winter_precip = calc_winter_precip_avg(precip, years) 
    winter_precip  = calc_winter_precip_avg(precip, 'all') 
    winter_precip = winter_precip[2]

    if years == 'all':
        start = 1901
        fdd_avg = fdd.grids.reshape(fdd.real_shape)
        tdd_avg = tdd.grids.reshape(tdd.real_shape)
    else:
        start, end = years.split('-')
        fdd_avg = fdd.get_grids_at_keys(range(int(start),int(end)+1))
        tdd_avg = tdd.get_grids_at_keys(range(int(start),int(end)+1))

    print fdd_avg.shape
    print tdd_avg.shape
    fdd_std = fdd_avg.std(0)
    tdd_std = tdd_avg.std(0)
    fdd_avg = fdd_avg.mean(0)
    tdd_avg = tdd_avg.mean(0)

    # wavg_1901_1950 = fty.calc_winter_precip_avg(precip, '1901-1950') 
    transform = precip.raster_metadata.transform
    projection = precip.raster_metadata.projection

    raster.save_raster(os.path.join(directory, years + '_precip_winter_avg.tif'), wavg, transform, projection)
    raster.save_raster(os.path.join(directory, years + '_fdd_avg.tif'), fdd_avg, transform, projection)
    raster.save_raster(os.path.join(directory, years + '_tdd_avg.tif'), tdd_avg, transform, projection)
    # raster.save_raster('/Users/rwspicer/Desktop/averages/precip_winter_avg_1901-1950.tif', wavg_1901_1950, transform, projection)

    shape = tdd.grid_shape
    fdd_grid = np.zeros(shape)  
    fdd_grid[::] = np.nan
    # show(fdd_grid)

    tdd_grid = np.zeros(shape)  
    tdd_grid[::] = np.nan

    precip_grid = np.zeros(shape)  
    precip_grid[::] = np.nan

    warm_winter = np.zeros(shape)  
    warm_winter[::] = np.nan

    for idx in range(fdd.grids.shape[0]):
        c_fdd = fdd.grids[idx].reshape(shape)
        c_tdd = tdd.grids[idx].reshape(shape)
        c_precip = winter_precip[idx].reshape(shape)

        


        fdd_grid[::] = c_fdd - c_fdd
        tdd_grid[::] = c_tdd - c_tdd
        precip_grid[::] = c_precip - c_precip
        for s in [0, 1, 2]:
            # fdd_grid[(c_fdd - fdd_avg) > s * fdd_std] = s + 1  
            # tdd_grid[(c_tdd - tdd_avg) > s * tdd_std] = s + 1  
            # precip_grid[(c_precip - wavg) > s * wstd] = s + 1 
            fdd_grid[c_fdd > (fdd_avg + s * fdd_std)] = s + 1  
            tdd_grid[c_tdd > (tdd_avg + s * tdd_std)] = s + 1 
            precip_grid[c_precip > (wavg + s * wstd)] = s + 1 
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
        raster.save_raster(os.path.join(directory, years, yr + '_trigger_areas.tif'), trigger, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_precip_gtavg.tif'), precip_grid, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_fdd_gtavg.tif'), fdd_grid, transform, projection)
        raster.save_raster(os.path.join(directory, years, yr + '_tdd_gtavg.tif'), tdd_grid, transform, projection)

        warm_winter = (fdd_grid)+ precip_grid

    show(fdd_grid, 'fdd')
    show(tdd_grid, 'tdd')
    show(precip_grid, 'winter precip')
    show(trigger, 'trigger')

    return wavg, wstd, tdd_avg, tdd_std, fdd_avg, fdd_std

   



precip = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_precip_monthly/cliped-precip-loaded-data-1901-2015.yml')
fdd = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_fdd/fdd.yml')
tdd = temporal_grid.TemporalGrid('/Users/rwspicer/Desktop/ns_tdd/tdd.yml')


## 0 = precip <= avg, fdd <= avg, fdd <= avg
## 1 = precip > avg, fdd <= avg, fdd <= avg
## 2 = precip > 1 std, fdd <= avg, fdd <= avg
## 3 = precip > 2 std, fdd <= avg, fdd <= avg
## 4 = precip <= avg std, fdd > avg, fdd <= avg
## 5 = precip <= avg std, fdd > avg, fdd <= avg
## 6 = precip <= avg std, fdd > avg, fdd <= avg
## 7 = precip <= avg std, fdd > avg, fdd <= avg


