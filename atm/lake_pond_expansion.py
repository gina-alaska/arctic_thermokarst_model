
import numpy as np
from copy import deepcopy


#~ def large_lake_check ( lp_cohorts, year, grids, control ):
    #~ """if entire cell is water move to large lakes
    #~ """
    #~ shape = grids.shape
    #~ total = np.zeros(shape)
    #~ for cohort in lp_cohorts:
        #~ total += grids.area[year,cohort]


    #~ normalize = total >= 1.0

    #~ large = [l for l in lp_cohorts if l.lower().find('large') != -1]
    #~ not_large = [l for l in lp_cohorts if l.lower().find('large') == -1]

    ##count = np.zeros(shape)
    ##for cohort in large:
    ##    has_area = grids.area[year,cohort] > 0
    ##    count[has_area] += 1


    #~ for cohort in large:
        #~ grids.area[year,cohort + '--0'][normalize] = (total / len(large))[normalize]

    #~ for cohort in not_large:
        #~ grids.area[year,cohort+ '--0'][ normalize ] = 0

def infill ( ponds, year, grids, control):
    """The purpose of this module is to infill ponds at a prescribed rate with
    vegetation, which will presumably be non-polygonal ground.

    This module is developed due to paper that states with warming temperatures,
    ponds are shrinking due in part to infilling of vegetation.  Paper is in
    press and was set out by Anna L. in March 2015.
    """
    ## no infill in first time step
    if year == control['start year']:
        return

    transitions_to = control['Lake_Pond_Control']['Ponds_fill_to']

    shape = grids.shape
    pond_area = np.zeros(shape)

    for p in ponds:
        pond_area += grids.area[year, p ]

    change_pond_area = np.logical_and(pond_area > 0,  pond_area < 1)

    ttd_greater = grids.degreedays.thawing[year] > grids.degreedays.thawing[year-1]

    change_pond_area = np.logical_and(ttd_greater, change_pond_area)

    for p in ponds:
        infill_const = control['Lake_Pond_Control'][p+'_Infill_Constant']

        p_buckets = [b for b in grids.area.key_to_index if b.find(p) != -1]
        p_buckets = [b for b in p_buckets if b.find('--') != -1]

        for b in p_buckets:
            change = grids.area[year, b][change_pond_area]  * infill_const
            grids.area[year, b][change_pond_area] -= change
            grids.area[year, transitions_to][change_pond_area] -= change





def expansion ( lp_cohorts, year, grids, control):
    """
    """

    shape = grids.shape

    ## get total
    total = np.zeros(shape)
    for cohort in lp_cohorts:
        total += grids.area[year,cohort]

    ## aoi

    model_area_mask = grids.area.area_of_interest()

    ## water bodies can expand if area is present and not filling entire cell
    can_expand = np.logical_and(total > 0.0, total < 1.0)

    can_expand = np.logical_and(can_expand, model_area_mask )

    ## create 2x multiplier where climate events is true
    ## True -> 1, False ->0, +1 -> 2, 1 respectivly
    climate_events = grids.climate_event[year].astype(int) + 1

    import matplotlib.pyplot as plt

    #~ plt.imshow(climate_events)
    #~ plt.colorbar()
    #~ plt.show()

    #~ climate_events = np.ones(shape)

    ## set up expansion amount
    expansion = np.zeros(shape)
    for cohort in lp_cohorts:
        expansion = expansion + (
            climate_events * control['Lake_Pond_Control'][cohort + '_Expansion']
        )


    all_cohorts = set([
        i for i in grids.area.key_to_index.keys() if i.find('--') == -1
    ])
    land_cohorts = all_cohorts - set(lp_cohorts)
    land_cohorts = land_cohorts - set([
        c for c in all_cohorts if c.lower().find('river') != -1
    ])
    land_cohorts = land_cohorts - set([
        c for c in all_cohorts if c.lower().find('urban') != -1
    ])

    #~ print 'land_cohorts',land_cohorts
    land_available = np.zeros(shape)
    for cohort in land_cohorts:
        land_available += grids.area[year,cohort]

    ## Expands to entire land area
    #~ plt.imshow(expansion)
    #~ plt.colorbar()
    #~ plt.show()
    entire_area = np.logical_and(can_expand, expansion >= land_available)
    for cohort in lp_cohorts:
        area = grids.area[year,cohort]
        exp = area  + (area / total) * land_available

        grids.area[year,cohort + '--0'][entire_area] = exp[entire_area]

    for cohort in land_cohorts:
        bucket_list = [
            b for b in grids.area.key_to_index if b.find(cohort) != -1
        ]
        for bucket in bucket_list:
            if bucket.find('--') == -1:
                continue
            grids.area[year, bucket][entire_area] = 0.0

    #~ return
    ## expand and reduce
    not_entire_area = np.logical_not( entire_area )
    not_entire_area = np.logical_and( not_entire_area, model_area_mask)
    not_entire_area = np.logical_and( not_entire_area, can_expand)
    #~ plt.imshow(not_entire_area)
    #~ plt.colorbar()
    #~ plt.show()


    for cohort in lp_cohorts:
        area = grids.area[year, cohort + '--0']
        exp = climate_events * control['Lake_Pond_Control'][cohort + '_Expansion']

        grids.area[year,cohort + '--0'][not_entire_area] = \
            area[not_entire_area] + exp[not_entire_area]


    land_cohorts = list(land_cohorts)

    count = np.zeros(shape)
    for cohort in land_cohorts:
        has_area = grids.area[year,cohort] > 0
        has_area = np.logical_and(has_area, not_entire_area )

        count[has_area] += 1

    fraction = expansion / count

    left_over = np.zeros(shape)
    for cohort in land_cohorts:
        has_area = grids.area[year,cohort] > 0
        has_area = np.logical_and(has_area, not_entire_area )


        not_enough = np.logical_and(has_area, grids.area[year,cohort] <= fraction )
        ## has_area = np.logical_and(has_area, grids.area[year,cohort] > fraction )

        grids.area[year,cohort + '--0'][ has_area ] -= fraction [ has_area ]

        left_over[not_enough] += np.abs(grids.area[year,cohort + '--0'][ not_enough ])
        grids.area[year,cohort+ '--0'][ not_enough ]  = 0

    count = np.zeros(shape)
    for cohort in lp_cohorts:
        has_area = grids.area[year,cohort] > 0
        has_area = np.logical_and(has_area, not_entire_area )
        count[has_area] += 1

    reduction = left_over/count

    for cohort in lp_cohorts:
        has_area = grids.area[year,cohort] > 0
        has_area = np.logical_and(has_area, not_entire_area )
        grids.area[year,cohort+ '--0'][  has_area ] -= reduction[ has_area ]


    total = np.zeros(shape)
    for cohort in lp_cohorts:
        total += grids.area[year,cohort]

    normalize = total >= 1.0

    #~ if normalize.any():
        #~ print 'normalize'

    for cohort in lp_cohorts:
        grids.area[year,cohort+ '--0'][ normalize ]  =  \
            grids.area[year,cohort+ '--0'][ normalize ]/\
            total[ normalize ]


    for cohort in land_cohorts:
        grids.area[year,cohort+ '--0'][ normalize ] = 0
