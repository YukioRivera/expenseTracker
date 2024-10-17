import sqlite3

def connect_db():
    conn = None
    try:
        # connceting to database 
        conn = sqlite3.connect("expenseDataBase")
        print(sqlite3.sqlite_version)
        
    except sqlite3.Error as e:
        print(e)
        
    return conn
    
def create_tables(conn):
    sql_statement = """
                CREATE TABLE IF NOT EXISTS expenses ( 
                id INTEGER PRIMARY KEY, 
                TransactionDate date NOT NULL, 
                Description TEXT NOT NULL,
                Category TEXT NOT NULL, 
                Type TEXT NOT NULL,
                Amount INTEGER NOT NULL
        );"""
    
    cursor = conn.cursor()
            
    # for statement in sql_statement:
    cursor.execute(sql_statement)
        
    conn.commit()
    
def insert_data(df):
    try:
        with sqlite3.connect("expenseDataBase") as conn:
            cursor = conn.cursor()    
    except sqlite3.Error as e:
        print(e)