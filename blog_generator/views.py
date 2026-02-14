from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import yt_dlp
import os
import assemblyai as aai
import google.generativeai as genai
from .models import BlogPost
import imageio_ffmpeg
import logging
import subprocess
import signal
from decouple import config

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            print(f"[DEBUG] Received YouTube link: {yt_link}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"[ERROR] Failed to parse request body: {str(e)}")
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        try:
            # get yt title
            print(f"[DEBUG] Getting YouTube title...")
            title = yt_title(yt_link)
            print(f"[DEBUG] Got title: {title}")
        except Exception as e:
            print(f"[ERROR] Failed to get YouTube title: {str(e)}")
            logger.error(f"Failed to get YouTube title: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Failed to get YouTube title: {str(e)}'}, status=500)

        try:
            # get transcript
            print(f"[DEBUG] Getting transcription (this may take several minutes)...")
            transcription = get_transcription(yt_link)
            print(f"[DEBUG] Got transcription (length: {len(transcription) if transcription else 0})")
            if not transcription:
                return JsonResponse({'error': "Failed to get transcript"}, status=500)
        except Exception as e:
            print(f"[ERROR] Failed to get transcription: {str(e)}")
            logger.error(f"Failed to get transcription: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Failed to get transcription: {str(e)}'}, status=500)

        try:
            # use OpenAI to generate the blog
            print(f"[DEBUG] Generating blog from transcription...")
            blog_content = generate_blog_from_transcription(transcription)
            print(f"[DEBUG] Generated blog (length: {len(blog_content) if blog_content else 0})")
            if not blog_content:
                return JsonResponse({'error': "Failed to generate blog article"}, status=500)
        except Exception as e:
            print(f"[ERROR] Failed to generate blog: {str(e)}")
            logger.error(f"Failed to generate blog: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Failed to generate blog: {str(e)}'}, status=500)

        try:
            # save blog article to database
            print(f"[DEBUG] Saving blog article to database...")
            new_blog_article = BlogPost.objects.create(
                user=request.user,
                youtube_title=title,
                youtube_link=yt_link,
                generated_content=blog_content,
            )
            new_blog_article.save()
            print(f"[DEBUG] Saved blog article with id: {new_blog_article.id}")
        except Exception as e:
            print(f"[ERROR] Failed to save blog article: {str(e)}")
            logger.error(f"Failed to save blog article: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Failed to save blog article: {str(e)}'}, status=500)

        # return blog article as a response
        print(f"[DEBUG] Returning success response")
        return JsonResponse({'content': blog_content, 'title': title})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def yt_title(link):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('title', 'Unknown Title')
    except Exception as e:
        raise Exception(f"Failed to get YouTube title: {str(e)}")

def download_audio(link):
    try:
        print(f"[DEBUG] download_audio() called with link: {link}")
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"[DEBUG] FFmpeg path: {ffmpeg_path}")
        print(f"[DEBUG] MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Ensure MEDIA_ROOT exists
        if not os.path.exists(settings.MEDIA_ROOT):
            print(f"[DEBUG] Creating MEDIA_ROOT directory: {settings.MEDIA_ROOT}")
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',  # Prefer m4a to avoid re-encoding
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Lower quality for faster processing
            }],
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s'),
            'quiet': False,
            'no_warnings': False,
            'ffmpeg_location': ffmpeg_path,
            'restrictfilenames': True,  # Restrict filenames to ASCII
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
        }
        
        print(f"[DEBUG] Starting download with yt-dlp (this may take 1-2 minutes)...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
        
        print(f"[DEBUG] Download complete, searching for MP3 file...")
        # Find the most recently created mp3 file in media folder
        mp3_files = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith('.mp3')]
        if mp3_files:
            # Get the most recently modified file
            audio_file = max([os.path.join(settings.MEDIA_ROOT, f) for f in mp3_files], 
                           key=os.path.getmtime)
            file_size = os.path.getsize(audio_file) / (1024 * 1024)  # Size in MB
            print(f"[DEBUG] Audio file found: {os.path.basename(audio_file)} ({file_size:.2f} MB)")
            return audio_file
        else:
            raise Exception("No MP3 file found after download")
            
    except Exception as e:
        print(f"[ERROR] download_audio failed: {str(e)}")
        logger.error(f"download_audio failed: {str(e)}", exc_info=True)
        raise Exception(f"Failed to download audio: {str(e)}")

def get_transcription(link):
    try:
        print(f"[DEBUG] download_audio() called")
        audio_file = download_audio(link)
        print(f"[DEBUG] Audio file downloaded: {audio_file}")
        
        # Verify audio file exists and has content
        if not os.path.exists(audio_file):
            raise Exception(f"Audio file not found: {audio_file}")
        
        file_size = os.path.getsize(audio_file)
        print(f"[DEBUG] Audio file size: {file_size / (1024*1024):.2f} MB")
        
        if file_size == 0:
            raise Exception("Audio file is empty")
        
        print(f"[DEBUG] Setting AssemblyAI API key")
        api_key = config('ASSEMBLYAI_API_KEY')
        if not api_key:
            raise Exception("ASSEMBLYAI_API_KEY environment variable not set")
        aai.settings.api_key = api_key
        print(f"[DEBUG] API Key set (first 10 chars): {api_key[:10]}...")
        
        transcriber = aai.Transcriber()
        
        print(f"[DEBUG] Starting transcription using AssemblyAI...")
        print(f"[DEBUG] Audio file: {audio_file}")
        
        # For the new AssemblyAI SDK, create config with speech_models
        config = aai.TranscriptionConfig(speech_models=["universal-2"])
        
        print(f"[DEBUG] Transcribing with config: {config}")
        
        # Transcribe using the config
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript is None:
            raise Exception("AssemblyAI returned None - API key may be invalid or account has no credits")
        
        # Log transcription response details
        print(f"[DEBUG] Transcription response type: {type(transcript)}")
        print(f"[DEBUG] Transcription object: {transcript}")
        
        if hasattr(transcript, 'status'):
            print(f"[DEBUG] Transcription status: {transcript.status}")
        
        if hasattr(transcript, 'error'):
            error = transcript.error
            print(f"[DEBUG] Transcription error attribute: {error}")
            if error:
                raise Exception(f"AssemblyAI API error: {error}")
        
        # Check for common error attributes
        for attr in ['error_message', 'message', 'error_code']:
            if hasattr(transcript, attr):
                val = getattr(transcript, attr)
                print(f"[DEBUG] {attr}: {val}")
                if val:
                    raise Exception(f"AssemblyAI {attr}: {val}")
        
        # Get the text
        text = transcript.text if hasattr(transcript, 'text') else str(transcript)
        
        print(f"[DEBUG] Raw transcript text length: {len(text) if text else 0}")
        print(f"[DEBUG] First 500 chars of transcript: {str(text)[:500]}")
        
        if not text or len(str(text).strip()) == 0:
            raise Exception(f"AssemblyAI returned empty/null text. Full response: {transcript}")
        
        print(f"[DEBUG] Transcription complete (length: {len(text)} characters)")
        return text
    except Exception as e:
        print(f"[ERROR] get_transcription failed: {str(e)}")
        logger.error(f"get_transcription failed: {str(e)}", exc_info=True)
        raise

def generate_blog_from_transcription(transcription):
    try:
        # Use Google Generative AI (Gemini) for blog generation
        google_api_key = config('GOOGLE_API_KEY')
        if not google_api_key:
            raise Exception("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=google_api_key)
        
        # Use the latest available model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""You are a professional blog writer. Convert the following YouTube video transcript into a well-structured, engaging blog article.

The article should have:
- A compelling introduction
- 3-4 main sections with relevant headers
- Clear paragraphs with good formatting
- A conclusion

Transcript:
{transcription}

Please generate a professional blog article."""
        
        print(f"[DEBUG] Calling Gemini API to generate blog...")
        response = model.generate_content(prompt)
        
        if response.text:
            generated_content = response.text
            print(f"[DEBUG] Blog article generated successfully (length: {len(generated_content)} characters)")
            return generated_content
        else:
            raise Exception("Gemini API returned empty response")
            
    except Exception as e:
        print(f"[ERROR] generate_blog_from_transcription failed: {str(e)}")
        logger.error(f"generate_blog_from_transcription failed: {str(e)}", exc_info=True)
        raise



def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message':error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'signup.html', {'error_message':error_message})
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
