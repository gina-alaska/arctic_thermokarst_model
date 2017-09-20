import numpy as np
import gdal, os, sys, glob, random
import pylab as pl
from math import exp as exp

"""
The purpose of this module is to check the status of the ponds.
Ponds are defined as shallow lakes, or lakes that are shallower
than the ice thickness.  Once the pond becomes deeper than
the ice thickness (either through climate change (thinner ice)
or thermokarst (deepening of the pond)), then the Pond becomes
a lake (or a deep lake).

In this module, I am assuming that Ponds can only deepen if
the Total Degree Days is the current (up to that time) maximum.
If the TDDs are less than the maximum, the pond depth remains
the same.
"""



def check_Ponds_WT_NA(self, element, time):#, growth_time_required):
    """No age place holder
    """
    pass
    
#=======================================================================
def check_Ponds_WT_Y(self, element, time):#, growth_time_required):

    # --------------------------------------
    # Check to see if the Total Degree Days
    # are at the current maximum.
    #
    # If yes, set new TDD max and increase
    # the pond count.
    # --------------------------------------
#    if element == 0:
    if self.Met['met_distribution'].lower() == 'point':
        if time == 0:
            self.TDD_max = self.degree_days[0,1]
        else:
            if self.degree_days[time,1] > self.TDD_max:
                # Set new TDD_max
                self.TDD_max = self.degree_days[time,1]
                # Increase the pond count
                self.Pond_WT_Y_count = self.Pond_WT_Y_count + 1
    else:
        if time == 0:
            self.TDD_max = self.TDD[0,:]
        else:
            for i in range(0,self.ATTM_nrows * self.ATTM_ncols):
                if self.TDD[time, i] > self.TDD_max[i]:
                    # Set new TDD_max
                    self.TDD_max[i] = self.TDD[time,i]
                    # Increase the pond count
                    self.Pond_WT_Y_count = self.Pond_WT_Y_count + 1
                        
    # ----------------------------------
    # Check to see if ponds are present
    # ----------------------------------
    if self.ATTM_Ponds_WT_Y[element] > 0.0:
        # --------------------------------------
        # Check to see if the Total Degree Days
        # are at the current maximum.
        # --------------------------------------
        if self.Met['met_distribution'].lower() == 'point':
            if self.degree_days[time,1] == self.TDD_max:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_Y_Depth[element] = self.Pond_WT_Y_Depth[element] + \
                  np.sqrt(self.Pond_WT_Y_count)/ \
                  self.LakePond['Pond_WT_Y_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_Y_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_Y[element] >= \
                      self.LakePond['Pond_WT_Y_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_Y[element] = self.ATTM_Lakes_WT_Y[element] + \
                          self.ATTM_Ponds_WT_Y[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_Y[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_Y_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_Y[element] = self.Pond_WT_Y_growth[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_Y_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_WT_Y_growth[element] >= self.LakePond['Pond_WT_Y_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_Y[element] = self.ATTM_Lakes_WT_Y[element] + \
                          self.ATTM_Ponds_WT_Y[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_Y[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_Y_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_Y[element] = self.Pond_growth_WT_Y[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_Y[element] = self.ATTM_Ponds_WT_Y[element]
                        self.Pond_growth_WT_Y[element] = 0.0
        else:
            if self.TDD[time, element] == self.TDD_max[element]:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_Y_Depth[element] = self.Pond_WT_Y_Depth[element] + \
                  np.sqrt(self.Pond_WT_Y_count)/ \
                  self.LakePond['Pond_WT_Y_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_Y_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_Y[element] >= self.LakePond['Pond_WT_Y_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_Y[element] = self.ATTM_Lakes_WT_Y[element] + \
                          self.ATTM_Ponds_WT_Y[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_Y[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_Y_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_Y[element] = self.Pond_growth_WT_Y[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_Y_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_growth_WT_Y[element] >= self.LakePond['Pond_WT_Y_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_Y[element] = self.ATTM_Lakes_WT_Y[element] + \
                          self.ATTM_Ponds_WT_Y[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_Y[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_Y_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_Y[element] = self.Pond_growth_WT_Y[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_Y[element] = self.ATTM_Ponds_WT_Y[element]
                        self.Pond_growth_WT_Y[element] = 0.0

#-----------------------------------------------------------------------------------------
def check_Ponds_WT_M(self, element, time):#, growth_time_required):

    # --------------------------------------
    # Check to see if the Total Degree Days
    # are at the current maximum.
    #
    # If yes, set new TDD max and increase
    # the pond count.
    # --------------------------------------
#    if element == 0:
    if self.Met['met_distribution'].lower() == 'point':
        if time == 0:
            self.TDD_max = self.degree_days[0,1]
        else:
            if self.degree_days[time,1] > self.TDD_max:
                # Set new TDD_max
                self.TDD_max = self.degree_days[time,1]
                # Increase the pond count
                self.Pond_WT_M_count = self.Pond_WT_M_count + 1
    else:
        if time == 0:
            self.TDD_max = self.TDD[0,:]
        else:
            for i in range(0,self.ATTM_nrows * self.ATTM_ncols):
                if self.TDD[time, i] > self.TDD_max[i]:
                    # Set new TDD_max
                    self.TDD_max[i] = self.TDD[time,i]
                    # Increase the pond count
                    self.Pond_WT_M_count = self.Pond_WT_M_count + 1
                        
    # ----------------------------------
    # Check to see if ponds are present
    # ----------------------------------
    if self.ATTM_Ponds_WT_M[element] > 0.0:
        # --------------------------------------
        # Check to see if the Total Degree Days
        # are at the current maximum.
        # --------------------------------------
        if self.Met['met_distribution'].lower() == 'point':
            if self.degree_days[time,1] == self.TDD_max:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_M_Depth[element] = self.Pond_WT_M_Depth[element] + \
                  np.sqrt(self.Pond_WT_M_count)/ \
                  self.LakePond['Pond_WT_M_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_M_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_M[element] >= \
                      self.LakePond['Pond_WT_M_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_M[element] = self.ATTM_Lakes_WT_M[element] + \
                          self.ATTM_Ponds_WT_M[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_M[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_M_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_M[element] = self.Pond_WT_M_growth[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_M_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_WT_M_growth[element] >= self.LakePond['Pond_WT_M_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_M[element] = self.ATTM_Lakes_WT_M[element] + \
                          self.ATTM_Ponds_WT_M[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_M[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_M_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_M[element] = self.Pond_growth_WT_M[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_M[element] = self.ATTM_Ponds_WT_M[element]
                        self.Pond_growth_WT_M[element] = 0.0
        else:
            if self.TDD[time, element] == self.TDD_max[element]:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_M_Depth[element] = self.Pond_WT_M_Depth[element] + \
                  np.sqrt(self.Pond_WT_M_count)/ \
                  self.LakePond['Pond_WT_M_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_M_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_M[element] >= self.LakePond['Pond_WT_M_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_M[element] = self.ATTM_Lakes_WT_M[element] + \
                          self.ATTM_Ponds_WT_M[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_M[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_M_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_M[element] = self.Pond_growth_WT_M[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_M_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_growth_WT_M[element] >= self.LakePond['Pond_WT_M_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_M[element] = self.ATTM_Lakes_WT_M[element] + \
                          self.ATTM_Ponds_WT_M[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_M[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_M_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_M[element] = self.Pond_growth_WT_M[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_M[element] = self.ATTM_Ponds_WT_M[element]
                        self.Pond_growth_WT_M[element] = 0.0


#-----------------------------------------------------------------------------------------
def check_Ponds_WT_O(self, element, time):#, growth_time_required):

    # --------------------------------------
    # Check to see if the Total Degree Days
    # are at the current maximum.
    #
    # If yes, set new TDD max and increase
    # the pond count.
    # --------------------------------------
#    if element == 0:
    if self.Met['met_distribution'].lower() == 'point':
        if time == 0:
            self.TDD_max = self.degree_days[0,1]
        else:
            if self.degree_days[time,1] > self.TDD_max:
                # Set new TDD_max
                self.TDD_max = self.degree_days[time,1]
                # Increase the pond count
                self.Pond_WT_O_count = self.Pond_WT_O_count + 1
    else:
        if time == 0:
            self.TDD_max = self.TDD[0,:]
        else:
            for i in range(0,self.ATTM_nrows * self.ATTM_ncols):
                if self.TDD[time, i] > self.TDD_max[i]:
                    # Set new TDD_max
                    self.TDD_max[i] = self.TDD[time,i]
                    # Increase the pond count
                    self.Pond_WT_O_count = self.Pond_WT_O_count + 1
                        
    # ----------------------------------
    # Check to see if ponds are present
    # ----------------------------------
    if self.ATTM_Ponds_WT_O[element] > 0.0:
        # --------------------------------------
        # Check to see if the Total Degree Days
        # are at the current maximum.
        # --------------------------------------
        if self.Met['met_distribution'].lower() == 'point':
            if self.degree_days[time,1] == self.TDD_max:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_O_Depth[element] = self.Pond_WT_O_Depth[element] + \
                  np.sqrt(self.Pond_WT_O_count)/ \
                  self.LakePond['Pond_WT_O_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_O_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_O[element] >= \
                      self.LakePond['Pond_WT_O_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_O[element] = self.ATTM_Lakes_WT_O[element] + \
                          self.ATTM_Ponds_WT_O[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_O[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_O_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_O[element] = self.Pond_WT_O_growth[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_O_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_WT_O_growth[element] >= self.LakePond['Pond_WT_O_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_O[element] = self.ATTM_Lakes_WT_O[element] + \
                          self.ATTM_Ponds_WT_O[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_O[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_O_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_O[element] = self.Pond_growth_WT_O[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_O[element] = self.ATTM_Ponds_WT_O[element]
                        self.Pond_growth_WT_O[element] = 0.0
        else:
            if self.TDD[time, element] == self.TDD_max[element]:
                # Increase the depth of the pond by sqrt[pond_count]
                self.Pond_WT_O_Depth[element] = self.Pond_WT_O_Depth[element] + \
                  np.sqrt(self.Pond_WT_O_count)/ \
                  self.LakePond['Pond_WT_O_depth_control']
                # Check if pond depth >= ice thickness
                if self.Pond_WT_O_Depth[element] >= self.ice_thickness[element]:
                    # Check if Pond Growth has been sustained over time
                    if self.Pond_growth_WT_O[element] >= self.LakePond['Pond_WT_O_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_O[element] = self.ATTM_Lakes_WT_O[element] + \
                          self.ATTM_Ponds_WT_O[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_O[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_O_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_O[element] = self.Pond_growth_WT_O[element] + 1.
            else:
                # Pond depth remains the same.
                # Check if pond depth >= ice thickness
                if self.Pond_WT_O_Depth[element] >= self.ice_thickness[element]:
                    if self.Pond_growth_WT_O[element] >= self.LakePond['Pond_WT_O_growth_time_required']:
                        # Transition Ponds -> Lakes
                        self.ATTM_Lakes_WT_O[element] = self.ATTM_Lakes_WT_O[element] + \
                          self.ATTM_Ponds_WT_O[element]
                        # Transition Ponds -> 0.0
                        self.ATTM_Ponds_WT_O[element] = 0.0
                        # Transition Pond Depth -> 0.0
                        self.Pond_WT_O_Depth[element] = 0.0
                        # Update pond growth array
                        self.Pond_growth_WT_O[element] = self.Pond_growth_WT_O[element] + 1.
                    else:
                        self.ATTM_Ponds_WT_O[element] = self.ATTM_Ponds_WT_O[element]
                        self.Pond_growth_WT_O[element] = 0.0



            


            
