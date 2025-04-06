"""
Script to run the update_schema.sql file using Python
This is an alternative to running the SQL script directly with the mysql command
"""

import mysql.connector
from mysql.connector import Error
import os

def run_sql_script():
    """Run the update_schema.sql script using Python"""
    print("Running update_schema.sql script...")
    
    # Get the path to the SQL file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(script_dir, 'update_schema.sql')
    
    # Check if the file exists
    if not os.path.exists(sql_file_path):
        print(f"❌ ERROR: SQL file not found at {sql_file_path}")
        return False
    
    # Read the SQL file
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    
    # Split the script into individual commands
    # This simple approach splits on semicolons, which works for basic SQL
    # but might not handle more complex SQL with stored procedures, etc.
    commands = sql_script.split(';')
    
    # Initialize connection and cursor as None
    connection = None
    cursor = None
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="AE-LP-2817\\PERFORMANCE_DASH",  # Windows server with double backslashes
            database="PERFORMANCEDB",
            user="arshia.goswami",
            password="Ather@123"
        )
        
        if connection.is_connected():
            print("✅ Connected to MySQL database")
            
            # Create a cursor
            cursor = connection.cursor()
            
            # Execute each command
            for command in commands:
                # Skip empty commands
                if command.strip():
                    try:
                        cursor.execute(command)
                        # For SELECT statements, fetch and print results
                        if command.strip().upper().startswith('SELECT') or command.strip().upper().startswith('SHOW'):
                            results = cursor.fetchall()
                            if results:
                                # Print column headers
                                if cursor.description:
                                    headers = [column[0] for column in cursor.description]
                                    print("\n" + " | ".join(headers))
                                    print("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
                                
                                # Print rows
                                for row in results:
                                    print(" | ".join(str(cell) for cell in row))
                        
                    except Error as e:
                        print(f"❌ Error executing command: {command.strip()}")
                        print(f"   Error message: {e}")
            
            # Commit the changes
            connection.commit()
            print("\n✅ Schema update completed successfully")
            
    except Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
        return False
    finally:
        # Close the connection
        if connection is not None and connection.is_connected():
            if cursor is not None:
                cursor.close()
            connection.close()
            print("MySQL connection closed")
    
    return True

if __name__ == "__main__":
    success = run_sql_script()
    exit(0 if success else 1)
