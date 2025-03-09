# Employee Performance Dashboard

A modern, industrial-grade dashboard for tracking employee performance metrics built with Streamlit.

![Dashboard Preview](https://i.imgur.com/example.png)

## Features

- **Employee Selection**: Searchable dropdown to select employees by ID
- **Date Range Filtering**: Select custom date ranges to view performance metrics
- **Performance Metrics**: View key metrics including Total Marks, Trainer Grade, and Training Count
- **Status Indicator**: Visual status indicator showing Pass/Fail status
- **Modern UI**: Dark theme with sleek animations and responsive design

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/employee-dashboard.git
cd employee-dashboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Method 1: Direct Run

```bash
streamlit run app.py
```

### Method 2: Using the Deployment Script

```bash
streamlit run deploy.py
```

This will provide you with deployment options:
- Local deployment
- Instructions for Streamlit Cloud deployment

## Deployment

### Local Deployment

Run the dashboard locally using the instructions above. The dashboard will be accessible at:
- Local URL: http://localhost:8501
- Network URL: http://your-ip-address:8501

### Cloud Deployment

To deploy to Streamlit Cloud:

1. Create a GitHub repository with your dashboard code
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Configure the deployment settings:
   - Main file path: `app.py`
   - Python version: 3.9+

## Data Structure

The dashboard expects a CSV file with the following columns:
- `employee_id`: Unique identifier for each employee
- `total_marks`: Numerical score
- `trainer_grade`: Decimal grade value
- `status`: "Pass" or "Fail"
- `training_count`: Number of training sessions
- `date`: Date in YYYY-MM-DD format

## Customization

You can customize the dashboard by modifying:
- `app.py`: Main application logic
- `src/styles/theme.py`: Theme configuration (if you want to separate styling)
- `src/assets/`: Place custom images and assets here

## License

[MIT License](LICENSE)
