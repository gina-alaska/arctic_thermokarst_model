Arctic Thermokarst Model

# Running the model
1. get the code by cloning this repo
2. get the data at <add location> and put it on your machine at <path to data>
3. cd <path to data>
4. edit the Run_dir line in 'Control' to be <path to data>
5. python <path to code repo>/atm/ATM.py Control
6. results will be stored in `./output/barrow/` with archived results in `./output/barrow/archive`


# running tests
from atm root

## run all
`python -m unittest discover tests/`

## run a test
`python tests/test_<file>.py`
