import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import json

# Default database configuration
DEFAULT_DB_CONFIG = {
    "host": "AE-LP-2817\\PERFORMANCE_DASH",  # Windows server with double backslashes
    "database": "PERFORMANCEDB",
    "user": "arshia.goswami",
    "password": "Ather@123"
}

def load_db_config():
    """Load database configuration from config file or environment variables"""
    config = DEFAULT_DB_CONFIG.copy()
    
    # Check for config file
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db_config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    # Environment variables override config file
    if os.environ.get('DB_HOST'):
        config['host'] = os.environ.get('DB_HOST')
    if os.environ.get('DB_NAME'):
        config['database'] = os.environ.get('DB_NAME')
    if os.environ.get('DB_USER'):
        config['user'] = os.environ.get('DB_USER')
    if os.environ.get('DB_PASSWORD'):
        config['password'] = os.environ.get('DB_PASSWORD')
    
    return config

def create_db_connection():
    """Create a connection to the MySQL database"""
    config = load_db_config()
    try:
        connection = mysql.connector.connect(**config)
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
            status,
            role,
            zone
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
            p.sl,
            p.pl,
            p.zone,
            p.line_loss,
            p.error_count,
            p.unsafe_act_reported,
            p.unsafe_act_responsible,
            p.kaizen_responsible,
            p.flexibility_credit,
            p.teamwork_credit,
            p.audit_nc_score,
            p.wi_ppe_score,
            p.ojt_test_score,
            p.dwm_adherence_score
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

def fetch_zone_leaders_data():
    """Fetch data for zone leaders only"""
    connection = create_db_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            e.employee_id,
            e.trainer_grade,
            e.training_count,
            e.status,
            e.zone,
            p.month,
            p.ul,
            p.sl,
            p.pl,
            p.line_loss,
            p.error_count,
            p.unsafe_act_reported,
            p.unsafe_act_responsible,
            p.kaizen_responsible,
            p.flexibility_credit,
            p.teamwork_credit,
            p.audit_nc_score,
            p.ojt_test_score,
            p.dwm_adherence_score
        FROM employee_core_data e
        LEFT JOIN performance_metrics p ON e.employee_id = p.employee_id
        WHERE e.role = 'ZONE_LEADER'
        """
        return pd.read_sql(query, connection)
    except Error as e:
        print(f"Error fetching zone leaders data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()

def fetch_r_cadres_data():
    """Fetch data for R cadres only"""
    connection = create_db_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            e.employee_id,
            e.trainer_grade,
            e.training_count,
            e.status,
            e.zone,
            p.month,
            p.ul,
            p.sl,
            p.pl,
            p.line_loss,
            p.error_count,
            p.unsafe_act_reported,
            p.unsafe_act_responsible,
            p.kaizen_responsible,
            p.flexibility_credit,
            p.teamwork_credit,
            p.wi_ppe_score,
            p.ojt_test_score
        FROM employee_core_data e
        LEFT JOIN performance_metrics p ON e.employee_id = p.employee_id
        WHERE e.role = 'R_CADRE'
        """
        return pd.read_sql(query, connection)
    except Error as e:
        print(f"Error fetching R cadres data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()

def fetch_line_loss_count(line_number, zone_number):
    """Fetch count of entries from performance_metrics for a specific line and zone"""
    connection = create_db_connection()
    if connection is None:
        return 0
    
    try:
        # Query to count entries in performance_metrics where zone matches the specified zone
        # and line_loss is greater than 0 (indicating a loss)
        query = f"""
        SELECT 
            COUNT(*) as count
        FROM performance_metrics
        WHERE zone = {zone_number} AND line_loss > 0
        """
        
        # If we need to filter by line number as well, we would need a column in the database
        # that indicates which line the entry belongs to. Since we don't have that in the
        # current schema, we're just filtering by zone.
        
        result = pd.read_sql(query, connection)
        if result.empty:
            return 0
        
        return result['count'].values[0]
    except Error as e:
        print(f"Error fetching line loss count: {e}")
        return 0
    finally:
        if connection.is_connected():
            connection.close()
