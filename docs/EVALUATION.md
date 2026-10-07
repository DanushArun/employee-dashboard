# Employee Performance — Evaluation guide

Start with the smallest path that exercises the project. Distinguish source inspection,
syntax/build checks, functional behavior and domain validation when recording a result.

## Guided reading and demonstration

1. **Prepare authorized data.** Review the core/metrics schema and use a synthetic test database.
The application does not manufacture data when a database is missing.

2. **Select an employee.** Inspect the employee record and selected period. Database helpers
produce the dataframes consumed by the dashboard.

3. **Compare the indicators.** Review training, performance, safety and teamwork metrics and their
grading criteria. Comparisons are product calculations, not independent employment judgments.

4. **Trace a chart.** Follow the displayed result back to its SQL query and input record. Validate
missing data and normalization before interpreting differences.

## Declared checks

These commands/checks describe the intended verification path. Their presence in this
guide does not claim that they passed. See the dated evidence below and the README for setup.

```text
python -m compileall -q app.py src
```

## Evidence levels

| Level | What it establishes | What it does not establish |
| --- | --- | --- |
| Source review | A path exists in tracked code | Successful runtime behavior |
| Syntax/build | Parser/compiler accepts that path | End-to-end correctness |
| Behavioral check | A specific input/output case passed | Generalization beyond cases |
| Domain evaluation | Performance on a stated target setting | Other users/data/environments |

## What to record

- Commit, environment, dependency versions and date.
- Input provenance and whether data is synthetic, public or privately supplied.
- Absolute pass/fail/skip counts; keep failed cases and their root causes.
- Whether external services, hardware or a production deployment were actually exercised.
- Expected output and an artifact showing the observation.

## Review scenarios

- **SQL is the active data path:** The application queries MySQL rather than reading the old
README CSV schema.

- **Input criteria are inspectable:** Grades and normalized chart values need review with their
underlying definitions.

- **Database changes are separate:** Schema scripts are reviewed against a test schema before
execution.

## Documentation inspection — 7 October 2026

The documentation was traced to committed source and checked for local links, balanced
code fences and supported implementation claims. Historical notebook outputs remain labeled
as historical. Live provider access, private databases and hardware behavior are not inferred
from configuration or dependency files. Any fresh run is recorded separately in the README.

## Next evidence to collect

- Build a synthetic database acceptance fixture.
- Check chart calculations against known records.
- Review data access, missingness and scoring interpretation.
