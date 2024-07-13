import whisper

model_whisper = None
def load_whisper():
  global model_whisper
  if model_whisper is None:
    model_whisper = whisper.load_model("large")

def transcribe_video(video_path):
  global model_whisper
  load_whisper()
  return model_whisper.transcribe(video_path)["text"]


