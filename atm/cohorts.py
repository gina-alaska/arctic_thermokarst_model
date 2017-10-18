"""
cohorts
-------

metadata for cohorts

"""

# maps alternate name to the names used by ATM internally
#
# See Also
# --------
#   find_canon_name
CANON_COHORT_NAMES = {
    ('CoalescentLowCenterPolygon_WetlandTundra_Medium',): 'CLC_WT_M',
    ('CoalescentLowCenterPolygon_WetlandTundra_Old',): 'CLC_WT_O',
    ('CoalescentLowCenterPolygon_WetlandTundra_Young',): 'CLC_WT_Y',
    
    ('CoastalWaters_WetlandTundra_Old',): 'CoastalWaters_WT_O',
    
    ('DrainedSlope_WetlandTundra_Medium',): 'DrainedSlope_WT_M',
    ('DrainedSlope_WetlandTundra_Old',): 'DrainedSlope_WT_O',
    ('DrainedSlope_WetlandTundra_Young',): 'DrainedSlope_WT_Y',
    
    ('FlatCenterPolygon_WetlandTundra_Medium',): 'FCP_WT_M',
    ('FlatCenterPolygon_WetlandTundra_Old',): 'FCP_WT_O',
    ('FlatCenterPolygon_WetlandTundra_Young',): 'FCP_WT_Y',
    
    ('HighCenterPolygon_WetlandTundra_Medium',): 'HCP_WT_M',
    ('HighCenterPolygon_WetlandTundra_Old',): 'HCP_WT_O',
    ('HighCenterPolygon_WetlandTundra_Young',): 'HCP_WT_Y',
    
    ('LargeLakes_WetlandTundra_Medium',): 'LargeLakes_WT_M',
    ('LargeLakes_WetlandTundra_Old',): 'LargeLakes_WT_O',
    ('LargeLakes_WetlandTundra_Young',): 'LargeLakes_WT_Y',
    
    ('LowCenterPolygon_WetlandTundra_Medium',): 'LCP_WT_M',
    ('LowCenterPolygon_WetlandTundra_Old',): 'LCP_WT_O',
    ('LowCenterPolygon_WetlandTundra_Young',): 'LCP_WT_Y',
    
    ('Meadow_WetlandTundra_Medium',): 'Meadow_WT_M',
    ('Meadow_WetlandTundra_Old',): 'Meadow_WT_O',
    ('Meadow_WetlandTundra_Young',): 'Meadow_WT_Y',
    
    ('MediumLakes_WetlandTundra_Medium',): 'MediumLakes_WT_M ',
    ('MediumLakes_WetlandTundra_Old',): 'MediumLakes_WT_O',
    ('MediumLakes_WetlandTundra_Young',): 'MediumLakes_WT_Y' ,
    
    ('NoData_WetlandTundra_Old', ): 'NoData_WT_O',
    
    ('Ponds_WetlandTundra_Medium',): 'Ponds_WT_M',
    ('Ponds_WetlandTundra_Old',): 'Ponds_WT_O',
    ('Ponds_WetlandTundra_Young',): 'Ponds_WT_Y',
    
    ('Rivers_WetlandTundra_Medium',): 'Rivers_WT_M',
    ('Rivers_WetlandTundra_Old',): 'Rivers_WT_O',
    ('Rivers_WetlandTundra_Young',): 'Rivers_WT_Y',
    
    ('SandDunes_WetlandTundra_Medium',): 'SandDunes_WT_M',
    ('SandDunes_WetlandTundra_Old',): 'SandDunes_WT_O',
    ('SandDunes_WetlandTundra_Young',): 'SandDunes_WT_Y',
    
    ('SaturatedBarrens_WetlandTundra_Medium',): 'SaturatedBarrens_WT_M',
    ('SaturatedBarrens_WetlandTundra_Old',): 'SaturatedBarrens_WT_O',
    ('SaturatedBarrens_WetlandTundra_Young',): 'SaturatedBarrens_WT_Y',
    
    ('Shrubs_WetlandTundra_Old',): 'Shrubs_WT_O',
    
    ('SmallLakes_WetlandTundra_Medium',): 'SmallLakes_WT_M',
    ('SmallLakes_WetlandTundra_Old',): 'SmallLakes_WT_O',
    ('SmallLakes_WetlandTundra_Young',): 'SmallLakes_WT_Y',
    
    ('Urban_WetlandTundra_Old',): 'Urban_WetlandTundra_Old',
    
    ## barrow NO AGE STUFF ?? ask bob.
    ('Rivers',): 'Rivers',
    ('Ponds',): 'Ponds',
    ('Lakes',): 'Lakes',
    ('FlatCenter',): 'FCP',
    ('Urban',): 'Urban',
    ('Meadows',): 'Meadows',
    ('CoalescentLowCenter',): 'CLC',
    ('HighCenter',) : 'HCP',
    
    ## Tanana flats
    ('OldBog',): 'TF_OB',
    ('OldFen',): 'TF_OF',
    ('Coniferous_PermafrostPlateau',): 'TF_Con_PP',
    ('Deciduous_PermafrostPlateau',): 'TF_Dec_PP',
    ('ThermokarstLake',): 'TF_TL',
    ('YoungBog',): 'TF_YB',
    ('YoungFen',): 'TF_YF',
    
    ## Yukon Flats
    ('Barren_Yukon',): 'Barren_Yukon',
    ('Bog_Yukon',): 'Bog_Yukon',
    ('DeciduousForest_Yukon',): 'DeciduousForest_Yukon',
    ('DwarfShrub_Yukon',): 'DwarfShrub_Yukon',
    ('EvergreenForest_Yukon',): 'EvergreenForest_Yukon',
    ('Fen_Yukon',): 'Fen_Yukon',
    ('Lake_Yukon',): 'Lake_Yukon',
    ('Pond_Yukon',): 'Pond_Yukon',
    ('River_Yukon',): 'River_Yukon',
    ('ShrubScrub_Yukon',): 'ShrubScrub_Yukon',
    ('Unclassified_Yukon',): 'Unclassified_Yukon',
}

def find_canon_name (name):
    """find canonical name of cohort given an alternate name
    
    Parameters
    ----------
    name: str
        the alternative name
        
    Raises
    ------
    KeyError
        if canon name not found
    
    Returns
    -------
    Str
        Canon name of cohort
    """
    ## is name a canon name
    if name in CANON_COHORT_NAMES.values():
        return name
    
    ## loop to find canon name
    for alt_names in CANON_COHORT_NAMES:
        if name in alt_names:
            return CANON_COHORT_NAMES[alt_names]
    raise KeyError, 'No canon cohort name for exists ' + name 



DISPLAY_COHORT_NAMES = {
    'CLC_WT_M': 'Coalescent Low Center Polygon Wetland Tundra Medium Age',
    'CLC_WT_O': 'Coalescent Low Center Polygon Wetland Tundra Old Age',
    'CLC_WT_Y': 'Coalescent Low Center Polygon Wetland Tundra Young Age',
    
    'CoastalWaters_WT_O': 'Coastal Waters Wetland Tundra Old Age',
    
    'DrainedSlope_WT_M': 'Drained Slope Wetland Tundra Medium Age',
    'DrainedSlope_WT_O': 'Drained Slope Wetland Tundra Old Age',
    'DrainedSlope_WT_Y': 'Drained Slope Wetland Tundra Young Age',
    
    'FCP_WT_M': 'Flat Center Poloygon Wetland Tundra Medium Age',
    'FCP_WT_O': 'Flat Center Poloygon Wetland Tundra Old Age',
    'FCP_WT_Y': 'Flat Center Poloygon Wetland Tundra Young Age',
    
    'HCP_WT_M': 'High Center Poloygon Wetland Tundra Medium Age',
    'HCP_WT_O': 'High Center Poloygon Wetland Tundra Old Age',
    'HCP_WT_Y': 'High Center Poloygon Wetland Tundra Young Age',
    
    'LargeLakes_WT_M': 'Large Lakes Wetland Tundra Medium Age',
    'LargeLakes_WT_O': 'Large Lakes Wetland Tundra Old Age',
    'LargeLakes_WT_Y': 'Large Lakes Wetland Tundra Young Age',
    
    'LCP_WT_M': 'Low Center Poloygon Wetland Tundra Medium Age',
    'LCP_WT_O': 'Low Center Poloygon Wetland Tundra Old Age',
    'LCP_WT_Y': 'Low Center Poloygon Wetland Tundra Young Age',
    
    'Meadow_WT_M': 'Medow Wetland Tundra Medium Age',
    'Meadow_WT_O': 'Medow Wetland Tundra Old Age',
    'Meadow_WT_Y': 'Medow Wetland Tundra Young Age',
    
    'MediumLakes_WT_M ': 'Medium Lakes Wetland Tundra Medium Age',
    'MediumLakes_WT_O': 'Medium Lakes Wetland Tundra Old Age',
    'MediumLakes_WT_Y' : 'Medium Lakes Wetland Tundra Young Age',
    
    'NoData_WT_O': 'No Data Wetland Tundra Old Age',
    
    'Ponds_WT_M': 'Ponds Wetland Tundra Medium Age',
    'Ponds_WT_O': 'Ponds Wetland Tundra Old Age',
    'Ponds_WT_Y': 'Ponds Wetland Tundra Young Age',
    
    'Rivers_WT_M': 'Rivers Wetland Tundra Medium Age',
    'Rivers_WT_O': 'Rivers Wetland Tundra Old Age',
    'Rivers_WT_Y': 'Rivers Wetland Tundra Young Age',
    
    'SandDunes_WT_M': 'Sand Dunes Wetland Tundra Medium Age',
    'SandDunes_WT_O': 'Sand Dunes Wetland Tundra Old Age',
    'SandDunes_WT_Y': 'Sand Dunes Wentland Tundra Young Age',
    
    'SaturatedBarrens_WT_M': 'Saturate Barrens Wetland Turnda Medium Age',
    'SaturatedBarrens_WT_O': 'Saturate Barrens Wetland Turnda Old Age',
    'SaturatedBarrens_WT_Y': 'Saturate Barrens Wetland Turnda Young Age',
    
    'Shrubs_WT_O': 'Shurbs Wetland Tundra Old Age',
    
    'SmallLakes_WT_M': 'Small Lakes Wetland Tundra Medium Age',
    'SmallLakes_WT_O': 'Small Lakes Wetland Tundra Old Age',
    'SmallLakes_WT_Y': 'Small Lakes Wetland Tundra Young Age',
    
    'Urban_WetlandTundra_Old': 'Urban Wetland Tundra Old Age',
    
    ## barrow NO AGE STUFF ?? ask bob.
    'Rivers': 'Rivers',
    'Ponds': 'Ponds',
    'Lakes': 'Lakes',
    'FCP': 'Flat Center Pologon',
    'Urban': 'Urban',
    'Meadows': 'Meadows',
    'CLC': 'Coalescent Low Center Polygon',
    'HCP': 'High Center Pologon',
    
    ## Tanana flats
    'TF_OB': 'Old Bog Tanana Flats',
    'TF_OF': 'Old Fen Tanana Flats',
    'TF_Con_PP': 'Coniferous Permafrost Plateau Tanana Flats',
    'TF_Dec_PP': 'Deciduous Permafrost Plateau Tanana Flats',
    'TF_TL': 'Thermokarst Lake Tanana Flats',
    'TF_YB': 'Young Bog Tanana Flats',
    'TF_YF': 'Young FenTanana Flats',
    
    ## Yukon Flats
    'Barren_Yukon': 'Barren Yukon Flats',
    'Bog_Yukon': 'Bog Yukon Flats',
    'DeciduousForest_Yukon': 'Deciduous Forest Yukon Flats',
    'DwarfShrub_Yukon': 'Dwar fShrubYukon Flats',
    'EvergreenForest_Yukon': 'Evergreen Forest Yukon Flats',
    'Fen_Yukon': 'Fen Yukon Flats',
    'Lake_Yukon': 'Lake Yukon Flats',
    'Pond_Yukon': 'Pond Yukon Flats',
    'River_Yukon': 'River Yukon Flats',
    'ShrubScrub_Yukon': 'Shrub Scrub Yukon Flats',
    'Unclassified_Yukon': 'Unclassified Yukon Flats',
}




### BOBS old code, To Be moved
import numpy as np

def initial_barrow(self):
#    self.Init_Wet_NPG = np.sum(self.ATTM_Wet_NPG)
#    self.Init_Wet_LCP = np.sum(self.ATTM_Wet_LCP)
#    self.Init_Wet_CLC = np.sum(self.ATTM_Wet_CLC)
#    self.Init_Wet_FCP = np.sum(self.ATTM_Wet_FCP)
#    self.Init_Wet_HCP = np.sum(self.ATTM_Wet_HCP)
#    self.Init_Ponds   = np.sum(self.ATTM_Ponds)
#    self.Init_Lakes   = np.sum(self.ATTM_Lakes)
    self.Init_CLC_WT_Y = np.sum(self.ATTM_CLC_WT_Y)
    self.Init_CLC_WT_M = np.sum(self.ATTM_CLC_WT_M)
    self.Init_CLC_WT_O = np.sum(self.ATTM_CLC_WT_O)
    self.Init_CoastalWaters_WT_O = np.sum(self.ATTM_CoastalWaters_WT_O)
    self.Init_DrainedSlope_WT_Y = np.sum(self.ATTM_DrainedSlope_WT_Y)
    self.Init_DrainedSlope_WT_M = np.sum(self.ATTM_DrainedSlope_WT_M)
    self.Init_DrainedSlope_WT_O = np.sum(self.ATTM_DrainedSlope_WT_O)
    self.Init_FCP_WT_Y = np.sum(self.ATTM_FCP_WT_Y)
    self.Init_FCP_WT_M = np.sum(self.ATTM_FCP_WT_M)
    self.Init_FCP_WT_O = np.sum(self.ATTM_FCP_WT_O)
    self.Init_HCP_WT_Y = np.sum(self.ATTM_HCP_WT_Y)
    self.Init_HCP_WT_M = np.sum(self.ATTM_HCP_WT_M)
    self.Init_HCP_WT_O = np.sum(self.ATTM_HCP_WT_O)
    self.Init_LCP_WT_Y = np.sum(self.ATTM_LCP_WT_Y)
    self.Init_LCP_WT_M = np.sum(self.ATTM_LCP_WT_M)
    self.Init_LCP_WT_O = np.sum(self.ATTM_LCP_WT_O)
    self.Init_Meadow_WT_Y = np.sum(self.ATTM_Meadow_WT_Y)
    self.Init_Meadow_WT_M = np.sum(self.ATTM_Meadow_WT_M)
    self.Init_Meadow_WT_O = np.sum(self.ATTM_Meadow_WT_O)
    self.Init_NoData_WT_O = np.sum(self.ATTM_NoData_WT_O)
    self.Init_SandDunes_WT_Y = np.sum(self.ATTM_SandDunes_WT_Y)
    self.Init_SandDunes_WT_M = np.sum(self.ATTM_SandDunes_WT_M)
    self.Init_SandDunes_WT_O = np.sum(self.ATTM_SandDunes_WT_O)
    self.Init_SaturatedBarrens_WT_Y = np.sum(self.ATTM_SaturatedBarrens_WT_Y)
    self.Init_SaturatedBarrens_WT_M = np.sum(self.ATTM_SaturatedBarrens_WT_M)
    self.Init_SaturatedBarrens_WT_O = np.sum(self.ATTM_SaturatedBarrens_WT_O)
    self.Init_Shrubs_WT_O = np.sum(self.ATTM_Shrubs_WT_O)
    self.Init_Urban_WT = np.sum(self.ATTM_Urban_WT)
    self.Init_LargeLakes_WT_Y = np.sum(self.ATTM_LargeLakes_WT_Y)
    self.Init_LargeLakes_WT_M = np.sum(self.ATTM_LargeLakes_WT_M)
    self.Init_LargeLakes_WT_O = np.sum(self.ATTM_LargeLakes_WT_O)
    self.Init_MediumLakes_WT_Y = np.sum(self.ATTM_MediumLakes_WT_Y)
    self.Init_MediumLakes_WT_M = np.sum(self.ATTM_MediumLakes_WT_M)
    self.Init_MediumLakes_WT_O = np.sum(self.ATTM_MediumLakes_WT_O)
    self.Init_SmallLakes_WT_Y = np.sum(self.ATTM_SmallLakes_WT_Y)
    self.Init_SmallLakes_WT_M = np.sum(self.ATTM_SmallLakes_WT_M)
    self.Init_SmallLakes_WT_O = np.sum(self.ATTM_SmallLakes_WT_O)
    self.Init_Ponds_WT_Y = np.sum(self.ATTM_Ponds_WT_Y)
    self.Init_Ponds_WT_M = np.sum(self.ATTM_Ponds_WT_M)
    self.Init_Ponds_WT_O = np.sum(self.ATTM_Ponds_WT_O)
    self.Init_Rivers_WT_Y = np.sum(self.ATTM_Rivers_WT_Y)
    self.Init_Rivers_WT_M = np.sum(self.ATTM_Rivers_WT_M)
    self.Init_Rivers_WT_O = np.sum(self.ATTM_Rivers_WT_O)
def initial_tanana(self):
    self.Init_TF_OB     = np.sum(self.ATTM_TF_OB)
    self.Init_TF_YB     = np.sum(self.ATTM_TF_YB)
    self.Init_TF_OF     = np.sum(self.ATTM_TF_OF)
    self.Init_TF_YF     = np.sum(self.ATTM_TF_YF)
    self.Init_TF_Dec_PP = np.sum(self.ATTM_TF_Dec_PP)
    self.Init_TF_Con_PP = np.sum(self.ATTM_TF_Con_PP)
    self.Init_TF_TL     = np.sum(self.ATTM_TF_TL)

def final_barrow(self):
    self.Final_CLC_WT_Y = np.sum(self.ATTM_CLC_WT_Y)
    self.Final_CLC_WT_M = np.sum(self.ATTM_CLC_WT_M)
    self.Final_CLC_WT_O = np.sum(self.ATTM_CLC_WT_O)
    self.Final_CoastalWaters_WT_O = np.sum(self.ATTM_CoastalWaters_WT_O)
    self.Final_DrainedSlope_WT_Y = np.sum(self.ATTM_DrainedSlope_WT_Y)
    self.Final_DrainedSlope_WT_M = np.sum(self.ATTM_DrainedSlope_WT_M)
    self.Final_DrainedSlope_WT_O = np.sum(self.ATTM_DrainedSlope_WT_O)
    self.Final_FCP_WT_Y = np.sum(self.ATTM_FCP_WT_Y)
    self.Final_FCP_WT_M = np.sum(self.ATTM_FCP_WT_M)
    self.Final_FCP_WT_O = np.sum(self.ATTM_FCP_WT_O)
    self.Final_HCP_WT_Y = np.sum(self.ATTM_HCP_WT_Y)
    self.Final_HCP_WT_M = np.sum(self.ATTM_HCP_WT_M)
    self.Final_HCP_WT_O = np.sum(self.ATTM_HCP_WT_O)
    self.Final_LCP_WT_Y = np.sum(self.ATTM_LCP_WT_Y)
    self.Final_LCP_WT_M = np.sum(self.ATTM_LCP_WT_M)
    self.Final_LCP_WT_O = np.sum(self.ATTM_LCP_WT_O)
    self.Final_Meadow_WT_Y = np.sum(self.ATTM_Meadow_WT_Y)
    self.Final_Meadow_WT_M = np.sum(self.ATTM_Meadow_WT_M)
    self.Final_Meadow_WT_O = np.sum(self.ATTM_Meadow_WT_O)
    self.Final_NoData_WT_O = np.sum(self.ATTM_NoData_WT_O)
    self.Final_SandDunes_WT_Y = np.sum(self.ATTM_SandDunes_WT_Y)
    self.Final_SandDunes_WT_M = np.sum(self.ATTM_SandDunes_WT_M)
    self.Final_SandDunes_WT_O = np.sum(self.ATTM_SandDunes_WT_O)
    self.Final_SaturatedBarrens_WT_Y = np.sum(self.ATTM_SaturatedBarrens_WT_Y)
    self.Final_SaturatedBarrens_WT_M = np.sum(self.ATTM_SaturatedBarrens_WT_M)
    self.Final_SaturatedBarrens_WT_O = np.sum(self.ATTM_SaturatedBarrens_WT_O)
    self.Final_Shrubs_WT_O = np.sum(self.ATTM_Shrubs_WT_O)
    self.Final_Urban_WT = np.sum(self.ATTM_Urban_WT)
    self.Final_LargeLakes_WT_Y = np.sum(self.ATTM_LargeLakes_WT_Y)
    self.Final_LargeLakes_WT_M = np.sum(self.ATTM_LargeLakes_WT_M)
    self.Final_LargeLakes_WT_O = np.sum(self.ATTM_LargeLakes_WT_O)
    self.Final_MediumLakes_WT_Y = np.sum(self.ATTM_MediumLakes_WT_Y)
    self.Final_MediumLakes_WT_M = np.sum(self.ATTM_MediumLakes_WT_M)
    self.Final_MediumLakes_WT_O = np.sum(self.ATTM_MediumLakes_WT_O)
    self.Final_SmallLakes_WT_Y = np.sum(self.ATTM_SmallLakes_WT_Y)
    self.Final_SmallLakes_WT_M = np.sum(self.ATTM_SmallLakes_WT_M)
    self.Final_SmallLakes_WT_O = np.sum(self.ATTM_SmallLakes_WT_O)
    self.Final_Ponds_WT_Y = np.sum(self.ATTM_Ponds_WT_Y)
    self.Final_Ponds_WT_M = np.sum(self.ATTM_Ponds_WT_M)
    self.Final_Ponds_WT_O = np.sum(self.ATTM_Ponds_WT_O)
    self.Final_Rivers_WT_Y = np.sum(self.ATTM_Rivers_WT_Y)
    self.Final_Rivers_WT_M = np.sum(self.ATTM_Rivers_WT_M)
    self.Final_Rivers_WT_O = np.sum(self.ATTM_Rivers_WT_O)    
#    self.Final_Wet_NPG = np.sum(self.ATTM_Wet_NPG)
#    self.Final_Wet_LCP = np.sum(self.ATTM_Wet_LCP)
#    self.Final_Wet_CLC = np.sum(self.ATTM_Wet_CLC)
#    self.Final_Wet_FCP = np.sum(self.ATTM_Wet_FCP)
#    self.Final_Wet_HCP = np.sum(self.ATTM_Wet_HCP)
#    self.Final_Ponds   = np.sum(self.ATTM_Ponds)
#    self.Final_Lakes   = np.sum(self.ATTM_Lakes)


def final_tanana(self):
    self.Final_TF_OB     = np.sum(self.ATTM_TF_OB)
    self.Final_TF_YB     = np.sum(self.ATTM_TF_YB)
    self.Final_TF_OF     = np.sum(self.ATTM_TF_OF)
    self.Final_TF_YF     = np.sum(self.ATTM_TF_YF)
    self.Final_TF_Dec_PP = np.sum(self.ATTM_TF_Dec_PP)
    self.Final_TF_Con_PP = np.sum(self.ATTM_TF_Con_PP)
    self.Final_TF_TL     = np.sum(self.ATTM_TF_TL)
