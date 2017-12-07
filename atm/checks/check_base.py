

import numpy as np
import functions

def check_base(grids, cohort_config, year):
    """assuming year '0' is the inital data, this should start with year 1
    """
    import matplotlib.pyplot as plt
    
    
    name = cohort_config['cohort']
    ## mask out non-test area
    model_area_mask = grids.area.area_of_intrest()
    
    #~ plt.imshow(model_area_mask.reshape(grids.shape))
    #~ plt.show()
    
    ## get_ice contents
    ice_slope = grids.ice.get_ice_slope_grid( name )#cohort_config ['ice content'])
    
    #~ plt.imshow(ice_slope.reshape(grids.shape))
    #~ plt.show()
    
    ## get_cell with 'current cohort present'
    
    cohort_present_mask = grids.area[ year, cohort_config['cohort'] ] > 0
    
    #~ plt.imshow(cohort_present_mask.reshape(grids.shape))
    #~ plt.show()
    ### where is ald >= PL
    pl_breach_mask = grids.ald['ALD', year] >= grids.ald[name, year]
    
    current_cell_mask = np.logical_and(
        np.logical_and(
            model_area_mask, cohort_present_mask
        ),  
        pl_breach_mask 
    )
    
    #~ plt.imshow(current_cell_mask.reshape(grids.shape))
    #~ plt.show()
    ## find 'x'
    x = np.zeros(grids.shape)
    x[current_cell_mask] = (
        grids.ald['ALD',year] / grids.ald[name ,year]
    )[current_cell_mask] - 1
    #~ print ' x ' 
    #~ plt.imshow(x.reshape(grids.shape))
    #~ plt.show()
    ## get function type
    fn = functions.table[cohort_config['POI_Function'].lower()]
    
    
    
    parameters = {
        'A1': cohort_config['A1_above'], 
        'A2': cohort_config['A2_above'], 
        'x0': cohort_config['x0_above'], 
        'dx': cohort_config['dx_above'], 
        'a': cohort_config['a_above'],
        'b': cohort_config['b_above'], 
        'K': cohort_config['K_above'], 
        'C': cohort_config['C_above'], 
        'A': cohort_config['A_above'], 
        'B': cohort_config['B_above'], 
        'hB': cohort_config['HillB_above'], 
        'hN': cohort_config['HillN_above']
    }
    
    POI_above = fn(x , parameters)
    
    #~ plt.imshow(POI_above.reshape(grids.shape))
    #~ plt.colorbar()
    #~ plt.show()
    parameters = {
        'A1': cohort_config['A1_below'], 
        'A2': cohort_config['A2_below'], 
        'x0': cohort_config['x0_below'], 
        'dx': cohort_config['dx_below'], 
        'a': cohort_config['a_below'],
        'b': cohort_config['b_below'], 
        'K': cohort_config['K_below'], 
        'C': cohort_config['C_below'], 
        'A': cohort_config['A_below'], 
        'B': cohort_config['B_below'], 
        'hB': cohort_config['HillB_below'], 
        'hN': cohort_config['HillN_below']
    }
    
    POI_below = fn(x , parameters)
    #~ plt.imshow(POI_below.reshape(grids.shape))
    #~ plt.colorbar()
    #~ plt.show()
    
    POI = POI_below 
    above_idx = grids.drainage.grid.reshape(grids.shape) == 'above'
    POI [above_idx] = POI_above[above_idx]
   
    #~ plt.imshow(POI.reshape(grids.shape))
    #~ plt.colorbar()
    #~ plt.show()
    

    ## update POI
    grids.poi[year, name] = grids.poi[year-1, name] + POI
      
      
    #~ plt.imshow(grids.poi[year-1, cohort_config['cohort']])
    #~ plt.colorbar()
    #~ plt.show()
    #~ plt.imshow(grids.poi[year, cohort_config['cohort']])
    #~ plt.colorbar()
    #~ plt.show()

    ## set PL[year]
    
    porosity = grids.ald.porosity[name]
    print name 
    grids.ald[name, year ] = grids.ald[name, year-1 ] + \
        (grids.ald['ALD', year] - grids.ald[name, year-1 ] ) * porosity
        
    grids.ald[name, year-1][np.logical_not(model_area_mask)] = np.nan
    #~ plt.imshow(grids.ald[name, year-1])
    #~ plt.colorbar()
    #~ plt.show()
    grids.ald[name, year][np.logical_not(model_area_mask)] = np.nan
    #~ plt.imshow(grids.ald[name, year])
    #~ plt.colorbar()
    #~ plt.show()

    #~ plt.imshow(grids.ald[name, year] - grids.ald[name, year - 1])
    #~ plt.colorbar()
    #~ plt.show()
    
    max_rot = cohort_config['max_terrain_transition']
    rate_of_transition = \
        grids.poi[year, name] * ice_slope.reshape(grids.shape) * max_rot
        
    
    
    rate_of_transition[ rate_of_transition > max_rot ] = max_rot
    
    #~ plt.imshow(rate_of_transition)
    #~ plt.colorbar()
    #~ plt.show()
    
    change = rate_of_transition * grids.area[ year, cohort_config['cohort'] ]
    
    #~ plt.imshow(change)
    #~ plt.colorbar()
    #~ plt.show()
    
    ## if change is bigger than area available
    ## TODO: handle age buckets
    current = grids.area[ year - 1, cohort_config['cohort'] ]
    change[ change > current ] = current [ change > current ]
    
    #~ plt.imshow(change)
    #~ plt.colorbar()
    #~ plt.show()
    
    transitions_to = cohort_config['transitions_to']
    grids.area[ year, transitions_to + '--0'] = \
        grids.area[ year - 1, transitions_to] + change
    
    grids.area[ year, name + '--0' ] = current - change

    plt.imshow( grids.area[ year-1, name])
    plt.colorbar()
    plt.show()
    
    #~ plt.imshow( grids.area[ year-1, transitions_to])
    #~ plt.colorbar()
    #~ plt.show()
   
    plt.imshow( grids.area[ year, name])
    plt.colorbar()
    plt.show()
    
    #~ plt.imshow( grids.area[ year, transitions_to])
    #~ plt.colorbar()
    #~ plt.show()
