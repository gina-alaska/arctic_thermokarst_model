"""
checks
------

Transition function metadata
"""
import poi_based
import lake_to_pond_jit as lake_to_pond
import pond_to_lake_jit as pond_to_lake
import poi_based_hill
import poi_based_hill_jit
import poi_based_sigmoid2
import poi_based_sigmoid2_jit
    
check_metadata = {
        
        #~ 'base': check_base.check_base,
        'poi': poi_based.transition,
        
        'pond_to_lake': pond_to_lake.transition,
        'lake_to_pond': lake_to_pond.transition,

    } 
