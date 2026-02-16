# AI Blog Article Generator 🤖✍️

An intelligent web application that automatically converts YouTube videos into well-structured blog articles using AI. Simply paste a YouTube link, and the application will download the audio, transcribe it, and generate a professional blog post.

![Django](https://img.shields.io/badge/Django-6.0.2-green)
![Python](https://img.shields.io/badge/Python-3.12.10-blue)
![Node.js](https://img.shields.io/badge/Node.js-20.11.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

## ✨ Features

- 🎥 **YouTube Video Processing**: Extract audio from any YouTube video
- 🎤 **Audio Transcription**: Accurate transcription using AssemblyAI
- 📝 **AI Blog Generation**: Convert transcripts to well-structured blog articles using Puter.js AI (500+ models available)
- 👤 **User Authentication**: Secure login and signup system
- 📚 **Blog Management**: View and manage your generated blog posts
- 💾 **Database Storage**: All blog posts are saved with PostgreSQL
- 🎨 **Responsive Design**: Clean and modern user interface

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Django 6.0.2 |
| Programming Language | Python 3.12.10 |
| Runtime | Node.js 20.11.0 |
| Database | PostgreSQL |
| AI Blog Generation | Puter.js (gpt-5-nano) |
| Audio Transcription | AssemblyAI |
| Audio Processing | yt-dlp + FFmpeg |
| Web Server | Gunicorn |
| Static Files | WhiteNoise |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12.10 or higher
- Node.js 20.11.0 or higher
- PostgreSQL
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aditibhatt04/ai_blog_article_generator.git
cd ai_blog_article_generator
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Node.js Dependencies

```bash
npm install
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_blog_db
# Or use individual settings:
DB_NAME=ai_blog_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# API Keys
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
PUTER_AUTH_TOKEN=your-puter-auth-token
```

#### Getting API Keys:

1. **AssemblyAI API Key**:
   - Sign up at [AssemblyAI](https://www.assemblyai.com)
   - Free tier available
   - Copy your API key from the dashboard

2. **Puter Auth Token**:
   - Visit [Puter.com](https://puter.com)
   - Open browser DevTools (F12)
   - Go to Application/Storage → Local Storage
   - Find and copy the auth token
   - Or run: `node get_puter_token.js`

3. **Django Secret Key**:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

### 6. Set Up Database

```bash
# Create PostgreSQL database
createdb ai_blog_db

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 🎮 Usage

### Running Locally

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

### Using the Application

1. **Sign Up / Login**: Create an account or log in
2. **Generate Blog**: 
   - Paste a YouTube video URL
   - Click "Generate"
   - Wait for the AI to process (may take 2-5 minutes)
3. **View Blogs**: Browse your generated blog articles
4. **Blog Details**: Click on any blog to view the full content

## 📁 Project Structure

```
ai_blog_article_generator/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── package.json               # Node.js dependencies
├── Procfile                   # Deployment configuration
├── runtime.txt                # Python version for deployment
├── .nvmrc                     # Node.js version
├── puter_ai.js               # Puter.js AI integration
├── get_puter_token.js        # Helper to get Puter token
├── .env.example              # Environment variables template
├── ai_blog_app/              # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── blog_generator/           # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   └── admin.py             # Admin configuration
├── templates/                # HTML templates
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   ├── signup.html          # Signup page
│   ├── all-blogs.html       # Blog list
│   └── blog-details.html    # Blog detail view
├── staticfiles/             # Static files (CSS, JS, images)
├── media/                   # User uploaded files
└── db.sqlite3              # SQLite database (dev only)
```

## 🚢 Deployment

This application is ready for deployment on Railway. See detailed deployment guides:

- **[RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)** - Step-by-step deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre/post deployment tasks
- **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** - Production readiness status
- **[PUTER_SETUP.md](PUTER_SETUP.md)** - Puter.js integration guide

### Quick Deployment to Railway

1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Create new project → Deploy from GitHub
4. Add PostgreSQL database
5. Set environment variables
6. Deploy! 🚀

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `ASSEMBLYAI_API_KEY` | AssemblyAI API key | Yes |
| `PUTER_AUTH_TOKEN` | Puter.js authentication token | Yes |

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test blog_generator
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [ISC License](LICENSE).

## 👤 Author

**Aditi Bhatt**

- GitHub: [@aditibhatt04](https://github.com/aditibhatt04)

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Puter.js](https://puter.com) - AI integration
- [AssemblyAI](https://www.assemblyai.com) - Audio transcription
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [Railway](https://railway.app) - Hosting platform

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```bash
   # Install FFmpeg
   # Ubuntu/Debian:
   sudo apt-get install ffmpeg
   # macOS:
   brew install ffmpeg
   # Windows: Download from ffmpeg.org
   ```

2. **Database connection error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify database exists: `psql -l`

3. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. **Puter.js authentication error**
   - Verify `PUTER_AUTH_TOKEN` is set correctly
   - Token may have expired, get a new one
   - Check `PUTER_SETUP.md` for details

5. **AssemblyAI transcription fails**
   - Check API key is valid
   - Ensure you have credits in your AssemblyAI account
   - Check internet connection

## 📞 Support

For support, please open an issue in the GitHub repository or contact the author.

## 🔄 Version History

- **1.0.0** (2026-02-16)
  - Initial release
  - YouTube to blog conversion
  - User authentication
  - Puter.js AI integration
  - Railway deployment ready

---

Made with ❤️ by Aditi Bhatt
