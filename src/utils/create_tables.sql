-- Create employee core data table
CREATE TABLE employee_core_data (
    employee_id VARCHAR(10) PRIMARY KEY,
    trainer_grade FLOAT,
    training_count INT,
    status VARCHAR(20)
);

-- Create performance metrics table
CREATE TABLE performance_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(10),
    month VARCHAR(10),
    ul FLOAT,
    pl FLOAT,
    zone INT,
    line_loss FLOAT,
    error_count INT,
    unsafe_act_reported INT,
    unsafe_act_responsible INT,
    kaizen_responsible INT,
    flexibility_credit INT,
    teamwork_credit INT,
    FOREIGN KEY (employee_id) REFERENCES employee_core_data(employee_id)
);

-- Create indices for better query performance
CREATE INDEX idx_employee_id ON performance_metrics(employee_id);
CREATE INDEX idx_month ON performance_metrics(month);
CREATE INDEX idx_zone ON performance_metrics(zone);
