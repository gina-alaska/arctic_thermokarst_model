import numpy as np
import os, sys
import datetime, time
from matplotlib.dates import date2num
from matplotlib.dates import num2date
from __init__ import __version__, __codeurl__

import cohorts

def construnct_results(self, start_time, end_time):
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
    string +=  'Code URL: '+str(__codeurl__)+ nl
    string +=  'Simulation name: '+ self.control.Simulation_name+ nl
    string +=  'Start Date / Time : '+str( start_time)+ nl
    string +=  'End Date / Time : '+str(end_time)+ nl
    string +=  'Total Simulation Time (minutes): '+ str( (start_time - end_time)) + nl
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
    #~ print self.control['Initialize_Control']
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


    start_year = self.control.start_year
    end_year =  self.control.initilzation_year + self.stop -1 
    
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
        
    return string
    
