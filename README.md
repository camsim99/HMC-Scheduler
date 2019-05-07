# OR Final Project

## Broad overview

The python script `generate-dat.py` reads in configuration `csv`'s
from `config/` and template `ampl`scripts from `templates/`.  The
script then generates plain old `ampl` files in `build/`.  This way,
the user can conveniently edit the configuration in their spreadsheet
program of choice (e.g. Libreoffice or Excel) and rerun the model to
obtain alternate schedules.

See our final report for more documentation.
	
## Set-up
1. `git clone https://github.com/ianrabt/OR-Final-Project.git`
2. make sure `ampl` and `cplex` are in your path
3. either install *Jinja2* globally, or create a virtual environment as follows:
  1. create a Python virtual environment: `python3 -m venv env`
  2. activate it: `source env/bin/activate` (you can call
     `deactivate` to exit after you are done)
  3. install requirements: `pip install -r requirements.txt`

## Generating AMPL files from the CSV's
1. edit `.csv` files in `config/` (can edit in an Excel spreadsheet and download the files as '.csv' files)
2. run `./generate-dat.py`

## Running the AMPL model
1. launch an AMPL shell by running `ampl`.  Then, in that shell run the
   following:
2. `include schedule.run;` (see `schedule.run` for the commands being
   run)
