import sqlite3
import matplotlib as plt
import numpy as np
import pandas as pd

def showCategories(conn):
    
    query = conn.execute("SELECT * FROM expenses")
    # print(query)
    
    # convert sql query to dataframe 
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    print(df)
    
    # find all the categories
    df_categories = df.groupby('Category', as_index=True).sum()
    # print(df_categories)
    

    # aggregate them by categories and show the amount spent for each category
    
    # show a pie chart of the percent of total spending 

# conn.close()