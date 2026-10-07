# Employee Performance — Architecture and implementation

This guide follows the tracked implementation. Proposed work is identified separately.

## The problem and the system boundary

Employee metrics become difficult to interpret when training, safety and production indicators sit
in separate records. This dashboard joins configured SQL-backed records into employee, trend,
comparison and zone views, while leaving the scoring criteria in source.

## Processing path

```mermaid
flowchart LR
    N0["MySQL tables"]
    N1["SQL helpers"]
    N2["Dataframes"]
    N3["Performance views"]
    N0 --> N1
    N1 --> N2
    N2 --> N3
```

## End-to-end behavior

### 1. Prepare authorized data

Review the core/metrics schema and use a synthetic test database. The application does not
manufacture data when a database is missing.

### 2. Select an employee

Inspect the employee record and selected period. Database helpers produce the dataframes consumed
by the dashboard.

### 3. Compare the indicators

Review training, performance, safety and teamwork metrics and their grading criteria. Comparisons
are product calculations, not independent employment judgments.

### 4. Trace a chart

Follow the displayed result back to its SQL query and input record. Validate missing data and
normalization before interpreting differences.

## Design choices and consequences

### SQL is the active data path

The application queries MySQL rather than reading the old README CSV schema.

### Input criteria are inspectable

Grades and normalized chart values need review with their underlying definitions.

### Database changes are separate

Schema scripts are reviewed against a test schema before execution.

## Source entry points

### [app.py](../app.py)

- `calculate_grade` — Calculate grade based on criteria
- `load_data` — Implementation entry; inspect source for its exact behavior.

### [src/utils/database.py](../src/utils/database.py)

- `load_db_config` — Load database configuration from config file or environment variables
- `create_db_connection` — Create a connection to the MySQL database
- `fetch_core_data` — Fetch core employee data from database
- `fetch_performance_data` — Fetch performance metrics from database
- `fetch_zone_leaders_data` — Fetch data for zone leaders only
- `fetch_r_cadres_data` — Fetch data for R cadres only

### [src/utils/create_tables.sql](../src/utils/create_tables.sql)

This file is part of the reviewed path described above. Follow its imports and calls
for the exact interface rather than inferring behavior from the filename.

### [src/utils/update_schema.sql](../src/utils/update_schema.sql)

This file is part of the reviewed path described above. Follow its imports and calls
for the exact interface rather than inferring behavior from the filename.

### [src/components/charts.py](../src/components/charts.py)

- `create_performance_chart` — Create a performance radar chart for the selected employee
- `create_trend_chart` — Create a trend chart for a specific metric over time
- `create_comparison_chart` — Create a chart comparing employee's metric with average
- `create_status_distribution` — Create a pie chart showing the distribution of pass/fail status
- `create_zone_distribution` — Create a bar chart showing the distribution of employees by zone

## Implementation state

| State | Evidence boundary |
| --- | --- |
| Present | SQL-backed views, grade logic and charts |
| Present | Schema/migration helper source |
| Configuration required | Populated, authorized MySQL instance |
| Not validated | Assessment fairness, data accuracy or production access controls |

“Present” means tracked source or assets exist. It does not mean a production or domain
validation has passed. See [Evaluation](EVALUATION.md) for reproducible checks and limits.
