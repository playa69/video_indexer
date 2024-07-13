import sys
import os
from core.ocr import download_videos
from core.ocr import video_to_text
from core.ocr import post_proc_text

import logging
import zoneinfo # added since python 3.9
import datetime

logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Moscow")).timetuple()
log_filepath = datetime.datetime.now().strftime('logs/log_%Y-%m-%d_%H-%M-%S.log')
handlers = [
  logging.FileHandler(log_filepath),
  logging.StreamHandler(),
]
logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
  handlers=handlers
)
logger = logging.getLogger(__name__)

def save_text_from_video(text, result_filepath):
  with open(result_filepath, 'wt', encoding='utf-8') as file:
    file.write(text)

def score_first_1000_videos():
  videos_url_src = sys.argv[1]      
  videos_dir = sys.argv[2]
  video_links_generator = download_videos.video_links_reader(videos_url_src)
  stop_number_of_videos = 1_000
  for video_num, row in enumerate(video_links_generator):
    logger.info(f'{video_num=}')
    if video_num == stop_number_of_videos: break
    video_url_src = row['link']
    _video_file = video_url_src.replace('https://cdn-st.rutubelist.ru/media', '').replace('/', '_').strip('_')
    video_filepath_dest = os.path.join(videos_dir, _video_file)
    logger.info(f'{video_url_src=}')
    logger.info(f'{video_filepath_dest=}')
    if os.path.exists(video_filepath_dest):
      logger.info(f'File exists {video_filepath_dest}')
    else:
      download_videos.download_video(video_url_src, video_filepath_dest)
    text_from_video_filepath_dest = video_filepath_dest.replace('.mp4', '.txt')
    logger.info(f'{text_from_video_filepath_dest=}')
    if os.path.exists(text_from_video_filepath_dest):
      logger.info(f'File exists {text_from_video_filepath_dest}')
    else:
      text_from_video = video_to_text.video_to_text(video_filepath_dest, save_frames=False)
      logger.info(f'{text_from_video=}')
      save_text_from_video(text_from_video, text_from_video_filepath_dest)

if __name__ == '__main__':
  post_proc_text.create_text_assistant("http://localhost:11434/api")
  score_first_1000_videos()

