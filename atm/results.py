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
        for c in self.control['Initialize_Control']:
            if c.find('Figure') != -1 and self.control['Initialize_Control'][c]:
                string += '  ' + c + nl
    string +=  ' '+ nl

    string +=  'Outputs of Normalized Cohort Distribution:'+ nl
    if self.control['Initialize_Control']['Normalized_Cohort_Distribution_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        for c in self.control['Initialize_Control']:
            if c.find('Normal') != -1 and self.control['Initialize_Control'][c]:
                string += '  ' + c + nl
    string +=  ' '+ nl

    string +=  'Outputs of Cohort Ages:'+ nl
    if self.control['Initialize_Control']['Initial_Cohort_Age_Figure'] == False:
        string +=  '  No outputs generated.'+ nl
    else:
        for c in self.control['Initialize_Control']:
            if c.find('Age') != -1 and self.control['Initialize_Control'][c]:
                string += '  ' + c + nl

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
    end_year =  self.control.initialization_year + self.stop -1 
    
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
    
