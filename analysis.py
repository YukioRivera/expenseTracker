import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def showCategories(conn):
    
    query = conn.execute("SELECT * FROM expenses")
    # print(query)
    
    # convert sql query to dataframe 
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    # print(df)

    # aggregate them by categories and show the amount spent for each category
    
    # show a pie chart of the percent of total spending 
    
    
    
    # Remove payment information, payments I made towards card 
    df_clean = df[df['Type'] != 'Payment']
    # print(df_clean)
    df_clean.plot(x="Category", y="Amount", kind="bar")
    plt.show()
    
    # removes education bills
    df_noEdu = df_clean[df_clean['Category'] != 'Education']
    print(df_noEdu)

# conn.close()