import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def showCategories(conn):
    
    query = conn.execute("SELECT TransactionDate, Description, Category, Type, ABS(Amount) FROM expenses")
    # print(query)
    
    # convert sql query to dataframe 
    df = pd.read_sql_query("SELECT TransactionDate, Description, Category, Type, ABS(Amount) FROM expenses", conn)
    
    # chaning all neg values to positive
    # print(df)

    # aggregate them by categories and show the amount spent for each category
    
    # show a pie chart of the percent of total spending 
    
    
    
    # Remove payment information, payments I made towards card 
    df_clean = df[df['Type'] != 'Payment']
    # df_clean = df[df['Type'] != 'Payment']
    # print(df_clean)
    
    # -------------------- Analysis with edu cost ----------------------------
    
    df_categories_wEducation = df_clean.groupby("Category")['ABS(Amount)'].sum()
    # print(df_categories)
    
    # Plotting
    plt.figure(figsize=(12, 6))  # Increase figure size
    
    # Capture the axes object returned by the plot function, you need to make the plot into an axe object
    ax = df_categories_wEducation.plot(kind='bar')

    plt.xticks(rotation=45)  # Rotate x-axis labels
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Expenses by Category (With Education)')
    plt.tight_layout()  # Adjust layout
    # plt.grid(True)
    
    # adding labels on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge')
    
    plt.savefig('graphs/Category/CategoryExpenses_wEdu.png')
    
    # -------------------- Analysis without edu cost ----------------------------
    # Remove 'Education' category
    df_noEdu = df_clean[df_clean['Category'] != 'Education']

    # Verify that 'Education' is removed
    # print(df_noEdu['Category'].unique())

    # Group and sum amounts by category
    df_categories_woEducation = df_noEdu.groupby("Category")['ABS(Amount)'].sum()

    # Verify grouped data
    # print(df_categories_woEducation)
    
    # Plotting
    plt.figure(figsize=(12, 6))  # Increase figure size
    
    # Capture the axes object returned by the plot function, you need to make the plot into an axe object
    ax = df_categories_woEducation.plot(kind='bar')

    # plot characteristics 
    plt.xticks(rotation=45)  # Rotate x-axis labels
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Expenses by Category (Without Education)')
    plt.tight_layout()  # Adjust layout
    # plt.grid(True)
    
    # adding labels on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge')
    
    plt.savefig('graphs/Category/CategoryExpenses_woEdu.png')
    # plt.show()  # Uncomment to display the plot
    
    # ------------------------ code for tables ------------------------
    # prepare table
    category_names = df_categories_wEducation.index.tolist()
    category_amount_each = df_clean.groupby('Category').size()
    category_values = [round(float(amnt), 2) for amnt in df_categories_woEducation.values.flatten()]
    
    # totals 
    totalAmount_Categories = df_categories_wEducation.sum().round(2)
    total_ExpenseCount = category_amount_each.sum()
    category_percents = df_categories_wEducation/totalAmount_Categories
    
    # print(f"total amount: {df_clean["Category"]}")
    # print(df_clean.groupby('Category'))
    # print(category_percents.iloc[0])
    for i in df_clean.index.tolist():
        print(i)
    
    plt.figure(figsize=(10,5)) # increase size of chart 
    
    # create the axes object 
    fig, ax = plt.subplots()
    
    # Hide axes
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    
    # print(df_clean.groupby('Category').size())


    # create table content with category and amount as columns  
    table_data = [[cat, numOf, amnt] for cat, numOf, amnt in zip(category_names, category_amount_each, category_values)]
    
    # add total row 
    table_data.append(["", "", ""])
    table_data.append(["Total: ", total_ExpenseCount, totalAmount_Categories])
    
    # create table
    table = ax.table(cellText=table_data, 
                     colLabels=["Category", "Expense Count", "Amount"],
                     cellLoc='center',
                     colColours=['green', 'green', 'green'],
                     loc='center')
    
    # Adjust layout and font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Make the table dynamic and adjust size based on text
    # table.auto_set_column_width(col=list(range(len(category_percents.columns))))
    
    plt.savefig('graphs/Category/Pie_CategoryExpenses_woEdu.png', 
                bbox_inches='tight') 
    
# conn.close()