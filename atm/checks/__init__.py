"""
checks
------

Transition function metadata
"""
from . import poi_based
from . import lake_to_pond
from . import pond_to_lake
from . import climate_priming_based

from . import poi_based_jit
from . import lake_to_pond_jit 
from . import pond_to_lake_jit

from . import poi_based_cuda
from . import lake_to_pond_cuda
from . import pond_to_lake_cuda


# table of transition functions
check_metadata = {
    'poi': poi_based.transition,
    'pond_to_lake': pond_to_lake.transition,
    'lake_to_pond': lake_to_pond.transition,
    'climate_priming': climate_priming_based.transition,

    'poi_jit': poi_based_jit.transition,
    'pond_to_lake_jit': pond_to_lake_jit.transition,
    'lake_to_pond_jit': lake_to_pond_jit.transition,

    'poi_cuda': poi_based_cuda.transition,
    'pond_to_lake_cuda': pond_to_lake_cuda.transition,
    'lake_to_pond_cuda': lake_to_pond_cuda.transition,


} 

cuda_precompile = [
    poi_based_cuda.compile, 
    lake_to_pond_cuda.compile, 
    pond_to_lake_cuda.compile
]
jit_precompile = [
    poi_based_jit.compile, 
    lake_to_pond_jit.compile, 
    pond_to_lake_jit.compile
]
