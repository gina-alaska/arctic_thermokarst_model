import control_tools
import clite 
from datetime import datetime
from pandas import read_csv
import os

def get_boolean_input ():
    """
    """
    while True:
        ip = raw_input()
        if ip.lower() in ['true', 'false' ,'t' ,'f', 'yes','no']:
            break
        else:
            print("Invalid input, Try again.")
            print("Valid options are 'true', 'false' ,'t' ,'f', 'yes','no'")
    if ip.lower() in ['true', 't' , 'yes']:
        return True
    return False

def get_category_input (categories):
    """
    """
    while True:
        ip = raw_input()
        if ip in categories:
            break
        else:
            print("Invalid input, Try again.")
            print("Valid options are " + str(categories))
    return ip

def utility ():
    """
    """
    try:
        arguments = clite.CLIte([
            '--main-control-file-name',
            '--control-dir',
            '--cohort-table',
            '--input-dir', 
            '--output-dir', 
            '--tdd-file',
            '--fdd-file',
            ],    
        )
    except (clite.CLIteHelpRequestedError, clite.CLIteMandatoryError):
        print utility.__doc__
        return

    control_dir = arguments['--control-dir']
    input_dir = arguments['--input-dir']
    output_dir = arguments['--output-dir']
    cohort_table = read_csv(arguments['--cohort-table'])

    settings = {
        "first": "control generator utility",
        "last": "",
        "date": datetime.now(),
        "input-dir": input_dir,
        "output-dir": output_dir,
        "control-dir": control_dir,
        'TDD-in': arguments['--tdd-file'],
        'FDD-in': arguments['--fdd-file']
    }

    print("Create a separate archive control file?")
    print("(These settings control which results are stored in the archive)")
    settings['seprate_archive_data'] = get_boolean_input()

    print("Create an init-area control file?")
    print("(These is the list of raster area input files)")
    settings['seprate_init_area_data'] = get_boolean_input()

    settings["cohorts"] = cohort_table['cohort'].to_list()
    settings["transition-order"] = \
        cohort_table[
            cohort_table['transition_to'] != 'None'
        ]['cohort'].to_list()

    print("Save initial cohort distribution figures?")
    settings['init-dist-fig'] = get_boolean_input()

    print("Save normalized initial cohort distribution figures?")
    settings['norm-dist-fig'] = get_boolean_input()
    
    print("Save initial cohort age figures?")
    settings['init-age-fig'] = get_boolean_input()

    # print("What is the underlying ice distribution?")
    # 'poor', 'pore', 'wedge', or 'massive'
    # settings['ice-distribution'] = ??

    settings["drainage-efficiency"] = "random"

    print("Which cohort do drained lakes become?")
    settings["lakes-drain-to"] = get_category_input(settings["cohorts"])

    print("Which cohort do ponds infill to?")
    settings["ponds-fill-to"] = get_category_input(settings["cohorts"])

    settings['lake_types'] = \
        cohort_table[ cohort_table['type'] == 'Lake']['cohort'].to_list()

    settings['pond_types'] = \
        cohort_table[ cohort_table['type'] == 'Pond']['cohort'].to_list()

    cohort_transitions = cohort_table\
        [cohort_table['transition_to'] != 'None']\
        [["transition_to","transition_type", 'cohort']]

    cohort_transitions.index = cohort_transitions['cohort']
    del cohort_transitions['cohort']

    settings['cohort-area-files'] = cohort_table['init_area_data'].to_list()

    settings['cohort-transitions'] = cohort_transitions.T.to_dict()

    configs = control_tools.generate(settings)

    if not os.path.exists(control_dir):
        os.makedirs(control_dir)

    if 'archive_data' in configs:
        with open(os.path.join(control_dir, '00_archive_data.yaml'), 'w') as fd:
            fd.write(configs['archive_data'])
    if 'init_area_data' in configs:
        with open(os.path.join(control_dir, '00_Cohort_List.yaml'), 'w') as fd:
            fd.write(configs['init_area_data'])
    
    with open(os.path.join(control_dir, '00_Terrestrial_Control.yaml'), 'w') as fd:
        fd.write(configs['terrestrial'])
    
    with open(os.path.join(control_dir, '00_Met_Control.yaml'), 'w') as fd:
        fd.write(configs['met'])
    
    with open(os.path.join(control_dir, '00_Lake_Pond_Control.yaml'), 'w') as fd:
        fd.write(configs['lake_pond'])

    with open(os.path.join(control_dir, '00_Initialize_Control.yaml'), 'w') as fd:
        fd.write(configs['initialize'])
    
    with open(arguments['--main-control-file-name'], 'w') as fd:
        fd.write(configs['main'])

    for cfg in configs:
        if not '_config' in cfg: 
            continue
        name = '01_' + cfg.replace('_config', "_Control.yaml")
        with open(os.path.join(control_dir, name), 'w') as fd:
            fd.write(configs[cfg])


if __name__ == '__main__':
    utility()
    
