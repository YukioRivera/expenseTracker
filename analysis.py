import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class dataAnalysis():
    
    def __init__(self, conn):
        df = pd.read_sql_query("SELECT TransactionDate, Description, Category, Type, ABS(Amount) FROM expenses", conn)
        df_cleaned = df[df['Type'] != 'Payment']
        df_cleaned = df_cleaned.drop(columns=['Type'])
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
        
    # creates bar charts the true or false determine the filter on the df
    # it includes education expenses and f filters out education exenses 
    def create_bar_charts(self, withEdu=True):
        # Determine title and file paths based on the 'withEdu' flag
        title_suffix = "(With Education)" if withEdu else "(Without Education)"
        filename_suffix = "wEdu" if withEdu else "woEdu"

        # Get data, grouping by category and summing amounts
        df_categories = self.get_data(withEdu).groupby("Category")["ABS(Amount)"].sum()

        # Plotting
        plt.figure(figsize=(12, 6))  # Adjust figure size as needed
        ax = df_categories.plot(kind='bar')

        # Configure plot appearance
        plt.xticks(rotation=45)
        plt.xlabel('Category')
        plt.ylabel('Total Amount')
        plt.title(f'Expenses by Category {title_suffix}')
        plt.tight_layout()

        # Add labels to bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', label_type='edge')

        # Save the plot
        plt.savefig(f'graphs/Category/CategoryExpenses_{filename_suffix}.png')

        return df_categories

    # creates the tables that show the count of each expense category 
    def create_tables(self, withEdu=True):
        # Group the data by 'Category'
        category_data = self.get_data(withEdu).groupby('Category')

        # Calculate sums and counts for each category
        category_amounts = category_data["ABS(Amount)"].sum().round(2)  # sum of expenses for each category, rounded to 2 decimal places
        category_expense_count = category_data.size()  # count of each category

        # Calculate sums and counts for each category 
        category_summary_df = pd.DataFrame({
            'Category': category_amounts.index,
            'Expense Count': category_expense_count,
            'Amount': category_amounts
        }).reset_index(drop=True) # resets the index to have category as a column, drop the old index 
        
        # print(category_amounts)
        # calcualte the sum totals 
        total_amount_sum = round(category_amounts.sum(), 2)  # sum of all expenses 
        total_expense_count = category_expense_count.sum()   # sum of total expense count 
        
        # add total row to the dataframe
        total_row = pd.DataFrame([["Total:", total_expense_count, total_amount_sum]], 
                             columns=["Category", "Expense Count", "Amount"])
        category_summary_df = pd.concat([category_summary_df, total_row], ignore_index=True)
        
        # create the ax object to crete the table
        fig, ax = plt.subplots()
         
        # hide axes
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)
        
        # convert dataframe to list of lists (which is what matpltlib expects for tables)
        table_data = category_summary_df.values.tolist()
        # print(category_summary_df)
        
        # create the table
        table = ax.table(cellText=table_data,
                     colLabels=["Category", "Expense Count", "Amount"],
                     cellLoc='center',
                     colColours=['green', 'green', 'green'],
                     loc='center')
        
        # Adjust layout and font size
        table.auto_set_font_size(False)
        table.set_fontsize(10)

        # Save the table as an image
        if withEdu:
            plt.savefig('graphs/Category/Table_CategoryExpenses_wEdu.png')
        else:
            plt.savefig('graphs/Category/Table_CategoryExpenses_woEdu.png')
    
        # returns df of (index, category, expense count, amount)
        return category_summary_df

# test code
# import database 
# conn = database.connect_db()

# test = dataAnalysis(conn)
# # print(test.get_data(True))
# # print("-------------------------------------------------------------")
# # print(test.get_data(False))
# test.create_bar_charts()
# test.create_bar_charts(False)

# test.create_tables()
# test.create_tables(False)
