The purpose of this repo is to perform API tests on the fabmo engine.

First create a virtual environment in this directory,
 > python -m venv ./venv

Then activate the virtual environment,
 > . venv/bin/activate

Download the requirements,
 > pip install -r requirements.txt

The tests in this directory depend on environment variables.
You can either define them in the environment yourself or 
create a ".venv" file for the python-dotenv package to load 
for you. There is a file named ".env.example" in this directory.
You can use it to see which variables and what the format of the
values they need looks like. Either copy it:
 > cp .env.example .env
 > vi .env
and edit it, or just create one from scratch

To run a test and see the output,
 > pytest some_test.py -s

To run all tests and see the output,
 > pytest -s
!!!!All tests currently will not work. We need to force the order somehow.

WIP status:

The more_tests directory contains tests that will hit an api endpoint
and produce a response, but are not necessarily useful in their
current state. i.e. They do not validate that anything actually happened.

The jobs directory holds test jobs.

test_runMacro_two_hundred_one.py is complete. The pauses are a bit longer
than they need to be, but sometimes this file takes a little bit longer to run.

test_runNextJob.py Works but only for a file that is already queued up
that is less than 600 seconds long. The file cannot contain a pause.

test_submitJob.py needs work. The job id is currently hard coded. Needs to be flexible.
