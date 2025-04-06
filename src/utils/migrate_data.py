import pandas as pd
import mysql.connector
from mysql.connector import Error

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

def migrate_data():
    """Migrate data from CSV to MySQL database"""
    connection = None
    cursor = None
    
    try:
        # Read the CSV file
        with open('data/Test Data.csv', 'r') as f:
            content = f.read()
        
        # Split by lines
        lines = content.split('\n')
        
        # Extract different sections
        core_section = []
        ul_pl_section = []
        zone_loss_section = []
        error_count_section = []
        unsafe_act_section = []
        kaizen_section = []
        flexibility_section = []
        teamwork_section = []
        
        current_section = core_section
        for line in lines:
            if not line.strip():
                continue
                
            if "Month,Employee ID,UL" in line:
                current_section = ul_pl_section
                ul_pl_section.append(line)
            elif "Month,Employee ID,ZONE,LINE LOSS" in line:
                current_section = zone_loss_section
                zone_loss_section.append(line)
            elif "Month,Employee ID,ZONE,ERROR COUNT" in line:
                current_section = error_count_section
                error_count_section.append(line)
            elif "Month,Employee ID,UNSAFE ACT REPORTED" in line:
                current_section = unsafe_act_section
                unsafe_act_section.append(line)
            elif "Month,Employee ID,KAIZEN RESPONSIBLE" in line:
                current_section = kaizen_section
                kaizen_section.append(line)
            elif "Month,Employee ID,FLEXIBILITY CREDIT" in line:
                current_section = flexibility_section
                flexibility_section.append(line)
            elif "Month,Employee ID,TEAMWORK CREDIT" in line:
                current_section = teamwork_section
                teamwork_section.append(line)
            else:
                current_section.append(line)
        
        # Create database connection
        connection = create_db_connection()
        if connection is None:
            print("Failed to establish database connection")
            return
        
        cursor = connection.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'PERFORMANCEDB'
            AND table_name IN ('employee_core_data', 'performance_metrics')
        """)
        
        try:
            result = cursor.fetchone()
            if result is None:
                print("Failed to check tables. Please verify database connection.")
                return
                
            # Safely unpack the tuple and convert to int
            count_value, *_ = result  # Unpack first value
            table_count = int(str(count_value)) if count_value is not None else 0
            
            if table_count != 2:
                print("Required tables do not exist. Please run create_tables.sql first.")
                return
        except (ValueError, TypeError) as e:
            print(f"Error checking tables: {e}")
            return
        
        # Insert core data
        for i, line in enumerate(core_section):
            if i == 0:  # Skip header
                continue
                
            parts = line.split(',')
            if len(parts) >= 4:
                employee_id = parts[0].strip()
                training_grade = parts[1].strip()
                training_count = parts[2].strip()
                status = parts[3].strip()
                
                cursor.execute("""
                    INSERT INTO employee_core_data 
                    (employee_id, trainer_grade, training_count, status)
                    VALUES (%s, %s, %s, %s)
                """, (
                    employee_id,
                    float(training_grade) if training_grade.isdigit() else 0,
                    int(training_count) if training_count.isdigit() else 0,
                    status.capitalize()
                ))
        
        # Process performance metrics
        performance_data = {}
        
        # Process UL/PL data
        for i, line in enumerate(ul_pl_section):
            if i == 0:  # Skip header
                continue
                
            parts = line.split(',')
            if len(parts) >= 4:
                month = parts[0].strip().lower()
                employee_id = parts[1].strip()
                ul = float(parts[2].strip()) if parts[2].strip().isdigit() else 0
                pl = float(parts[3].strip()) if parts[3].strip().isdigit() else 0
                
                key = (employee_id, month)
                if key not in performance_data:
                    performance_data[key] = {
                        'employee_id': employee_id,
                        'month': month,
                        'ul': ul,
                        'pl': pl,
                        'zone': 0,
                        'line_loss': 0,
                        'error_count': 0,
                        'unsafe_act_reported': 0,
                        'unsafe_act_responsible': 0,
                        'kaizen_responsible': 0,
                        'flexibility_credit': 0,
                        'teamwork_credit': 0
                    }
                else:
                    performance_data[key].update({'ul': ul, 'pl': pl})
        
        # Process Zone/Line Loss data
        for i, line in enumerate(zone_loss_section):
            if i == 0:  # Skip header
                continue
                
            parts = line.split(',')
            if len(parts) >= 4:
                month = parts[0].strip().lower()
                employee_id = parts[1].strip()
                zone = int(parts[2].strip()) if parts[2].strip().isdigit() else 0
                line_loss = float(parts[3].strip()) if parts[3].strip().isdigit() else 0
                
                key = (employee_id, month)
                if key not in performance_data:
                    performance_data[key] = {
                        'employee_id': employee_id,
                        'month': month,
                        'ul': 0,
                        'pl': 0,
                        'zone': zone,
                        'line_loss': line_loss,
                        'error_count': 0,
                        'unsafe_act_reported': 0,
                        'unsafe_act_responsible': 0,
                        'kaizen_responsible': 0,
                        'flexibility_credit': 0,
                        'teamwork_credit': 0
                    }
                else:
                    performance_data[key].update({'zone': zone, 'line_loss': line_loss})
        
        # Insert performance data
        for key, data in performance_data.items():
            cursor.execute("""
                INSERT INTO performance_metrics 
                (employee_id, month, ul, pl, zone, line_loss, error_count,
                unsafe_act_reported, unsafe_act_responsible, kaizen_responsible,
                flexibility_credit, teamwork_credit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['employee_id'],
                data['month'],
                data['ul'],
                data['pl'],
                data['zone'],
                data['line_loss'],
                data['error_count'],
                data['unsafe_act_reported'],
                data['unsafe_act_responsible'],
                data['kaizen_responsible'],
                data['flexibility_credit'],
                data['teamwork_credit']
            ))
        
        # Commit changes
        connection.commit()
        print("Data migration completed successfully")
        
    except Exception as e:
        print(f"Error during data migration: {e}")
        if connection is not None:
            connection.rollback()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

if __name__ == "__main__":
    migrate_data()
