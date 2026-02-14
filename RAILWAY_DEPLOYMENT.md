# Railway Deployment Guide

Your Django project is now ready for production deployment! Follow these steps to deploy to Railway:

## Step 1: Add a .env file locally (for development)

Create a `.env` file in your project root with the environment variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.railway.app,www.yourdomain.railway.app
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
GOOGLE_API_KEY=your-google-api-key
```

**Note:** The .env file is already in .gitignore, so it won't be pushed to GitHub.

## Step 2: Initialize a Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: AI Blog Generator ready for production"
```

## Step 3: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (name it `ai-blog-article-generator`)
3. Do NOT initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 4: Push Your Code to GitHub

```bash
git remote add origin https://github.com/your-username/ai-blog-article-generator.git
git branch -M main
git push -u origin main
```

(Replace `your-username` with your actual GitHub username)

## Step 5: Deploy on Railway

1. Go to https://railway.app
2. Sign up or log in (you can use GitHub login)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your GitHub account
6. Select the `ai-blog-article-generator` repository
7. Railway will auto-detect the Django project

## Step 6: Configure Environment Variables in Railway

Once the project is connected to Railway:

1. Go to your project dashboard
2. Click on the web service (it should be created automatically)
3. Go to "Variables" tab
4. Add these environment variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generate a new secret key (use `python manage.py shell` then `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-domain.railway.app` (Railway will show you the domain) |
| `ASSEMBLYAI_API_KEY` | Your AssemblyAI API key from https://www.assemblyai.com |
| `GOOGLE_API_KEY` | Your Google Generative AI key from https://aistudio.google.com |

**Railway will automatically provide:**
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Port for the app

## Step 7: Configure PostgreSQL Database

1. In your Railway project, click "New"
2. Select "PostgreSQL"
3. Railway will create a PostgreSQL database and set the `DATABASE_URL` environment variable automatically

## Step 8: Run Migrations on Railway

After deployment, you need to run Django migrations on the production database:

1. In Railway dashboard, click on your web service
2. Go to "Deployments" tab
3. Click on the latest deployment
4. Go to "Logs" to see the deployment output

To run migrations manually:
1. Open Railway shell for your web service
2. Run: `python manage.py migrate`

Or add this to the Procfile to run migrations automatically before starting the server:

```
release: python manage.py migrate
web: gunicorn ai_blog_app.wsgi
```

## Step 9: Create a Superuser (Optional)

If you need admin access:

1. Open Railway shell for your web service
2. Run: `python manage.py createsuperuser`
3. Follow the prompts

## Files Already Created for Deployment

✅ **Procfile** - Tells Railway how to start your app
✅ **.gitignore** - Prevents sensitive files from being pushed
✅ **requirements.txt** - All Python dependencies
✅ **runtime.txt** - Python version specification
✅ **.env.example** - Template for environment variables

## What Each File Does

- **Procfile**: `web: gunicorn ai_blog_app.wsgi` - Starts the Gunicorn WSGI server
- **settings.py**: Updated to use environment variables and WhiteNoise for static files
- **views.py**: Updated to use environment variables for API keys
- **dj-database-url**: Allows Django to parse the DATABASE_URL from Railway

## Deployment Checklist

- [ ] Git repository created and code pushed
- [ ] Railway project created
- [ ] PostgreSQL database added to Railway
- [ ] Environment variables configured in Railway
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (optional)
- [ ] Test the deployed app

## Troubleshooting

### "Page not found" or 404 errors
- Make sure `ALLOWED_HOSTS` is set correctly to your Railway domain
- Check that DEBUG is set to False in production

### "Static files not loading"
- Run `collectstatic` locally and push to GitHub
- WhiteNoise middleware will serve them automatically

### Database errors
- Verify `DATABASE_URL` is set in Railway's Variables
- Check PostgreSQL service is running in Railway

### API errors
- Verify API keys are set correctly in Railway's Variables
- Check that AssemblyAI and Google API services are working

## Support

For Railway documentation: https://docs.railway.app
For Django deployment help: https://docs.djangoproject.com/en/4.1/howto/deployment/
