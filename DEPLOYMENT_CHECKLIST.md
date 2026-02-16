# Deployment Checklist

Complete these steps before deploying to production:

## Pre-Deployment

- [ ] **Get Puter Auth Token**
  - Go to https://puter.com
  - Log in to your account
  - Open DevTools (F12) → Application → Local Storage
  - Find your `auth_token` and copy it

- [ ] **Get AssemblyAI API Key**
  - Go to https://www.assemblyai.com
  - Sign up and get your free tier API key

- [ ] **Generate Django Secret Key**
  ```bash
  python manage.py shell
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
  - Copy the output

- [ ] **Test Locally**
  ```bash
  python manage.py runserver
  ```
  - Try generating a blog from a YouTube video
  - Verify the Puter.js AI integration works

- [ ] **Update .env with all required variables**
  ```
  SECRET_KEY=<your-generated-key>
  DEBUG=False
  ALLOWED_HOSTS=yourdomain.railway.app
  ASSEMBLYAI_API_KEY=<your-assemblyai-key>
  PUTER_AUTH_TOKEN=<your-puter-token>
  ```

## Deployment Steps

- [ ] **Initialize Git (if not done)**
  ```bash
  git init
  git add .
  git commit -m "Ready for production deployment"
  ```

- [ ] **Push to GitHub**
  ```bash
  git remote add origin https://github.com/your-username/ai-blog-article-generator.git
  git branch -M main
  git push -u origin main
  ```

- [ ] **Deploy on Railway**
  1. Go to https://railway.app
  2. Create a new project from GitHub
  3. Select your repository
  4. Railway will auto-detect Python + Node.js

- [ ] **Configure Environment Variables in Railway**
  - Set all variables from the Pre-Deployment checklist

- [ ] **Add PostgreSQL Database**
  1. In Railway dashboard → New → PostgreSQL
  2. DATABASE_URL will be auto-set

- [ ] **Verify Deployment**
  - Check Railway logs for any errors
  - Visit your deployed URL
  - Try generating a blog article

## Post-Deployment

- [ ] **Monitor Logs**
  ```
  Railway Dashboard → Logs
  ```

- [ ] **Test All Features**
  - User registration
  - User login
  - Blog generation from YouTube
  - Blog list viewing
  - Blog details viewing

- [ ] **Set up Custom Domain (Optional)**
  - Railway → Settings → Domain
  - Add your custom domain

## Troubleshooting

### "npm: command not found"
- Railway needs Node.js buildpack
- Check that `.nvmrc` file exists in project root with Node.js version

### "Puter auth token error"
- Verify `PUTER_AUTH_TOKEN` is set in Railway environment variables
- Get a fresh token from https://puter.com

### "AssemblyAI error"
- Verify `ASSEMBLYAI_API_KEY` is set correctly
- Check that your AssemblyAI account has credits

### "Database connection error"
- Verify PostgreSQL is added to Railway project
- Check that `DATABASE_URL` is auto-set

## Technology Stack

- **Backend**: Django 6.0.2 (Python 3.12)
- **Frontend**: HTML/CSS/JavaScript
- **Database**: PostgreSQL
- **AI Integration**: 
  - Puter.js (Blog Generation) - 500+ AI models available
  - AssemblyAI (Transcription)
- **Audio**: yt-dlp + FFmpeg
- **Hosting**: Railway

## Project Files

- `Procfile` - Railway deployment config (runs npm install + Django migrations)
- `.nvmrc` - Node.js version (20.11.0)
- `runtime.txt` - Python version (3.12.10)
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `puter_ai.js` - Node.js script for Puter.js AI calls
- `.env.example` - Environment variables template
