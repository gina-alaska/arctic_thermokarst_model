
import numpy as np

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
   
    print 'land_cohorts',land_cohorts
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
    
    while (expansion[not_entire_area] > 0 ).any():
        print 'outer'
        has_area_count = np.zeros(shape)
        min_area = np.zeros(shape)  
        min_area[not_entire_area] = grids.area[year,land_cohorts[0]][not_entire_area]
        for cohort in land_cohorts:
            has_area = grids.area[year,cohort] > 0
            has_area = np.logical_and(has_area, not_entire_area)
            has_area_count[has_area] += 1
            
            min_area[has_area] = \
                np.minimum(grids.area[year,cohort], min_area)[has_area]
        expansion_fraction = np.zeros(shape)
        expansion_fraction[not_entire_area] = \
            (expansion / has_area_count)[not_entire_area]
        
        
        expansion_fraction[not_entire_area] = \
            np.minimum(min_area, expansion_fraction)[not_entire_area]
          
        for cohort in land_cohorts:
            has_cohort = grids.area[year,cohort] > 0.0
            has_cohort = np.logical_and(has_cohort, not_entire_area)
            
            ## constant
            bucket_list = [
                b for b in grids.area.key_to_index if b.find(cohort) != -1
            ]

            bucket_list = [b for b in bucket_list if b.find('--') != -1]
           
            bucket_reduction = np.zeros(shape)
            bucket_reduction[has_cohort] = expansion_fraction[has_cohort] 
            while (bucket_reduction[has_cohort] > 0).any():
                print 'inner'
                bucket_count = np.zeros(shape)
                min_bucket = np.zeros(shape)  
                min_bucket[has_cohort] = grids.area[year,bucket_list[0]][has_cohort]
                for bucket in bucket_list:
                    has_bucket = grids.area[year,bucket] > 0
                    has_bucket = np.logical_and(has_bucket, not_entire_area)
                    bucket_count[has_bucket] += 1
                    
                    min_bucket[has_bucket] = \
                        np.minimum(grids.area[year,bucket], min_bucket)[has_bucket]
                
                #fractional bucket reduction
                fb_reduction = np.zeros(shape)
                fb_reduction = bucket_reduction / bucket_count
                fb_reduction = np.minimum(fb_reduction, min_bucket)
                
                for bucket in bucket_list:
                    has_bucket = grids.area[year,bucket] > 0
                    has_bucket = np.logical_and(has_bucket, not_entire_area)
                    grids.area[year,bucket][has_bucket] -= fb_reduction[has_bucket]
                    
                
                bucket_reduction = bucket_reduction - bucket_count * fb_reduction 
        
        
        expansion = expansion - expansion_fraction * has_area_count
        print expansion[not_entire_area].max()
        
    
        
    
        
