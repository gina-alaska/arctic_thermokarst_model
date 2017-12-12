"""
checks
------

Transition function metadata
"""
import lake_pond_expansion

import poi_based
import lake_to_pond
import pond_to_lake
    
check_metadata = {
        
        #~ 'base': check_base.check_base,
        'poi': poi_based.transition,
        
        'base_pond': pond_to_lake.transition,
        'base_lake': lake_to_pond.transition,

        'lake_pond_expansion': lake_pond_expansion.lake_pond_expansion,
        'pond_infill': lake_pond_expansion.pond_infill,

    } 
