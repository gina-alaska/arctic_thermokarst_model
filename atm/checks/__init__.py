import  check_CLC_WT 
import  check_FCP_WT 
import  check_HCP_WT 
import  check_Lakes_WT 
import  check_Lakes 
import  check_LCP_WT 
import  check_Meadow_WT 
import  check_Ponds_WT 
import  check_Ponds 
import  check_water_climate 
import  check_Wet_CLC 
import  check_Wet_FCP 
import  check_Wet_HCP 
import  check_Wet_LCP 
import  check_Wet_NPG 

import lake_pond_expansion

import check_base

    
check_metadata = {
        
        'base': check_base.check_base,
        'poi': check_base.check_base,

        'lake_pond_expansion': lake_pond_expansion.lake_pond_expansion,
        'pond_infill': lake_pond_expansion.pond_infill,

      
        
        
        
        
        ### NOTE: 17 Oct 2016. The following are place holders
        ### until we figure out if/how these sets of cohorts
        ### can transition into other cohorts.
        #~ 'CoastalWaters_WT_O': check_CoastalWaters_WT.check_CoastalWaters_WT_O,
        #~ 'DrainedSlope_WT_Y': check_DrainedSlope_WT.check_DrainedSlope_WT_Y,
        #~ 'DrainedSlope_WT_M': check_DrainedSlope_WT.check_DrainedSlope_WT_M,
        #~ 'DrainedSlope_WT_O': check_DrainedSlope_WT.check_DrainedSlope_WT_O,
        #~ 'NoData_WT_O': check_NoData_WT.check_NoData_WT_O,
        #~ 'SandDunes_WT_Y': check_SandDunes_WT.check_SandDunes_WT_Y,
        #~ 'SandDunes_WT_M': check_SandDunes_WT.check_SandDunes_WT_M,
        #~ 'SandDunes_WT_O': check_SandDunes_WT.check_SandDunes_WT_O,
        #~ 'SaturatedBarrens_WT_Y': check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_Y,
        #~ 'SaturatedBarrens_WT_M': check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_M,
        #~ 'check_SaturatedBarrens_WT_O': check_SaturatedBarrens_WT.check_SaturatedBarrens_WT_O,
        #~ 'Shrubs_WT_O': check_Shrubs_WT.check_Shrubs_WT_O,
        #~ 'Urban_WT': check_Urban_WT.check_Urban_WT,
        
        
        ### Note: 17 Oct 2016. The following checks are pretty much obsolete
        ### at this point. Will clean up once everything is working well.
        #~ 'Wet_NPG': check_Wet_NPG.check_Wet_NPG,
        #~ 'Wet_LCP': check_Wet_LCP.check_Wet_LCP,
        #~ 'Wet_CLC': check_Wet_CLC.check_Wet_CLC,
        #~ 'Wet_FCP': check_Wet_FCP.check_Wet_FCP,
        #~ 'Wet_HCP': check_Wet_HCP.check_Wet_HCP,
        
        
        
        'check_Ponds_WT_Y': check_Ponds_WT.check_Ponds_WT_Y,
        'check_Ponds_WT_M': check_Ponds_WT.check_Ponds_WT_M,
        'check_Ponds_WT_O': check_Ponds_WT.check_Ponds_WT_O,
        'check_Ponds_WT_NA': check_Ponds_WT.check_Ponds_WT_NA,
        
        'check_LargeLakes_WT_Y': check_Lakes_WT.check_LargeLakes_WT_Y,
        'check_LargeLakes_WT_M': check_Lakes_WT.check_LargeLakes_WT_M,
        'check_LargeLakes_WT_O': check_Lakes_WT.check_LargeLakes_WT_O,
        'check_LargeLakes_WT_NA': check_Lakes_WT.check_LargeLakes_WT_NA,
        
        'check_MediumLakes_WT_Y': check_Lakes_WT.check_MediumLakes_WT_Y,
        'check_MediumLakes_WT_M': check_Lakes_WT.check_MediumLakes_WT_M,
        'check_MediumLakes_WT_O': check_Lakes_WT.check_MediumLakes_WT_O,
        'check_MediumLakes_WT_NA': check_Lakes_WT.check_MediumLakes_WT_NA,
        
        'check_SmallLakes_WT_Y': check_Lakes_WT.check_SmallLakes_WT_Y,
        'check_SmallLakes_WT_M': check_Lakes_WT.check_SmallLakes_WT_M,
        'check_SmallLakes_WT_O': check_Lakes_WT.check_SmallLakes_WT_O,
        'check_SmallLakes_WT_NA': check_Lakes_WT.check_SmallLakes_WT_NA,
    } 
