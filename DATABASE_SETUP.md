# Database Setup Guide for Windows

This guide will help you set up the MySQL database for the Employee Performance Dashboard on Windows.

## Prerequisites

1. MySQL Server installed on Windows
   - Download from: https://dev.mysql.com/downloads/installer/
   - Choose "MySQL Server" and "MySQL Workbench" during installation
   - Select "Developer Default" setup type
   - Keep default port (3306)
   - Choose "Use Legacy Authentication Method"
   - Set and note your root password during installation
   - Complete the installation and verify MySQL Server is installed

2. Python 3.x with required packages:
   ```cmd
   # Open Command Prompt as Administrator
   pip install -r requirements.txt
   ```
   This will install:
   - mysql-connector-python>=8.0.0 (Database connection)
   - pandas>=1.4.0 (Data handling)
   - streamlit>=1.10.0 (Dashboard interface)
   - numpy>=1.21.0 (Numerical operations)
   - plotly>=5.7.0 (Interactive charts)
   - Pillow>=9.0.0 (Image handling)

3. Project files in place:
   - Verify `data\Test Data.csv` exists
   - Check all required Python files are present:
     * src\utils\database.py
     * src\utils\migrate_data.py
     * src\utils\create_tables.sql
     * app.py

## Setup Steps

1. **Start MySQL Server**
   - Open Services (Win + R, type "services.msc")
   - Find "MySQL80" service
   - Ensure it's running (Status: Running)
   - If not, right-click → Start

2. **Create Database and User**
   - Open Command Prompt as Administrator
   - Connect to MySQL as root:
     ```cmd
     mysql -u root -p
     ```
   - Enter your root password when prompted
   - Create database and user:
     ```sql
     CREATE DATABASE PERFORMANCEDB;
     CREATE USER 'arshia.goswami'@'localhost' IDENTIFIED BY 'Ather@123';
     GRANT ALL PRIVILEGES ON PERFORMANCEDB.* TO 'arshia.goswami'@'localhost';
     FLUSH PRIVILEGES;
     EXIT;
     ```

3. **Create Database Tables**
   - Open Command Prompt in your project directory
   - Run the SQL script:
     ```cmd
     mysql -u arshia.goswami -p PERFORMANCEDB < src\utils\create_tables.sql
     ```
   - Enter password: `Ather@123`

4. **Update Connection Settings**
   - Open `src\utils\database.py`
   - Verify connection settings:
     ```python
     connection = mysql.connector.connect(
         host="localhost",
         database="PERFORMANCEDB",
         user="arshia.goswami",
         password="Ather@123"
     )
     ```

5. **Migrate Data**
   - In Command Prompt:
     ```cmd
     python src\utils\migrate_data.py
     ```

6. **Verify Setup**
   - Connect to MySQL:
     ```cmd
     mysql -u arshia.goswami -p PERFORMANCEDB
     ```
   - Enter password: `Ather@123`
   - Run verification queries:
     ```sql
     -- Check if tables exist
     SHOW TABLES;
     
     -- Check table structure
     DESCRIBE employee_core_data;
     DESCRIBE performance_metrics;
     
     -- Verify indices
     SHOW INDEX FROM employee_core_data;
     SHOW INDEX FROM performance_metrics;
     
     -- Check data
     SELECT * FROM employee_core_data LIMIT 5;
     SELECT * FROM performance_metrics LIMIT 5;
     
     -- Check foreign key relationship
     SELECT e.employee_id, e.trainer_grade, p.month, p.ul, p.pl
     FROM employee_core_data e
     JOIN performance_metrics p ON e.employee_id = p.employee_id
     LIMIT 5;
     
     -- Exit MySQL
     EXIT;
     ```

## Troubleshooting

1. **MySQL Service Issues**
   - Check service status in Services
   - Try restarting the service
   - Check Windows Event Viewer for errors

2. **Connection Issues**
   - Verify MySQL is running: `netstat -an | findstr "3306"`
   - Test connection: `mysql -u arshia.goswami -p`
   - Check Windows Firewall settings for port 3306

3. **Data Migration Issues**
   - Ensure correct file paths (use backslashes in Windows)
   - Check file permissions
   - Verify CSV file exists in `data\Test Data.csv`
   - Run Python with administrator privileges if needed

## Database Schema

### employee_core_data
- employee_id (VARCHAR(10), Primary Key)
- trainer_grade (FLOAT)
- training_count (INT)
- status (VARCHAR(20))
- role (VARCHAR(20)) - 'ZONE_LEADER' or 'R_CADRE'
- zone (INT)

### performance_metrics
- id (INT, Auto Increment, Primary Key)
- employee_id (VARCHAR(10), Foreign Key)
- month (VARCHAR(10))
- ul (FLOAT) - Unplanned Leave
- sl (FLOAT) - Sick Leave
- pl (FLOAT) - Planned Leave
- zone (INT)
- line_loss (FLOAT)
- error_count (INT)
- unsafe_act_reported (INT)
- unsafe_act_responsible (INT)
- kaizen_responsible (INT)
- flexibility_credit (INT)
- teamwork_credit (INT)
- audit_nc_score (FLOAT) - For Zone Leaders
- wi_ppe_score (FLOAT) - For R Cadres
- ojt_test_score (FLOAT)
- dwm_adherence_score (FLOAT) - For Zone Leaders

## Dashboard Features

The dashboard now includes the following features based on the Excel specifications:

1. **Role-Based Metrics**
   - Zone Leaders: Audit NCs, Line Loss, Associate Error, Absenteeism, Performance Credits, OJT Test Score, DWM Adherence
   - R Cadres: Line Loss, Associate Error, Absenteeism, Performance Credits, WI & PPE, OJT Test Score

2. **Grading System**
   - Audit NCs: 4=100%, 3=85-99%, 2=65-85%, 1=<65%
   - Line Loss: 4=0, 3=1-3%, 2=3-5%, 1=>5%
   - Associate Error: 4=0, 3=1-3, 2=4-6, 1=>6
   - Absenteeism: Based on UL and SL counts
   - Performance Credits: 4=>9, 3=6-9, 2=3-6, 1=<3
   - OJT Test Score: Normalized to 4.0 scale
   - WI & PPE: Based on yes/no questions
   - DWM Adherence: Normalized to 4.0 scale

3. **Real-time Updates**
   - Data refreshes automatically every 60 seconds
   - Manual refresh button available

## Running the Dashboard

1. **Start the Dashboard**
   - Open Command Prompt in your project directory
   - First, test the database connection:
     ```cmd
     python -c "from src.utils.database import create_db_connection; conn = create_db_connection(); print('Database connection successful!' if conn else 'Connection failed!')"
     ```
   - If connection is successful, run the Streamlit app:
     ```cmd
     streamlit run app.py
     ```
   - The dashboard will open in your default browser
   - Default URL: http://localhost:8501
   - Check console for any error messages

2. **Testing with Sample Data**
   - The dashboard requires employee role information to display correctly
   - Sample data is generated with roles based on employee ID pattern
   - Employee IDs starting with 'Z' are assigned as Zone Leaders
   - All other employee IDs are assigned as R Cadres
   - You can modify this logic in migrate_data.py if needed

2. **Real-time Updates**
   - The dashboard automatically refreshes data every 60 seconds
   - Click the refresh button in the UI for manual updates
   - Data changes in MySQL will reflect in real-time

3. **Verify Dashboard Operation**
   - Check if employee data is displayed
   - Verify metrics are updating
   - Test the search and filter functionality
   - Ensure graphs and charts are rendering correctly

## Common Issues and Solutions

1. **Dashboard Not Showing Data**
   - Verify MySQL service is running
   - Check database connection in database.py
   - Ensure all tables are populated (use verification queries)
   - Look for error messages in the Streamlit output

2. **Data Not Updating**
   - Check MySQL connection is stable
   - Verify auto-refresh is working (check timestamp)
   - Try manual refresh button
   - Restart the Streamlit server if needed

3. **Performance Issues**
   - Check system resources:
     ```cmd
     tasklist | findstr "mysql python streamlit"
     ```
   - Verify MySQL query performance:
     ```sql
     -- In MySQL
     SHOW VARIABLES LIKE '%slow_query%';
     SHOW VARIABLES LIKE '%long_query_time%';
     ```
   - Monitor memory usage:
     ```cmd
     wmic process where "name like '%python%' or name like '%streamlit%'" get processid,commandline,workingsetsize
     ```
   - Database indices are already created for:
     * employee_id (both tables)
     * month (performance_metrics)
     * zone (performance_metrics)

4. **Backup Your Data**
   - Create database backup:
     ```cmd
     mysqldump -u arshia.goswami -p PERFORMANCEDB > backup.sql
     ```
   - Restore if needed:
     ```cmd
     mysql -u arshia.goswami -p PERFORMANCEDB < backup.sql
     ```
