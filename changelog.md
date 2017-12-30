# Changelog
All notable changes to this project will be documented in this file.

## [0.4.2] - 2017-12-29
### added
- comments in the calc_degree_days utilit
- phase 4 report


## [0.4.1] - 2017-12-29
### fixes
- testing suite
- in area grid last append_grid_year is changed to add_time_step

### changes
- example_control_files/Control_v2.yaml to 
example_control_files_Control_barrow.yaml


## [0.4.0] - 2017-12-28
## changes
- parameters section for poi transtiontions

## adds
- comments to atm.py

## [0.3.1] - 2017-12-21
### fixes
- fixes various bugs caused by typos 
- fixes missing commas
- fixes results to allow various cohort types

## [0.3.0] - 2017-12-21
### changed
- entire codebase and framework have been rewritten to use new grids and checks

## [0.2.5] - 2017-12-19
### fixed
- lake pond expasion function

## [0.2.4] - 2017-11-02
### fixed
- fixed bug with lake_pond_expansion

## [0.2.3] - 2017-10-19
### added
- atm/io/control.py control file io, and matching tests in tests/
- atm/control.py with Contol class, and matching tests in tests/

## [0.2.2] - 2017-10-18
## added
- grids submodule
  - ModelGrids class
  - AreaGrid class
  - ALDGrid class
  - POIGrid class
  - ICEGrid class
- testing suite for grid classes
- IO submodule
  - raster IO 
  - image IO
  - binary IO
- metadata describing canon cohort names
- metadata describing display cohort names
- skeleton for new check funcution

## [0.2.1] - 2017-10-03
### added 
- documents directory

### fixed 
- depth typo in LakePond

## [0.2.0] - 2017-09-21
### added
- run_general.py with run function that can run a list of checks for any checks defined
- added metadata map for checks in to atm/checks/__init__.py
- placeholder NA (no age) check functions for currently operating (barrow) checks

### changed
- moved python code into atm/
- moved check into atm/checks

### removed
- backup files 


## [0.1.0] - initial code from Bob Bolton
