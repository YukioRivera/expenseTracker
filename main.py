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
from analysis import dataAnalysis

# ------------------------------- class
import analysis

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

# --------------------------------------------------------------------

# ----------------------- Analysis -----------------------
# Analysis code
# showCategories(conn)


# ------------------- Class Test
test = dataAnalysis(conn)

# test.dayofTheWeek(True)
# print("Without Edu")
# test.dayofTheWeek(False)
# combinedMonths = test.monthlySpending(False)
# print(combinedMonths)
# year_month = test.monthlySpending_withYear(False)
# print(year_month)


# catMonth = test.category_by_month(False)
# catMonth = test.category_by_year(False)
# print(catMonth)

# result = test.SpecificVendors_TotalSpent(False)
result = test.SpecificVendors_TotalSpent_Monthly(False)
# result = test.SpecificVendors_TotalSpent_Yearly(False)
print(result.to_string())
# bar
# test.create_bar_charts(True)
# test.create_bar_charts(False)

# table
# test.create_tables(True)
# test.create_tables(False)
# for index, row in test.iterrows():
#     print(row)

