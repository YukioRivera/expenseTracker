import csv
import os
import pandas as pd
import shutil

# TODO: Automate directory management - done
# TODO: Automate processing and moving files - done
# TODO: Automate CSV cleanup (remove unnecessary columns like post date and memo) - done
# TODO: Create a specific import process for Bank of America files to standardize data structure

def importData(conn):
    # Define directory paths
    data_directory = 'data/Chase'
    processed_directory = 'data/processed'

    # Create directories if they don't exist
    os.makedirs(data_directory, exist_ok=True)
    os.makedirs(processed_directory, exist_ok=True)

    # List files in the Chase data directory
    paths = [f for f in os.listdir(data_directory) if os.path.isfile(os.path.join(data_directory, f))]
    
    # Iterate over files in the Chase data directory
    for filename in paths:
        full_path = os.path.join(data_directory, filename)
        
        try:
            # Read CSV into a DataFrame for cleanup and standardization
            df = pd.read_csv(full_path)
            print(df)
            
            # Example cleanup: Drop unnecessary columns (customize as needed)
            # unnecessary_columns = ['Post Date', 'Memo']  # Adjust as per your actual column names
            # df = df.drop(columns=[col for col in unnecessary_columns if col in df.columns], errors='ignore')
            
            # Additional cleanup: Rename columns for consistency
            column_mapping = {
                'Date': 'TransactionDate',
                'Description': 'Description',
                'Category': 'Category',
                'Type': 'Type',
                'Amount': 'Amount'
            }
            df = df.rename(columns=column_mapping)
            
            # Ensure required columns exist (fill missing ones with default values)
            required_columns = ['TransactionDate', 'Description', 'Category', 'Type', 'Amount']
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None  # Add missing columns with default None values
            
            # Insert data into the database
            curr = conn.cursor()
            for _, row in df.iterrows():
                conn.execute(
                    "INSERT INTO expenses (TransactionDate, Description, Category, Type, Amount) VALUES (?,?,?,?,?)",
                    (row['TransactionDate'], row['Description'], row['Category'], row['Type'], row['Amount'])
                )
            conn.commit()
            
            # Move the file to the processed directory
            shutil.move(full_path, os.path.join(processed_directory, filename))
            print(f"Successfully processed and moved file: {filename}")
        
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            # Optionally log errors for further investigation

