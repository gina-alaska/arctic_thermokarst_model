"""
checks
------

Transition function metadata
"""
import poi_based
import lake_to_pond
import pond_to_lake
    
check_metadata = {
        
        #~ 'base': check_base.check_base,
        'poi': poi_based.transition,
        
        'pond_to_lake': pond_to_lake.transition,
        'lake_to_pond': lake_to_pond.transition,

    } 
