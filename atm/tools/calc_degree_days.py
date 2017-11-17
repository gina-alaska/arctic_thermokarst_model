import numpy as np
from scipy import interpolate
from multiprocessing import Process, Lock, active_children, cpu_count


def calc_degree_days(day_array, temp_array, expected_roots = 230):
    #print day_array
    #print temp_array
    spline = interpolate.UnivariateSpline(day_array, temp_array,s=10)
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


def calc_and_store  (index, day_array, temp_array, tdd_grid, fdd_grid, lock = Lock()):
    tdd, fdd  = calc_degree_days(day_array, temp_array)
    lock.acquire()
    tdd_grid[:,index] = tdd
    fdd_grid[:,index] = [0] + fdd
    lock.release()




def calc_gird_degree_days (day_array, temp_grid, tdd_grid, fdd_grid, start = 0):
    p_lock = Lock()
    w_lock = Lock()
    for idx in  range(start, temp_grid.shape[1]): # flatted area grid index
        while len(active_children()) >= cpu_count():
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




