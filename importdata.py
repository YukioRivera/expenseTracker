import csv
import os
import pandas as pd


def importData(conn):
    # TODO: find a way to iterate through directory and import each one
    # TODO: also automate the process of moving imported files to a diff directory
    # TODO: check which entiries donnt need to be readded, may be solved with moving files 
    # TODO: create an import for bank of america, needs to be able to clean up the data to look like chase, that requires we add classifiers for the purchases to designate a category
    data = pd.DataFrame()
    
    # Files in the directory 
    paths = [
        'data/Chase9197_Activity20240101_20241014_20241015.CSV',
        'data/Chase1664_Activity20240101_20241014_20241015.CSV'
    ]
    
    try:
        # iterates through files in paths dir 
        for path in paths: 
            
            # opens each file individually 
            with open(path, newline="") as csvfile:
                
                expenseReader = list(csv.reader(csvfile))
                # print(expenseReader)
                curr = conn.cursor()
                
                # starts at index 1, to avoid adding headers to table
                for row in expenseReader[1:]:
                    conn.execute("INSERT INTO expenses ('TransactionDate', Description, Category, Type, Amount) VALUES (?,?,?,?,?)", row)
                    conn.commit()
                
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    