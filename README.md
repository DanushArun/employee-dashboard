# Employee Performance Dashboard

A modern, industrial-grade dashboard for tracking employee performance metrics built with Streamlit.

## Features

- **Employee Selection**: Searchable dropdown to select employees by ID
- **Date Range Filtering**: Select custom date ranges to view performance metrics
- **Performance Radar Chart**: Interactive radar visualization showing normalized scores for:
  - Trainer Grade (0-4 scale)
  - Training Count
  - Upper Limit (UL) Score
  - Performance Level (PL) Score
  - Error Count
  - Kaizen Responsibility
  - Flexibility
  - Teamwork
- **Trend Analysis**: Line charts showing metric progression over time
- **Comparative Analysis**: Bar charts comparing individual metrics against team averages
- **Status Distribution**: Visual breakdown of Pass/Fail ratios
- **Zone Distribution**: Bar chart showing employee distribution across work zones

## Installation

1. Clone this repository:
```bash
git clone https://github.com/DanushArun/employee-dashboard.git
cd employee-dashboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the database connection:
   - Rename `db_config.json.template` to `db_config.json`
   - Edit the file to match your database configuration:
   ```json
   {
     "host": "your-database-server",
     "database": "your-database-name",
     "user": "your-username",
     "password": "your-password"
   }
   ```
   - Alternatively, you can set the following environment variables:
     - `DB_HOST`: Database server hostname
     - `DB_NAME`: Database name
     - `DB_USER`: Database username
     - `DB_PASSWORD`: Database password

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

For detailed instructions on deploying to Streamlit Cloud, see the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) file.

In summary:
1. Push your code to GitHub
2. Sign up for [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Deploy with a few clicks
5. Share the generated URL with anyone

The dashboard will be accessible from anywhere with an internet connection, and updates automatically when you push changes to GitHub.

## Data Structure

The dashboard expects a CSV file with the following columns:
- `employee_id`: Unique identifier for each employee
- `trainer_grade`: Decimal grade value (0-4 scale)
- `training_count`: Number of training sessions completed
- `ul`: Upper limit score (0-5 scale, lower is better)
- `pl`: Performance level score (0-5 scale, lower is better)
- `error_count`: Number of errors (0-5 scale, lower is better)
- `kaizen_responsible`: Kaizen responsibility score (0-4 scale)
- `flexibility_credit`: Flexibility rating (0-4 scale)
- `teamwork_credit`: Teamwork rating (0-4 scale)
- `status`: "Pass" or "Fail"
- `zone`: Work zone assignment
- `date`: Date in YYYY-MM-DD format

## Tech Stack

- **Frontend**: Streamlit for the web interface
- **Data Visualization**: Altair for interactive charts
- **Data Processing**: Pandas and NumPy for data manipulation
- **Styling**: Custom theme configuration for a modern look

## Dependencies

The dashboard requires the following main packages:
- streamlit
- pandas
- numpy
- altair

All dependencies are listed in `requirements.txt`.

## Customization

You can customize the dashboard by modifying:
- `app.py`: Main application logic
- `src/styles/theme.py`: Theme configuration
- `src/assets/`: Place custom images and assets here
- `src/components/charts.py`: Visualization components

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate tests.

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

[MIT License](LICENSE)
