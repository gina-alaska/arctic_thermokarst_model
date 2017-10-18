Rawser W Spicer

2017-10-18

Introduction
============

The Arctic Thermokarst Model (ATM) models thermokarst disturbances in
the Alaskan arctic and boreal forests, as discussed in more detail in
the introduction to the report on [Phase
1](https://github.com/gina-alaska/arctic_thermokarst_model/blob/master/documents/Arctic_Thermokarst_Model_Phase_0_1.docx)
\[1\]. While Phase 1 focused on the project management, and ability to
extend the ATM to further regions, Phase 2 was intended to create better
data structures to represent the grid like data in the model.

Phase 2: Grids, and Checks 
===========================

There were two primary goals for phase 2: design objects to represent
the various grid like data in the model, and to create a simplified
check function (functions that determine the change in cohorts at each
time step) that leverages the grid objects. A scheme for canon cohort
names (name used internally by the model) was also determined. See the
[Project
board](https://github.com/gina-alaska/arctic_thermokarst_model/projects/2?)\[2\]
or Issues [Issues
List](https://github.com/gina-alaska/arctic_thermokarst_model/issues?utf8=✓&q=is%3Aissue%20project%3Agina-alaska%2Farctic_thermokarst_model%2F2%20)\[3\]
for issues in this phase.

Initially the grids that were determined to be needed were for the
fractional area of each cohort, the active layer depth(ALD), The
protective layer (PL) at each cohort, and the probability of
instantiation(POI) for each cohort. These grids all vary over time. A
final ice grid was determined to be needed at a later point, and added.
The ice grid tracks ice quality and is static in time.

The new check function was created to take advantage of these new grids,
and the fact the internal logic of most of the cohort checks was the
same. The current checks mainly varied in the final step where the
transition occurs. The information on how transitions occur could be
passed to the new function.

The design of the class (GitHub issue 15) AreaGrid in
atm/grids/area\_grid.py served as the main template for the other grid
objects. It represents each the fractional area for all cohorts present
in all of the grid cells, as separate grids. These grids are flattened
and stored as a 2D grid where the first dimension is a number that can
be mapped to with the canon cohort names, and the second is the index
into the flattened grid. The 2D grids were stored in a list with each
index representing the time step of the model. Various getter and setter
methods were implemented to access data, as was the ability to add a new
time step to the grid.

The other grids all were based on this design with some differences. The
ALD, and PL grids are represented as a single object where the ALD is
constant for all cohorts but the PL is not at a given time step. The POI
grid was implemented with more limited setting functions, and the Ice
grid removes the temporal element. A final Model Grid object was created
which has an instance of each of the other grids for ease of management.
A suite of tests was also implemented for all of the gird objects.

When designing the area grid, a lot of extra IO functions for images and
raster were created. The canon cohort name scheme was also implemented.
During the clean up this was all moved to better locations.

Issues Encountered
==================

There were two main issues with the development of phase 2. The first
was that Bob Bolton indicated that the model may need to track how long
a the different parts of the fractional areas were in a specific cohort.
This was solved by adding age buckets to each of the Area grid cohorts.
The indexers can take care of accessing the sum of all the values by
passing just the canon cohort name, or just the bit for an age range by
giving the name followed by two dashes age.

The second problem came is integration of new model objects. It became
apparent that it would create unnecessary extra work to intergrade the
new objects before a scheme for tracking the configuration values was
devised. It was decided to move the integration, and create other output
function tasks to a later phase (phase 4) while the next phase (phase 3)
would tackle the configuration object.

Other issues were minor, but include the discovery that an Ice grid was
needed, and weather time sensitive objects changes should be treated as
current year values are modified previous year values, or next year
values are modified this year values. The was decided to use t current
year values are modified previous year values paradigm.

Phase 3: Moving Forward
=======================

Phase 3 will tackle the configuration values, and phase 4 will return to
the integration of objects created here. Other issues that could be
tackled in the future include standardizing the index format between
grids; the ALD grid is different from the other objects, or refactoring
all of the grids to inherit form an grid object that contains the common
functionality. Documentation of the testing code could also be imporved.

References
==========

\[1\] Phase 1 status report:
<https://github.com/gina-alaska/arctic_thermokarst_model/blob/master/documents/Arctic_Thermokarst_Model_Phase_0_1.docx>

\[2\] Phase 2 project board:
<https://github.com/gina-alaska/arctic_thermokarst_model/projects/2>?

\[3\] Issues
https://github.com/gina-alaska/arctic\_thermokarst\_model/issues?utf8=✓&q=is%3Aissue%20project%3Agina-alaska%2Farctic\_thermokarst\_model%2F2%20
