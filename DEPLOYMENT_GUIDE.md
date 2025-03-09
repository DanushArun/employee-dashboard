# Deploying Your Employee Dashboard to Streamlit Cloud

This guide will walk you through the process of deploying your Employee Dashboard to Streamlit Cloud, making it accessible from anywhere with an internet connection.

## Prerequisites

- A GitHub account (create one at [github.com](https://github.com/signup) if you don't have one)
- Your code is already initialized as a Git repository (which we've done)

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in to your account
2. Click on the "+" icon in the top-right corner and select "New repository"
3. Name your repository (e.g., "employee-dashboard")
4. Add a description (optional)
5. Choose "Public" or "Private" (Public is recommended for Streamlit Cloud free tier)
6. Click "Create repository"

## Step 2: Push Your Code to GitHub

After creating the repository, GitHub will show instructions for pushing an existing repository. Follow these commands in your terminal:

```bash
# Replace the URL with your repository URL
git remote add origin https://github.com/YOUR-USERNAME/employee-dashboard.git
git branch -M main
git push -u origin main
```

## Step 3: Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Accept the terms and conditions

## Step 4: Deploy Your Dashboard

1. Once signed in to Streamlit Cloud, click on "New app"
2. Select your GitHub repository, branch (main), and the main file path (app.py)
3. Click "Deploy"

Your app will now be deployed and accessible via a URL like: `https://YOUR-USERNAME-employee-dashboard-app-RANDOM.streamlit.app`

## Step 5: Configure Advanced Settings (Optional)

You can configure additional settings for your app:

1. Go to your app on Streamlit Cloud
2. Click on the three dots (⋮) in the top-right corner of your app
3. Select "Settings"
4. Here you can configure:
   - App name
   - Python version
   - Package dependencies (these are automatically detected from your requirements.txt)
   - Secrets (for sensitive information like API keys)

## Sharing Your Dashboard

Once deployed, you can share your dashboard with anyone by sending them the URL. They can access it from any device with an internet connection.

## Updating Your Dashboard

When you want to update your dashboard:

1. Make changes to your code locally
2. Commit the changes to Git:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
3. Push the changes to GitHub:
   ```bash
   git push
   ```
4. Streamlit Cloud will automatically detect the changes and redeploy your app

## Troubleshooting

If you encounter any issues during deployment:

1. Check the logs in Streamlit Cloud
2. Ensure all dependencies are listed in requirements.txt
3. Make sure your app runs locally without errors
4. Verify that your GitHub repository is accessible to Streamlit Cloud

For more information, visit the [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-cloud).
