# Deployment Guide for Employee Performance Dashboard

This guide provides detailed instructions for deploying the Employee Performance Dashboard to different environments, including the system with the database.

## Local Deployment

### Prerequisites
- Python 3.x installed
- MySQL Server installed and running
- All required dependencies installed (`pip install -r requirements.txt`)
- Database configured (see [DATABASE_SETUP.md](DATABASE_SETUP.md))

### Steps

1. **Configure Database Connection**
   - Create a `db_config.json` file in the project root directory:
   ```json
   {
     "host": "localhost",
     "database": "PERFORMANCEDB",
     "user": "your-username",
     "password": "your-password"
   }
   ```
   - Or set environment variables:
     - `DB_HOST`: Database server hostname
     - `DB_NAME`: Database name
     - `DB_USER`: Database username
     - `DB_PASSWORD`: Database password

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Access the Dashboard**
   - Local URL: http://localhost:8501
   - Network URL: http://your-ip-address:8501

## Deployment to Remote System with Database

### Prerequisites
- Target system has Python 3.x installed
- MySQL Server installed and running on the target system
- Network connectivity between the application server and database server

### Steps

1. **Transfer Files to Target System**
   - Copy all project files to the target system
   - Ensure the directory structure is preserved

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database Connection**
   - Create a `db_config.json` file with the correct database server details:
   ```json
   {
     "host": "database-server-hostname",
     "database": "PERFORMANCEDB",
     "user": "your-username",
     "password": "your-password"
   }
   ```
   - For Windows systems with SQL Server using named instances, use double backslashes:
   ```json
   {
     "host": "SERVER-NAME\\INSTANCE-NAME",
     "database": "PERFORMANCEDB",
     "user": "your-username",
     "password": "your-password"
   }
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the Dashboard**
   - Local URL: http://localhost:8501
   - Network URL: http://server-ip-address:8501

## Production Deployment

For production environments, it's recommended to use a more robust setup:

### Option 1: Using Streamlit Sharing (Cloud)

1. Push your code to GitHub
2. Sign up for [Streamlit Sharing](https://streamlit.io/sharing)
3. Connect your GitHub repository
4. Configure secrets for database credentials
5. Deploy with a few clicks

### Option 2: Using Docker

1. **Create a Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and Run the Docker Image**
   ```bash
   docker build -t employee-dashboard .
   docker run -p 8501:8501 -e DB_HOST=your-db-host -e DB_NAME=PERFORMANCEDB -e DB_USER=your-user -e DB_PASSWORD=your-password employee-dashboard
   ```

### Option 3: Using a Production WSGI Server

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create a WSGI Entry Point (app_wsgi.py)**
   ```python
   import streamlit.web.bootstrap as bootstrap
   from streamlit.web.server import Server

   def run_server():
       bootstrap.run("app.py", "", [], flag_options={})

   if __name__ == "__main__":
       run_server()
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8501 app_wsgi:run_server
   ```

## Security Considerations

1. **Database Credentials**
   - Never commit database credentials to version control
   - Use environment variables or secure credential storage
   - Implement proper access controls on the database

2. **Network Security**
   - Use HTTPS for production deployments
   - Consider using a reverse proxy (Nginx, Apache) for SSL termination
   - Implement proper firewall rules

3. **Authentication**
   - Consider adding authentication for the dashboard
   - Streamlit has built-in authentication options
   - Or use a reverse proxy with authentication

## Monitoring and Maintenance

1. **Logging**
   - Configure logging to capture application events
   - Monitor for errors and performance issues

2. **Backup**
   - Regularly backup the database
   - Document the backup and restore procedures

3. **Updates**
   - Keep dependencies updated
   - Test updates in a staging environment before deploying to production

## Troubleshooting

1. **Connection Issues**
   - Verify network connectivity between application and database
   - Check firewall settings
   - Ensure database server is running and accessible

2. **Performance Issues**
   - Monitor system resources (CPU, memory, disk)
   - Optimize database queries
   - Consider scaling resources if needed

3. **Application Errors**
   - Check application logs
   - Verify database schema is correct
   - Ensure all dependencies are installed correctly
