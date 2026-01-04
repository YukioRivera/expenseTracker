import os
import shutil
import pandas as pd

def clean_excel_files():
    # Define directories
    chase_dir = "data/Chase"
    boa_dir = "data/BOA"
    backup_dir = "data/backup"
    
    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    def backup_and_clean(file_path):
        """
        Backups and cleans a file.
        """
        file_name = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, file_name)

        if not os.path.exists(backup_path):
            shutil.copy(file_path, backup_path)
            print(f"Backed up: {file_name}")
        else:
            print(f"Backup already exists for: {file_name}")

    def rename_transaction_date(df):
        """
        Rename 'Transaction Date' (or similar variations) to 'TransactionDate'.
        """
        for column in df.columns:
            if column.strip().lower() in ['transaction date', 'transactiondate', 'posted date']:
                df = df.rename(columns={column: "TransactionDate"})
        return df

    def process_chase_files():
        """
        Process files in the Chase directory.
        """
        if not os.path.exists(chase_dir) or not os.listdir(chase_dir):
            print(f"No files found in {chase_dir}")
            return

        for file in os.listdir(chase_dir):
            file_path = os.path.join(chase_dir, file)
            if file.lower().endswith((".xlsx", ".csv")):
                # Backup the file
                backup_and_clean(file_path)

                # Load the file (CSV or Excel)
                try:
                    if file.lower().endswith(".csv"):
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    continue

                # Rename 'Transaction Date' to 'TransactionDate'
                df = rename_transaction_date(df)

                # **Remove rows where 'Type' is 'Payment'**
                if 'Type' in df.columns:
                    df = df[df['Type'] != 'Payment']

                # Check columns and drop unnecessary ones
                required_columns = ["TransactionDate", "Description", "Category", "Type", "Amount"]
                extra_columns = set(df.columns) - set(required_columns)

                if extra_columns:
                    df = df.drop(columns=list(extra_columns))
                    print(f"Removed columns {extra_columns} from {file}")

                # Ensure only required columns exist in the correct order
                df = df[required_columns]

                # Save cleaned file
                if file.lower().endswith(".csv"):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)
                print(f"Cleaned and saved: {file}")
            else:
                print(f"Skipped unsupported file: {file}")

    def process_boa_files():
        """
        Process files in the BOA directory.
        """
        if not os.path.exists(boa_dir) or not os.listdir(boa_dir):
            print(f"No files found in {boa_dir}")
            return

        for file in os.listdir(boa_dir):
            file_path = os.path.join(boa_dir, file)
            if file.lower().endswith((".xlsx", ".csv")):
                # Backup the file
                backup_and_clean(file_path)

                # Load the file (CSV or Excel)
                try:
                    if file.lower().endswith(".csv"):
                        df = pd.read_csv(file_path)
                    else:
                        df = pd.read_excel(file_path)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    continue

                # Rename 'Posted Date' or 'Transaction Date' to 'TransactionDate'
                df = rename_transaction_date(df)

                # Required transformations
                required_columns = ["TransactionDate", "Description", "Amount"]
                # Adjust column names if necessary
                column_mappings = {
                    "Payee": "Description",
                    "Description": "Description",  # Ensures 'Description' column is correctly named
                    "Amount": "Amount"
                }
                df = df.rename(columns=column_mappings)

                # **Add 'Type' column and remove 'Payment' rows if 'Type' exists**
                if 'Type' in df.columns:
                    df = df[df['Type'] != 'Payment']
                else:
                    df['Type'] = "Sale"  # Assuming all BOA transactions are 'Sale' unless specified

                # Add 'Category' column
                df["Category"] = ""

                # Keep and reorder relevant columns
                df = df[["TransactionDate", "Description", "Category", "Type", "Amount"]]

                # Save cleaned file
                if file.lower().endswith(".csv"):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)
                print(f"Cleaned and saved: {file}")
            else:
                print(f"Skipped unsupported file: {file}")

    # Process Chase files
    process_chase_files()

    # Process BOA files
    process_boa_files()

# Call the function
clean_excel_files()
