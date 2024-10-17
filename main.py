import pandas as pd
import matplotlib
import seaborn as sns
import sklearn
import numpy as np
import csv
import sqlite3

# imports from files
from database import connect_db, create_tables
from importdata import importData
from analysis import showCategories

print("All imports worked")

# connecting to the database
conn = connect_db()

# ----------------------- create tables -----------------------
# create tables - rerun this when want to tupdate the tables 
# create_tables(conn)
# -------------------------------------------------------------

# ----------------------- import data from csv -----------------------
# import data from csv
# df = importData(conn)
# print(df) # check the table putput
# --------------------------------------------------------------------

# ----------------------- Analysis -----------------------
# Analysis code
showCategories(conn)
