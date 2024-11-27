# Import necessary libraries
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import calendar
import re
import util
from thefuzz import fuzz
from thefuzz import process
from collections import OrderedDict  # Possibly unused, consider removing if not required

# Define the dataAnalysis class
class dataAnalysis():

    def __init__(self, conn):
        """
        Initializes the dataAnalysis class.
        - Reads data from a SQLite database.
        - Filters out payments and standardizes descriptions.
        """
        # Load data from database
        df = pd.read_sql_query("SELECT TransactionDate, Description, Category, Type, ABS(Amount) FROM expenses", conn)
        
        # Rename columns for clarity
        df.rename(columns={'ABS(Amount)': 'Amount'}, inplace=True)
        
        # Remove rows where the transaction type is 'Payment'
        df_cleaned = df[df['Type'] != 'Payment']
        df_cleaned = df_cleaned.drop(columns=['Type'])
        
        # Standardize vendor descriptions (using utility function)
        df_matches = util.StandardizeDescriptions(df_cleaned)
        
        # Assign cleaned data to instance variables
        self.conn = conn
        self.df = df_cleaned

    def print(self):
        """
        Prints the dataframe for a quick review.
        """
        print(self.df)

    def get_data(self, withEdu=True):
        """
        Retrieves transaction data, optionally excluding education-related expenses.
        - withEdu=True: Include education expenses.
        - withEdu=False: Exclude education expenses.
        """
        if withEdu:
            return self.df
        else:
            return self.df[self.df['Category'] != 'Education']

    def get_category_expenses(self, withEdu=True):
        """
        Returns a DataFrame with total expenses grouped by category.
        """
        df_categories = self.get_data(withEdu).groupby("Category")["Amount"].sum().reset_index()
        return df_categories

    def get_category_summary(self, withEdu=True):
        """
        Provides a summary of spending by category, including:
        - Total amount spent.
        - Count of transactions per category.
        - A total row summarizing all categories.
        """
        category_data = self.get_data(withEdu).groupby('Category')
        category_amounts = category_data["Amount"].sum().round(2)  # Total spent per category
        category_expense_count = category_data.size()  # Number of transactions per category
        
        # Create summary DataFrame
        category_summary_df = pd.DataFrame({
            'Category': category_amounts.index,
            'Expense Count': category_expense_count,
            'Amount': category_amounts
        }).reset_index(drop=True)

        # Add a total row to summarize all categories
        total_amount_sum = round(category_amounts.sum(), 2)
        total_expense_count = category_expense_count.sum()
        total_row = pd.DataFrame([["Total:", total_expense_count, total_amount_sum]],
                                 columns=["Category", "Expense Count", "Amount"])
        category_summary_df = pd.concat([category_summary_df, total_row], ignore_index=True)
        
        return category_summary_df

    def get_day_of_week_expenses(self, withEdu=True):
        """
        Analyzes spending by the day of the week.
        - Groups transactions by the day (Monday-Sunday).
        - Summarizes total spending per day.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Day'] = df['TransactionDate'].dt.day_name()

        # Group by day and sum amounts
        spending_by_day = df.groupby('Day')['Amount'].sum().round(2)

        # Reorder days for consistent output
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        spending_by_day = spending_by_day.reindex(days_order)

        # Convert to DataFrame for uniformity
        spending_by_day_df = spending_by_day.reset_index()
        spending_by_day_df.columns = ['Day', 'Amount']
        
        return spending_by_day_df
    
    def get_day_of_month_week_expenses(self, withEdu=True):
        """
        Analyzes spending by the day of the week separated by month.
        - Groups transactions by the day (Monday-Sunday) separated by month.
        - Summarizes total spending per day.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Month'] = df['TransactionDate'].dt.month
        df['Day'] = df['TransactionDate'].dt.day_name()

        # Group by month and day, then sum the amounts
        spending_by_day = df.groupby(['Month', 'Day'])['Amount'].sum().round(2)

        # Reset index to convert the Series to a DataFrame
        spending_by_day_df = spending_by_day.reset_index()

        # Define the order of the days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Convert 'Day' to a categorical type with the specified order
        spending_by_day_df['Day'] = pd.Categorical(spending_by_day_df['Day'],
                                                categories=days_order, ordered=True)

        # Sort the DataFrame by 'Month' and 'Day'
        spending_by_day_df = spending_by_day_df.sort_values(['Month', 'Day'])

        return spending_by_day_df
    
    def get_day_of_year_month_week_expenses(self, withEdu=True):
        """
        Analyzes spending by the day of the week separated by year and month.
        - Groups transactions by 'Year', 'Month', and 'Day' (Monday-Sunday).
        - Summarizes total spending per day.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month
        df['Day'] = df['TransactionDate'].dt.day_name()

        # Group by year, month, and day, then sum the amounts
        spending_by_day = df.groupby(['Year', 'Month', 'Day'])['Amount'].sum().round(2)

        # Reset index to convert the Series to a DataFrame
        spending_by_day_df = spending_by_day.reset_index()

        # Define the order of the days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Convert 'Day' to a categorical type with the specified order
        spending_by_day_df['Day'] = pd.Categorical(
            spending_by_day_df['Day'],
            categories=days_order,
            ordered=True
        )

        # Sort the DataFrame by 'Year', 'Month', and 'Day'
        spending_by_day_df = spending_by_day_df.sort_values(['Year', 'Month', 'Day'])

        return spending_by_day_df

    def monthlySpending(self, withEdu=True):
        """
        Summarizes total spending by month (ignoring the year).
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Month'] = df['TransactionDate'].dt.month  # Extract month number
        
        # Group by month and sum spending
        spending_by_month = df.groupby('Month')['Amount'].sum().round(2)
        
        return spending_by_month

    def monthlySpending_withYear(self, withEdu=True):
        """
        Summarizes spending by both month and year, keeping chronological order.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month

        # Group by year and month, then sum amounts
        spending_by_year_month = df.groupby(['Year', 'Month'])['Amount'].sum().round(2)

        # Format the index for readability
        spending_by_year_month.index = spending_by_year_month.index.map(
            lambda x: f"{x[0]}-{calendar.month_name[x[1]]}"
        )

        return spending_by_year_month

    def category_by_month(self, withEdu=True):
        """
        Summarizes spending by category for each month and year.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month

        # Group by year, month, and category, then sum amounts
        month_cat = df.groupby(['Year', 'Month', 'Category'])['Amount'].sum()
        
        return month_cat

    def category_by_year(self, withEdu=True):
        """
        Summarizes spending by category for each year.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year

        # Group by year and category, then sum amounts
        year_cat = df.groupby(['Year', 'Category'])['Amount'].sum()
        
        return year_cat

    def SpecificVendors_TotalSpent(self, withEdu=True):
        """
        Lists total spending by specific vendors, sorted by amount (highest first).
        """
        df = self.get_data(withEdu)
        # print(df.to_string())
        print(df[df['Matches'] == ''].to_string())
        result = df.groupby("Matches")['Amount'].sum()
        result = result.sort_values(ascending=False)
        
        # print(result.to_string())  # Display results
        return result

    def SpecificVendors_TotalSpent_Monthly(self, withEdu=True):
        """
        Lists total spending by specific vendors, grouped by year and month.
        - Sorted within each month by descending amount.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year
        df['Month'] = df['TransactionDate'].dt.month

        # Group by year, month, and vendor, then sum amounts
        month_cat = df.groupby(['Year', 'Month', 'Matches'])['Amount'].sum().reset_index()
        
        # Sort by year, month, and amount in descending order
        month_cat = month_cat.sort_values(by=['Year', 'Month', 'Amount'], ascending=[True, True, False])
        
        # Set hierarchical index for output structure
        month_cat = month_cat.set_index(['Year', 'Month', 'Matches'])
        
        return month_cat

    def SpecificVendors_TotalSpent_Yearly(self, withEdu=True):
        """
        Lists total spending by specific vendors, grouped by year.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year

        # Group by year and vendor, then sum amounts
        year_cat = df.groupby(['Year', 'Matches'])['Amount'].sum()
        year_cat = year_cat.sort_values(ascending=False)
        
        return year_cat

    def spending_trends_over_time(self, withEdu=True, freq='M'):
        """
        Analyzes spending trends over time.
        - freq: Frequency for resampling ('D' for daily, 'W' for weekly, 'M' for monthly, 'Q' for quarterly, 'A' for annual).
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df.set_index('TransactionDate', inplace=True)
        spending_trend = df['Amount'].resample(freq).sum()
        spending_trend = spending_trend.reset_index()
        return spending_trend
    
    def average_transaction_by_category(self, withEdu=True):
        """
        Calculates the average transaction amount per category.
        """
        df = self.get_data(withEdu)
        avg_transaction = df.groupby('Category')['Amount'].mean().round(2).reset_index()
        avg_transaction.rename(columns={'Amount': 'Average Transaction Amount'}, inplace=True)
        return avg_transaction
    
    def median_transaction_by_category(self, withEdu=True):
        """
        Calculates the median transaction amount per category.
        """
        df = self.get_data(withEdu)
        median_transaction = df.groupby('Category')['Amount'].median().round(2).reset_index()
        median_transaction.rename(columns={'Amount': 'Median Transaction Amount'}, inplace=True)
        return median_transaction
    
    def transaction_count_by_vendor_over_time(self, withEdu=True, freq='M'):
        """
        Counts the number of transactions per vendor over time.
        - freq: Frequency for resampling ('D' for daily, 'W' for weekly, 'M' for monthly, etc.).
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df.set_index('TransactionDate', inplace=True)
        transaction_counts = df.groupby('Matches').resample(freq).size().unstack(level=0).fillna(0)
        return transaction_counts
    
    def category_spending_proportions(self, withEdu=True):
        """
        Calculates the spending proportion of each category.
        """
        df = self.get_data(withEdu)
        total_spending = df['Amount'].sum()
        category_spending = df.groupby('Category')['Amount'].sum()
        category_proportions = (category_spending / total_spending * 100).round(2).reset_index()
        category_proportions.rename(columns={'Amount': 'Spending Proportion (%)'}, inplace=True)
        return category_proportions
    
    def year_over_year_category_comparison(self, withEdu=True):
        """
        Compares spending by category year over year.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['Year'] = df['TransactionDate'].dt.year
        yoy_comparison = df.groupby(['Year', 'Category'])['Amount'].sum().unstack('Year').fillna(0)
        return yoy_comparison
    
    def top_n_vendors(self, n=10, withEdu=True):
        """
        Lists the top N vendors by total spending.
        - n: Number of top vendors to return.
        """
        df = self.get_data(withEdu)
        top_vendors = df.groupby('Matches')['Amount'].sum().nlargest(n).reset_index()
        return top_vendors
    
    def monthly_average_spending_per_category(self, withEdu=True):
        """
        Calculates the average monthly spending per category.
        """
        df = self.get_data(withEdu)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['YearMonth'] = df['TransactionDate'].dt.to_period('M')
        monthly_spending = df.groupby(['YearMonth', 'Category'])['Amount'].sum().reset_index()
        average_monthly_spending = monthly_spending.groupby('Category')['Amount'].mean().round(2).reset_index()
        average_monthly_spending.rename(columns={'Amount': 'Average Monthly Spending'}, inplace=True)
        return average_monthly_spending