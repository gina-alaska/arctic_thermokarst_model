import numpy as np
import gdal, os, sys, glob, random
import pylab as pl
from math import exp as exp

#-----------------------------------------------------------------------------------------------
def check_LargeLakes_WT_Y(self, element, time):
    
    if self.ATTM_LargeLakes_WT_Y[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['LargeLake_WT_Y_depth_control'] 
        self.LargeLake_WT_Y_Depth[element] = self.LargeLake_WT_Y_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.LargeLake_WT_Y_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_Y[element] = self.ATTM_Ponds_WT_Y[element] + \
              self.ATTM_LargeLakes_WT_Y[element]
            self.ATTM_LargeLakes_WT_Y[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_LargeLakes_WT_M(self, element, time):
    
    if self.ATTM_LargeLakes_WT_M[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['LargeLake_WT_M_depth_control'] 
        self.LargeLake_WT_M_Depth[element] = self.LargeLake_WT_M_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.LargeLake_WT_M_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_M[element] = self.ATTM_Ponds_WT_M[element] + \
              self.ATTM_LargeLakes_WT_M[element]
            self.ATTM_LargeLakes_WT_M[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_LargeLakes_WT_O(self, element, time):
    
    if self.ATTM_LargeLakes_WT_O[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['LargeLake_WT_O_depth_control'] 
        self.LargeLake_WT_O_Depth[element] = self.LargeLake_WT_O_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.LargeLake_WT_O_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_O[element] = self.ATTM_Ponds_WT_O[element] + \
              self.ATTM_LargeLakes_WT_O[element]
            self.ATTM_LargeLakes_WT_O[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_MediumLakes_WT_Y(self, element, time):
    
    if self.ATTM_MediumLakes_WT_Y[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['MediumLake_WT_Y_depth_control'] 
        self.MediumLake_WT_Y_Depth[element] = self.MediumLake_WT_Y_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.MediumLake_WT_Y_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_Y[element] = self.ATTM_Ponds_WT_Y[element] + \
              self.ATTM_MediumLakes_WT_Y[element]
            self.ATTM_MediumLakes_WT_Y[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_MediumLakes_WT_M(self, element, time):
    
    if self.ATTM_MediumLakes_WT_M[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['MediumLake_WT_M_depth_control'] 
        self.MediumLake_WT_M_Depth[element] = self.MediumLake_WT_M_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.MediumLake_WT_M_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_M[element] = self.ATTM_Ponds_WT_M[element] + \
              self.ATTM_MediumLakes_WT_M[element]
            self.ATTM_MediumLakes_WT_M[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_MediumLakes_WT_O(self, element, time):
    
    if self.ATTM_MediumLakes_WT_O[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['MediumLake_WT_O_depth_control'] 
        self.MediumLake_WT_O_Depth[element] = self.MediumLake_WT_O_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.MediumLake_WT_O_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_O[element] = self.ATTM_Ponds_WT_O[element] + \
              self.ATTM_MediumLakes_WT_O[element]
            self.ATTM_MediumLakes_WT_O[element] = 0.0
            
#-----------------------------------------------------------------------------------------------
def check_SmallLakes_WT_Y(self, element, time):
    
    if self.ATTM_SmallLakes_WT_Y[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['SmallLake_WT_Y_depth_control'] 
        self.SmallLake_WT_Y_Depth[element] = self.SmallLake_WT_Y_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.SmallLake_WT_Y_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_Y[element] = self.ATTM_Ponds_WT_Y[element] + \
              self.ATTM_SmallLakes_WT_Y[element]
            self.ATTM_SmallLakes_WT_Y[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_SmallLakes_WT_M(self, element, time):
    
    if self.ATTM_SmallLakes_WT_M[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['SmallLake_WT_M_depth_control'] 
        self.SmallLake_WT_M_Depth[element] = self.SmallLake_WT_M_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.SmallLake_WT_M_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_M[element] = self.ATTM_Ponds_WT_M[element] + \
              self.ATTM_SmallLakes_WT_M[element]
            self.ATTM_SmallLakes_WT_M[element] = 0.0

#-----------------------------------------------------------------------------------------------
def check_SmallLakes_WT_O(self, element, time):
    
    if self.ATTM_SmallLakes_WT_O[element] > 0.0:
        
        # Determine the new lake depth
        depth_change = np.sqrt(time)/self.LakePond['SmallLake_WT_O_depth_control'] 
        self.SmallLake_WT_O_Depth[element] = self.SmallLake_WT_O_Depth[element] + depth_change

        # Determine the fractional change from Lakes -> Ponds
        # (if ice thickness is greater than lake depth)
        if self.SmallLake_WT_O_Depth[element] <= self.ice_thickness[element]:
            self.ATTM_Ponds_WT_O[element] = self.ATTM_Ponds_WT_O[element] + \
              self.ATTM_SmallLakes_WT_O[element]
            self.ATTM_SmallLakes_WT_O[element] = 0.0


            
