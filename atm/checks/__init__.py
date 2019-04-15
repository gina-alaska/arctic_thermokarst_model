"""
checks
------

Transition function metadata
"""
import poi_based
import lake_to_pond
import pond_to_lake

import poi_based_jit
import lake_to_pond_jit 
import pond_to_lake_jit

import poi_based_cuda
import lake_to_pond_cuda
import pond_to_lake_cuda


# table of transition functions
check_metadata = {
        'poi': poi_based.transition,
        'pond_to_lake': pond_to_lake.transition,
        'lake_to_pond': lake_to_pond.transition,
        
        'poi_jit': poi_based_jit.transition,
        'pond_to_lake_jit': pond_to_lake_jit.transition,
        'lake_to_pond_jit': lake_to_pond_jit.transition,

        'poi_cuda': poi_based_cuda.transition,
        'pond_to_lake_cuda': pond_to_lake_cuda.transition,
        'lake_to_pond_cuda': lake_to_pond_cuda.transition,

} 
