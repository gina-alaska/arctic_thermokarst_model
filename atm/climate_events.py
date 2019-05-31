
import numpy as np


def drain_lakes (drain_to, year, grids, control):
    """
    """
    #~ water_cohorts = \
        #~ grids.lake_pond.lake_type + grids.lake_pond.ponds_types
        
    shape = grids.shape
    lakes = np.zeros(shape)

    pond_types = control['_FAST_get_pond_types']
    lake_types = control['_FAST_get_lake_types']
    lp_types = pond_types + lake_types
                
    # print lp_types

    for cohort in lake_types:
        # print grids.area[cohort, year].shape
        lakes += grids.area[cohort, year]
            
    ponds = np.zeros(shape)
    for cohort in pond_types:
        ponds += grids.area[cohort, year]
    
    lake_rates = np.zeros(shape)
    pond_rates = np.zeros(shape)
    
    
    idx = ponds == 0.0
    pond_rates[idx] = 0.0
    idx = np.logical_and(np.logical_not(idx), ponds < 0.01)
    pond_rates[idx] = control['Met_Control'][ 'pond_drain_rate_<0.01'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'pond_drain_rate_<0.01'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), ponds < 0.1)
    pond_rates[idx] = control['Met_Control'][ 'pond_drain_rate_0.01<0.1']+\
        np.random.uniform(
            0., control['Met_Control'][ 'pond_drain_rate_0.01<0.1'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), ponds < 0.4)
    pond_rates[idx] = control['Met_Control'][ 'pond_drain_rate_0.1<0.4'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'pond_drain_rate_0.1<0.4'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), ponds < 1.0)
    pond_rates[idx] = control['Met_Control'][ 'pond_drain_rate_0.1<0.4'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'pond_drain_rate_0.4<1.0'],
            shape
        )[idx]
    idx = ponds == 1.0
    pond_rates[idx] = 0.0
    
    idx = lakes == 0.0
    lake_rates[idx] = 0.0
    idx = np.logical_and(np.logical_not(idx), lakes < 0.01)
    lake_rates[idx] = control['Met_Control'][ 'lake_drain_rate_<0.01'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'lake_drain_rate_<0.01'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), lakes < 0.1)
    lake_rates[idx] = control['Met_Control'][ 'lake_drain_rate_0.01<0.1']+\
        np.random.uniform(
            0., control['Met_Control'][ 'lake_drain_rate_0.01<0.1'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), lakes < 0.4)
    lake_rates[idx] = control['Met_Control'][ 'lake_drain_rate_0.1<0.4'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'lake_drain_rate_0.1<0.4'],
            shape
        )[idx]
    idx = np.logical_and(np.logical_not(idx), lakes < 1.0)
    lake_rates[idx] = control['Met_Control'][ 'lake_drain_rate_0.1<0.4'] +\
        np.random.uniform(
            0., control['Met_Control'][ 'lake_drain_rate_0.4<1.0'],
            shape
        )[idx]
    idx = lakes == 1.0
    lake_rates[idx] = 0.0
    
    for cohort in pond_types:
        change = np.minimum(
            grids.area[cohort, year] * pond_rates, grids.area[cohort, year]
        )
        grids.area[cohort + '--0', year] = grids.area[cohort, year] - change
        grids.area[drain_to + '--0', year] = grids.area[drain_to, year]  + change
    
    for cohort in lake_types:
        change = np.minimum(
            grids.area[cohort, year] * pond_rates, grids.area[cohort, year]
        )
        grids.area[cohort + '--0', year] = grids.area[cohort, year] - change
        grids.area[drain_to + '--0', year] = grids.area[drain_to, year] + change
            

    
   
