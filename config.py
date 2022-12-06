import os
from dotenv import load_dotenv
# The tests in this directory depend on environment variables.
# You can either define them in the environment yourself or 
# create a ".venv" file for the python-dotenv package to load 
# for you. There is a file named ".env.example" in this directory.
# You can use it to see which variables and what the format of the
# values they need looks like. Eitheer copy it:
# > cp .env.example .env
# > vi .env
# and edit it, or just create one from scratch

load_dotenv()

class Config:
    API_URL = os.getenv("API_URL")

config = Config()

