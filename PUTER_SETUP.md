# Puter.js AI Integration Setup Guide

This project has been updated to use **Puter.js** for AI-powered blog generation instead of Google Gemini.

## What Changed

- **Replaced**: Google Generative AI (Gemini) → **Puter.js AI** 
- The app now uses Node.js to call Puter.js AI models
- All AI requests go through `puter_ai.js` script

## Setup Steps

### 1. Get Your Puter Auth Token

1. Go to [puter.com](https://puter.com)
2. Sign up or log in to your account
3. Open your browser's developer console (F12)
4. Go to **Application** tab → **Local Storage** → Select your Puter domain
5. Find and copy the `auth_token` value

### 2. Add the Token to Your Environment

Create or update your `.env` file in the project root:

```env
# Existing configuration
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
SECRET_KEY=your-django-secret-key

# NEW: Add your Puter auth token
PUTER_AUTH_TOKEN=your-puter-auth-token-here
```

### 3. Restart the Django Server

```bash
python manage.py runserver
```

## How It Works

```
User Request
    ↓
Django views.py
    ↓
Calls Node.js script (puter_ai.js)
    ↓
puter_ai.js uses Puter.js library
    ↓
Connects to Puter AI API with auth token
    ↓
Returns generated blog content
    ↓
Saved to database
```

## Available Models

Puter.js supports 500+ AI models. Currently configured to use `gpt-5-nano`, but you can change this in `puter_ai.js`:

```javascript
const response = await puter.ai.chat(prompt, {
    model: 'gpt-5-nano'  // Change this to any available model
});
```

### Popular Models:
- `gpt-5-nano` (fast, free tier friendly)
- `claude-opus` (Claude model)
- `gemini-2.0-flash-lite` (Google Gemini)
- `deepseek-v3` (DeepSeek model)
- See all: https://developer.puter.com/ai/models/

## Troubleshooting

### Error: "PUTER_AUTH_TOKEN environment variable not set"
- Make sure you've added `PUTER_AUTH_TOKEN` to your `.env` file
- Restart the Django server after updating `.env`

### Error: "Node.js script failed"
- Ensure Node.js is installed: `node --version`
- Check that `puter_ai.js` exists in the project root
- Run `npm install` to ensure all dependencies are installed

### Error: "Puter.js returned empty response"
- Check your internet connection
- Verify your auth token is valid
- Check if your Puter account has AI credits remaining

## Project Files

- `puter_ai.js` - Node.js script that interfaces with Puter.js
- `blog_generator/views.py` - Updated to call puter_ai.js
- `package.json` - Node.js dependencies (includes @heyputer/puter.js)
- `.env.example` - Example environment variables

## Learning Resources

- [Puter.js Documentation](https://docs.puter.com/)
- [AI API Guide](https://docs.puter.com/AI/)
- [Available Models](https://developer.puter.com/ai/models/)
