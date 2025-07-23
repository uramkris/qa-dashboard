import sqlite3

DATABASE_NAME = "qa_dashboard.db"

def create_db_and_tables():
    # Connect to the database. This will create the file if it doesn't exist.
    conn = sqlite3.connect(DATABASE_NAME)
    # Get a "cursor" object. This is what you use to execute SQL commands.
    cursor = conn.cursor()

    print("Creating the 'results' table if it doesn't exist...")
    
    # This is the SQL command to create our table.
    # "CREATE TABLE IF NOT EXISTS" is safe to run multiple times.
    # We define columns that match our Pydantic model from Day 2.
    # "TEXT" is for strings, "INTEGER" is for numbers.
    # "PRIMARY KEY AUTOINCREMENT" creates a unique ID for each row automatically.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT NOT NULL,
        status TEXT NOT NULL,
        duration_ms INTEGER NOT NULL,
        test_suite TEXT NOT NULL,
        error_message TEXT
    )
    """)

    # Commit the changes (save them to the file) and close the connection.
    conn.commit()
    conn.close()
    print("Table 'results' is ready.")

def insert_result(result: 'TestResult'):
    
    # NOW we import it, only when this function is actually called.
    from main import TestResult 

    # It's good practice to also check if the incoming data matches the type
    if not isinstance(result, TestResult):
        # Handle error appropriately, for now we can just return or raise
        print("Error: Invalid data type provided to insert_result")
        return
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # The '?' are placeholders. This is the SAFE way to insert data.
    # It prevents a security vulnerability called SQL Injection.
    # The tuple that follows contains the actual values to be inserted.
    cursor.execute("""
    INSERT INTO results (test_name, status, duration_ms, test_suite, error_message)
    VALUES (?, ?, ?, ?, ?)
    """, (result.test_name, result.status, result.duration_ms, result.test_suite, result.error_message))
    
    conn.commit()
    conn.close()

def get_all_results():
    conn = sqlite3.connect(DATABASE_NAME)
    # This line is new! It makes the database return rows that behave like dictionaries.
    # This is a very convenient feature of the sqlite3 library.
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()

    print("Fetching all results from the database...")
    # This SQL command selects all columns (*) from all rows in the results table.
    cursor.execute("SELECT * FROM results ORDER BY id DESC") # Order by most recent
    
    # fetchall() retrieves all the rows from the query result.
    results = cursor.fetchall()
    
    conn.close()
    
    # The 'results' are now a list of special sqlite3.Row objects.
    # We need to convert them into a list of plain Python dictionaries
    # for FastAPI to handle them correctly.
    # The list comprehension below does this efficiently.
    return [dict(row) for row in results]