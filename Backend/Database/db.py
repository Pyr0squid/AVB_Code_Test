import sqlite3

# create a connection to a database
def connect_db(database: str) -> sqlite3.Connection:

    # Connect to the SQLite database
    conn = sqlite3.connect(database)

    # Enable Foreign Key Constraint
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

# creates a database instance from sql schema file
def create_db_instance(schema: str, database: str):

    # connect to database
    conn = connect_db(database)

    # create cursor
    cursor = conn.cursor()

    # check if database is new
    res = cursor.execute("SELECT name FROM sqlite_master")
    if(len(res.fetchall()) == 0):

        # Open and read the SQL file if database is new
        with open(schema, 'r') as sql_file:
            sql_script = sql_file.read()

        # Execute the SQL script if database is new
        cursor.executescript(sql_script)

        # Commit the changes and close the connection if database is new
        conn.commit()

    # Close Cursor and Connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_db_instance('Backend/Database/schema.sql', 'Backend/Database/database.db')