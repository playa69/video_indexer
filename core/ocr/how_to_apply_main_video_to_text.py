from . import main_video_to_text as video_to_text
import sys

input_video_filepath = sys.argv[1]
text_from_video = video_to_text.video_to_text(input_video_filepath, save_frames=False)
print(text_from_video)

