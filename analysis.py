import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import calendar 
import re
import util
from thefuzz import fuzz
from thefuzz import process

# maybe remove 
from collections import OrderedDict


class dataAnalysis():
    
    def __init__(self, conn):
        df = pd.read_sql_query("SELECT TransactionDate, Description, Category, Type, ABS(Amount) FROM expenses", conn)
        df.rename(columns={'ABS(Amount)': 'Amount'}, inplace=True)
        df_cleaned = df[df['Type'] != 'Payment']
        df_cleaned = df_cleaned.drop(columns=['Type'])
        df_matches = util.StandardizeDescriptions(df_cleaned)
        self.conn = conn
        self.df = df_cleaned
        
    def print(self):
        print(self.df)
    
    # Defaulted at True and it will return data with edu expenses included, 
    # false will return data filtered without edu expenses 
    def get_data(self, withEdu=True):
        
        if withEdu:
            return self.df
               
        else:
            check_edu = self.df[self.df['Category'] != 'Education']
            return check_edu     
        
    def get_category_expenses(self, withEdu=True):
        """
        Returns a DataFrame with total expenses grouped by category.
        """
        df_categories = self.get_data(withEdu).groupby("Category")["Amount"].sum().reset_index()
        return df_categories

    def get_category_summary(self, withEdu=True):
        """
        Returns a summary DataFrame with category, expense count, and amount.
        """
        category_data = self.get_data(withEdu).groupby('Category')
        category_amounts = category_data["Amount"].sum().round(2)  # Sum of expenses
        category_expense_count = category_data.size()  # Count of expenses

        # Create summary DataFrame
        category_summary_df = pd.DataFrame({
            'Category': category_amounts.index,
            'Expense Count': category_expense_count,
            'Amount': category_amounts
        }).reset_index(drop=True)

        # Add total row
        total_amount_sum = round(category_amounts.sum(), 2)
        total_expense_count = category_expense_count.sum()
        total_row = pd.DataFrame([["Total:", total_expense_count, total_amount_sum]],
                                columns=["Category", "Expense Count", "Amount"])
        category_summary_df = pd.concat([category_summary_df, total_row], ignore_index=True)
        return category_summary_df

#   1.	Temporal Insights:
#       
#       Month and Quarter: Examine if spending varies seasonally or monthly.
#       Time of Day: Split transactions into periods (morning, afternoon, evening) to find peak spending times.
#       Rolling Totals: Calculate 7-day, 30-day, and 90-day rolling averages to observe short- and long-term spending trends.
    
    def get_day_of_week_expenses(self, withEdu=True):
        """
        Returns a DataFrame with total expenses grouped by day of the week.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Day'] = df['TransactionDate'].dt.day_name()

        # Group by day and sum
        spending_by_day = df.groupby('Day')['Amount'].sum().round(2)

        # Reorder days of the week
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        spending_by_day = spending_by_day.reindex(days_order)

        # Convert to DataFrame for consistency
        spending_by_day_df = spending_by_day.reset_index()
        spending_by_day_df.columns = ['Day', 'Amount']
        return spending_by_day_df
        
    def monthlySpending(self, withEdu=True):
        
        # get data
        df = self.get_data(withEdu)
        
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        # df['Month'] = df['TransactionDate'].dt.to_period('M') # keeps year and month 
        df['Month'] = df['TransactionDate'].dt.month # just keeps month in number format 
        print(df['Month'])
        
        # group by day and sum of spending
        spending_by_month = df.groupby('Month')['Amount'].sum().round(2)
                
        return spending_by_month 
    
    def monthlySpending_withYear(self, withEdu=True):
        
        """
        Analyze spending by month and year in chronological order. 
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        
        # Extract month and year as integers for accurate sorting
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month
        
        # Group by year and month, then sum the spending
        spending_by_year_month = df.groupby(['Year', 'Month'])['Amount'].sum().round(2)

        # Create a new 'Year-Month' index for presentation
        spending_by_year_month.index = spending_by_year_month.index.map(lambda x: f"{x[0]}-{calendar.month_name[x[1]]}")

        # print(spending_by_year_month)
        return spending_by_year_month
    
    def category_by_month(self, withEdu=True):
        
        # get data
        df = self.get_data(withEdu)
        
        # make into datetime 
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        
        # Extract month and year as integers for accurate sorting
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month

        month_cat = df.groupby(['Year', 'Month', 'Category'])['Amount'].sum()
        
        return month_cat 
    
    def category_by_year(self, withEdu=True):
        
        # get data
        df = self.get_data(withEdu)
        
        # make into datetime 
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        
        # Extract month and year as integers for accurate sorting
        df['Year'] = df['TransactionDate'].dt.year

        year_cat = df.groupby(['Year', 'Category'])['Amount'].sum()
        
        return year_cat  
    
    ##### ----- specific locations ----- #####
    
    # this is displaying specific stores where most of the money is spent 
    # going to groupby the specific vendor and total amount spent there 
    def SpecificVendors_TotalSpent(self, withEdu=True):
        
        # get data 
        df = self.get_data(withEdu)

        # group by specific vendors
        result = df.groupby("Matches")['Amount'].sum()
        result = result.sort_values(ascending=False)
        print(result.to_string())

        return df
    
    # this is displaying specific stores where most of the money is spent 
    # going to groupby the specific vendor and total amount spent there by year 
    def SpecificVendors_TotalSpent_Monthly(self, withEdu=True):
        # get data
        df = self.get_data(withEdu)
        
        # make into datetime 
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        
        # Extract month and year as integers for accurate sorting
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month

        # group by year, month, and matches and sum amount
        month_cat = df.groupby(['Year', 'Month', 'Matches'])['Amount'].sum().reset_index()
        
        # sort by year, month, and then amount (descending with in each month)
        month_cat = month_cat.sort_values(ascending=False)
        
        # set the index for the desired output structure 
        month_cat = month_cat.set_index(['Year', 'Month', 'Matches'])
        
        return month_cat 
        
        
        
    def SpecificVendors_TotalSpent_Yearly(self, withEdu=True):
        # get data
        df = self.get_data(withEdu)
        
        # make into datetime 
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        
        # Extract month and year as integers for accurate sorting
        df['Year'] = df['TransactionDate'].dt.year

        year_cat = df.groupby(['Year', 'Matches'])['Amount'].sum()
        year_cat =  year_cat.sort_values(ascending=False)
        
        return year_cat 

# test code
# import database 
# conn = database.connect_db()

# test = dataAnalysis(conn)
# test.dayofTheWeek()

# print(test.get_data(True))
# print("-------------------------------------------------------------")
# print(test.get_data(False))
# test.create_bar_charts()
# test.create_bar_charts(False)

# test.create_tables()
# test.create_tables(False)
