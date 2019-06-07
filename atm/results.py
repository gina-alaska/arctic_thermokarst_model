import numpy as np
import os, sys
import datetime, time

from __init__ import __version__, __codeurl__

import cohorts

def as_string(atm_obj, start_time, end_time):
    """
    The purpose of this module is to compile simulation results
    and output to the terminal screen.
    """
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
    string +=  'Simulation name: '+ atm_obj.control['Simulation_name']+ nl
    string +=  'Start Date / Time : '+str( start_time)+ nl
    string +=  'End Date / Time : '+str(end_time)+ nl
    duration = (end_time - start_time)
    string +=  'Total Simulation Time (minutes): '+ str(duration) + nl
    string +=  'Total Simulation Time (seconds): '+ str(duration.total_seconds()) + nl
    string +=  'Number of time steps in the simulation: '+ str(atm_obj.stop)+ nl
    string +=  'Time(Seconds)/Timestemp: ' + str(duration.total_seconds()/atm_obj.stop) + nl

    # return string
    if atm_obj.control['Archive_simulation']:
        string +=  'Archive Status: Active'+ nl
        string +=  'Archive Name : '+str(atm_obj.control['Simulation_name'])+ nl
    else:
        string +=  'Archive Status: Inactive'+ nl
    string +=  ' '+ nl
    string +=  'Number of time steps in the simulation: '+ str(atm_obj.stop)+ nl
    string +=  ' '+ nl
    string +=  '-' * short_divider+ nl
    string +=  ' Initial Cohort Information'+ nl
    string +=  '-' * short_divider+ nl
    string +=  'Outputs of Initial Cohort Distribution:'+ nl
    #~ print atm_obj.control['Initialize_Control']
    if atm_obj.control['Initialize_Control']['Initial_Cohort_Distribution_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        for c in atm_obj.control['Initialize_Control']:
            if c.find('Figure') != -1 and atm_obj.control['Initialize_Control'][c]:
                string += '  ' + c + nl
    string +=  ' '+ nl

    string +=  'Outputs of Normalized Cohort Distribution:'+ nl
    if atm_obj.control['Initialize_Control']['Normalized_Cohort_Distribution_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        for c in atm_obj.control['Initialize_Control']:
            if c.find('Normal') != -1 and atm_obj.control['Initialize_Control'][c]:
                string += '  ' + c + nl
    string +=  ' '+ nl

    string +=  'Outputs of Cohort Ages:'+ nl
    if atm_obj.control['Initialize_Control']['Initial_Cohort_Age_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        for c in atm_obj.control['Initialize_Control']:
            if c.find('Age') != -1 and atm_obj.control['Initialize_Control'][c]:
                string += '  ' + c + nl

    string +=  ' '+ nl
    ##########################################################################
    string +=  '-' * short_divider+ nl
    string +=  '   Meteorologic Data Information   '+ nl
    string +=  '-' * short_divider+ nl
    # if atm_obj.control['Met_Control']['met_distribution'].lower() == 'point':
    #     string +=  'Point meteorologic data is used.'+ nl
    # else:
    #     string +=  'Meteorologic data is distributed.'+ nl
    # string +=  'Meteorologic Data File: '+ str(atm_obj.control['Met_Control']['met_file_distributed'])+ nl
    # if atm_obj.control['Met_Control']['degree_day_method'].lower() == 'read':
    #     string +=  'Degree Days read from files: ' + atm_obj.control['Met_Control']['TDD_file'] +' and '+atm_obj.control['Met_Control']['FDD_file']+ nl
    # else:
    #     string +=  'Degree Days calculated during simulation.'+ nl
    # string +=  ' '+ nl

    string +=  'Outputs:'+ nl
    if atm_obj.control['Met_Control']['Degree_Day_Output']:
        string +=  '  Degree-Days are output.'+ nl
        
    # Note: Might want to add climatic event probability and block size here
    ############################################################################
    string +=  '-' * short_divider+ nl
    string +=  '   General Terrestrial Information   '+ nl
    string +=  '-' * short_divider+ nl
    # string +=  'Ground Ice Distribution: '+atm_obj.control['Terrestrial_Control']['Ice_Distribution']+ nl
    string +=  'Drainage Efficiency Distribution: '+ atm_obj.control['Terrestrial_Control']['Drainage_Efficiency_Distribution']+ nl
    string +=  'Initial Active Layer Depth Distribution: '+atm_obj.control['Terrestrial_Control']['ALD_Distribution']+ nl
    string +=  ' '+ nl


    start_year = atm_obj.control['start_year']
    end_year =  atm_obj.control['initialization year'] + atm_obj.stop -1 
    
    cohort_list = atm_obj.grids.area.key_to_index.keys()
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
                init_total += atm_obj.grids.area[c, start_year].sum()
                final_total += atm_obj.grids.area[c, end_year].sum()
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
        
        init_total = atm_obj.grids.area[cohort, start_year].sum()
        final_total = atm_obj.grids.area[cohort, end_year].sum()
        string += 'Initial Fractional Area (km2): ' +  str(init_total )  + nl
        string += 'Final Fractional Area (km2): ' +   str(final_total)  + nl
        diff = final_total - init_total
        string += 'Total Fractional Change (km2): ' + str(diff)  + nl
        percent =  ((diff)/init_total)*100.
        string += 'Percent difference: ' + str(percent)  + nl
        #~ string += ' '  + nl
        
    return string
    
