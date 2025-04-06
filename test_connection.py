"""
Test script to verify database connection and schema
Run this script to check if your database connection is working correctly
and if the required tables and columns exist.
"""

import sys
from typing import List, Tuple, Any, Optional, cast, TypeVar, Union
from src.utils.database import create_db_connection

def test_connection():
    """Test database connection and schema"""
    print("Testing database connection...")
    
    # Test connection
    connection = create_db_connection()
    if connection is None:
        print("❌ ERROR: Failed to connect to the database.")
        print("Please check your connection settings in src/utils/database.py")
        return False
    
    print("✅ Successfully connected to the database.")
    
    try:
        # Check if tables exist
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables
            WHERE table_schema = 'PERFORMANCEDB'
            AND table_name IN ('employee_core_data', 'performance_metrics')
        """)
        
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables if table[0]]  # type: ignore
        
        if 'employee_core_data' not in table_names:
            print("❌ ERROR: 'employee_core_data' table not found.")
            return False
            
        if 'performance_metrics' not in table_names:
            print("❌ ERROR: 'performance_metrics' table not found.")
            return False
        
        print("✅ Required tables exist.")
        
        # Check employee_core_data columns
        cursor.execute("SHOW COLUMNS FROM employee_core_data")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns if column[0]]  # type: ignore
        
        required_columns = ['employee_id', 'trainer_grade', 'training_count', 'status', 'role', 'zone']
        missing_columns = []
        
        for col in required_columns:
            if col not in column_names:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ ERROR: Missing columns in employee_core_data: {', '.join(missing_columns)}")
            print("Run the update_schema.sql script to add these columns.")
            return False
        
        print("✅ employee_core_data has all required columns.")
        
        # Check performance_metrics columns
        cursor.execute("SHOW COLUMNS FROM performance_metrics")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns if column[0]]  # type: ignore
        
        required_columns = [
            'employee_id', 'month', 'ul', 'sl', 'pl', 'zone', 'line_loss', 
            'error_count', 'unsafe_act_reported', 'unsafe_act_responsible', 
            'kaizen_responsible', 'flexibility_credit', 'teamwork_credit',
            'audit_nc_score', 'wi_ppe_score', 'ojt_test_score', 'dwm_adherence_score'
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in column_names:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ ERROR: Missing columns in performance_metrics: {', '.join(missing_columns)}")
            print("Run the update_schema.sql script to add these columns.")
            return False
        
        print("✅ performance_metrics has all required columns.")
        
        # Check if roles are assigned
        cursor.execute("SELECT COUNT(*) FROM employee_core_data WHERE role IS NULL OR role = ''")
        result = cursor.fetchone()
        # Use string index to satisfy type checker
        null_roles = int(result[0]) if result else 0  # type: ignore
        
        if null_roles > 0:
            print(f"⚠️ WARNING: {null_roles} employees have no role assigned.")
            print("Run the update_schema.sql script to assign roles.")
        else:
            print("✅ All employees have roles assigned.")
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM employee_core_data")
        result = cursor.fetchone()
        employee_count = int(result[0]) if result else 0  # type: ignore
        
        cursor.execute("SELECT COUNT(*) FROM performance_metrics")
        result = cursor.fetchone()
        metrics_count = int(result[0]) if result else 0  # type: ignore
        
        print(f"\nDatabase contains {employee_count} employees and {metrics_count} performance records.")
        
        if employee_count > 0:
            # Show sample employee data
            cursor.execute("""
                SELECT employee_id, trainer_grade, training_count, status, role, zone 
                FROM employee_core_data LIMIT 3
            """)
            
            print("\nSample employee data:")
            print("-" * 80)
            print(f"{'Employee ID':<15} {'Trainer Grade':<15} {'Training Count':<15} {'Status':<10} {'Role':<15} {'Zone':<5}")
            print("-" * 80)
            
            for row in cursor.fetchall():
                print(f"{str(row[0]):<15} {str(row[1]):<15} {str(row[2]):<15} {str(row[3]):<10} {str(row[4]):<15} {str(row[5]):<5}")  # type: ignore
        
        print("\n✅ Database connection and schema verification completed successfully.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
