Rawser W Spicer

2017-10-23

Introduction
============

The Arctic Thermokarst Model (ATM) models thermokarst disturbances in
the Alaskan arctic and boreal forests, as discussed in more detail in
the introduction to the report on [Phase
1](https://github.com/gina-alaska/arctic_thermokarst_model/blob/master/documents/Arctic_Thermokarst_Model_Phase_0_1.docx)
\[1\]. Phase 1 and 2 focused on the expanding the capabilities, and
improving the data structurers for the ATM. Originally phase 2 was going
to include the integration of the new data structures designed in that
phase, but that was deemed to be difficult to before the model
configuration system was redesigned, and moved to a later phase. Phase 3
will tackle the reading and internal management of the control files and
internal management of the configuration values.

Phase 2: Control Files
======================

The control files for the ATM contain all of the information needed for
modeling the transition of area between cohorts. These files are
structured as a main control file that is used to launch the ATM, and
control files for each of the cohorts, and other model inputs. The main
control files contain the directory structure for the model. This phase
also archived a set of control files that should run the barrow region,
in the directory ‘example\_control\_files’. See the [Project
board](https://github.com/gina-alaska/arctic_thermokarst_model/projects/3?)\[2\]
or Issues
[List](https://github.com/gina-alaska/arctic_thermokarst_model/milestone/3)\[3\]
for issues in this phase.

The first thing that needed to be handled was the reading of the control
files. These files consist of key value pairs, or lists. The key value
pair files are the most common, and consist of white space separated key
value pairs on each line. The list files contain an item on each line.
In the current frame work the files are read in several places, with
duplicated code. ‘atm/io/control\_file.py’ was created to centralize the
reading of these file. A function to write the files was also created.

Next an object was created to manage the configuration values stored in
the control files. In the current framework the configuration values are
stored as attributes of the main ATM class in ‘atm/ATM.py’. These
attributes are created as they are read across the different
initialization functions. The new object centralized the configuration.
When the new object is loaded, the main control file is passed as input,
and loaded. The other control files are loaded, from the information in
the main control file. The configuration is stored in a hierarchal
dictionary with the main values at the highest level, and the values
from the other files at the next level down. For example:
CONFIGURATION\[‘Simulation\_area\`\] will access a value from the main
control file, and CONFIGURATION\[‘Lake\_Pond\_Control\`\]\[‘
Lake\_Distribution’\] will access a value form the file
’00\_lake\_pond\_control’.

The values in the new control are accessible via an overloaded
\_\_getitem\_\_, and \_\_getattr\_\_ functions. The \_\_setitem\_\_
function is also overloaded allowing runtime configuration values to be
set. The values loaded at the objects initialization are protected from
being over written by the objects this \_\_setitem\_\_ function.

Issues Encountered
==================

This phase arose as an issue with development during phase 2, but there
were no major issues in countered during this phase of development
itself.

An Issue in phase 2 that was not recorded in that report was a problem
with the loading of the raster files. Bob’s initial code for resizing
the grid had a bug causing the resized grid to be off by one row and one
column of initial grid elements. The bug was caused by an index being
off by one. This still needs to be tested once the object for fractional
areas is integrated.

Phase 4: Moving Forward
=======================

Phase 4 will included the reaming integration tasks from phase 2, and
new tasks for creating input rasters, and control files for the entire
Arctic Costal Plane. Future improvements to the control objects could
include the ability save the configuration values.

References
==========

\[1\] Phase 1 status report:
<https://github.com/gina-alaska/arctic_thermokarst_model/blob/master/documents/Arctic_Thermokarst_Model_Phase_0_1.docx>

\[2\] Phase 2 project board:
<https://github.com/gina-alaska/arctic_thermokarst_model/projects/3>?

\[3\] Issues
<https://github.com/gina-alaska/arctic_thermokarst_model/milestone/3>
