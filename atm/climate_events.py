
import numpy as np


def drain_lakes (drain_to, year, grids, control):
    """
    """
    #~ water_cohorts = \
        #~ grids.lake_pond.lake_type + grids.lake_pond.ponds_types
        
    shape = grids.shape
    lakes = np.zeros(shape)
    for cohort in grids.lake_pond.lake_types:
        lakes += grids.area[year, cohort]
            
    ponds = np.zeros(shape)
    for cohort in grids.lake_pond.pond_types:
        ponds += grids.area[year, cohort]
    
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
    
    for cohort in grids.lake_pond.pond_types:
        change = np.minimum(
            grids.area[year, cohort] * pond_rates, grids.area[year, cohort]
        )
        grids.area[year, cohort + '--0'] = grids.area[year, cohort] - change
        grids.area[year, drain_to + '--0'] = grids.area[year, drain_to] + change
    
    for cohort in grids.lake_pond.lake_types:
        change = np.minimum(
            grids.area[year, cohort] * pond_rates, grids.area[year, cohort]
        )
        grids.area[year, cohort + '--0'] = grids.area[year, cohort] - change
        grids.area[year, drain_to + '--0'] = grids.area[year, drain_to] + change
            

    
   
