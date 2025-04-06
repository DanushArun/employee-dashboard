-- SQL script to update existing database schema for Employee Performance Dashboard

-- Add new columns to employee_core_data if they don't exist
ALTER TABLE employee_core_data ADD COLUMN IF NOT EXISTS role VARCHAR(20);
ALTER TABLE employee_core_data ADD COLUMN IF NOT EXISTS zone INT;

-- Add new columns to performance_metrics if they don't exist
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS sl FLOAT DEFAULT 0;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS audit_nc_score FLOAT DEFAULT 0;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS wi_ppe_score FLOAT DEFAULT 0;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS ojt_test_score FLOAT DEFAULT 0;
ALTER TABLE performance_metrics ADD COLUMN IF NOT EXISTS dwm_adherence_score FLOAT DEFAULT 0;

-- Update employee roles based on employee ID pattern
-- Employees with IDs starting with 'Z' are assigned as Zone Leaders
UPDATE employee_core_data SET role = 'ZONE_LEADER' WHERE employee_id LIKE 'Z%';

-- All other employees are assigned as R Cadres
UPDATE employee_core_data SET role = 'R_CADRE' WHERE role IS NULL OR role = '';

-- Set default zone if not already set
UPDATE employee_core_data SET zone = 1 WHERE zone IS NULL;

-- Create indices for better performance if they don't exist
CREATE INDEX IF NOT EXISTS idx_employee_id ON performance_metrics(employee_id);
CREATE INDEX IF NOT EXISTS idx_month ON performance_metrics(month);
CREATE INDEX IF NOT EXISTS idx_zone ON performance_metrics(zone);
CREATE INDEX IF NOT EXISTS idx_role ON employee_core_data(role);

-- Display updated schema
SELECT 'employee_core_data columns:' AS message;
SHOW COLUMNS FROM employee_core_data;

SELECT 'performance_metrics columns:' AS message;
SHOW COLUMNS FROM performance_metrics;

-- Display sample data
SELECT 'Sample employee data:' AS message;
SELECT employee_id, trainer_grade, training_count, status, role, zone 
FROM employee_core_data LIMIT 5;

SELECT 'Sample performance metrics:' AS message;
SELECT employee_id, month, ul, sl, pl, zone, line_loss, error_count, 
       audit_nc_score, wi_ppe_score, ojt_test_score, dwm_adherence_score
FROM performance_metrics LIMIT 5;
