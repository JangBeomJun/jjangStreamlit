from openai import OpenAI
import yt_dlp
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os

def get_youtube_video_info(video_url):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download = False)
        video_id = video_info['id']
        title = video_info['title']
        upload_date = video_info['upload_date']
        channel = video_info['channel']
        duration = video_info['duration_string']
        
    return video_id, title, upload_date, channel, duration
def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]
    
    return video_id
def get_transcript_from_youtube(video_url, lang='en'):
    video_id = get_video_id(video_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=[lang])
    text_formatter = TextFormatter()
    text_formatted = text_formatter.format_transcript(transcript)
    
    return text_formatted
