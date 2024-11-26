import csv
import os
import pandas as pd
import util
import shutil

# TODO: find a way to iterate through directory and import each one - done 
# TODO: also automate the process of moving imported files to a diff directory 
# TODO: check which entiries donnt need to be readded, may be solved with moving files 
# TODO: add a way to clean up the csv files, rightg now i neede to manually remove post date and memo so it would be nice to remove them automatically 
# TODO: create an import for bank of america, needs to be able to clean up the data to look like chase, that requires we add classifiers for the purchases to designate a category
def importData(conn):
    # Initialize directories
    data_directory = 'data'
    processed_directory = os.path.join(data_directory, 'processed')  # Subdirectory within 'data'

    # Create directories if they don't exist
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(processed_directory, exist_ok=True)   
        
    # List files in the data directory (excluding the 'processed' subdirectory)
    paths = [f for f in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory, f))]
    
    # Iterate over files in the data directory
    for filename in paths:
        full_path = os.path.join(data_directory, filename)
        try:
            # Open each file individually
            with open(full_path, newline='') as csvfile:
                expenseReader = list(csv.reader(csvfile))
                curr = conn.cursor()
                
                # Start at index 1 to skip headers
                for row in expenseReader[1:]:
                    conn.execute("INSERT INTO expenses ('TransactionDate', Description, Category, Type, Amount) VALUES (?,?,?,?,?)", row)
                conn.commit()
            
            # Move the file after successful processing
            shutil.move(full_path, os.path.join(processed_directory, filename))
            print(f"Successfully processed and moved file: {filename}")
        
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            # File remains in the data directory for reprocessing