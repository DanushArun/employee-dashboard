import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_db_connection():
    """Create a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="PERFORMANCEDB",
            user="arshia.goswami",
            password="Ather@123"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def fetch_core_data():
    """Fetch core employee data from database"""
    connection = create_db_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            employee_id,
            trainer_grade,
            training_count,
            status
        FROM employee_core_data
        """
        return pd.read_sql(query, connection)
    except Error as e:
        print(f"Error fetching core data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()

def fetch_performance_data():
    """Fetch performance metrics from database"""
    connection = create_db_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            e.employee_id,
            p.month,
            p.ul,
            p.pl,
            p.zone,
            p.line_loss,
            p.error_count,
            p.unsafe_act_reported,
            p.unsafe_act_responsible,
            p.kaizen_responsible,
            p.flexibility_credit,
            p.teamwork_credit
        FROM employee_core_data e
        LEFT JOIN performance_metrics p ON e.employee_id = p.employee_id
        """
        return pd.read_sql(query, connection)
    except Error as e:
        print(f"Error fetching performance data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()
