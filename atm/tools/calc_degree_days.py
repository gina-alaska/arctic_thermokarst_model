import numpy as np
from scipy import interpolate
from multiprocessing import Process, Lock, active_children, cpu_count


def calc_degree_days(day_array, temp_array, expected_roots = None):
    """Calc degree days (thawing, and freezing)
    
    Parameters
    ----------
    day_array: list like
        day number for each temperature value. 
        len(days_array) == len(temp_array).
    temp_array: list like
        Temperature values. len(days_array) == len(temp_array).
    expected_roots: int, None
        # of roots expected to find
        
    Returns
    -------
    tdd, fdd: lists
        thawing and freezing degree day lists
    """
    spline = interpolate.UnivariateSpline(day_array, temp_array)
    if not expected_roots is None and len(spline.roots()) != expected_roots:
        print len(spline.roots())
        print 'expected roots is not the same as spline.roots()'
        return np.zeros(115) - np.inf,np.zeros(115) - np.inf

    tdd = []
    fdd = []
    for rdx in range(len(spline.roots())-1):
        val = spline.integral(spline.roots()[rdx], spline.roots()[rdx+1])
        if val > 0:
            tdd.append(val)
        else:
            fdd.append(val)

    return tdd, fdd


def calc_and_store  (
        index, day_array, temp_array, tdd_grid, fdd_grid, lock = Lock()
        ):
    """Caclulate degree days (thawing, and freezing) and store in to 
    a grid.
    
    Parameters
    ----------
    index: int
        Flattened grid cell index.
    day_array: list like
        day number for each temperature value. 
        len(days_array) == len(temp_array).
    temp_array: list like
        Temperature values. len(days_array) == len(temp_array).
    tdd_grid: np.array
        2d grid of # years by flattend grid size. TDD values are stored here.
    fdd_grid: np.array
        2d grid of # years by flattend grid size. FDD values are stored here.
    lock: multiprocessing.Lock, Optional.
        lock object, If not passed a new lock is created. 
        
    """
    expected_roots = 2 * len(tdd_grid)
    tdd, fdd  = calc_degree_days(day_array, temp_array, expected_roots)
    lock.acquire()
    tdd_grid[:,index] = tdd
    fdd_grid[:,index] = fdd[0] + fdd ## add frist value equal to second value
    lock.release()




def calc_gird_degree_days (
        day_array, temp_grid, tdd_grid, fdd_grid, start = 0, num_process = 1
        ):
    """Calculate degree days (Thawing, and Freezing) for an area. 
    
    Parameters
    ----------
    day_array: list like
        day number for each temperature value. 
        len(days_array) == temp_grid.shape[0].
    temp_grid: np.array
        2d numpy array temperature values of timestep by flattened grid sizze.
        len(days_array) == temp_grid.shape[0].
    tdd_grid: np.array
        Empty thawing degree day grid. Size should be # of years to model by 
        flattened grid size. Values are set based on integration of a curve
        caluclated from days_array, and a timeseries from temp_grid. If
        the timeseries is all no data values np.nan is set as all valus 
        for element. If the curve has too many roots, or too few 
        (# roots != 2*# years) -inf is set as all values.
    fdd_grid: np.array
        Empty freezing degree day grid. Size should be # of years to model by 
        flattened grid size. Values are set based on integration of a curve
        caluclated from days_array, and a timeseries from temp_grid. If
        the timeseries is all no data values np.nan is set as all valus 
        for element. If the curve has too many roots, or too few 
        (# roots != 2*# years) -inf is set as all values.
    start: int, defaults to 0 , or list
        Calculate values starting at flattened grid index equal to start.
        If it is a list, list values should be grid indices, and only 
        values for those indices will be caclulated.
    num_process: int, Defaults to 1.
        number of processes to use to do calcualtion. If set to None,
        cpu_count() value is used. If greater than 1 ttd_grid, and fdd_grid 
        should be memory mapped numpy arrays.
    """
    p_lock = Lock()
    w_lock = Lock()
    
    if num_process is None:
       num_process = cpu_count()
    
    if type(start) is int:   
        indices = range(start, temp_grid.shape[1])
    else:
        indices = start
    
    for idx in  indices: # flatted area grid index
        while len(active_children()) >= num_process:
            continue
        print 'calculating degree days for element ', idx
        if (temp_grid[:,idx] == -9999).all():
            w_lock.acquire()
            tdd_grid[:,idx] = np.nan
            fdd_grid[:,idx] = np.nan
            w_lock.release()
            continue
        Process(target=calc_and_store,
            args=(idx,day_array,temp_grid[:,idx], tdd_grid, fdd_grid, w_lock)
        ).start()
    
    while len(active_children()) > 0 :
        continue
        
        
def create_day_array (dates):
    """Calulates number of days after start day for each date in dates array
    
    Parameters
    ----------
    dates: datetime.datetime
        sorted list of dates
        
    Returns
    -------
    days: list
        list of interger days since first date. The first value will be 0.
        len(days) == len(dates)
    """
    init = dates[0]
    days = []
    for date in dates:
        days.append((date - init).days)
        
    return days
    
    
    




