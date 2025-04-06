# Database Setup Guide

This guide will help you set up the MySQL database for the Employee Performance Dashboard.

## Prerequisites

1. MySQL Server installed on Windows
2. Python 3.x with required packages:
   ```bash
   python3 -m pip install mysql-connector-python pandas
   ```

## Setup Steps

1. **Create Database Tables**
   
   Run the SQL script to create the necessary tables:
   ```bash
   mysql -u arshia.goswami -p PERFORMANCEDB < src/utils/create_tables.sql
   ```
   When prompted, enter your password: `Ather@123`

2. **Migrate Data**
   
   Run the Python script to migrate data from CSV to MySQL:
   ```bash
   python3 src/utils/migrate_data.py
   ```

3. **Verify Setup**
   
   You can verify the setup by running these SQL queries:
   ```sql
   -- Check employee core data
   SELECT * FROM employee_core_data LIMIT 5;
   
   -- Check performance metrics
   SELECT * FROM performance_metrics LIMIT 5;
   ```

## Troubleshooting

1. **Connection Issues**
   - Verify MySQL server is running on the remote machine
   - Check credentials in database.py
   - Ensure the server name is correct: `AE-LP-2817\\PERFORMANCE_DASH`
   - Make sure the remote MySQL server:
     * Is configured to accept remote connections
     * Has the correct port open (default 3306)
     * Has granted access to your user from your IP address

2. **Data Migration Issues**
   - Ensure Test Data.csv exists in the data/ directory
   - Check file permissions
   - Verify CSV format matches expected structure
   - If you get connection errors:
     * Try using the IP address instead of hostname
     * Check network connectivity to the remote server
     * Verify firewall settings on both machines

## Database Schema

### employee_core_data
- employee_id (VARCHAR(10), Primary Key)
- trainer_grade (FLOAT)
- training_count (INT)
- status (VARCHAR(20))

### performance_metrics
- id (INT, Auto Increment, Primary Key)
- employee_id (VARCHAR(10), Foreign Key)
- month (VARCHAR(10))
- ul (FLOAT)
- pl (FLOAT)
- zone (INT)
- line_loss (FLOAT)
- error_count (INT)
- unsafe_act_reported (INT)
- unsafe_act_responsible (INT)
- kaizen_responsible (INT)
- flexibility_credit (INT)
- teamwork_credit (INT)

## Real-time Updates

The dashboard automatically refreshes data every 60 seconds. You can also manually refresh using the refresh button in the UI.
