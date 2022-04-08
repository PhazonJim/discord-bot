# Installation guide

## Install Python
1. Install Python v3.9 or higher
2. https://www.python.org/downloads/

## Create a Virtual Environment for Python
1. `cd` into the root directory of this project
2. run `python3 -m venv .venv` (or install the virtual environment wherever is convenient)
3. Activate the virtual environment:
 * On Windows in bash you can run: `.venv\Scripts\activate.bat`
 * On Mac OS and Linux you can run `source .venv/bin/activate`

## Install Dependencies

1. In the same directory, run `pip install -r requirements.txt`

## Configuration
1. Rename `.env.example` to `.env`
2. Replace the values in the `.env` file with the appropriate data
 * `TEMP_PATH`, `DB_NAME`, and `USER_TABLE` can be left as-is unless you have a preference for your db and table names and location 

## Running
1. In the root directory of this project, run `python -m main`