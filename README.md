Arctic Thermokarst Model

# Setup
An anaconda environment is provided to help run the model. You will also have to install ffmpeg. 

From the model repository directory,
Run `conda env create -f environment3yml` to set up the environment. 

If you don't need to change the environment, or run the tests skip to Running the model

## Changes to the anaconda envenvironment
Use `source activate atm-env` to start using the environemnt, and `source deactivate` to stop using it.
When the environment is active you can install new packages for the code to use, and run the code directly via python. 

For more information on anconada environments see [Managing environments](https://conda.io/docs/user-guide/tasks/manage-environments.html)

# Running the model
1. Get the code by cloning this repo.
2. Get the  acp data or barrow data at https://drive.google.com/drive/folders/1LIWLwiMtuuMxhaZwV8LztJngzJIB1YHf?usp=sharing 
  * download and uzip either acp_data.zip or barrow_data.zip.
3. cd to repo root.
4. Make a copy of control_barrow.yaml or control_acp.yaml in example_control_files as my_control_copy.yaml.
5. Change the Input_dir field in my_control_copy.yaml to be the absoloute path to the data you downloaded.
6. Running the model.
 * If atm-env is active run: `python atm/ATM.py example_control_files/my_control_copy.yaml`.
 * If it is not: `run_atm.sh example_control_files/my_control_copy.yaml`.
7. Results will be generated in the directory output.

# running tests
From atm root with the atm-env active.

## run all
`python -m unittest discover tests/`

## run a test
`python tests/test_<file>.py`
