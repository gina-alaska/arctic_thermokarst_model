import numpy as np
import os, sys
import datetime, time
from matplotlib.dates import date2num
from matplotlib.dates import num2date
from __init__ import __version__

import cohorts

def on_screen(self, start_time, end_time):
    """
    The purpose of this module is to compile simulation results
    and output to the terminal screen.
    """
    ########################################################################
    
    nl = '\n'
    long_divider = 69
    short_divider = 35
    string = ''
    string +=  ' '+ nl   
    string +=  ' '+ nl
    string +=  '=' * long_divider + nl
    string +=  '       Simulation Results         '+ nl
    string +=  '=' * long_divider+ nl
    string +=  'ATM version: '+str(__version__)+ nl
    string +=  'Simulation name: '+ self.control.Simulation_name+ nl
    string +=  'Start Date / Time : '+str( start_time)+ nl
    string +=  'End Date / Time : '+str(end_time)+ nl
    string +=  'Total Simulation Time (minutes): '+ str( (self.finish - self.start)/60.0) + nl
    if self.control.Archive_simulation:
        string +=  'Archive Status: Active'+ nl
        string +=  'Archive Name : '+str(self.control.Simulation_name)+ nl
    else:
        string +=  'Archive Status: Inactive'+ nl
    string +=  ' '+ nl
    string +=  'Number of time steps in the simulation: '+ str(self.stop)+ nl
    string +=  ' '+ nl
    string +=  '-' * short_divider+ nl
    string +=  ' Initial Cohort Information'+ nl
    string +=  '-' * short_divider+ nl
    string +=  'Outputs of Initial Cohort Distribution:'+ nl
    print self.control['Initialize_Control']
    if self.control['Initialize_Control']['Initial_Cohort_Distribution_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Figure']:
            string +=  '  Initial Meadow, Wetland Tundra, Young age Figure [Output/Barrow/Meadow_WT_Y]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_M_Figure']:
            string +=  '  Initial Meadow, Wetland Tundra, Medium age Figure [Output/Barrow/Meadow_WT_M]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_O_Figure']:
            string +=  '  Initial Meadow, Wetland Tundra, Old age Figure [Output/Barrow/Meadow_WT_O]'+ nl
        if self.control['Initialize_Control']['LCP_WT_Y_Figure']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/LCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['LCP_WT_M_Figure']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/LCP_WT_M]'+ nl
        if self.control['Initialize_Control']['LCP_WT_O_Figure']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/LCP_WT_O]'+ nl
        if self.control['Initialize_Control']['CLC_WT_Y_Figure']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/CLC_WT_Y]'+ nl
        if self.control['Initialize_Control']['CLC_WT_M_Figure']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/CLC_WT_M]'+ nl
        if self.control['Initialize_Control']['CLC_WT_O_Figure']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/CLC_WT_O]'+ nl
        if self.control['Initialize_Control']['FCP_WT_Y_Figure']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/FCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['FCP_WT_M_Figure']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/FCP_WT_M]'+ nl
        if self.control['Initialize_Control']['FCP_WT_O_Figure']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/FCP_WT_O]'+ nl
        if self.control['Initialize_Control']['HCP_WT_Y_Figure']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/HCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['HCP_WT_M_Figure']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/HCP_WT_M]'+ nl
        if self.control['Initialize_Control']['HCP_WT_O_Figure']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/HCP_WT_O]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Figure']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/LargeLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_M_Figure']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/LargeLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_O_Figure']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/LargeLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Figure']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/MediumLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_M_Figure']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/MediumLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_O_Figure']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/MediumLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Figure']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/SmallLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_M_Figure']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/SmallLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_O_Figure']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/SmallLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_Y_Figure']:
            string +=  '  Initial Ponds, Wetland Tundra, Young age Figure [Output/Barrow/Ponds_WT_Y]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_M_Figure']:
            string +=  '  Initial Ponds, Wetland Tundra, Medium age Figure [Output/Barrow/Ponds_WT_M]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_O_Figure']:
            string +=  '  Initial Ponds, Wetland Tundra, Old age Figure [Output/Barrow/Ponds_WT_O]'+ nl
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Figure']:
            string +=  '  Initial Coastal Waters, Wetland Tundra, Old age Figure [Output/Barrow/CoastalWaters_WT_O]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Figure']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Young age Figure [Output/Barrow/DrainedSlope_WT_Y]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Figure']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Medium age Figure [Output/Barrow/DrainedSlope_WT_M]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Figure']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Old age Figure [Output/Barrow/DrainedSlope_WT_O]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_Y_Figure']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Young age Figure [Output/Barrow/SandDunes/WT_Y]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_M_Figure']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Medium age Figure [Output/Barrow/SandDunes_WT_M]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_O_Figure']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Old age Figure [Output/Barrow/SandDunes_WT_O]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Figure']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Young age Figure [Output/Barrow/SaturatedBarrens_WT_Y]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Figure']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Medium age Figure [Output/Barrow/SaturatedBarrens_WT_M]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Figure']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Old age Figure [Output/Barrow/SaturatedBarrens_WT_O]'+ nl
        if self.control['Initialize_Control']['Shrubs_WT_O_Figure']:
            string +=  '  Initial Shrubs, Wetland Tundra, Old age Figure [Output/Barrow/Shrubs_WT_O]'+ nl
        if self.control['Initialize_Control']['Urban_WT_Figure']:
            string +=  '  Initial Urban area, Wetland Tundra, Figure [Output/Barrow/Urban_WT]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_Y_Figure']:
            string +=  '  Initial Rivers, Wetland Tundra, Young age Figure [Output/Barrow/Rivers_WT_Y]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_M_Figure']:
            string +=  '  Initial Rivers, Wetland Tundra, Medium age Figure [Output/Barrow/Rivers_WT_M]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_O_Figure']:
            string +=  '  Initial Rivers, Wetland Tundra, old age Figure [Output/Barrow/Rivers_WT_O]'+ nl
        
#        if self.control['Initialize_Control']['WetNPG_Figure']:
#            string +=  '  Initial Wetland Non-polygonal Ground Figure [Output/Wet_NPG]'
#        if self.control['Initialize_Control']['WetLCP_Figure']:
#            string +=  '  Initial Wetland Low Center Polygon Figure [Output/Wet_LCP]'
#        if self.control['Initialize_Control']['WetCLC_Figure']:
#            string +=  '  Initial Wetland Coalescent Low Center Polygon Figure [Output/Wet_CLC]'
#        if self.control['Initialize_Control']['WetFCP_Figure']:
#            string +=  '  Initial Wetland Flat Center Polygon Figure [Output/Wet_FCP]'
#        if self.control['Initialize_Control']['WetHCP_Figure']:
#            string +=  '  Initial Wetland High Center Polygon Figure [Output/Wet_HCP]'
#        if self.control['Initialize_Control']['Lakes_Figure']:
#            string +=  '  Initial Lakes Figure [Output/Lakes]'
#        if self.control['Initialize_Control']['Ponds_Figure']:
#            string +=  '  Initial Ponds Figure [Output/Ponds]'
#        if self.control['Initialize_Control']['Rivers_Figure']:
#            string +=  '  Initial Rivers Figure [Output/Other_Cohorts]'
#        if self.control['Initialize_Control']['Urban_Figure']:
#            string +=  '  Initial Urban Figure [Output/Other_Cohorts]'
        if self.control['Initialize_Control']['All_Cohorts_Figure']:
            string +=  '  Total Cohorts Figure [Output/Barrow/All_Cohorts]'+ nl
    string +=  ' '+ nl

    string +=  'Outputs of Normalized Cohort Distribution:'+ nl
    if self.control['Initialize_Control']['Normalized_Cohort_Distribution_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Normal']:
            string +=  '  Initial Meadow, Wetland Tundra, Young age Normalized [Output/Barrow/Meadow_WT_Y]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_M_Normal']:
            string +=  '  Initial Meadow, Wetland Tundra, Medium age Normalized [Output/Barrow/Meadow_WT_M]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_O_Normal']:
            string +=  '  Initial Meadow, Wetland Tundra, Old age Normalized [Output/Barrow/Meadow_WT_O]'+ nl
        if self.control['Initialize_Control']['LCP_WT_Y_Normal']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/LCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['LCP_WT_M_Normal']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/LCP_WT_M]'+ nl
        if self.control['Initialize_Control']['LCP_WT_O_Normal']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/LCP_WT_O]'+ nl
        if self.control['Initialize_Control']['CLC_WT_Y_Normal']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/CLC_WT_Y]'+ nl
        if self.control['Initialize_Control']['CLC_WT_M_Normal']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/CLC_WT_M]'+ nl
        if self.control['Initialize_Control']['CLC_WT_O_Normal']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/CLC_WT_O]'+ nl
        if self.control['Initialize_Control']['FCP_WT_Y_Normal']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/FCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['FCP_WT_M_Normal']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/FCP_WT_M]'+ nl
        if self.control['Initialize_Control']['FCP_WT_O_Normal']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/FCP_WT_O]'+ nl
        if self.control['Initialize_Control']['HCP_WT_Y_Normal']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/HCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['HCP_WT_M_Normal']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/HCP_WT_M]'+ nl
        if self.control['Initialize_Control']['HCP_WT_O_Normal']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/HCP_WT_O]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Normal']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/LargeLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_M_Normal']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/LargeLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_O_Normal']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/LargeLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Normal']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/MediumLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_M_Normal']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/MediumLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_O_Normal']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/MediumLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Normal']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/SmallLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_M_Normal']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/SmallLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_O_Normal']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/SmallLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_Y_Normal']:
            string +=  '  Initial Ponds, Wetland Tundra, Young age Normalized [Output/Barrow/Ponds_WT_Y]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_M_Normal']:
            string +=  '  Initial Ponds, Wetland Tundra, Medium age Normalized [Output/Barrow/Ponds_WT_M]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_O_Normal']:
            string +=  '  Initial Ponds, Wetland Tundra, Old age Normalized [Output/Barrow/Ponds_WT_O]'+ nl
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Normal']:
            string +=  '  Initial Coastal Waters, Wetland Tundra, Old age Normalized [Output/Barrow/CoastalWaters_WT_O]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Normal']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Young age Normalized [Output/Barrow/DrainedSlope_WT_Y]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Normal']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Medium age Normalized [Output/Barrow/DrainedSlope_WT_M]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Normal']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Old age Normalized [Output/Barrow/DrainedSlope_WT_O]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_Y_Normal']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Young age Normalized [Output/Barrow/SandDunes/WT_Y]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_M_Normal']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Medium age Normalized [Output/Barrow/SandDunes_WT_M]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_O_Normal']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Old age Normalized [Output/Barrow/SandDunes_WT_O]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Normal']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Young age Normalized [Output/Barrow/SaturatedBarrens_WT_Y]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Normal']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Medium age Normalized [Output/Barrow/SaturatedBarrens_WT_M]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Normal']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Old age Normalized [Output/Barrow/SaturatedBarrens_WT_O]'+ nl
        if self.control['Initialize_Control']['Shrubs_WT_O_Normal']:
            string +=  '  Initial Shrubs, Wetland Tundra, Old age Normalized [Output/Barrow/Shrubs_WT_O]'+ nl
        if self.control['Initialize_Control']['Urban_WT_Normal']:
            string +=  '  Initial Urban area, Wetland Tundra, Normal [Output/Barrow/Urban_WT]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_Y_Normal']:
            string +=  '  Initial Rivers, Wetland Tundra, Young age Normalized [Output/Barrow/Rivers_WT_Y]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_M_Normal']:
            string +=  '  Initial Rivers, Wetland Tundra, Medium age Normalized [Output/Barrow/Rivers_WT_M]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_O_Normal']:
            string +=  '  Initial Rivers, Wetland Tundra, old age Normalized [Output/Barrow/Rivers_WT_O]'+ nl
        
        
#        if self.control['Initialize_Control']['WetNPG_Normal']:
#            string +=  '  Normalized Wetland Non-polygonal Ground Figure [Output/Wet_NPG]'
#        if self.control['Initialize_Control']['WetLCP_Normal']:
#            string +=  '  Normalized Wetland Low Center Polygon Figure [Output/Wet_LCP]'
#        if self.control['Initialize_Control']['WetCLC_Normal']:
#            string +=  '  Normalized Wetland Coalescent Low Center Polygon Figure [Output/Wet_CLC]'
#        if self.control['Initialize_Control']['WetFCP_Normal']:
#            string +=  '  Normalized Wetland Flat Center Polygon Figure [Output/Wet_FCP]'
#        if self.control['Initialize_Control']['WetHCP_Normal']:
#            string +=  '  Normalized Wetland High Center Polygon Figure [Output/Wet_HCP]'
#        if self.control['Initialize_Control']['Lakes_Normal']:
#            string +=  '  Normalized Lakes Figure [Output/Lakes]'
#        if self.control['Initialize_Control']['Ponds_Normal']:
#            string +=  '  Normalized Ponds Figure [Output/Ponds]'
#        if self.control['Initialize_Control']['Rivers_Normal']:
#            string +=  '  Normalized Rivers Figure [Output/Other_Cohorts]'
#        if self.control['Initialize_Control']['Urban_Normal']:
#            string +=  '  Normalized Urban Figure [Output/Other_Cohorts]'
        if self.control['Initialize_Control']['Total_Cohorts_Normal']:
            string +=  '  Normalize Total Cohorts [Output/All_Cohorts]'+ nl
    string +=  ' '+ nl

    string +=  'Outputs of Cohort Ages:'+ nl
    if self.control['Initialize_Control']['Initial_Cohort_Age_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Age']:
            string +=  '  Initial Meadow, Wetland Tundra, Young age distribution [Output/Barrow/Meadow_WT_Y]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_M_Age']:
            string +=  '  Initial Meadow, Wetland Tundra, Medium age distribution [Output/Barrow/Meadow_WT_M]'+ nl
        if self.control['Initialize_Control']['Meadow_WT_O_Age']:
            string +=  '  Initial Meadow, Wetland Tundra, Old age distribution [Output/Barrow/Meadow_WT_O]'+ nl
        if self.control['Initialize_Control']['LCP_WT_Y_Age']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/LCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['LCP_WT_M_Age']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/LCP_WT_M]'+ nl
        if self.control['Initialize_Control']['LCP_WT_O_Age']:
            string +=  '  Initial Low Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/LCP_WT_O]'+ nl
        if self.control['Initialize_Control']['CLC_WT_Y_Age']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/CLC_WT_Y]'+ nl
        if self.control['Initialize_Control']['CLC_WT_M_Age']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/CLC_WT_M]'+ nl
        if self.control['Initialize_Control']['CLC_WT_O_Age']:
            string +=  '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/CLC_WT_O]'+ nl
        if self.control['Initialize_Control']['FCP_WT_Y_Age']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/FCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['FCP_WT_M_Age']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/FCP_WT_M]'+ nl
        if self.control['Initialize_Control']['FCP_WT_O_Age']:
            string +=  '  Initial Flat Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/FCP_WT_O]'+ nl
        if self.control['Initialize_Control']['HCP_WT_Y_Age']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/HCP_WT_Y]'+ nl
        if self.control['Initialize_Control']['HCP_WT_M_Age']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/HCP_WT_M]'+ nl
        if self.control['Initialize_Control']['HCP_WT_O_Age']:
            string +=  '  Initial High Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/HCP_WT_O]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Age']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/LargeLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_M_Age']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/LargeLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['LargeLakes_WT_O_Age']:
            string +=  '  Initial Large (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/LargeLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Age']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/MediumLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_M_Age']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/MediumLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['MediumLakes_WT_O_Age']:
            string +=  '  Initial Medium (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/MediumLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Age']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/SmallLakes_WT_Y]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_M_Age']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/SmallLakes_WT_M]'+ nl
        if self.control['Initialize_Control']['SmallLakes_WT_O_Age']:
            string +=  '  Initial Small (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/SmallLakes_WT_O]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_Y_Age']:
            string +=  '  Initial Ponds, Wetland Tundra, Young age distribution [Output/Barrow/Ponds_WT_Y]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_M_Age']:
            string +=  '  Initial Ponds, Wetland Tundra, Medium age distribution [Output/Barrow/Ponds_WT_M]'+ nl
        if self.control['Initialize_Control']['Ponds_WT_O_Age']:
            string +=  '  Initial Ponds, Wetland Tundra, Old age distribution [Output/Barrow/Ponds_WT_O]'+ nl
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Age']:
            string +=  '  Initial Coastal Waters, Wetland Tundra, Old age distribution [Output/Barrow/CoastalWaters_WT_O]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Age']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Young age distribution [Output/Barrow/DrainedSlope_WT_Y]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Age']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Medium age distribution [Output/Barrow/DrainedSlope_WT_M]'+ nl
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Age']:
            string +=  '  Initial Drained Slope, Wetland Tundra, Old age distribution [Output/Barrow/DrainedSlope_WT_O]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_Y_Age']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Young age distribution [Output/Barrow/SandDunes/WT_Y]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_M_Age']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Medium age distribution [Output/Barrow/SandDunes_WT_M]'+ nl
        if self.control['Initialize_Control']['SandDunes_WT_O_Age']:
            string +=  '  Initial Sand Dunes, Wetland Tundra, Old age distribution [Output/Barrow/SandDunes_WT_O]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Age']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Young age distribution [Output/Barrow/SaturatedBarrens_WT_Y]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Age']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Medium age distribution [Output/Barrow/SaturatedBarrens_WT_M]'+ nl
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Age']:
            string +=  '  Initial Saturated Barrens, Wetland Tundra, Old age distribution [Output/Barrow/SaturatedBarrens_WT_O]'+ nl
        if self.control['Initialize_Control']['Shrubs_WT_O_Age']:
            string +=  '  Initial Shrubs, Wetland Tundra, Old age distribution [Output/Barrow/Shrubs_WT_O]'+ nl
        if self.control['Initialize_Control']['Urban_WT_Age']:
            string +=  '  Initial Urban area, Wetland Tundra, Normal [Output/Barrow/Urban_WT]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_Y_Age']:
            string +=  '  Initial Rivers, Wetland Tundra, Young age distribution [Output/Barrow/Rivers_WT_Y]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_M_Age']:
            string +=  '  Initial Rivers, Wetland Tundra, Medium age distribution [Output/Barrow/Rivers_WT_M]'+ nl
        if self.control['Initialize_Control']['Rivers_WT_O_Age']:
            string +=  '  Initial Rivers, Wetland Tundra, old age distribution [Output/Barrow/Rivers_WT_O]'+ nl

#        if self.control['Initialize_Control']['WetNPG_Age']:
#            string +=  '  Wetland Non-polygonal Ground Age [Output/Wet_NPG]'
#        if self.control['Initialize_Control']['WetLCP_Age']:
#            string +=  '  Wetland Low Center Polygon Age [Output/Wet_LCP]'
#        if self.control['Initialize_Control']['WetCLC_Age']:
#            string +=  '  Wetland Coalescent Low Center Polygon Age [Output/Wet_CLC]'
#        if self.control['Initialize_Control']['WetFCP_Age']:
#            string +=  '  Wetland Flat Center Polygon Age [Output/Wet_FCP]'
#        if self.control['Initialize_Control']['WetHCP_Age']:
#            string +=  '  Wetland High Center Polygon Age [Output/Wet_HCP]'
#        if self.control['Initialize_Control']['Lakes_Age']:
#            string +=  '  Lakes Age [Output/Lakes]'
#        if self.control['Initialize_Control']['Ponds_Age']:
#            string +=  '  Normalized Ponds Age [Output/Ponds]'
    string +=  ' '+ nl
    ##########################################################################
    string +=  '-' * short_divider+ nl
    string +=  '   Meteorologic Data Information   '+ nl
    string +=  '-' * short_divider+ nl
    if self.control.Met_Control['met_distribution'].lower() == 'point':
        string +=  'Point meteorologic data is used.'+ nl
    else:
        string +=  'Meteorologic data is distributed.'+ nl
    string +=  'Meteorologic Data File: '+ str(self.control.Met_Control['met_file_distributed'])+ nl
    if self.control.Met_Control['degree_day_method'].lower() == 'read':
        string +=  'Degree Days read from files: ' + self.control.Met_Control['TDD_file'] +' and '+self.control.Met_Control['FDD_file']+ nl
    else:
        string +=  'Degree Days calculated during simulation.'+ nl
    string +=  ' '+ nl

    string +=  'Outputs:'+ nl
    if self.control.Met_Control['Degree_Day_Output']:
        string +=  '  Degree-Days are output.'+ nl
        
    # Note: Might want to add climatic event probability and block size here
    ############################################################################
    string +=  '-' * short_divider+ nl
    string +=  '   General Terrestrial Information   '+ nl
    string +=  '-' * short_divider+ nl
    string +=  'Ground Ice Distribution: '+self.control.Terrestrial_Control['Ice_Distribution']+ nl
    string +=  'Drainage Efficiency Distribution: '+ self.control.Terrestrial_Control['Drainage_Efficiency_Distribution']+ nl
    string +=  'Initial Active Layer Depth Distribution: '+self.control.Terrestrial_Control['ALD_Distribution']+ nl
    string +=  ' '+ nl
    ## #________________________________________________________+ nl
    ## # Setting Protective Layer Factor Shorthand for results
    ## #________________________________________________________
    ## WNPG = self.control.Terrestrial_Control['Wet_NPG_PLF']
    ## WLCP = self.control.Terrestrial_Control['Wet_LCP_PLF']
    ## WCLC = self.control.Terrestrial_Control['Wet_CLC_PLF']
    ## WFCP = self.control.Terrestrial_Control['Wet_FCP_PLF']
    ## WHCP = self.control.Terrestrial_Control['Wet_HCP_PLF']
    ## GNPG = self.control.Terrestrial_Control['Gra_NPG_PLF']
    ## GLCP = self.control.Terrestrial_Control['Gra_LCP_PLF']
    ## GFCP = self.control.Terrestrial_Control['Gra_FCP_PLF']
    ## GHCP = self.control.Terrestrial_Control['Gra_HCP_PLF']
    ## SNPG = self.control.Terrestrial_Control['Shr_NPG_PLF']
    ## SLCP = self.control.Terrestrial_Control['Shr_LCP_PLF']
    ## SFCP = self.control.Terrestrial_Control['Shr_FCP_PLF']
    ## SHCP = self.control.Terrestrial_Control['Shr_HCP_PLF']
    ## LPLF = self.control.Terrestrial_Control['Lakes_PLF']
    ## PPLF = self.control.Terrestrial_Control['Ponds_PLF']
    ## #_________________________________________________________
    ## string +=  '__________________________________________________'
    ## string +=  '              Protective Layer Factors            '
    ## string +=  '__________________________________________________'
    ## string +=  '     | Wetland | Graminoid | Shrub | Lake | Pond |'
    ## string +=  '__________________________________________________'
    ## string +=  ' NPG |  '+str(WNPG)+'    |   '+str(GNPG)+'     | '+str(SNPG)+'   |  '+\
    ##   str(LPLF)+' | '+str(PPLF)+'  |'
    ## string +=  ' LCP |  '+str(WLCP)+'    |   '+str(GLCP)+'     | '+str(SLCP)+'   |  '+\
    ##   '--  | --   |'
    ## string +=  ' CLC |  '+str(WCLC)+'    |    --     |  --   |  '+\
    ##   '--  | --   |'
    ## string +=  ' FCP |  '+str(WFCP)+'   |   '+str(GFCP)+'    | '+str(SFCP)+'   |  '+\
    ##   '--  | --   |'
    ## string +=  ' HCP |  '+str(WHCP)+'    |   '+str(GHCP)+'     | '+str(SHCP)+'   |  '+\
    ##   '--  | --   |'
    ## string +=  '__________________________________________________'
    ## string +=  ' '
    ############################################################################
    start_year = self.control.start_year
    end_year =  self.control.start_year + self.stop - 1
    
    cohort_list = self.grids.area.key_to_index.keys()
    cohort_list = [c for c in cohort_list if c.find('--') == -1]
    
    all_ages = []
    nl = '\n'
    for cohort in sorted(cohort_list):
        cohort_type = cohort.split('_')[0]
        #~ string +=  not (cohort_type in all_ages)
        #~ string = ''
        if not (cohort_type in all_ages):
            string += '='*long_divider + nl
            string += '-'*short_divider  + nl
            string += cohort_type  + nl
            string += '-'*short_divider  + nl
            init_total = 0
            final_total = 0
            for c in sorted(cohort_list):
                if c.find(cohort_type) == -1:
                    continue
                init_total += self.grids.area[start_year,c].sum()
                final_total += self.grids.area[end_year,c].sum()
            string += 'Initial Fractional Area (km2): ' +  str(init_total)  + nl
            string += 'Final Fractional Area (km2): ' +  str(final_total)  + nl
            diff = final_total - init_total
            string += 'Total Fractional Change (km2): ' + str(diff)  + nl
            percent =  ((diff)/init_total)*100.
            string += 'Percent difference: ' + str(percent)  + nl
            string += ' '   + nl
            
            all_ages.append(cohort_type)
        
        string += '='*long_divider + nl
        string += '-'*short_divider + nl
        string += cohorts.DISPLAY_COHORT_NAMES[cohort]  + nl
        string += '-'*short_divider  + nl
        
        init_total = self.grids.area[start_year,cohort].sum()
        final_total = self.grids.area[end_year,cohort].sum()
        string += 'Initial Fractional Area (km2): ' +  str(init_total )  + nl
        string += 'Final Fractional Area (km2): ' +   str(final_total)  + nl
        diff = final_total - init_total
        string += 'Total Fractional Change (km2): ' + str(diff)  + nl
        percent =  ((diff)/init_total)*100.
        string += 'Percent difference: ' + str(percent)  + nl
        #~ string += ' '  + nl
        
    print string
    


############################################################################
###    string +=  '----------------------------------'
###    string +=  '        Simulation Notes '
###    string +=  '----------------------------------'
###    file = open(self.control['Run_dir']+self.Input_directory+str('/Notes/')+self.notes_file, 'r')
###    string +=  file.read()
###    file.close()
###    string +=  '----------------------------------'
###    string +=  ' '
#============================================================================================
#============================================================================================
def on_file(self, start_time, end_time):
    return
    if self.Simulation_area.lower() == 'barrow':
        file = open(self.control['Run_dir']+self.Output_directory+str('/Barrow/Archive/')+ \
            self.archive_time+str('_')+self.simulation_name+str('.txt'), 'a')
    elif self.Simulation_area.lower() == 'yukon':
         file = open(self.control['Run_dir']+self.Output_directory+str('/Yukon/Archive/')+ \
            self.archive_time+str('_')+self.simulation_name+str('.txt'), 'a')       
    elif self.Simulation_area.lower() == 'tanana':
         file = open(self.control['Run_dir']+self.Output_directory+str('/Tanana/Archive/')+ \
            self.archive_time+str('_')+self.simulation_name+str('.txt'), 'a')     
    

    file.write('=====================================================\n')
    file.write('       Simulation Results        \n')
    file.write('=====================================================\n')
    file.write('ATM version: '+  __version__ +str('\n'))
    file.write('Simulation name: '+ self.simulation_name +str('\n'))
    file.write('Start Date / Time : ' + start_time +str('\n'))
    file.write('End Date / Time : '+ end_time +str('\n'))
    file.write('Total Simulation Time (minutes): '+ str((end_time - start_time)/60.0) + str('\n'))
    if self.archive_simulation:
        file.write('Archive Status: Active \n')
        file.write('Archive Name : '+ self.simulation_name + str('\n'))
    else:
        file.write('Archive Status: Inactive \n')

    file.write('Number of time-steps in the simulation: '+str(self.stop)+str('\n'))
    file.write(' \n')
    ##########################################################################
    file.write( '-----------------------------------\n')
    file.write( ' Initial Cohort Information \n')
    file.write( '-----------------------------------\n')
    file.write( 'Outputs of Initial Cohort Distribution:\n')
    if self.control['Initialize_Control']['Initial_Cohort_Distribution_Figure'] == False:
        file.write( '  No outputs generated. \n')
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Figure']:
            file.write( '  Initial Meadow, Wetland Tundra, Young age Figure [Output/Barrow/Meadow_WT_Y] \n')
        if self.control['Initialize_Control']['Meadow_WT_M_Figure']:
            file.write( '  Initial Meadow, Wetland Tundra, Medium age Figure [Output/Barrow/Meadow_WT_M] \n')
        if self.control['Initialize_Control']['Meadow_WT_O_Figure']:
            file.write( '  Initial Meadow, Wetland Tundra, Old age Figure [Output/Barrow/Meadow_WT_O] \n')
        if self.control['Initialize_Control']['LCP_WT_Y_Figure']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/LCP_WT_Y] \n')
        if self.control['Initialize_Control']['LCP_WT_M_Figure']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/LCP_WT_M] \n')
        if self.control['Initialize_Control']['LCP_WT_O_Figure']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/LCP_WT_O] \n')
        if self.control['Initialize_Control']['CLC_WT_Y_Figure']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/CLC_WT_Y] \n')
        if self.control['Initialize_Control']['CLC_WT_M_Figure']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/CLC_WT_M] \n')
        if self.control['Initialize_Control']['CLC_WT_O_Figure']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/CLC_WT_O] \n')
        if self.control['Initialize_Control']['FCP_WT_Y_Figure']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/FCP_WT_Y] \n')
        if self.control['Initialize_Control']['FCP_WT_M_Figure']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/FCP_WT_M] \n')
        if self.control['Initialize_Control']['FCP_WT_O_Figure']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/FCP_WT_O] \n')
        if self.control['Initialize_Control']['HCP_WT_Y_Figure']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Young age Figure [Output/Barrow/HCP_WT_Y] \n')
        if self.control['Initialize_Control']['HCP_WT_M_Figure']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Medium age Figure [Output/Barrow/HCP_WT_M] \n')
        if self.control['Initialize_Control']['HCP_WT_O_Figure']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Old age Figure [Output/Barrow/HCP_WT_O] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Figure']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/LargeLakes_WT_Y] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_M_Figure']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/LargeLakes_WT_M] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_O_Figure']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/LargeLakes_WT_O] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Figure']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/MediumLakes_WT_Y] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_M_Figure']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/MediumLakes_WT_M] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_O_Figure']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/MediumLakes_WT_O] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Figure']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Young age Figure [Output/Barrow/SmallLakes_WT_Y] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_M_Figure']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Medium age Figure [Output/Barrow/SmallLakes_WT_M] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_O_Figure']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Old age Figure [Output/Barrow/SmallLakes_WT_O] \n')
        if self.control['Initialize_Control']['Ponds_WT_Y_Figure']:
            file.write( '  Initial Ponds, Wetland Tundra, Young age Figure [Output/Barrow/Ponds_WT_Y] \n')
        if self.control['Initialize_Control']['Ponds_WT_M_Figure']:
            file.write( '  Initial Ponds, Wetland Tundra, Medium age Figure [Output/Barrow/Ponds_WT_M] \n')
        if self.control['Initialize_Control']['Ponds_WT_O_Figure']:
            file.write( '  Initial Ponds, Wetland Tundra, Old age Figure [Output/Barrow/Ponds_WT_O] \n')
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Figure']:
            file.write( '  Initial Coastal Waters, Wetland Tundra, Old age Figure [Output/Barrow/CoastalWaters_WT_O] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Figure']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Young age Figure [Output/Barrow/DrainedSlope_WT_Y] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Figure']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Medium age Figure [Output/Barrow/DrainedSlope_WT_M] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Figure']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Old age Figure [Output/Barrow/DrainedSlope_WT_O] \n')
        if self.control['Initialize_Control']['SandDunes_WT_Y_Figure']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Young age Figure [Output/Barrow/SandDunes/WT_Y] \n')
        if self.control['Initialize_Control']['SandDunes_WT_M_Figure']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Medium age Figure [Output/Barrow/SandDunes_WT_M] \n')
        if self.control['Initialize_Control']['SandDunes_WT_O_Figure']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Old age Figure [Output/Barrow/SandDunes_WT_O] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Figure']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Young age Figure [Output/Barrow/SaturatedBarrens_WT_Y] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Figure']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Medium age Figure [Output/Barrow/SaturatedBarrens_WT_M] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Figure']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Old age Figure [Output/Barrow/SaturatedBarrens_WT_O] \n')
        if self.control['Initialize_Control']['Shrubs_WT_O_Figure']:
            file.write( '  Initial Shrubs, Wetland Tundra, Old age Figure [Output/Barrow/Shrubs_WT_O] \n')
        if self.control['Initialize_Control']['Urban_WT_Figure']:
            file.write( '  Initial Urban area, Wetland Tundra, Figure [Output/Barrow/Urban_WT] \n')
        if self.control['Initialize_Control']['Rivers_WT_Y_Figure']:
            file.write( '  Initial Rivers, Wetland Tundra, Young age Figure [Output/Barrow/Rivers_WT_Y] \n')
        if self.control['Initialize_Control']['Rivers_WT_M_Figure']:
            file.write( '  Initial Rivers, Wetland Tundra, Medium age Figure [Output/Barrow/Rivers_WT_M] \n')
        if self.control['Initialize_Control']['Rivers_WT_O_Figure']:
            file.write( '  Initial Rivers, Wetland Tundra, old age Figure [Output/Barrow/Rivers_WT_O] \n')
        if self.control['Initialize_Control']['All_Cohorts_Figure']:
            file.write( '  Total Cohorts Figure [Output/All_Cohorts] \n \n')
        
 #       if self.control['Initialize_Control']['WetNPG_Figure']:
 #           file.write( '  Initial Wetland Non-polygonal Ground Figure [Output/Wet_NPG] \n')
 #       if self.control['Initialize_Control']['WetLCP_Figure']:
 #           file.write( '  Initial Wetland Low Center Polygon Figure [Output/Wet_LCP] \n')
 #       if self.control['Initialize_Control']['WetCLC_Figure']:
 #           file.write( '  Initial Wetland Coalescent Low Center Polygon Figure [Output/Wet_CLC] \n')
 #       if self.control['Initialize_Control']['WetFCP_Figure']:
 #           file.write( '  Initial Wetland Flat Center Polygon Figure [Output/Wet_FCP] \n')
 #       if self.control['Initialize_Control']['WetHCP_Figure']:
 #           file.write( '  Initial Wetland High Center Polygon Figure [Output/Wet_HCP] \n')
 #       if self.control['Initialize_Control']['Lakes_Figure']:
 #           file.write( '  Initial Lakes Figure [Output/Lakes] \n')
 #       if self.control['Initialize_Control']['Ponds_Figure']:
 #           file.write( '  Initial Ponds Figure [Output/Ponds] \n')
 #       if self.control['Initialize_Control']['Rivers_Figure']:
 #           file.write( '  Initial Rivers Figure [Output/Other_Cohorts] \n')
 #       if self.control['Initialize_Control']['Urban_Figure']:
 #           file.write( '  Initial Urban Figure [Output/Other_Cohorts] \n')

    
    file.write( 'Outputs of Initial Cohort Fractional Distribution:\n')
        
    if self.control['Initialize_Control']['Normalized_Cohort_Distribution_Figure'] == False:
        file.write( '  No outputs generated. \n')
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Normal']:
            file.write( '  Initial Meadow, Wetland Tundra, Young age Normalized [Output/Barrow/Meadow_WT_Y] \n')
        if self.control['Initialize_Control']['Meadow_WT_M_Normal']:
            file.write( '  Initial Meadow, Wetland Tundra, Medium age Normalized [Output/Barrow/Meadow_WT_M] \n')
        if self.control['Initialize_Control']['Meadow_WT_O_Normal']:
            file.write( '  Initial Meadow, Wetland Tundra, Old age Normalized [Output/Barrow/Meadow_WT_O] \n')
        if self.control['Initialize_Control']['LCP_WT_Y_Normal']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/LCP_WT_Y] \n')
        if self.control['Initialize_Control']['LCP_WT_M_Normal']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/LCP_WT_M] \n')
        if self.control['Initialize_Control']['LCP_WT_O_Normal']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/LCP_WT_O] \n')
        if self.control['Initialize_Control']['CLC_WT_Y_Normal']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/CLC_WT_Y] \n')
        if self.control['Initialize_Control']['CLC_WT_M_Normal']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/CLC_WT_M] \n')
        if self.control['Initialize_Control']['CLC_WT_O_Normal']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/CLC_WT_O] \n')
        if self.control['Initialize_Control']['FCP_WT_Y_Normal']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/FCP_WT_Y] \n')
        if self.control['Initialize_Control']['FCP_WT_M_Normal']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/FCP_WT_M] \n')
        if self.control['Initialize_Control']['FCP_WT_O_Normal']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/FCP_WT_O] \n')
        if self.control['Initialize_Control']['HCP_WT_Y_Normal']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Young age Normalized [Output/Barrow/HCP_WT_Y] \n')
        if self.control['Initialize_Control']['HCP_WT_M_Normal']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Medium age Normalized [Output/Barrow/HCP_WT_M] \n')
        if self.control['Initialize_Control']['HCP_WT_O_Normal']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Old age Normalized [Output/Barrow/HCP_WT_O] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Normal']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/LargeLakes_WT_Y] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_M_Normal']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/LargeLakes_WT_M] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_O_Normal']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/LargeLakes_WT_O] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Normal']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/MediumLakes_WT_Y] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_M_Normal']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/MediumLakes_WT_M] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_O_Normal']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/MediumLakes_WT_O] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Normal']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Young age Normalized [Output/Barrow/SmallLakes_WT_Y] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_M_Normal']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Medium age Normalized [Output/Barrow/SmallLakes_WT_M] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_O_Normal']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Old age Normalized [Output/Barrow/SmallLakes_WT_O] \n')
        if self.control['Initialize_Control']['Ponds_WT_Y_Normal']:
            file.write( '  Initial Ponds, Wetland Tundra, Young age Normalized [Output/Barrow/Ponds_WT_Y] \n')
        if self.control['Initialize_Control']['Ponds_WT_M_Normal']:
            file.write( '  Initial Ponds, Wetland Tundra, Medium age Normalized [Output/Barrow/Ponds_WT_M] \n')
        if self.control['Initialize_Control']['Ponds_WT_O_Normal']:
            file.write( '  Initial Ponds, Wetland Tundra, Old age Normalized [Output/Barrow/Ponds_WT_O] \n')
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Normal']:
            file.write( '  Initial Coastal Waters, Wetland Tundra, Old age Normalized [Output/Barrow/CoastalWaters_WT_O] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Normal']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Young age Normalized [Output/Barrow/DrainedSlope_WT_Y] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Normal']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Medium age Normalized [Output/Barrow/DrainedSlope_WT_M] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Normal']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Old age Normalized [Output/Barrow/DrainedSlope_WT_O] \n')
        if self.control['Initialize_Control']['SandDunes_WT_Y_Normal']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Young age Normalized [Output/Barrow/SandDunes/WT_Y] \n')
        if self.control['Initialize_Control']['SandDunes_WT_M_Normal']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Medium age Normalized [Output/Barrow/SandDunes_WT_M] \n')
        if self.control['Initialize_Control']['SandDunes_WT_O_Normal']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Old age Normalized [Output/Barrow/SandDunes_WT_O] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Normal']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Young age Normalized [Output/Barrow/SaturatedBarrens_WT_Y] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Normal']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Medium age Normalized [Output/Barrow/SaturatedBarrens_WT_M] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Normal']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Old age Normalized [Output/Barrow/SaturatedBarrens_WT_O] \n')
        if self.control['Initialize_Control']['Shrubs_WT_O_Normal']:
            file.write( '  Initial Shrubs, Wetland Tundra, Old age Normalized [Output/Barrow/Shrubs_WT_O] \n')
        if self.control['Initialize_Control']['Urban_WT_Normal']:
            file.write( '  Initial Urban area, Wetland Tundra, Normal [Output/Barrow/Urban_WT] \n')
        if self.control['Initialize_Control']['Rivers_WT_Y_Normal']:
            file.write( '  Initial Rivers, Wetland Tundra, Young age Normalized [Output/Barrow/Rivers_WT_Y] \n')
        if self.control['Initialize_Control']['Rivers_WT_M_Normal']:
            file.write( '  Initial Rivers, Wetland Tundra, Medium age Normalized [Output/Barrow/Rivers_WT_M] \n')
        if self.control['Initialize_Control']['Rivers_WT_O_Normal']:
            file.write( '  Initial Rivers, Wetland Tundra, old age Normalized [Output/Barrow/Rivers_WT_O] \n')        

#        if self.control['Initialize_Control']['WetNPG_Normal']:
#            file.write( '  Normalized Wetland Non-polygonal Ground Figure [Output/Wet_NPG] \n')
#        if self.control['Initialize_Control']['WetLCP_Normal']:
#            file.write( '  Normalized Wetland Low Center Polygon Figure [Output/Wet_LCP] \n')
#        if self.control['Initialize_Control']['WetCLC_Normal']:
#            file.write( '  Normalized Wetland Coalescent Low Center Polygon Figure [Output/Wet_CLC] \n')
#        if self.control['Initialize_Control']['WetFCP_Normal']:
#            file.write( '  Normalized Wetland Flat Center Polygon Figure [Output/Wet_FCP] \n')
#        if self.control['Initialize_Control']['WetHCP_Normal']:
#            file.write( '  Normalized Wetland High Center Polygon Figure [Output/Wet_HCP] \n')
#        if self.control['Initialize_Control']['Lakes_Normal']:
#            file.write( '  Normalized Lakes Figure [Output/Lakes] \n')
#        if self.control['Initialize_Control']['Ponds_Normal']:
#            file.write( '  Normalized Ponds Figure [Output/Ponds] \n')
#        if self.control['Initialize_Control']['Rivers_Normal']:
#            file.write( '  Normalized Rivers Figure [Output/Other_Cohorts] \n')
#        if self.control['Initialize_Control']['Urban_Normal']:
#            file.write( '  Normalized Urban Figure [Output/Other_Cohorts] \n')
#        if self.control['Initialize_Control']['Total_Cohorts_Normal']:
#            file.write( '  Normalized Total Cohorts [Output/All_Cohorts] \n \n')

    file.write( 'Outputs of Initial Cohort Age:\n')
        
    if self.control['Initialize_Control']['Initial_Cohort_Age_Figure'] == False:
        file.write( '  No outputs generated. \n')
    else:
        if self.control['Initialize_Control']['Meadow_WT_Y_Age']:
            file.write( '  Initial Meadow, Wetland Tundra, Young age distribution [Output/Barrow/Meadow_WT_Y] \n')
        if self.control['Initialize_Control']['Meadow_WT_M_Age']:
            file.write( '  Initial Meadow, Wetland Tundra, Medium age distribution [Output/Barrow/Meadow_WT_M] \n')
        if self.control['Initialize_Control']['Meadow_WT_O_Age']:
            file.write( '  Initial Meadow, Wetland Tundra, Old age distribution [Output/Barrow/Meadow_WT_O] \n')
        if self.control['Initialize_Control']['LCP_WT_Y_Age']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/LCP_WT_Y] \n')
        if self.control['Initialize_Control']['LCP_WT_M_Age']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/LCP_WT_M] \n')
        if self.control['Initialize_Control']['LCP_WT_O_Age']:
            file.write( '  Initial Low Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/LCP_WT_O] \n')
        if self.control['Initialize_Control']['CLC_WT_Y_Age']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/CLC_WT_Y] \n')
        if self.control['Initialize_Control']['CLC_WT_M_Age']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/CLC_WT_M] \n')
        if self.control['Initialize_Control']['CLC_WT_O_Age']:
            file.write( '  Initial Coalescent Low Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/CLC_WT_O] \n')
        if self.control['Initialize_Control']['FCP_WT_Y_Age']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/FCP_WT_Y] \n')
        if self.control['Initialize_Control']['FCP_WT_M_Age']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/FCP_WT_M] \n')
        if self.control['Initialize_Control']['FCP_WT_O_Age']:
            file.write( '  Initial Flat Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/FCP_WT_O] \n')
        if self.control['Initialize_Control']['HCP_WT_Y_Age']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Young age distribution [Output/Barrow/HCP_WT_Y] \n')
        if self.control['Initialize_Control']['HCP_WT_M_Age']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Medium age distribution [Output/Barrow/HCP_WT_M] \n')
        if self.control['Initialize_Control']['HCP_WT_O_Age']:
            file.write( '  Initial High Center Polygon, Wetland Tundra, Old age distribution [Output/Barrow/HCP_WT_O] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_Y_Age']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/LargeLakes_WT_Y] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_M_Age']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/LargeLakes_WT_M] \n')
        if self.control['Initialize_Control']['LargeLakes_WT_O_Age']:
            file.write( '  Initial Large (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/LargeLakes_WT_O] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_Y_Age']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/MediumLakes_WT_Y] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_M_Age']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/MediumLakes_WT_M] \n')
        if self.control['Initialize_Control']['MediumLakes_WT_O_Age']:
            file.write( '  Initial Medium (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/MediumLakes_WT_O] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_Y_Age']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Young age distribution [Output/Barrow/SmallLakes_WT_Y] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_M_Age']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Medium age distribution [Output/Barrow/SmallLakes_WT_M] \n')
        if self.control['Initialize_Control']['SmallLakes_WT_O_Age']:
            file.write( '  Initial Small (size) Lakes, Wetland Tundra, Old age distribution [Output/Barrow/SmallLakes_WT_O] \n')
        if self.control['Initialize_Control']['Ponds_WT_Y_Age']:
            file.write( '  Initial Ponds, Wetland Tundra, Young age distribution [Output/Barrow/Ponds_WT_Y] \n')
        if self.control['Initialize_Control']['Ponds_WT_M_Age']:
            file.write( '  Initial Ponds, Wetland Tundra, Medium age distribution [Output/Barrow/Ponds_WT_M] \n')
        if self.control['Initialize_Control']['Ponds_WT_O_Age']:
            file.write( '  Initial Ponds, Wetland Tundra, Old age distribution [Output/Barrow/Ponds_WT_O] \n')
        if self.control['Initialize_Control']['CoastalWaters_WT_O_Age']:
            file.write( '  Initial Coastal Waters, Wetland Tundra, Old age distribution [Output/Barrow/CoastalWaters_WT_O] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_Y_Age']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Young age distribution [Output/Barrow/DrainedSlope_WT_Y] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_M_Age']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Medium age distribution [Output/Barrow/DrainedSlope_WT_M] \n')
        if self.control['Initialize_Control']['DrainedSlope_WT_O_Age']:
            file.write( '  Initial Drained Slope, Wetland Tundra, Old age distribution [Output/Barrow/DrainedSlope_WT_O] \n')
        if self.control['Initialize_Control']['SandDunes_WT_Y_Age']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Young age distribution [Output/Barrow/SandDunes/WT_Y] \n')
        if self.control['Initialize_Control']['SandDunes_WT_M_Age']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Medium age distribution [Output/Barrow/SandDunes_WT_M] \n')
        if self.control['Initialize_Control']['SandDunes_WT_O_Age']:
            file.write( '  Initial Sand Dunes, Wetland Tundra, Old age distribution [Output/Barrow/SandDunes_WT_O] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_Y_Age']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Young age distribution [Output/Barrow/SaturatedBarrens_WT_Y] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_M_Age']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Medium age distribution [Output/Barrow/SaturatedBarrens_WT_M] \n')
        if self.control['Initialize_Control']['SaturatedBarrens_WT_O_Age']:
            file.write( '  Initial Saturated Barrens, Wetland Tundra, Old age distribution [Output/Barrow/SaturatedBarrens_WT_O] \n')
        if self.control['Initialize_Control']['Shrubs_WT_O_Age']:
            file.write( '  Initial Shrubs, Wetland Tundra, Old age distribution [Output/Barrow/Shrubs_WT_O] \n')
        if self.control['Initialize_Control']['Urban_WT_Age']:
            file.write( '  Initial Urban area, Wetland Tundra, Normal [Output/Barrow/Urban_WT] \n')
        if self.control['Initialize_Control']['Rivers_WT_Y_Age']:
            file.write( '  Initial Rivers, Wetland Tundra, Young age distribution [Output/Barrow/Rivers_WT_Y] \n')
        if self.control['Initialize_Control']['Rivers_WT_M_Age']:
            file.write( '  Initial Rivers, Wetland Tundra, Medium age distribution [Output/Barrow/Rivers_WT_M] \n')
        if self.control['Initialize_Control']['Rivers_WT_O_Age']:
            file.write( '  Initial Rivers, Wetland Tundra, old age distribution [Output/Barrow/Rivers_WT_O] \n')        
        
#        if self.control['Initialize_Control']['WetNPG_Age']:
#            file.write( '  Wetland Non-polygonal Ground Age [Output/Wet_NPG] \n')
#        if self.control['Initialize_Control']['WetLCP_Age']:
#            file.write( '  Wetland Low Center Polygon Age [Output/Wet_LCP] \n')
#        if self.control['Initialize_Control']['WetCLC_Age']:
#            file.write( '  Wetland Coalescent Low Center Polygon Age [Output/Wet_CLC] \n')
#        if self.control['Initialize_Control']['WetFCP_Age']:
#            file.write( '  Wetland Flat Center Polygon Age [Output/Wet_FCP] \n')
#        if self.control['Initialize_Control']['WetHCP_Age']:
#            file.write( '  Wetland High Center Polygon Age [Output/Wet_HCP] \n')
#        if self.control['Initialize_Control']['Lakes_Age']:
#            file.write( '  Lakes Age [Output/Lakes] \n')
#        if self.control['Initialize_Control']['Ponds_Age']:
#            file.write( '  Ponds Age [Output/Ponds] \n \n')
    
    ##########################################################################    
    file.write( '====================================================\n')
    file.write( '        Meteorologic Data Information               \n')
    file.write( '====================================================\n')
    if self.control.Met_Control['met_distribution'].lower() == 'point':
        file.write( 'Point meteorologic data is used. \n')
    else:
        file.write( 'Meteorologic data is distributed. \n')
    file.write( 'Meteorologic Data File: '+ self.control.Met_Control['met_file_distributed'] + str('\n'))
    if self.control.Met_Control['degree_day_method'].lower() == 'read':
        file.write('Degree Days read from files: '+ self.control.Met_Control['TDD_file'] +' and '+ \
                   self.control.Met_Control['FDD_file'] +str('\n'))
    else:
        file.write( 'Degree Days calculated during simulation. \n')
    file.write( ' \n')
    
    file.write( 'Output: \n')
    if self.control.Met_Control['Degree_Day_Output']:
        file.write('  Degree-days are output. \n')
        
    # Note: Might want to add climatic event probability and block size here
    ############################################################################
    file.write( '====================================================\n')
    file.write( '           General Terrestrial Information          \n')
    file.write( '====================================================\n')
    file.write( 'Ground Ice distribution: '+str(self.control.Terrestrial_Control['Ice_Distribution'])+str('\n'))
    file.write( 'Drainage efficiency distribution: '+ \
                str(self.control.Terrestrial_Control['Drainage_Efficiency_Distribution'])+str('\n'))
    file.write( 'Initial Active Layer Depth Distribution: '+ \
                str(self.control.Terrestrial_Control['ALD_Distribution'])+str('\n \n'))
    #-------------------------------------------------------------------------
    file.write( '- - - - - - - - - - - - - - - - - - - - - - - - - -\n')
    file.write( 'Protective Layer Factors        \n')
    file.write( '  Meadow, Wetland Tundra, Young age:   ' + str(self.control.Terrestrial_Control['Meadow_WT_Y_PLF']) + str(' \n'))
    file.write( '  Meadow, Wetland Tundra, Medium age:  ' + str(self.control.Terrestrial_Control['Meadow_WT_M_PLF']) + str(' \n'))
    file.write( '  Meadow, Wetland Tundra, Old age:     ' + str(self.control.Terrestrial_Control['Meadow_WT_O_PLF']) + str(' \n'))
    file.write( '  Low Center Polygon, Wetland Tundra, Young age:  ' + str(self.control.Terrestrial_Control['LCP_WT_Y_PLF']) + str(' \n'))
    file.write( '  Low Center Polygon, Wetland Tundra, Medium age: ' + str(self.control.Terrestrial_Control['LCP_WT_M_PLF']) + str(' \n'))
    file.write( '  Low Center Polygon, Wetland Tundra, Old age:    ' + str(self.control.Terrestrial_Control['LCP_WT_O_PLF']) + str(' \n'))
    file.write( '  Coalescent Low Center Polygon, Wetland Tundra, Young age: ' + str(self.control.Terrestrial_Control['CLC_WT_Y_PLF']) + str('\n'))
    file.write( '  Coalescent Low Center Polygon, Wetland Tundra, Medium age: ' + str(self.control.Terrestrial_Control['CLC_WT_M_PLF'])+ str('\n'))
    file.write( '  Coalescent Low Center Polygon, Wetland Tundra, Old age: ' + str(self.control.Terrestrial_Control['CLC_WT_O_PLF']) + str('\n'))
    file.write( '  Flat Center Polygon, Wetland Tundra, Young age: ' + str(self.control.Terrestrial_Control['FCP_WT_Y_PLF']) + str('\n'))
    file.write( '  Flat Center Polygon, Wetland Tundra, Medium age: ' + str(self.control.Terrestrial_Control['FCP_WT_M_PLF']) + str('\n'))
    file.write( '  Flat Center Polygon, Wetland Tundra, Old age: ' +str(self.control.Terrestrial_Control['FCP_WT_O_PLF']) + str('\n'))
    file.write( '  High Center Polygon, Wetland Tundra, Young age: ' + str(self.control.Terrestrial_Control['HCP_WT_Y_PLF'])+str('\n'))
    file.write( '  High Center Polygon, Wetland Tundra, Medium age: ' + str(self.control.Terrestrial_Control['HCP_WT_M_PLF'])+str('\n'))
    file.write( '  High Center Polygon, Wetland Tundra, Old age: '+ str(self.control.Terrestrial_Control['HCP_WT_O_PLF'])+str('\n'))
    file.write( '  Large Lakes, Wetland Tundra, Young age: ' + str(self.control.Terrestrial_Control['LargeLakes_WT_Y_PLF']) + str('\n'))
    file.write( '  Large Lakes, Wetland Tundra, Medium age: ' + str(self.control.Terrestrial_Control['LargeLakes_WT_M_PLF']) + str('\n'))
    file.write( '  Large Lakes, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['LargeLakes_WT_O_PLF'])+str('\n'))
    file.write( '  Medium Lakes, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['MediumLakes_WT_Y_PLF'])+str('\n'))
    file.write( '  Medium Lakes, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['MediumLakes_WT_M_PLF'])+str('\n'))
    file.write( '  Medium Lakes, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['MediumLakes_WT_O_PLF'])+str('\n'))
    file.write( '  Small Lakes, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['SmallLakes_WT_Y_PLF'])+str('\n'))
    file.write( '  Small Lakes, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['SmallLakes_WT_M_PLF'])+str('\n'))
    file.write( '  Small Lakes, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['SmallLakes_WT_O_PLF'])+str('\n'))
    file.write( '  Ponds, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['Ponds_WT_Y_PLF'])+str('\n'))
    file.write( '  Ponds, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['Ponds_WT_M_PLF'])+str('\n'))
    file.write( '  Ponds, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['Ponds_WT_O_PLF'])+str('\n'))
    file.write( '  Rivers, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['Rivers_WT_Y_PLF'])+str('\n'))
    file.write( '  Rivers, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['Rivers_WT_M_PLF'])+str('\n'))
    file.write( '  Rivers, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['Rivers_WT_O_PLF'])+str('\n'))
    file.write( '  Drained Slope, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['DrainedSlope_WT_Y_PLF'])+str('\n'))
    file.write( '  Drained Slope, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['DrainedSlope_WT_M_PLF'])+str('\n'))
    file.write( '  Drained Slope, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['DrainedSlope_WT_O_PLF'])+str('\n'))
    file.write( '  Coastal Waters, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['CoastalWaters_WT_O_PLF'])+str('\n'))
    file.write( '  Sand Dunes, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['SandDunes_WT_Y_PLF'])+str('\n'))
    file.write( '  Sand Dunes, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['SandDunes_WT_M_PLF'])+str('\n'))
    file.write( '  Sand Dunes, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['SandDunes_WT_O_PLF'])+str('\n'))
    file.write( '  Saturated Barrens, Wetland Tundra, Young age: '+str(self.control.Terrestrial_Control['SaturatedBarrens_WT_Y_PLF'])+str('\n'))
    file.write( '  Saturated Barrens, Wetland Tundra, Medium age: '+str(self.control.Terrestrial_Control['SaturatedBarrens_WT_M_PLF'])+str('\n'))
    file.write( '  Saturated Barrens, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['SaturatedBarrens_WT_O_PLF'])+str('\n'))
    file.write( '  Shrubs, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['Shrubs_WT_O_PLF'])+str('\n'))
    file.write( '  No Data, Wetland Tundra, Old age: '+str(self.control.Terrestrial_Control['NoData_WT_O_PLF'])+str('\n'))
    file.write( '  Urban, Wetland Tundra: '+str(self.control.Terrestrial_Control['Urban_WT_PLF'])+str('\n'))

    file.write( '- - - - - - - - - - - - - - - - - - - - - - - - - -\n')

        
    file.write( '\nOutput: \n')
    if self.control.Terrestrial_Control['Ice_Distribution_Figure']:
        file.write('  Initial Ice Distribution Figure \n')
    if self.control.Terrestrial_Control['Drainage_Efficiency_Figure']:
        file.write('  Drainage Efficiency Figure \n')
    if self.control.Terrestrial_Control['ALD_Distribution_Output']:
        file.write('  Initial Active Layer Depth Figure \n')
    if self.control.Terrestrial_Control['ALD_Factor_Output']:
        file.write('  Active Layer Factor Figure \n')
    file.write( '- - - - - - - - - - - - - - - - - - - - - - - - - -\n \n')
    
    ############################################################################
        
    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Meadows (Non polygonal ground) \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Meadows, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_Meadow_WT_Y + self.Init_Meadow_WT_M + self.Init_Meadow_WT_O
    final_total = self.Final_Meadow_WT_Y + self.Final_Meadow_WT_M + self.Final_Meadow_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Meadows, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Meadow_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Meadow_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Meadow_WT_Y - self.Init_Meadow_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Meadow_WT_Y - self.Init_Meadow_WT_Y)/self.Init_Meadow_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.Meadow_WT_Y['POI_Function']) + str('\n'))
    if self.Meadow_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.Meadow_WT_Y['A1_above'])+\
                   ' | '+str(self.Meadow_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.Meadow_WT_Y['A2_above'])+\
                   ' | '+str(self.Meadow_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.Meadow_WT_Y['x0_above'])+\
                   ' | '+str(self.Meadow_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.Meadow_WT_Y['dx_above'])+\
                   ' | '+str(self.Meadow_WT_Y['dx_below'])+str('\n \n'))
    elif self.Meadow_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.Meadow_WT_Y['a_above'])+\
                   str(' | ')+str(self.Meadow_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.Meadow_WT_Y['b_above']) +\
                   str(' | ')+str(self.Meadow_WT_Y['b_below'])+str('\n \n'))
    elif self.Meadow_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.Meadow_WT_Y['K_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.Meadow_WT_Y['C_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.Meadow_WT_Y['A_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_Y['B_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['B_below'])+str('\n \n'))
    elif self.Meadow_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.Meadow_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.Meadow_WT_Y['HillN_below'])+str('\n \n'))
                   
    file.write(' Maximum rate of terrain transition: '+str(self.Meadow_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.Meadow_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.Meadow_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.Meadow_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.Meadow_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.Meadow_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.Meadow_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.Meadow_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.Meadow_WT_Y['Figures'].lower() == 'no' and self.Meadow_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '===========================================================\n')
    file.write('\n')
    file.write( '----------------------------------- \n')
    file.write( ' Meadows, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_Meadow_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Meadow_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Meadow_WT_M - self.Init_Meadow_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Meadow_WT_M - self.Init_Meadow_WT_M)/self.Init_Meadow_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.Meadow_WT_M['POI_Function']) + str('\n'))
    if self.Meadow_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.Meadow_WT_M['A1_above'])+\
                   ' | '+str(self.Meadow_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.Meadow_WT_M['A2_above'])+\
                   ' | '+str(self.Meadow_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.Meadow_WT_M['x0_above'])+\
                   ' | '+str(self.Meadow_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.Meadow_WT_M['dx_above'])+\
                   ' | '+str(self.Meadow_WT_M['dx_below'])+str('\n \n'))
    elif self.Meadow_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.Meadow_WT_M['a_above'])+\
                   str(' | ')+str(self.Meadow_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.Meadow_WT_M['b_above']) +\
                   str(' | ')+str(self.Meadow_WT_M['b_below'])+str('\n \n'))
    elif self.Meadow_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.Meadow_WT_M['K_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.Meadow_WT_M['C_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.Meadow_WT_M['A_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_M['B_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['B_below'])+str('\n \n'))
    elif self.Meadow_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.Meadow_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.Meadow_WT_M['HillN_below'])+str('\n \n'))
                   
    file.write(' Maximum rate of terrain transition: '+str(self.Meadow_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.Meadow_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.Meadow_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.Meadow_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.Meadow_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.Meadow_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.Meadow_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.Meadow_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.Meadow_WT_M['Figures'].lower() == 'no' and self.Meadow_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
    file.write( '----------------------------------- \n')
    file.write( ' Meadows, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Meadow_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_Meadow_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_Meadow_WT_O - self.Init_Meadow_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Meadow_WT_O - self.Init_Meadow_WT_O)/self.Init_Meadow_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.Meadow_WT_O['POI_Function']) + str('\n'))
    if self.Meadow_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.Meadow_WT_O['A1_above'])+\
                   ' | '+str(self.Meadow_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.Meadow_WT_O['A2_above'])+\
                   ' | '+str(self.Meadow_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.Meadow_WT_O['x0_above'])+\
                   ' | '+str(self.Meadow_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.Meadow_WT_O['dx_above'])+\
                   ' | '+str(self.Meadow_WT_O['dx_below'])+str('\n \n'))
    elif self.Meadow_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.Meadow_WT_O['a_above'])+\
                   str(' | ')+str(self.Meadow_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.Meadow_WT_O['b_above']) +\
                   str(' | ')+str(self.Meadow_WT_O['b_below'])+str('\n \n'))
    elif self.Meadow_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.Meadow_WT_O['K_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.Meadow_WT_O['C_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.Meadow_WT_O['A_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_O['B_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['B_below'])+str('\n \n'))
    elif self.Meadow_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.Meadow_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.Meadow_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.Meadow_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.Meadow_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.Meadow_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.Meadow_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.Meadow_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.Meadow_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.Meadow_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.Meadow_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.Meadow_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.Meadow_WT_O['Figures'].lower() == 'no' and self.Meadow_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Low Center Polygons \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Low Center Polygons, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_LCP_WT_Y + self.Init_LCP_WT_M + self.Init_LCP_WT_O
    final_total = self.Final_LCP_WT_Y + self.Final_LCP_WT_M + self.Final_LCP_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Low Center Polygons, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_LCP_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_LCP_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_LCP_WT_Y - self.Init_LCP_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LCP_WT_Y - self.Init_LCP_WT_Y)/self.Init_LCP_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.LCP_WT_Y['POI_Function']) + str('\n'))
    if self.LCP_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.LCP_WT_Y['A1_above'])+\
                   ' | '+str(self.LCP_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.LCP_WT_Y['A2_above'])+\
                   ' | '+str(self.LCP_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.LCP_WT_Y['x0_above'])+\
                   ' | '+str(self.LCP_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.LCP_WT_Y['dx_above'])+\
                   ' | '+str(self.LCP_WT_Y['dx_below'])+str('\n \n'))
    elif self.LCP_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.LCP_WT_Y['a_above'])+\
                   str(' | ')+str(self.LCP_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.LCP_WT_Y['b_above']) +\
                   str(' | ')+str(self.LCP_WT_Y['b_below'])+str('\n \n'))
    elif self.LCP_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.LCP_WT_Y['K_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.LCP_WT_Y['C_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.LCP_WT_Y['A_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_Y['B_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['B_below'])+str('\n \n'))
    elif self.LCP_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.LCP_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.LCP_WT_Y['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.LCP_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.LCP_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.LCP_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.LCP_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.LCP_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.LCP_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.LCP_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.LCP_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.LCP_WT_Y['Figures'].lower() == 'no' and self.LCP_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


        
    file.write( '----------------------------------- \n')
    file.write( ' Low Center Polygons, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_LCP_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_LCP_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_LCP_WT_M - self.Init_LCP_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LCP_WT_M - self.Init_LCP_WT_M)/self.Init_LCP_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.LCP_WT_M['POI_Function']) + str('\n'))
    if self.LCP_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.LCP_WT_M['A1_above'])+\
                   ' | '+str(self.LCP_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.LCP_WT_M['A2_above'])+\
                   ' | '+str(self.LCP_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.LCP_WT_M['x0_above'])+\
                   ' | '+str(self.LCP_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.LCP_WT_M['dx_above'])+\
                   ' | '+str(self.LCP_WT_M['dx_below'])+str('\n \n'))
    elif self.LCP_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.LCP_WT_M['a_above'])+\
                   str(' | ')+str(self.LCP_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.LCP_WT_M['b_above']) +\
                   str(' | ')+str(self.LCP_WT_M['b_below'])+str('\n \n'))
    elif self.LCP_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.LCP_WT_M['K_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.LCP_WT_M['C_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.LCP_WT_M['A_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_M['B_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['B_below'])+str('\n \n'))
    elif self.LCP_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.LCP_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.LCP_WT_M['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.LCP_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.LCP_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.LCP_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.LCP_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.LCP_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.LCP_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.LCP_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.LCP_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.LCP_WT_M['Figures'].lower() == 'no' and self.LCP_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

        
    file.write( '----------------------------------- \n')
    file.write( ' Low Center Polygons, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_LCP_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_LCP_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_LCP_WT_O - self.Init_LCP_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LCP_WT_O - self.Init_LCP_WT_O)/self.Init_LCP_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.LCP_WT_O['POI_Function']) + str('\n'))
    if self.LCP_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.LCP_WT_O['A1_above'])+\
                   ' | '+str(self.LCP_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.LCP_WT_O['A2_above'])+\
                   ' | '+str(self.LCP_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.LCP_WT_O['x0_above'])+\
                   ' | '+str(self.LCP_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.LCP_WT_O['dx_above'])+\
                   ' | '+str(self.LCP_WT_O['dx_below'])+str('\n \n'))
    elif self.LCP_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.LCP_WT_O['a_above'])+\
                   str(' | ')+str(self.LCP_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.LCP_WT_O['b_above']) +\
                   str(' | ')+str(self.LCP_WT_O['b_below'])+str('\n \n'))
    elif self.LCP_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.LCP_WT_O['K_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.LCP_WT_O['C_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.LCP_WT_O['A_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_O['B_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['B_below'])+str('\n \n'))
    elif self.LCP_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.LCP_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.LCP_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.LCP_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.LCP_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.LCP_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.LCP_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.LCP_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.LCP_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.LCP_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.LCP_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.LCP_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.LCP_WT_O['Figures'].lower() == 'no' and self.LCP_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Coalescent Low Center Polygons \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Coalescent Low Center Polygons, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_CLC_WT_Y + self.Init_CLC_WT_M + self.Init_CLC_WT_O
    final_total = self.Final_CLC_WT_Y + self.Final_CLC_WT_M + self.Final_CLC_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Coalescent Low Center Polygons, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_CLC_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_CLC_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_CLC_WT_Y - self.Init_CLC_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_CLC_WT_Y - self.Init_CLC_WT_Y)/self.Init_CLC_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.CLC_WT_Y['POI_Function']) + str('\n'))
    if self.CLC_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.CLC_WT_Y['A1_above'])+\
                   ' | '+str(self.CLC_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.CLC_WT_Y['A2_above'])+\
                   ' | '+str(self.CLC_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.CLC_WT_Y['x0_above'])+\
                   ' | '+str(self.CLC_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.CLC_WT_Y['dx_above'])+\
                   ' | '+str(self.CLC_WT_Y['dx_below'])+str('\n \n'))
    elif self.CLC_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.CLC_WT_Y['a_above'])+\
                   str(' | ')+str(self.CLC_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.CLC_WT_Y['b_above']) +\
                   str(' | ')+str(self.CLC_WT_Y['b_below'])+str('\n \n'))
    elif self.CLC_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.CLC_WT_Y['K_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.CLC_WT_Y['C_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.CLC_WT_Y['A_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_Y['B_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['B_below'])+str('\n \n'))
    elif self.CLC_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.CLC_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.CLC_WT_Y['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.CLC_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.CLC_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.CLC_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.CLC_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.CLC_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.CLC_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.CLC_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.CLC_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.CLC_WT_Y['Figures'].lower() == 'no' and self.CLC_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '----------------------------------- \n')
    file.write( ' Coalescent Low Center Polygons, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_CLC_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_CLC_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_CLC_WT_M - self.Init_CLC_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_CLC_WT_M - self.Init_CLC_WT_M)/self.Init_CLC_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.CLC_WT_M['POI_Function']) + str('\n'))
    if self.CLC_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.CLC_WT_M['A1_above'])+\
                   ' | '+str(self.CLC_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.CLC_WT_M['A2_above'])+\
                   ' | '+str(self.CLC_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.CLC_WT_M['x0_above'])+\
                   ' | '+str(self.CLC_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.CLC_WT_M['dx_above'])+\
                   ' | '+str(self.CLC_WT_M['dx_below'])+str('\n \n'))
    elif self.CLC_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.CLC_WT_M['a_above'])+\
                   str(' | ')+str(self.CLC_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.CLC_WT_M['b_above']) +\
                   str(' | ')+str(self.CLC_WT_M['b_below'])+str('\n \n'))
    elif self.CLC_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.CLC_WT_M['K_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.CLC_WT_M['C_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.CLC_WT_M['A_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_M['B_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['B_below'])+str('\n \n'))
    elif self.CLC_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.CLC_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.CLC_WT_M['HillN_below'])+str('\n \n'))
                   
    file.write(' Maximum rate of terrain transition: '+str(self.CLC_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.CLC_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.CLC_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.CLC_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.CLC_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.CLC_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.CLC_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.CLC_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.CLC_WT_M['Figures'].lower() == 'no' and self.CLC_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '----------------------------------- \n')
    file.write( ' Coalescent Low Center Polygons, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_CLC_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_CLC_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_CLC_WT_O - self.Init_CLC_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_CLC_WT_O - self.Init_CLC_WT_O)/self.Init_CLC_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.CLC_WT_O['POI_Function']) + str('\n'))
    if self.CLC_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.CLC_WT_O['A1_above'])+\
                   ' | '+str(self.CLC_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.CLC_WT_O['A2_above'])+\
                   ' | '+str(self.CLC_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.CLC_WT_O['x0_above'])+\
                   ' | '+str(self.CLC_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.CLC_WT_O['dx_above'])+\
                   ' | '+str(self.CLC_WT_O['dx_below'])+str('\n \n'))
    elif self.CLC_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.CLC_WT_O['a_above'])+\
                   str(' | ')+str(self.CLC_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.CLC_WT_O['b_above']) +\
                   str(' | ')+str(self.CLC_WT_O['b_below'])+str('\n \n'))
    elif self.CLC_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.CLC_WT_O['K_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.CLC_WT_O['C_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.CLC_WT_O['A_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_O['B_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['B_below'])+str('\n \n'))
    elif self.CLC_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.CLC_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.CLC_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.CLC_WT_O['HillN_below'])+str('\n \n'))

                   
    file.write(' Maximum rate of terrain transition: '+str(self.CLC_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.CLC_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.CLC_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.CLC_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.CLC_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.CLC_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.CLC_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.CLC_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.CLC_WT_O['Figures'].lower() == 'no' and self.CLC_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        

    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Flat Center Polygons \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Flat Center Polygons, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_FCP_WT_Y + self.Init_FCP_WT_M + self.Init_FCP_WT_O
    final_total = self.Final_FCP_WT_Y + self.Final_FCP_WT_M + self.Final_FCP_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Flat Center Polygons, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_FCP_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_FCP_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_FCP_WT_Y - self.Init_FCP_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_FCP_WT_Y - self.Init_FCP_WT_Y)/self.Init_FCP_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.FCP_WT_Y['POI_Function']) + str('\n'))
    if self.FCP_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.FCP_WT_Y['A1_above'])+\
                   ' | '+str(self.FCP_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.FCP_WT_Y['A2_above'])+\
                   ' | '+str(self.FCP_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.FCP_WT_Y['x0_above'])+\
                   ' | '+str(self.FCP_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.FCP_WT_Y['dx_above'])+\
                   ' | '+str(self.FCP_WT_Y['dx_below'])+str('\n \n'))
    elif self.FCP_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.FCP_WT_Y['a_above'])+\
                   str(' | ')+str(self.FCP_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.FCP_WT_Y['b_above']) +\
                   str(' | ')+str(self.FCP_WT_Y['b_below'])+str('\n \n'))
    elif self.FCP_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.FCP_WT_Y['K_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.FCP_WT_Y['C_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.FCP_WT_Y['A_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_Y['B_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['B_below'])+str('\n \n'))
    elif self.FCP_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.FCP_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.FCP_WT_Y['HillN_below'])+str('\n \n'))

                   
    file.write(' Maximum rate of terrain transition: '+str(self.FCP_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.FCP_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.FCP_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.FCP_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.FCP_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.FCP_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.FCP_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.FCP_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.FCP_WT_Y['Figures'].lower() == 'no' and self.FCP_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        



    file.write( '----------------------------------- \n')
    file.write( ' Flat Center Polygons, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_FCP_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_FCP_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_FCP_WT_M - self.Init_FCP_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_FCP_WT_M - self.Init_FCP_WT_M)/self.Init_FCP_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.FCP_WT_M['POI_Function']) + str('\n'))
    if self.FCP_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.FCP_WT_M['A1_above'])+\
                   ' | '+str(self.FCP_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.FCP_WT_M['A2_above'])+\
                   ' | '+str(self.FCP_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.FCP_WT_M['x0_above'])+\
                   ' | '+str(self.FCP_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.FCP_WT_M['dx_above'])+\
                   ' | '+str(self.FCP_WT_M['dx_below'])+str('\n \n'))
    elif self.FCP_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.FCP_WT_M['a_above'])+\
                   str(' | ')+str(self.FCP_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.FCP_WT_M['b_above']) +\
                   str(' | ')+str(self.FCP_WT_M['b_below'])+str('\n \n'))
    elif self.FCP_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.FCP_WT_M['K_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.FCP_WT_M['C_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.FCP_WT_M['A_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_M['B_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['B_below'])+str('\n \n'))
    elif self.FCP_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.FCP_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.FCP_WT_M['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.FCP_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.FCP_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.FCP_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.FCP_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.FCP_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.FCP_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.FCP_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.FCP_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.FCP_WT_M['Figures'].lower() == 'no' and self.FCP_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '----------------------------------- \n')
    file.write( ' Flat Center Polygons, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_FCP_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_FCP_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_FCP_WT_O - self.Init_FCP_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_FCP_WT_O - self.Init_FCP_WT_O)/self.Init_FCP_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.FCP_WT_O['POI_Function']) + str('\n'))
    if self.FCP_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.FCP_WT_O['A1_above'])+\
                   ' | '+str(self.FCP_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.FCP_WT_O['A2_above'])+\
                   ' | '+str(self.FCP_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.FCP_WT_O['x0_above'])+\
                   ' | '+str(self.FCP_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.FCP_WT_O['dx_above'])+\
                   ' | '+str(self.FCP_WT_O['dx_below'])+str('\n \n'))
    elif self.FCP_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.FCP_WT_O['a_above'])+\
                   str(' | ')+str(self.FCP_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.FCP_WT_O['b_above']) +\
                   str(' | ')+str(self.FCP_WT_O['b_below'])+str('\n \n'))
    elif self.FCP_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.FCP_WT_O['K_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.FCP_WT_O['C_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.FCP_WT_O['A_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_O['B_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['B_below'])+str('\n \n'))
    elif self.FCP_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.FCP_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.FCP_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.FCP_WT_O['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.FCP_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.FCP_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.FCP_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.FCP_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.FCP_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.FCP_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.FCP_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.FCP_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.FCP_WT_O['Figures'].lower() == 'no' and self.FCP_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')
        
    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, High Center Polygons \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' High Center Polygons, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_HCP_WT_Y + self.Init_HCP_WT_M + self.Init_HCP_WT_O
    final_total = self.Final_HCP_WT_Y + self.Final_HCP_WT_M + self.Final_HCP_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' High Center Polygons, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_HCP_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_HCP_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_HCP_WT_Y - self.Init_HCP_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_HCP_WT_Y - self.Init_HCP_WT_Y)/self.Init_HCP_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.HCP_WT_Y['POI_Function']) + str('\n'))
    if self.HCP_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.HCP_WT_Y['A1_above'])+\
                   ' | '+str(self.HCP_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.HCP_WT_Y['A2_above'])+\
                   ' | '+str(self.HCP_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.HCP_WT_Y['x0_above'])+\
                   ' | '+str(self.HCP_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.HCP_WT_Y['dx_above'])+\
                   ' | '+str(self.HCP_WT_Y['dx_below'])+str('\n \n'))
    elif self.HCP_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.HCP_WT_Y['a_above'])+\
                   str(' | ')+str(self.HCP_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.HCP_WT_Y['b_above']) +\
                   str(' | ')+str(self.HCP_WT_Y['b_below'])+str('\n \n'))
    elif self.HCP_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.HCP_WT_Y['K_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.HCP_WT_Y['C_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.HCP_WT_Y['A_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_Y['B_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['B_below'])+str('\n \n'))
    elif self.HCP_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.HCP_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.HCP_WT_Y['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.HCP_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.HCP_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.HCP_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.HCP_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.HCP_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.HCP_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.HCP_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.HCP_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.HCP_WT_Y['Figures'].lower() == 'no' and self.HCP_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '----------------------------------- \n')
    file.write( ' High Center Polygons, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_HCP_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_HCP_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_HCP_WT_M - self.Init_HCP_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_HCP_WT_M - self.Init_HCP_WT_M)/self.Init_HCP_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.HCP_WT_M['POI_Function']) + str('\n'))
    if self.HCP_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.HCP_WT_M['A1_above'])+\
                   ' | '+str(self.HCP_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.HCP_WT_M['A2_above'])+\
                   ' | '+str(self.HCP_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.HCP_WT_M['x0_above'])+\
                   ' | '+str(self.HCP_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.HCP_WT_M['dx_above'])+\
                   ' | '+str(self.HCP_WT_M['dx_below'])+str('\n \n'))
    elif self.HCP_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.HCP_WT_M['a_above'])+\
                   str(' | ')+str(self.HCP_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.HCP_WT_M['b_above']) +\
                   str(' | ')+str(self.HCP_WT_M['b_below'])+str('\n \n'))
    elif self.HCP_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.HCP_WT_M['K_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.HCP_WT_M['C_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.HCP_WT_M['A_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_M['B_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['B_below'])+str('\n \n'))
    elif self.HCP_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.HCP_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.HCP_WT_M['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.HCP_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.HCP_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.HCP_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.HCP_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.HCP_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.HCP_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.HCP_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.HCP_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.HCP_WT_M['Figures'].lower() == 'no' and self.HCP_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    
    file.write( '----------------------------------- \n')
    file.write( ' High Center Polygons, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_HCP_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_HCP_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_HCP_WT_O - self.Init_HCP_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_HCP_WT_O - self.Init_HCP_WT_O)/self.Init_HCP_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.HCP_WT_O['POI_Function']) + str('\n'))
    if self.HCP_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.HCP_WT_O['A1_above'])+\
                   ' | '+str(self.HCP_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.HCP_WT_O['A2_above'])+\
                   ' | '+str(self.HCP_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.HCP_WT_O['x0_above'])+\
                   ' | '+str(self.HCP_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.HCP_WT_O['dx_above'])+\
                   ' | '+str(self.HCP_WT_O['dx_below'])+str('\n \n'))
    elif self.HCP_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.HCP_WT_O['a_above'])+\
                   str(' | ')+str(self.HCP_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.HCP_WT_O['b_above']) +\
                   str(' | ')+str(self.HCP_WT_O['b_below'])+str('\n \n'))
    elif self.HCP_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.HCP_WT_O['K_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.HCP_WT_O['C_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.HCP_WT_O['A_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_O['B_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['B_below'])+str('\n \n'))
    elif self.HCP_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.HCP_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.HCP_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.HCP_WT_O['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.HCP_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.HCP_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.HCP_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.HCP_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.HCP_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.HCP_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.HCP_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.HCP_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.HCP_WT_O['Figures'].lower() == 'no' and self.HCP_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    #-------------------------------------------------------------------------------------------
    file.write( '===========================================================\n' )
    file.write( '       Lake and Pond Ice Information  \n')
    file.write( '===========================================================\n')
    if self.LakePond['ice_thickness_distribution'].lower() == 'random':
        file.write('Ice thickness alpha value is RANDOM. \n')
        file.write('  Lower | Upper bounds of alpha values are: ' +\
                   str(self.LakePond['Lower_ice_thickness_alpha']) +str(' | ') +\
                   str(self.LakePond['Upper_ice_thickness_alpha']) +str(' \n \n'))
    elif self.LakePond['ice_thickness_distribution'].lower() == 'uniform':
        file.write('Ice thickness alpha value is UNIFORM. \n')
        file.write('  The alpha value is: '+str(self.LakePond['ice_thickness_uniform_alpha']) +\
                   str(' \n \n'))

    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Lakes \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Lakes, Wetland Tundra, Small, Medium, Large, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_LargeLakes_WT_Y + self.Init_LargeLakes_WT_M + self.Init_LargeLakes_WT_O + \
                 self.Init_MediumLakes_WT_Y + self.Init_MediumLakes_WT_M + self.Init_MediumLakes_WT_O + \
                 self.Init_SmallLakes_WT_Y + self.Init_SmallLakes_WT_M + self.Init_SmallLakes_WT_O
    final_total = self.Final_LargeLakes_WT_Y + self.Final_LargeLakes_WT_M + self.Final_LargeLakes_WT_O + \
                  self.Final_MediumLakes_WT_Y + self.Final_MediumLakes_WT_M + self.Final_MediumLakes_WT_O + \
                  self.Final_SmallLakes_WT_Y + self.Final_SmallLakes_WT_M + self.Final_SmallLakes_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( '\n'  )
    file.write( '----------------------------------- \n')
    file.write( ' Large Lakes, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_LargeLakes_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_LargeLakes_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_LargeLakes_WT_Y - self.Init_LargeLakes_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LargeLakes_WT_Y - self.Init_LargeLakes_WT_Y)/\
                                                 self.Init_LargeLakes_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( 'Large Lake, Wetland Tundra, Young age expansion constant is set to: ' \
                +str(self.LakePond['LargeLake_WT_Y_Expansion'])+str('\n\n'))
    #--------------------------------------------------------------------------------------------
    if self.LakePond['Lake_Distribution'].lower() == 'random':
        file.write('Large Lake, Wetland Tundra, Young age lake depth distribution is RANDOM.\n')
        file.write('   Lower | Upper bounds of the random function are: ' \
                   +str(self.LakePond['Lower_LargeLake_WT_Y_Depth']) + str(' | ') + \
                   str(self.LakePond['Upper_LargeLake_WT_Y_Depth']))
    elif self.LakePond['Lake_Distribution'].lower() == 'uniform':
        file.write('Large Lake, Wetland Tundra, Young age lake depth distribution is UNIFORM. \n')
        file.write('   The initial lake depth is : ' + str(self.LakePond['Uniform_Lake_Depth'])+str('\n \n'))
    #-------------------------------------------------------------------------------------------
    if self.LakePond['ice_thickness_distribution'].lower() == 'random':
        file.write('Ice thickness alpha value is RANDOM. \n')
        file.write('  Lower | Upper bounds of alpha values are: ' +\
                   str(self.LakePond['Lower_ice_thickness_alpha']) +str(' | ') +\
                   str(self.LakePond['Upper_ice_thickness_alpha']) +str(' \n \n'))
    elif self.LakePond['ice_thickness_distribution'].lower() == 'uniform':
        file.write('Ice thickness alpha value is UNIFORM. \n')
        file.write('  The alpha value is: '+str(self.LakePond['ice_thickness_uniform_alpha']) +\
                   str(' \n \n'))
    #---------------------------------------------------------------------------------------------

                
    file.write( ' \n \n')
    file.write( '----------------------------------- \n')
    file.write( ' Large Lakes, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_LargeLakes_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_LargeLakes_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_LargeLakes_WT_M - self.Init_LargeLakes_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LargeLakes_WT_M - self.Init_LargeLakes_WT_M)/\
                                                 self.Init_LargeLakes_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Large Lakes, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_LargeLakes_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_LargeLakes_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_LargeLakes_WT_O - self.Init_LargeLakes_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_LargeLakes_WT_O - self.Init_LargeLakes_WT_O)/\
                                                 self.Init_LargeLakes_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Medium Lakes, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_MediumLakes_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_MediumLakes_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_MediumLakes_WT_Y - self.Init_MediumLakes_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_MediumLakes_WT_Y - self.Init_MediumLakes_WT_Y)/\
                                                 self.Init_MediumLakes_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Medium Lakes, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_MediumLakes_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_MediumLakes_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_MediumLakes_WT_M - self.Init_MediumLakes_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_MediumLakes_WT_M - self.Init_MediumLakes_WT_M)/\
                                                 self.Init_MediumLakes_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Small Lakes, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SmallLakes_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_SmallLakes_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_SmallLakes_WT_O - self.Init_SmallLakes_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SmallLakes_WT_O - self.Init_SmallLakes_WT_O)/\
                                                 self.Init_SmallLakes_WT_O)*100.)+str('\n'))
    file.write( ' \n')    
    file.write( '----------------------------------- \n')
    file.write( ' Small Lakes, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SmallLakes_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SmallLakes_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SmallLakes_WT_Y - self.Init_SmallLakes_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SmallLakes_WT_Y - self.Init_SmallLakes_WT_Y)/\
                                                 self.Init_SmallLakes_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Small Lakes, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_SmallLakes_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SmallLakes_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SmallLakes_WT_M - self.Init_SmallLakes_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SmallLakes_WT_M - self.Init_SmallLakes_WT_M)/\
                                                 self.Init_SmallLakes_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Small Lakes, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SmallLakes_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_SmallLakes_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_SmallLakes_WT_O - self.Init_SmallLakes_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SmallLakes_WT_O - self.Init_SmallLakes_WT_O)/\
                                                 self.Init_SmallLakes_WT_O)*100.)+str('\n'))
    file.write( ' \n')

    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Ponds \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Ponds, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_Ponds_WT_Y + self.Init_Ponds_WT_M + self.Init_Ponds_WT_O
    final_total = self.Final_Ponds_WT_Y + self.Final_Ponds_WT_M + self.Final_Ponds_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Ponds, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Ponds_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Ponds_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Ponds_WT_Y - self.Init_Ponds_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Ponds_WT_Y - self.Init_Ponds_WT_Y)/\
                                                 self.Init_Ponds_WT_Y)*100.) + str('\n'))
    if self.LakePond['Pond_Distribution'].lower() == 'random':
        file.write(' Pond Depth Distribution is RANDOM function. \n')
        file.write('  Lower | Upper bounds of the random functions are: '+\
                       str(self.LakePond['Lower_Pond_WT_Y_Depth']) + str(' | ') + \
                       str(self.LakePond['Upper_Pond_WT_Y_Depth']) + str('\n'))
    else:
        file.write(' Pond Depth Distribution is initialized as UNIFORM. \n')
        file.write('  The initial pond depth (wetland tundra, young age) is: '+\
                       str(self.LakePond['Uniform_Pond_Depth'])+str('\n'))
    file.write(' The Pond (Wetland Tundra, Young age) expansion constant is: ' +\
                   str(self.LakePond['Pond_WT_Y_Expansion']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Young age) infilling constant is: ' +\
                   str(self.LakePond['Pond_WT_Y_Infill_Constant']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Young age) depth control constant is: ' +\
                   str(self.LakePond['Pond_WT_Y_depth_control']) + str('\n'))
    file.write(' Number of consecutive years of pond growth (depth) before lake transition is allowed: '\
                   +str(self.LakePond['Pond_WT_Y_growth_time_required']))
    file.write('Output Results: \n')
    if self.LakePond['Pond_WT_Y_Depth_Figure']:
        file.write('  Initial pond depth (wetland tundra, young age) output as figure. \n')
    
    if self.LakePond['Pond_WT_Y_Figures']:
        file.write('  Yearly Figures output. \n')
    if self.LakePond['Pond_WT_Y_Movie']:
        file.write('  Animation output. \n')
    file.write( ' \n')

    file.write( '----------------------------------- \n')
    file.write( ' Ponds, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_Ponds_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Ponds_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Ponds_WT_M - self.Init_Ponds_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Ponds_WT_M - self.Init_Ponds_WT_M)/\
                                                 self.Init_Ponds_WT_M)*100.)+str('\n'))
    if self.LakePond['Pond_Distribution'].lower() == 'random':
        file.write(' Pond Depth Distribution is RANDOM function. \n')
        file.write('  Lower | Upper bounds of the random functions are: '+\
                       str(self.LakePond['Lower_Pond_WT_M_Depth']) + str(' | ') + \
                       str(self.LakePond['Upper_Pond_WT_M_Depth']) + str('\n'))
    else:
        file.write(' Pond Depth Distribution is initialized as UNIFORM. \n')
        file.write('  The initial pond depth (wetland tundra, medium age) is: '+\
                       str(self.LakePond['Uniform_Pond_Depth'])+str('\n'))
    file.write(' The Pond (Wetland Tundra, Medium age) expansion constant is: ' +\
                   str(self.LakePond['Pond_WT_M_Expansion']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Medium age) infilling constant is: ' +\
                   str(self.LakePond['Pond_WT_M_Infill_Constant']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Medium age) depth control constant is: ' +\
                   str(self.LakePond['Pond_WT_M_depth_control']) + str('\n'))
    file.write(' Number of consecutive years of pond growth (depth) before lake transition is allowed: '\
                   +str(self.LakePond['Pond_WT_M_growth_time_required']))
    file.write('Output Results: \n')
    if self.LakePond['Pond_WT_M_Depth_Figure']:
        file.write('  Initial pond depth (wetland tundra, medium age) output as figure. \n')
    
    if self.LakePond['Pond_WT_M_Figures']:
        file.write('  Yearly Figures output. \n')
    if self.LakePond['Pond_WT_M_Movie']:
        file.write('  Animation output. \n')    
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Ponds, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Ponds_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_Ponds_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_Ponds_WT_O - self.Init_Ponds_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Ponds_WT_O - self.Init_Ponds_WT_O)/\
                                                 self.Init_Ponds_WT_O)*100.)+str('\n'))
    if self.LakePond['Pond_Distribution'].lower() == 'random':
        file.write(' Pond Depth Distribution is RANDOM function. \n')
        file.write('  Lower | Upper bounds of the random functions are: '+\
                       str(self.LakePond['Lower_Pond_WT_O_Depth']) + str(' | ') + \
                       str(self.LakePond['Upper_Pond_WT_O_Depth']) + str('\n'))
    else:
        file.write(' Pond Depth Distribution is initialized as UNIFORM. \n')
        file.write('  The initial pond depth (wetland tundra, old age) is: '+\
                       str(self.LakePond['Uniform_Pond_Depth'])+str('\n'))
    file.write(' The Pond (Wetland Tundra, Old age) expansion constant is: ' +\
                   str(self.LakePond['Pond_WT_O_Expansion']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Old age) infilling constant is: ' +\
                   str(self.LakePond['Pond_WT_O_Infill_Constant']) + str('\n'))
    file.write(' The Pond (Wetland Tundra, Old age) depth control constant is: ' +\
                   str(self.LakePond['Pond_WT_O_depth_control']) + str('\n'))
    file.write(' Number of consecutive years of pond growth (depth) before lake transition is allowed: '\
                   +str(self.LakePond['Pond_WT_O_growth_time_required']))
    file.write('Output Results: \n')
    if self.LakePond['Pond_WT_O_Depth_Figure']:
        file.write('  Initial pond depth (wetland tundra, old age) output as figure. \n')
    
    if self.LakePond['Pond_WT_O_Figures']:
        file.write('  Yearly Figures output. \n')
    if self.LakePond['Pond_WT_O_Movie']:
        file.write('  Animation output. \n')   
    file.write( ' \n')
    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Drained Slopes \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Drained Slopes, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_DrainedSlope_WT_Y + self.Init_DrainedSlope_WT_M + self.Init_DrainedSlope_WT_O
    final_total = self.Final_DrainedSlope_WT_Y + self.Final_DrainedSlope_WT_M + self.Final_DrainedSlope_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Drained Slopes, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_DrainedSlope_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_DrainedSlope_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_DrainedSlope_WT_Y - self.Init_DrainedSlope_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_DrainedSlope_WT_Y - self.Init_DrainedSlope_WT_Y)/\
                                                 self.Init_DrainedSlope_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.DrainedSlope_WT_Y['POI_Function']) + str('\n'))
    if self.DrainedSlope_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['A1_above'])+\
                   ' | '+str(self.DrainedSlope_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['A2_above'])+\
                   ' | '+str(self.DrainedSlope_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['x0_above'])+\
                   ' | '+str(self.DrainedSlope_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['dx_above'])+\
                   ' | '+str(self.DrainedSlope_WT_Y['dx_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['a_above'])+\
                   str(' | ')+str(self.DrainedSlope_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['b_above']) +\
                   str(' | ')+str(self.DrainedSlope_WT_Y['b_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['K_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['C_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['A_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['B_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['B_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.DrainedSlope_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_Y['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.DrainedSlope_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.DrainedSlope_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.DrainedSlope_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.DrainedSlope_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.DrainedSlope_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.DrainedSlope_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.DrainedSlope_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.DrainedSlope_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.DrainedSlope_WT_Y['Figures'].lower() == 'no' and self.DrainedSlope_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '----------------------------------- \n')
    file.write( ' Drained Slopes, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_DrainedSlope_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_DrainedSlope_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_DrainedSlope_WT_M - self.Init_DrainedSlope_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_DrainedSlope_WT_M - self.Init_DrainedSlope_WT_M)/\
                                                 self.Init_DrainedSlope_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.DrainedSlope_WT_M['POI_Function']) + str('\n'))
    if self.DrainedSlope_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['A1_above'])+\
                   ' | '+str(self.DrainedSlope_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['A2_above'])+\
                   ' | '+str(self.DrainedSlope_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['x0_above'])+\
                   ' | '+str(self.DrainedSlope_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['dx_above'])+\
                   ' | '+str(self.DrainedSlope_WT_M['dx_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['a_above'])+\
                   str(' | ')+str(self.DrainedSlope_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['b_above']) +\
                   str(' | ')+str(self.DrainedSlope_WT_M['b_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['K_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['C_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['A_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['B_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['B_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.DrainedSlope_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_M['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.DrainedSlope_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.DrainedSlope_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.DrainedSlope_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.DrainedSlope_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.DrainedSlope_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.DrainedSlope_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.DrainedSlope_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.DrainedSlope_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.DrainedSlope_WT_M['Figures'].lower() == 'no' and self.DrainedSlope_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

                   
    file.write( '----------------------------------- \n')
    file.write( ' Drained Slope, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_DrainedSlope_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_DrainedSlope_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_DrainedSlope_WT_O - self.Init_DrainedSlope_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_DrainedSlope_WT_O - self.Init_DrainedSlope_WT_O)/\
                                                 self.Init_DrainedSlope_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.DrainedSlope_WT_O['POI_Function']) + str('\n'))
    if self.DrainedSlope_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['A1_above'])+\
                   ' | '+str(self.DrainedSlope_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['A2_above'])+\
                   ' | '+str(self.DrainedSlope_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['x0_above'])+\
                   ' | '+str(self.DrainedSlope_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['dx_above'])+\
                   ' | '+str(self.DrainedSlope_WT_O['dx_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['a_above'])+\
                   str(' | ')+str(self.DrainedSlope_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['b_above']) +\
                   str(' | ')+str(self.DrainedSlope_WT_O['b_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['K_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['C_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['A_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['B_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['B_below'])+str('\n \n'))
    elif self.DrainedSlope_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.DrainedSlope_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.DrainedSlope_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.DrainedSlope_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.DrainedSlope_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.DrainedSlope_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.DrainedSlope_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.DrainedSlope_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.DrainedSlope_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.DrainedSlope_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.DrainedSlope_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.DrainedSlope_WT_O['Figures'].lower() == 'no' and self.DrainedSlope_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Sand Dunes \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Sand Dunes, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_SandDunes_WT_Y + self.Init_SandDunes_WT_M + self.Init_SandDunes_WT_O
    final_total = self.Final_SandDunes_WT_Y + self.Final_SandDunes_WT_M + self.Final_SandDunes_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Sand Dunes, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SandDunes_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SandDunes_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SandDunes_WT_Y - self.Init_SandDunes_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SandDunes_WT_Y - self.Init_SandDunes_WT_Y)/\
                                                 self.Init_SandDunes_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SandDunes_WT_Y['POI_Function']) + str('\n'))
    if self.SandDunes_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['A1_above'])+\
                   ' | '+str(self.SandDunes_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['A2_above'])+\
                   ' | '+str(self.SandDunes_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['x0_above'])+\
                   ' | '+str(self.SandDunes_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['dx_above'])+\
                   ' | '+str(self.SandDunes_WT_Y['dx_below'])+str('\n \n'))
    elif self.SandDunes_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['a_above'])+\
                   str(' | ')+str(self.SandDunes_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['b_above']) +\
                   str(' | ')+str(self.SandDunes_WT_Y['b_below'])+str('\n \n'))
    elif self.SandDunes_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['K_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['C_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['A_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['B_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['B_below'])+str('\n \n'))
    elif self.SandDunes_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SandDunes_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_Y['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.SandDunes_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SandDunes_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SandDunes_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SandDunes_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SandDunes_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SandDunes_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SandDunes_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.SandDunes_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.SandDunes_WT_Y['Figures'].lower() == 'no' and self.SandDunes_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '----------------------------------- \n')
    file.write( ' Sand Dunes, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_SandDunes_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SandDunes_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SandDunes_WT_M - self.Init_SandDunes_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SandDunes_WT_M - self.Init_SandDunes_WT_M)/\
                                                 self.Init_SandDunes_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SandDunes_WT_M['POI_Function']) + str('\n'))
    if self.SandDunes_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SandDunes_WT_M['A1_above'])+\
                   ' | '+str(self.SandDunes_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SandDunes_WT_M['A2_above'])+\
                   ' | '+str(self.SandDunes_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SandDunes_WT_M['x0_above'])+\
                   ' | '+str(self.SandDunes_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SandDunes_WT_M['dx_above'])+\
                   ' | '+str(self.SandDunes_WT_M['dx_below'])+str('\n \n'))
    elif self.SandDunes_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SandDunes_WT_M['a_above'])+\
                   str(' | ')+str(self.SandDunes_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SandDunes_WT_M['b_above']) +\
                   str(' | ')+str(self.SandDunes_WT_M['b_below'])+str('\n \n'))
    elif self.SandDunes_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SandDunes_WT_M['K_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SandDunes_WT_M['C_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SandDunes_WT_M['A_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_M['B_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['B_below'])+str('\n \n'))
    elif self.SandDunes_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SandDunes_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_M['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.SandDunes_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SandDunes_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SandDunes_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SandDunes_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SandDunes_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SandDunes_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SandDunes_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.SandDunes_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.SandDunes_WT_M['Figures'].lower() == 'no' and self.SandDunes_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '----------------------------------- \n')
    file.write( ' Sand Dunes, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SandDunes_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_SandDunes_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_SandDunes_WT_O - self.Init_SandDunes_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SandDunes_WT_O - self.Init_SandDunes_WT_O)/\
                                                 self.Init_SandDunes_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SandDunes_WT_O['POI_Function']) + str('\n'))
    if self.SandDunes_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SandDunes_WT_O['A1_above'])+\
                   ' | '+str(self.SandDunes_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SandDunes_WT_O['A2_above'])+\
                   ' | '+str(self.SandDunes_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SandDunes_WT_O['x0_above'])+\
                   ' | '+str(self.SandDunes_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SandDunes_WT_O['dx_above'])+\
                   ' | '+str(self.SandDunes_WT_O['dx_below'])+str('\n \n'))
    elif self.SandDunes_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SandDunes_WT_O['a_above'])+\
                   str(' | ')+str(self.SandDunes_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SandDunes_WT_O['b_above']) +\
                   str(' | ')+str(self.SandDunes_WT_O['b_below'])+str('\n \n'))
    elif self.SandDunes_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SandDunes_WT_O['K_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SandDunes_WT_O['C_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SandDunes_WT_O['A_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_O['B_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['B_below'])+str('\n \n'))
    elif self.SandDunes_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SandDunes_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SandDunes_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.SandDunes_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.SandDunes_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SandDunes_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SandDunes_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SandDunes_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SandDunes_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SandDunes_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SandDunes_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.SandDunes_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.SandDunes_WT_O['Figures'].lower() == 'no' and self.SandDunes_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '=============================================================\n')
    file.write( '       Wetland Tundra, Saturated Barrens \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Saturated Barrens, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_SaturatedBarrens_WT_Y + self.Init_SaturatedBarrens_WT_M + self.Init_SaturatedBarrens_WT_O
    final_total = self.Final_SaturatedBarrens_WT_Y + self.Final_SaturatedBarrens_WT_M + self.Final_SaturatedBarrens_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Saturated Barrens, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SaturatedBarrens_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SaturatedBarrens_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SaturatedBarrens_WT_Y - self.Init_SaturatedBarrens_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SaturatedBarrens_WT_Y - self.Init_SaturatedBarrens_WT_Y)/\
                                                 self.Init_SaturatedBarrens_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SaturatedBarrens_WT_Y['POI_Function']) + str('\n'))
    if self.SaturatedBarrens_WT_Y['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['A1_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_Y['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['A2_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_Y['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['x0_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_Y['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['dx_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_Y['dx_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_Y['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['a_above'])+\
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['b_above']) +\
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['b_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_Y['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['K_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['C_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['A_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['B_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['B_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_Y['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['HillB_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_Y['HillN_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_Y['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.SaturatedBarrens_WT_Y['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SaturatedBarrens_WT_Y['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SaturatedBarrens_WT_Y['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SaturatedBarrens_WT_Y['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SaturatedBarrens_WT_Y['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SaturatedBarrens_WT_Y['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SaturatedBarrens_WT_Y['Figures']:
        file.write('  Yearly Figures \n')
    if self.SaturatedBarrens_WT_Y['Movie']:
        file.write('  Animation \n' )
    if self.SaturatedBarrens_WT_Y['Figures'].lower() == 'no' and self.SaturatedBarrens_WT_Y['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '----------------------------------- \n')
    file.write( ' Saturated Barrens, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_SaturatedBarrens_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_SaturatedBarrens_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_SaturatedBarrens_WT_M - self.Init_SaturatedBarrens_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SaturatedBarrens_WT_M - self.Init_SaturatedBarrens_WT_M)/\
                                                 self.Init_SaturatedBarrens_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SaturatedBarrens_WT_M['POI_Function']) + str('\n'))
    if self.SaturatedBarrens_WT_M['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['A1_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_M['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['A2_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_M['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['x0_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_M['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['dx_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_M['dx_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_M['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['a_above'])+\
                   str(' | ')+str(self.SaturatedBarrens_WT_M['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['b_above']) +\
                   str(' | ')+str(self.SaturatedBarrens_WT_M['b_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_M['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['K_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['C_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['A_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['B_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['B_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_M['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['HillB_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_M['HillN_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_M['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.SaturatedBarrens_WT_M['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SaturatedBarrens_WT_M['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SaturatedBarrens_WT_M['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SaturatedBarrens_WT_M['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SaturatedBarrens_WT_M['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SaturatedBarrens_WT_M['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SaturatedBarrens_WT_M['Figures']:
        file.write('  Yearly Figures \n')
    if self.SaturatedBarrens_WT_M['Movie']:
        file.write('  Animation \n' )
    if self.SaturatedBarrens_WT_M['Figures'].lower() == 'no' and self.SaturatedBarrens_WT_M['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '----------------------------------- \n')
    file.write( ' Saturated Barrens, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_SaturatedBarrens_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_SaturatedBarrens_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_SaturatedBarrens_WT_O - self.Init_SaturatedBarrens_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_SaturatedBarrens_WT_O - self.Init_SaturatedBarrens_WT_O)/\
                                                 self.Init_SaturatedBarrens_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.SaturatedBarrens_WT_O['POI_Function']) + str('\n'))
    if self.SaturatedBarrens_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['A1_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['A2_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['x0_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['dx_above'])+\
                   ' | '+str(self.SaturatedBarrens_WT_O['dx_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['a_above'])+\
                   str(' | ')+str(self.SaturatedBarrens_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['b_above']) +\
                   str(' | ')+str(self.SaturatedBarrens_WT_O['b_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['K_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['C_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['A_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['B_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['B_below'])+str('\n \n'))
    elif self.SaturatedBarrens_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.SaturatedBarrens_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.SaturatedBarrens_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.SaturatedBarrens_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.SaturatedBarrens_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.SaturatedBarrens_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.SaturatedBarrens_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.SaturatedBarrens_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.SaturatedBarrens_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.SaturatedBarrens_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.SaturatedBarrens_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.SaturatedBarrens_WT_O['Figures'].lower() == 'no' and self.SaturatedBarrens_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Rivers, Wetland Tundra, All ages \n')
    file.write( '----------------------------------- \n')
    init_total = self.Init_Rivers_WT_Y + self.Init_Rivers_WT_M + self.Init_Rivers_WT_O
    final_total = self.Final_Rivers_WT_Y + self.Final_Rivers_WT_M + self.Final_Rivers_WT_O
    file.write( 'Initial Fractional Area (km2): ' +str( init_total )+str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str(  final_total) +str('\n'))
    file.write( 'Total Fractional Change (km2):' + str( final_total - init_total) +str('\n'))
    file.write( 'Percent difference: ' + str( ((final_total - init_total)/init_total)*100.) +str('\n'))
    file.write( ' \n'    )
    file.write( '----------------------------------- \n')
    file.write( ' Rivers, Wetland Tundra Young age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Rivers_WT_Y ) + str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Rivers_WT_Y) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Rivers_WT_Y - self.Init_Rivers_WT_Y) + str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Rivers_WT_Y - self.Init_Rivers_WT_Y)/\
                                                 self.Init_Rivers_WT_Y)*100.) + str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Rivers, Wetland Tundra Medium age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): ' +str( self.Init_Rivers_WT_M) +str('\n'))
    file.write( 'Final Fractional Area (km2): ' + str( self.Final_Rivers_WT_M) + str('\n'))
    file.write( 'Total Fractional Change (km2): ' + str( self.Final_Rivers_WT_M - self.Init_Rivers_WT_M)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Rivers_WT_M - self.Init_Rivers_WT_M)/\
                                                 self.Init_Rivers_WT_M)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '----------------------------------- \n')
    file.write( ' Rivers, Wetland Tundra Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Rivers_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_Rivers_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_Rivers_WT_O - self.Init_Rivers_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Rivers_WT_O - self.Init_Rivers_WT_O)/\
                                                 self.Init_Rivers_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Shrubs, Wetland Tundra, Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Shrubs_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_Shrubs_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_Shrubs_WT_O - self.Init_Shrubs_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Shrubs_WT_O - self.Init_Shrubs_WT_O)/\
                                                 self.Init_Shrubs_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.Shrubs_WT_O['POI_Function']) + str('\n'))
    if self.Shrubs_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.Shrubs_WT_O['A1_above'])+\
                   ' | '+str(self.Shrubs_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.Shrubs_WT_O['A2_above'])+\
                   ' | '+str(self.Shrubs_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.Shrubs_WT_O['x0_above'])+\
                   ' | '+str(self.Shrubs_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.Shrubs_WT_O['dx_above'])+\
                   ' | '+str(self.Shrubs_WT_O['dx_below'])+str('\n \n'))
    elif self.Shrubs_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.Shrubs_WT_O['a_above'])+\
                   str(' | ')+str(self.Shrubs_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.Shrubs_WT_O['b_above']) +\
                   str(' | ')+str(self.Shrubs_WT_O['b_below'])+str('\n \n'))
    elif self.Shrubs_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.Shrubs_WT_O['K_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.Shrubs_WT_O['C_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.Shrubs_WT_O['A_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.Shrubs_WT_O['B_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['B_below'])+str('\n \n'))
    elif self.Shrubs_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.Shrubs_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.Shrubs_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.Shrubs_WT_O['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.Shrubs_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.Shrubs_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.Shrubs_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.Shrubs_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.Shrubs_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.Shrubs_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.Shrubs_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.Shrubs_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.Shrubs_WT_O['Figures'].lower() == 'no' and self.Shrubs_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Coastal Waters, Wetland Tundra, Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_CoastalWaters_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_CoastalWaters_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_CoastalWaters_WT_O - self.Init_CoastalWaters_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_CoastalWaters_WT_O - self.Init_CoastalWaters_WT_O)/\
                                                 self.Init_CoastalWaters_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.CoastalWaters_WT_O['POI_Function']) + str('\n'))
    if self.CoastalWaters_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['A1_above'])+\
                   ' | '+str(self.CoastalWaters_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['A2_above'])+\
                   ' | '+str(self.CoastalWaters_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['x0_above'])+\
                   ' | '+str(self.CoastalWaters_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['dx_above'])+\
                   ' | '+str(self.CoastalWaters_WT_O['dx_below'])+str('\n \n'))
    elif self.CoastalWaters_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['a_above'])+\
                   str(' | ')+str(self.CoastalWaters_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['b_above']) +\
                   str(' | ')+str(self.CoastalWaters_WT_O['b_below'])+str('\n \n'))
    elif self.CoastalWaters_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['K_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['C_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['A_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['B_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['B_below'])+str('\n \n'))
    elif self.CoastalWaters_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.CoastalWaters_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.CoastalWaters_WT_O['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.CoastalWaters_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.CoastalWaters_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.CoastalWaters_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.CoastalWaters_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.CoastalWaters_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.CoastalWaters_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.CoastalWaters_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.CoastalWaters_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.CoastalWaters_WT_O['Figures'].lower() == 'no' and self.CoastalWaters_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')

    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' Urban Area, Wetland Tundra \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_Urban_WT) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_Urban_WT)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_Urban_WT - self.Init_Urban_WT)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_Urban_WT - self.Init_Urban_WT)/\
                                                 self.Init_Urban_WT)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' POI Function Used: '+str(self.Urban_WT['POI_Function']) + str('\n'))
    if self.Urban_WT['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.Urban_WT['A1_above'])+\
                   ' | '+str(self.Urban_WT['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.Urban_WT['A2_above'])+\
                   ' | '+str(self.Urban_WT['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.Urban_WT['x0_above'])+\
                   ' | '+str(self.Urban_WT['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.Urban_WT['dx_above'])+\
                   ' | '+str(self.Urban_WT['dx_below'])+str('\n \n'))
    elif self.Urban_WT['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.Urban_WT['a_above'])+\
                   str(' | ')+str(self.Urban_WT['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.Urban_WT['b_above']) +\
                   str(' | ')+str(self.Urban_WT['b_below'])+str('\n \n'))
    elif self.Urban_WT['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.Urban_WT['K_above'])+ \
                   str(' | ')+str(self.Urban_WT['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.Urban_WT['C_above'])+ \
                   str(' | ')+str(self.Urban_WT['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.Urban_WT['A_above'])+ \
                   str(' | ')+str(self.Urban_WT['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.Urban_WT['B_above'])+ \
                   str(' | ')+str(self.Urban_WT['B_below'])+str('\n \n'))
    elif self.Urban_WT['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.Urban_WT['HillB_above'])+ \
                   str(' | ')+str(self.Urban_WT['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.Urban_WT['HillN_above'])+ \
                   str(' | ')+str(self.Urban_WT['HillN_below'])+str('\n \n'))


    file.write(' Maximum rate of terrain transition: '+str(self.Urban_WT['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.Urban_WT['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.Urban_WT['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.Urban_WT['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.Urban_WT['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.Urban_WT['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.Urban_WT['Figures']:
        file.write('  Yearly Figures \n')
    if self.Urban_WT['Movie']:
        file.write('  Animation \n' )
    if self.Urban_WT['Figures'].lower() == 'no' and self.Urban_WT['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '=============================================================\n')
    file.write( '-----------------------------------  \n')
    file.write( ' No Data, Wetland Tundra, Old age \n')
    file.write( '----------------------------------- \n')
    file.write( 'Initial Fractional Area (km2): '+str( self.Init_NoData_WT_O) + str('\n'))
    file.write( 'Final Fractional Area (km2): '+str( self.Final_NoData_WT_O)+str('\n'))
    file.write( 'Total Fractional Change (km2): '+str( self.Final_NoData_WT_O - self.Init_NoData_WT_O)+str('\n'))
    file.write( 'Percent difference: '+str( ((self.Final_NoData_WT_O - self.Init_NoData_WT_O)/\
                                                 self.Init_NoData_WT_O)*100.)+str('\n'))
    file.write( ' \n')
    file.write( ' Wetland Tundra, No Data, Old age \n')
    file.write( ' POI Function Used: '+str(self.NoData_WT_O['POI_Function']) + str('\n'))
    if self.NoData_WT_O['POI_Function'].lower() == 'sigmoid':
        file.write(' POI = A2 + (A1 - A2) / (1. + exp((x - x0) / dx)) \n')
        file.write('  A1 [above | below drainage threshold]: '+str(self.NoData_WT_O['A1_above'])+\
                   ' | '+str(self.NoData_WT_O['A1_below'])+str('\n'))
        file.write('  A2 [above | below drainage threshold]: '+str(self.NoData_WT_O['A2_above'])+\
                   ' | '+str(self.NoData_WT_O['A2_below'])+str('\n'))
        file.write('  x0 [above | below drainage threshold]: '+str(self.NoData_WT_O['x0_above'])+\
                   ' | '+str(self.NoData_WT_O['x0_below'])+str('\n'))
        file.write('  dx [above | below drainage threshold]: '+str(self.NoData_WT_O['dx_above'])+\
                   ' | '+str(self.NoData_WT_O['dx_below'])+str('\n \n'))
    elif self.NoData_WT_O['POI_Function'].lower() == 'linear':
        file.write(' POI = a + (b * x) \n')
        file.write('  a [above | below drainage threshold]: '+str(self.NoData_WT_O['a_above'])+\
                   str(' | ')+str(self.NoData_WT_O['a_below'])+str('\n'))
        file.write('  b [above | below drainage threshold]: '+str(self.NoData_WT_O['b_above']) +\
                   str(' | ')+str(self.NoData_WT_O['b_below'])+str('\n \n'))
    elif self.NoData_WT_O['POI_Function'].lower() == 'sigmoid2':
        file.write(' POI = K / (C + (A*x**B)) \n')
        file.write('  K [above | below drainage threshold]: '+str(self.NoData_WT_O['K_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['K_below'])+str('\n'))
        file.write('  C [above | below drainage threshold]: '+str(self.NoData_WT_O['C_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['C_below'])+str('\n'))        
        file.write('  A [above | below drainage threshold]: '+str(self.NoData_WT_O['A_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['A_below'])+str('\n'))        
        file.write('  B [above | below drainage threshold]: '+str(self.NoData_WT_O['B_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['B_below'])+str('\n \n'))
    elif self.NoData_WT_O['POI_Function'].lower() == 'hill':
        file.write(' POI = (B * (x^n))/(1+(x^n)) \n')
        file.write('  B [above | below drainage threshold]: '+str(self.NoData_WT_O['HillB_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['HillB_below'])+str('\n'))        
        file.write('  n [above | below drainage threshold]: '+str(self.NoData_WT_O['HillN_above'])+ \
                   str(' | ')+str(self.NoData_WT_O['HillN_below'])+str('\n \n'))

    file.write(' Maximum rate of terrain transition: '+str(self.NoData_WT_O['max_terrain_transition'])+\
               str(' \n \n'))
    file.write(' Soil Porosity: '+str(self.NoData_WT_O['porosity'])+str('\n \n'))

    file.write(' Rate Transitions as a function of ground ice content: \n')
    file.write('  Poor Ground Ice: '+str(self.NoData_WT_O['ice_slope_poor'])+str('\n'))
    file.write('  Pore Ground Ice: '+str(self.NoData_WT_O['ice_slope_pore'])+str('\n'))
    file.write('  Wedge Ground Ice: '+str(self.NoData_WT_O['ice_slope_wedge'])+str('\n'))
    file.write('  Massive Ground Ice: '+str(self.NoData_WT_O['ice_slope_massive'])+str('\n \n'))

    file.write(' Output Results: ' +str('\n'))
    if self.NoData_WT_O['Figures']:
        file.write('  Yearly Figures \n')
    if self.NoData_WT_O['Movie']:
        file.write('  Animation \n' )
    if self.NoData_WT_O['Figures'].lower() == 'no' and self.NoData_WT_O['Movie'].lower() == 'no':
        file.write('  No output written to disk. \n')


    file.write( '============================================================== \n')

    ############################################################################
    file.write( '===================================================\n')
    file.write( '                Simulation Notes                   \n')
    file.write( '===================================================\n')
    sim_notes = open(self.control['Run_dir']+self.Input_directory+str('/Notes/')+self.notes_file, 'r')
    file.write(sim_notes.read())
    sim_notes.close()
    ############################################################################
    file.close()

    #-------------------------
    # Return to Run Directory
    #-------------------------
    os.chdir(self.control['Run_dir'])
