import pandas as pd
import matplotlib
import seaborn as sns
import sklearn
import numpy as np
import csv
import sqlite3

# Imports from files
from database import connect_db, create_tables
from importdata import importData

# Main Class 
from analysis import dataAnalysis

print("All imports worked")

# Updated Main Function
def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('expenseDataBase.db')

    # Create an instance of dataAnalysis
    analysis = dataAnalysis(conn)

    # Call each function and print outputs

    # print("----- DataFrame -----")
    # analysis.print()  

    print("\n----- get_data() -----")
    df_data = analysis.get_data()
    print(df_data.to_string())

    print("\n----- get_category_expenses() -----")
    df_category_expenses = analysis.get_category_expenses(False)
    print(df_category_expenses.to_string())

    print("\n----- get_category_summary() -----")
    df_category_summary = analysis.get_category_summary(False)
    print(df_category_summary.to_string())

    print("\n----- get_day_of_week_expenses() -----")
    df_day_of_week_expenses = analysis.get_day_of_week_expenses(False)
    print(df_day_of_week_expenses.to_string())
    
    print("\n----- get_day_of_month_week_expenses() -----")
    df_get_day_of_month_week_expenses = analysis.get_day_of_month_week_expenses(False)
    print(df_get_day_of_month_week_expenses.to_string())
    
    print("\n----- get_day_of_year_month_week_expenses() -----")
    df_day_year_month_week = analysis.get_day_of_year_month_week_expenses(False)
    print(df_day_year_month_week.to_string())

    print("\n----- monthlySpending() -----")
    df_monthly_spending = analysis.monthlySpending(False)
    print(df_monthly_spending.to_string())

    print("\n----- monthlySpending_withYear() -----")
    df_monthly_spending_with_year = analysis.monthlySpending_withYear(False)
    print(df_monthly_spending_with_year.to_string())

    print("\n----- category_by_month() -----")
    df_category_by_month = analysis.category_by_month(False)
    print(df_category_by_month.to_string())

    print("\n----- category_by_year() -----")
    df_category_by_year = analysis.category_by_year(False)
    print(df_category_by_year.to_string())

    print("\n----- SpecificVendors_TotalSpent() -----")
    df_specific_vendors_total_spent = analysis.SpecificVendors_TotalSpent(False)
    print(df_specific_vendors_total_spent.to_string())

    print("\n----- SpecificVendors_TotalSpent_Monthly() -----")
    df_specific_vendors_total_spent_monthly = analysis.SpecificVendors_TotalSpent_Monthly(False)
    print(df_specific_vendors_total_spent_monthly.to_string())

    print("\n----- SpecificVendors_TotalSpent_Yearly() -----")
    df_specific_vendors_total_spent_yearly = analysis.SpecificVendors_TotalSpent_Yearly(False)
    print(df_specific_vendors_total_spent_yearly.to_string())

    print("\n----- spending_trends_over_time() -----")
    df_overtime_daily = analysis.spending_trends_over_time(False, "D")
    df_overtime_monthly = analysis.spending_trends_over_time(False, "ME")
    df_overtime_yearly = analysis.spending_trends_over_time(False, "YE")
    print(df_overtime_daily.to_string())
    print(df_overtime_monthly.to_string())
    print(df_overtime_yearly.to_string())

    print("\n----- average_transaction_by_category() -----")
    df_avg_transaction = analysis.average_transaction_by_category(False)
    print(df_avg_transaction.to_string())

    print("\n----- median_transaction_by_category() -----")
    df_median_transaction = analysis.median_transaction_by_category(False)
    print(df_median_transaction.to_string())

    print("\n----- transaction_count_by_vendor_over_time() -----")
    df_transaction_count_vendor = analysis.transaction_count_by_vendor_over_time(False, "M")
    print(df_transaction_count_vendor.to_string())

    print("\n----- category_spending_proportions() -----")
    df_category_proportions = analysis.category_spending_proportions(False)
    print(df_category_proportions.to_string())

    print("\n----- year_over_year_category_comparison() -----")
    df_yoy_comparison = analysis.year_over_year_category_comparison(False)
    print(df_yoy_comparison.to_string())

    print("\n----- top_n_vendors() -----")
    df_top_vendors = analysis.top_n_vendors(n=10, withEdu=False)
    print(df_top_vendors.to_string())

    print("\n----- monthly_average_spending_per_category() -----")
    df_monthly_avg_spending = analysis.monthly_average_spending_per_category(False)
    print(df_monthly_avg_spending.to_string())

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
