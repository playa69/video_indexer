from tasks import video_2_text
from core.video_transcribe import load_whisper

video_2_text.load_clip()
load_whisper()

# Used only in Dockerfile
# Load models on docker build stage
