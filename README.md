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

IMPORTANT!
Currently requires fabmo-engine change https://github.com/FabMo/FabMo-Engine/commit/680f8dd03f5fc7f5b800881056742851982e2f27
Until a PR is submitted
