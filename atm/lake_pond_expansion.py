
import numpy as np
from copy import deepcopy

def infill ( ponds, year, grids, control):
    """The purpose of this module is to infill ponds at a prescribed rate with 
    vegetation, which will presumably be non-polygonal ground.
    
    This module is developed due to paper that states with warming temperatures,
    ponds are shrinking due in part to infilling of vegetation.  Paper is in 
    press and was set out by Anna L. in March 2015.
    """
    ## no infill in first time step
    if year == control['start year']:
        return 
    
    transitions_to = control['Lake_Pond_Control']['Ponds_fill_to']
    
    shape = grids.shape
    pond_area = np.zeros(shape)
    
    for p in ponds:
        pond_area += grids.area[year, p ]
    
    change_pond_area = np.logical_and(pond_area > 0,  pond_area < 1)   
    
    ttd_greater = grids.degreedays.thawing[year] > grids.degreedays.thawing[year-1]
    
    change_pond_area = np.logical_and(ttd_greater, change_pond_area)
    
    for p in ponds:
        infill_const = control['Lake_Pond_Control'][p+'_Infill_Constant']
    
        p_buckets = [b for b in grids.area.key_to_index if b.find(p) != -1]
        p_buckets = [b for b in p_buckets if b.find('--') != -1]
        
        for b in p_buckets:
            change = grids.area[year, b][change_pond_area]  * infill_const
            grids.area[year, b][change_pond_area] -= change
            grids.area[year, transitions_to][change_pond_area] -= change
        
            
        


def expansion ( lp_cohorts, year, grids, control):
    """
    """
    shape = grids.shape
    
    ## get total
    total = np.zeros(shape)
    for cohort in lp_cohorts:
        total += grids.area[year,cohort]
        
    ## aoi 
    
    model_area_mask = grids.area.area_of_intrest()
    
    ## water bodies can expand if area is present and not filling entire cell
    can_expand = np.logical_and(total > 0.0, total < 1.0)
    
    can_expand = np.logical_and(can_expand, model_area_mask )
    
    ## create 2x multiplier where climate events is true
    ## True -> 1, False ->0, +1 -> 2, 1 respectivly
    climate_events = grids.climate_event[year].astype(int) + 1
    
    ## set up expansion amount
    expansion = np.zeros(shape)
    for cohort in lp_cohorts:
        expansion = expansion + (
            climate_events * control['Lake_Pond_Control'][cohort + '_Expansion']
        )
        
        
    all_cohorts = set([
        i for i in grids.area.key_to_index.keys() if i.find('--') == -1
    ])
    land_cohorts = all_cohorts - set(lp_cohorts)
    land_cohorts = land_cohorts - set([
        c for c in all_cohorts if c.lower().find('river') != -1
    ])
    land_cohorts = land_cohorts - set([
        c for c in all_cohorts if c.lower().find('urban') != -1
    ])
   
    #~ print 'land_cohorts',land_cohorts
    land_available = np.zeros(shape)
    for cohort in land_cohorts:
        land_available += grids.area[year,cohort]
        
    ## Expands to entire land area
    entire_area = np.logical_and(can_expand, expansion >= land_available)
    for cohort in lp_cohorts:
        area = grids.area[year,cohort]
        exp = area  + (area / total) * land_available
    
        grids.area[year,cohort + '--0'][entire_area] = exp[entire_area]
    
    for cohort in land_cohorts:
        bucket_list = [
            b for b in grids.area.key_to_index if b.find(cohort) != -1
        ]
        for bucket in bucket_list:
            if bucket.find('--') == -1:
                continue
            grids.area[year, bucket][entire_area] = 0.0
            
    ## expand and reduce 
    not_entire_area = np.logical_not( entire_area )
    not_entire_area = np.logical_and( not_entire_area ,model_area_mask)
    
    for cohort in lp_cohorts:
        area = grids.area[year, cohort + '--0']
        exp = climate_events * control['Lake_Pond_Control'][cohort + '_Expansion']
        grids.area[year,cohort + '--0'][not_entire_area] = \
            area[not_entire_area] + exp[not_entire_area]
    
    
    land_cohorts = list(land_cohorts)
    
    ## make list of all buckets in land cohorts
    
    land_bucktes = []
    for cohort in land_cohorts:
        buckets = [b for b in grids.area.key_to_index if b.find('--') != -1]
        buckets = [b for b in buckets if b.find(cohort) != -1]
        
        land_bucktes += buckets
    
    expansion_left = deepcopy(expansion)
    while (expansion_left > 0).any():
        has_area_count = np.zeros(shape)
        left_over = np.zeros(shape)
        for cohort in land_cohorts:
            has_area = grids.area[year,cohort] > 0
            has_area = np.logical_and(has_area, not_entire_area)
            has_area_count[has_area] += 1
        
        expansion_fraction = expansion_left / has_area_count
        
        
        
       
        
        
        #~ for cohort in land_cohorts:
        for cohort in land_bucktes:
            has_area = grids.area[year,cohort] > 0
            has_area = np.logical_and(has_area, not_entire_area)
            
            #~ ## single age bucket only ----
            #~ grids.area[year,cohort+'--0'][has_area] = grids.area[year,cohort+'--0'][has_area] - expansion_fraction[has_area] 
            grids.area[year,cohort][has_area] = grids.area[year,cohort][has_area] - expansion_fraction[has_area] 
           
            less_than_zero = grids.area[year,cohort] < 0
            less_than_zero = np.logical_and(less_than_zero,has_area)
            left_over[less_than_zero] += np.abs(grids.area[year,cohort][less_than_zero])
            #~ grids.area[year,cohort+'--0'][less_than_zero] = 0
            grids.area[year,cohort][less_than_zero] = 0
            #~ ## -----
            
        expansion_left = left_over
        
            ## age buckets version
            #~ bucket_list = [
                #~ b for b in grids.area.key_to_index if b.find(cohort) != -1
            #~ ]

            #~ bucket_list = [b for b in bucket_list if b.find('--') != -1]
            
        
            #~ area_less_than_expansion = grids.area[year,cohort] < expansion_fraction
            #~ area_less_than_expansion = np.logical_and(has_area, area_less_than_expansion)
            
            #~ area_greater_than_expansion = grids.area[year,cohort] > expansion_fraction
            #~ area_greater_than_expansion = np.logical_and(has_area, area_greater_than_expansion)
            
            
            
        
            #~ bucket_left = deepcopy(expansion_fraction)
            #~ while (bucket_left > 0).any():
                #~ has_bucket_count = np.zeros(shape)
                #~ bucket_left_over = np.zeros(shape)
                
                #~ for bucket in bucket_list:
                    #~ has_bucket = grids.area[year,cohort] > 0
                    #~ has_bucket = np.logical_and(has_bucket, has_area)
                    #~ has_bucket_count[has_bucket] += 1
                #~ bucket_fraction = expansion_fraction / has_bucket_count 
                
                #~ for bucket in bucket_list:
                    #~ has_bucket = grids.area[year,cohort] > 0
                    #~ has_bucket = np.logical_and(has_bucket, has_area)
                    
                    #~ grids.area[year,bucket][has_bucket] = grids.area[year,bucket][has_bucket] - bucket_fraction[has_bucket] 
                    
                    #~ less_than_zero = grids.area[year,cohort] < 0
                    #~ less_than_zero = np.logical_and(less_than_zero,has_bucket)
                    
                    #~ bucket_left_over[less_than_zero] += np.abs(grids.area[year,bucket][less_than_zero])
                    #~ grids.area[year,bucket][less_than_zero] = 0
                
                
                
                #~ bucket_left = bucket_left_over
            #~ left_over = bucket_left
            
        #~ expansion_left = left_over
    
    
   
