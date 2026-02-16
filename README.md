# AI Blog Article Generator

An intelligent Django application that automatically generates professional blog articles from YouTube videos using AI. Simply paste a YouTube link, and the app will download the video, transcribe the audio, and generate a well-structured blog article using AI.

## ✨ Features

- 🎥 **YouTube Integration** - Download and process YouTube videos
- 🎤 **Audio Transcription** - Convert video audio to text using AssemblyAI
- 🤖 **AI Blog Generation** - Generate professional blog articles using Puter.js (500+ AI models available)
- 👤 **User Authentication** - Secure user registration and login
- 📚 **Blog Management** - View, manage, and organize generated blogs
- 🗄️ **PostgreSQL Database** - Scalable data persistence
- 🚀 **Production Ready** - Configured for Railway deployment

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 6.0.2 |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | PostgreSQL |
| **AI Integration** | Puter.js (500+ models via single API) |
| **Transcription** | AssemblyAI |
| **Audio Processing** | yt-dlp + FFmpeg |
| **Node.js** | 20.11.0 (for Puter.js integration) |
| **Server** | Gunicorn |
| **Hosting** | Railway |
| **Python** | 3.12.10 |

## 🚀 Quick Start

### Local Development

#### 1. Clone the Repository
```bash
git clone https://github.com/aditibhatt04/ai_blog_article_generator.git
cd ai_blog_article_generator
```

#### 2. Create Environment File
```bash
cp .env.example .env
```

Fill in the `.env` file with:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
PUTER_AUTH_TOKEN=your-puter-auth-token
```

#### 3. Install Dependencies

**Python:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**Node.js:**
```bash
npm install
```

#### 4. Setup Database
```bash
python manage.py migrate
```

#### 5. Create Superuser
```bash
python manage.py createsuperuser
```

#### 6. Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## 🔑 Getting API Keys

### Puter Auth Token (Free)
1. Go to https://puter.com
2. Log in to your account
3. Open DevTools (F12) → Application → Local Storage
4. Find `auth_token` and copy it
5. Add to `.env` as `PUTER_AUTH_TOKEN`

**Or use the helper script:**
```bash
node get_puter_token.js
```

### AssemblyAI API Key (Free Tier Available)
1. Go to https://www.assemblyai.com
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env` as `ASSEMBLYAI_API_KEY`

## 📖 How It Works

```
User Input (YouTube URL)
    ↓
Django Backend (views.py)
    ↓
yt-dlp: Download audio from YouTube
    ↓
FFmpeg: Convert to MP3
    ↓
AssemblyAI: Transcribe audio to text
    ↓
Node.js Script (puter_ai.js)
    ↓
Puter.js: Generate blog using AI (500+ models available)
    ↓
Django: Save blog to PostgreSQL
    ↓
Frontend: Display generated blog
```

## 🎯 Available AI Models (via Puter.js)

Puter.js provides access to 500+ AI models including:
- **OpenAI**: GPT-5-nano, GPT-5, o3-mini
- **Claude**: Claude 3 Opus, Sonnet, Haiku
- **Google**: Gemini 2.0 Flash, Gemini 1.5
- **DeepSeek**: DeepSeek v3
- **Meta**: Llama 3.1
- **Mistral**: Large, Medium, Small
- And many more...

Configure in `puter_ai.js`:
```javascript
const response = await puter.ai.chat(prompt, {
    model: 'gpt-5-nano'  // Change model here
});
```

## 📁 Project Structure

```
ai_blog_article_generator/
├── manage.py                  # Django management
├── Procfile                  # Railway deployment config
├── runtime.txt              # Python version
├── .nvmrc                   # Node.js version
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
├── puter_ai.js             # Puter.js AI integration
├── ai_blog_app/            # Django project config
│   ├── settings.py         # Production-ready settings
│   ├── urls.py
│   └── wsgi.py
├── blog_generator/         # Main Django app
│   ├── views.py           # API endpoints
│   ├── models.py          # Database models
│   └── urls.py
├── templates/             # HTML templates
└── DEPLOYMENT_READY.md    # Deployment guide
```

## 🌐 Deployment on Railway

### Prerequisites
- GitHub account
- Railway account (free at railway.app)
- Environment variables ready (see below)

### Step-by-Step Deployment

1. **Get Required Variables**
   - `SECRET_KEY`: Generate with `python manage.py shell` then run:
     ```python
     from django.core.management.utils import get_random_secret_key
     print(get_random_secret_key())
     ```
   - `PUTER_AUTH_TOKEN`: From https://puter.com
   - `ASSEMBLYAI_API_KEY`: From https://www.assemblyai.com

2. **Deploy on Railway**
   - Go to https://railway.app
   - Create new project → Deploy from GitHub
   - Select `ai_blog_article_generator`
   - Railway auto-detects Django + Node.js

3. **Configure Environment Variables**
   - In Railway dashboard, add variables:
     - `SECRET_KEY`
     - `DEBUG=False`
     - `ALLOWED_HOSTS=your-domain.railway.app`
     - `ASSEMBLYAI_API_KEY`
     - `PUTER_AUTH_TOKEN`

4. **Add PostgreSQL Database**
   - Railway → New → PostgreSQL
   - `DATABASE_URL` auto-sets

5. **Deploy!**
   - Railway handles:
     - `npm install` (Node.js deps)
     - `python manage.py migrate` (Database setup)
     - Starting Gunicorn server

For detailed instructions, see [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)

## 🔒 Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `SECRET_KEY` | Django secret key | Generate with Django |
| `DEBUG` | Debug mode (False in production) | Set to False |
| `ALLOWED_HOSTS` | Allowed domain(s) | Your domain |
| `ASSEMBLYAI_API_KEY` | Transcription API key | https://assemblyai.com |
| `PUTER_AUTH_TOKEN` | Puter.js auth token | https://puter.com |
| `DATABASE_URL` | PostgreSQL connection | Auto-set by Railway |

## 📝 Usage

### Generate Blog from YouTube

1. **Sign up/Login** at http://yourapp.com
2. **Paste YouTube URL** in the input field
3. **Click Generate**
4. **Wait** (1-3 minutes depending on video length)
5. **View** your generated blog

### View Generated Blogs

- Go to "All Blogs" to see your blog history
- Click on any blog to view full details
- Delete blogs you no longer need

## 🐛 Troubleshooting

### "PUTER_AUTH_TOKEN not found"
- Make sure `.env` file exists with the token
- Restart the server after adding env vars
- Verify token format (should be JWT-like)

### "AssemblyAI error"
- Check API key is correct
- Verify your AssemblyAI account has credits
- Check internet connection for API calls

### "Database connection error"
- In production: Railway should auto-set `DATABASE_URL`
- Locally: Ensure PostgreSQL is running
- Check connection string in `settings.py`

### "Node.js script not found"
- Verify `puter_ai.js` exists in project root
- Run `npm install` to ensure dependencies
- Check that `node` is in PATH

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙏 Credits

- **Original Project**: Tomi Tokko, Oluwatomi Tokko
- **Puter.js Enhancement**: aditibhatt04 (2026)
- **AI Models**: OpenAI, Anthropic, Google, Meta, and others via Puter.js
- **Transcription**: AssemblyAI
- **Audio Processing**: yt-dlp, FFmpeg

## 📧 Support

For issues, questions, or suggestions:
- GitHub Issues: https://github.com/aditibhatt04/ai_blog_article_generator/issues
- Documentation: See `DEPLOYMENT_READY.md` and `PUTER_SETUP.md`

---

**Status**: ✅ Production Ready | 🚀 Ready for Deployment

**Last Updated**: February 16, 2026
