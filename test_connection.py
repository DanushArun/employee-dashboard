#!/usr/bin/env python3
"""
Database Connection Test Script for Employee Performance Dashboard

This script tests the connection to the MySQL database using the configuration
from db_config.json or environment variables. It helps verify that the database
connection is properly configured before running the full application.

Usage:
    python test_connection.py
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, cast

try:
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector.cursor import MySQLCursor
except ImportError:
    print("Error: mysql-connector-python package is not installed.")
    print("Please install it using: pip install mysql-connector-python")
    sys.exit(1)

def load_db_config() -> Dict[str, str]:
    """Load database configuration from config file or environment variables"""
    # Default configuration
    config: Dict[str, str] = {
        "host": "AE-LP-2817\\PERFORMANCE_DASH",
        "database": "PERFORMANCEDB",
        "user": "arshia.goswami",
        "password": "Ather@123"
    }
    
    # Check for config file
    config_path = Path(__file__).parent / 'db_config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                print(f"Loading configuration from {config_path}")
                file_config = json.load(f)
                for key, value in file_config.items():
                    if isinstance(value, str):
                        config[key] = value
        except Exception as e:
            print(f"Error loading config file: {e}")
    else:
        print(f"Config file not found at {config_path}")
        print("Using default configuration or environment variables.")
    
    # Environment variables override config file
    db_host = os.environ.get('DB_HOST')
    if db_host is not None:
        print("Using DB_HOST from environment variables")
        config['host'] = db_host
    
    db_name = os.environ.get('DB_NAME')
    if db_name is not None:
        print("Using DB_NAME from environment variables")
        config['database'] = db_name
    
    db_user = os.environ.get('DB_USER')
    if db_user is not None:
        print("Using DB_USER from environment variables")
        config['user'] = db_user
    
    db_password = os.environ.get('DB_PASSWORD')
    if db_password is not None:
        print("Using DB_PASSWORD from environment variables")
        config['password'] = db_password
    
    return config

def test_connection() -> None:
    """Test connection to the MySQL database"""
    config = load_db_config()
    connection = None
    cursor = None
    
    print("\nAttempting to connect to MySQL database with the following settings:")
    print(f"Host: {config['host']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Password: {'*' * 8}")
    
    try:
        # Create connection
        connection = mysql.connector.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("\n✅ Connection successful!")
            print(f"MySQL Server version: {db_info}")
            
            # Get cursor
            cursor = connection.cursor()
            
            # Get database info
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            if result is not None:
                database_name = result[0]
                print(f"Connected to database: {database_name}")
            
            # Check tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"\nTables in database:")
            for table in tables:
                if table and len(table) > 0:
                    print(f"  - {table[0]}")
                
            # Check employee_core_data table
            employee_table_exists = any(table[0] == 'employee_core_data' for table in tables if table and len(table) > 0)
            if employee_table_exists:
                cursor.execute("SELECT COUNT(*) FROM employee_core_data;")
                result = cursor.fetchone()
                if result is not None:
                    count = int(result[0])
                    print(f"\nemployee_core_data table has {count} records")
                    
                    if count > 0:
                        cursor.execute("SELECT employee_id, role, zone FROM employee_core_data LIMIT 5;")
                        rows = cursor.fetchall()
                        print("\nSample employee data:")
                        for row in rows:
                            if row and len(row) >= 3:
                                print(f"  - Employee ID: {row[0]}, Role: {row[1]}, Zone: {row[2]}")
            
            # Check performance_metrics table
            performance_table_exists = any(table[0] == 'performance_metrics' for table in tables if table and len(table) > 0)
            if performance_table_exists:
                cursor.execute("SELECT COUNT(*) FROM performance_metrics;")
                result = cursor.fetchone()
                if result is not None:
                    count = int(result[0])
                    print(f"\nperformance_metrics table has {count} records")
                    
                    if count > 0:
                        cursor.execute("SELECT employee_id, month, line_loss FROM performance_metrics LIMIT 5;")
                        rows = cursor.fetchall()
                        print("\nSample performance data:")
                        for row in rows:
                            if row and len(row) >= 3:
                                print(f"  - Employee ID: {row[0]}, Month: {row[1]}, Line Loss: {row[2]}")
            
            print("\nDatabase connection test completed successfully.")
            print("You can now run the dashboard using: streamlit run app.py")
            
    except Error as e:
        print("\n❌ Error connecting to MySQL database:")
        print(f"  {e}")
        
        # Provide troubleshooting tips
        print("\nTroubleshooting tips:")
        print("1. Check if the MySQL server is running")
        print("2. Verify the host, database, username, and password are correct")
        print("3. Ensure the user has proper permissions to access the database")
        print("4. Check if the database exists")
        print("5. Verify network connectivity to the database server")
        print("\nTo configure database connection:")
        print("- Create a db_config.json file in the project root directory")
        print("- Or set environment variables: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD")
        
    finally:
        # Close connection if it was established
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    print("=" * 60)
    print("Employee Performance Dashboard - Database Connection Test")
    print("=" * 60)
    test_connection()
