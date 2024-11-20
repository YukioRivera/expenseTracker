import csv
import os
import pandas as pd


def importData(conn):
    # TODO: find a way to iterate through directory and import each one - done 
    # TODO: also automate the process of moving imported files to a diff directory 
    # TODO: check which entiries donnt need to be readded, may be solved with moving files 
    # TODO: add a way to clean up the csv files, rightg now i neede to manually remove post date and memo so it would be nice to remove them automatically 
    # TODO: create an import for bank of america, needs to be able to clean up the data to look like chase, that requires we add classifiers for the purchases to designate a category
    data = pd.DataFrame()
    
    # Files in the directory 
    directory = 'data'
        # ['data/Chase1664_Activity20240101_20241119_20241120.CSV',
        # 'data/Chase9197_Activity20240101_20241119_20241120.CSV']
        
    
    
    paths = os.listdir(directory)
    
    # print(paths)
    
    try:
        # iterates through files in paths dir 
        for path in paths: 
            path = os.path.join(directory, path)
            # print(path)
            
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
    