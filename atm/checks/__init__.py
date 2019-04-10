"""
checks
------

Transition function metadata
"""
import poi_based
import poi_based_jit

import lake_to_pond
import pond_to_lake
import lake_to_pond_jit 
import pond_to_lake_jit

# import poi_based_hill
# import poi_based_hill_jit
# import poi_based_sigmoid2
# import poi_based_sigmoid2_jit

    
check_metadata = {
        
        #~ 'base': check_base.check_base,
        'poi': poi_based.transition,
        'poi_jit': poi_based_jit.transition,
        
        'pond_to_lake': pond_to_lake.transition,
        'lake_to_pond': lake_to_pond.transition,
        'pond_to_lake_jit': pond_to_lake_jit.transition,
        'lake_to_pond_jit': lake_to_pond_jit.transition,


    } 
