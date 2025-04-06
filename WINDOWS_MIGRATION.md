# Windows Migration Guide

This guide provides instructions for migrating the Employee Performance Dashboard to a Windows system with an existing MySQL database.

## Prerequisites

- Existing MySQL database on Windows server `AE-LP-2817\PERFORMANCE_DASH`
- Database name: `PERFORMANCEDB`
- User credentials: `arshia.goswami` / `Ather@123`
- Python 3.x installed on Windows

## Migration Steps

### 1. Copy Project Files

Copy all project files to your Windows system, maintaining the directory structure:

```
employee-dashboard/
├── app.py
├── requirements.txt
├── data/
│   └── Test Data.csv
└── src/
    ├── assets/
    │   └── ather-logo.png
    ├── components/
    │   └── charts.py
    ├── styles/
    │   └── theme.py
    └── utils/
        ├── create_tables.sql
        ├── database.py
        └── migrate_data.py
```

### 2. Install Required Packages

Open Command Prompt as Administrator and run:

```cmd
pip install -r requirements.txt
```

Make sure the mysql-connector-python package is installed correctly:

```cmd
pip show mysql-connector-python
```

If it's not installed or you encounter any issues, install it directly:

```cmd
pip install mysql-connector-python
```

### 3. Update Database Schema

Run the provided SQL script to update your existing database schema:

```cmd
mysql -u arshia.goswami -p PERFORMANCEDB < src\utils\update_schema.sql
```

This script will:
- Add new columns to the employee_core_data table (role, zone)
- Add new columns to the performance_metrics table (sl, audit_nc_score, wi_ppe_score, ojt_test_score, dwm_adherence_score)
- Update employee roles based on employee ID pattern
- Create necessary indices for better performance
- Display the updated schema and sample data

The script uses `IF NOT EXISTS` clauses, so it's safe to run even if some columns already exist.

### 4. Update Connection Settings

Edit `src/utils/database.py` to ensure the connection settings match your Windows server:

```python
connection = mysql.connector.connect(
    host="AE-LP-2817\\PERFORMANCE_DASH",  # Use double backslashes for Windows paths
    database="PERFORMANCEDB",
    user="arshia.goswami",
    password="Ather@123"
)
```

### 5. Test the Connection

Run the test script to verify your database connection and schema:

```cmd
python test_connection.py
```

This script will:
- Test the connection to your database
- Verify that all required tables exist
- Check for all required columns
- Verify that employee roles are assigned
- Display sample data from your database

If any issues are found, the script will provide specific error messages and instructions for fixing them.

### 6. Run the Dashboard

Once the connection test passes, start the dashboard with:

```cmd
streamlit run app.py
```

The dashboard will open in your default browser at http://localhost:8501

## Verifying the Migration

1. **Check Database Connection**
   - The dashboard should connect to your database without errors
   - Employee data should be displayed correctly

2. **Verify Role-Based Display**
   - Select a Zone Leader employee to verify they see:
     * Audit NCs section
     * DWM Adherence section
   - Select an R Cadre employee to verify they see:
     * WI & PPE Adherence section

3. **Test Metrics Calculation**
   - Verify all metrics are calculated according to the Excel specifications
   - Check that grades are displayed correctly (on a 4.0 scale)

4. **Test Real-Time Updates**
   - Make changes to the database and verify they appear in the dashboard
   - Test the manual refresh button

## Troubleshooting

1. **Connection Issues**
   - Verify the server name format: `AE-LP-2817\\PERFORMANCE_DASH` (double backslashes)
   - Check that the MySQL server is running
   - Ensure the user has proper permissions

2. **Missing Data**
   - Verify that the role column is populated for all employees
   - Check that all required metrics are present in the database

3. **Display Issues**
   - Check the browser console for JavaScript errors
   - Verify that Streamlit is running correctly

4. **Performance Issues**
   - Add indices to frequently queried columns
   - Optimize database queries if needed
