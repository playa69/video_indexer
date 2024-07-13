'''
Input:
  - Video memory object descriptor / file
  - Frames freq 10/20/100 etc
Output:
  - Text from video
'''

import cv2
from core.ocr import split_video_on_frames as m_split_video_on_frames
from core.ocr import image_to_text
from core.ocr import post_proc_text

def read_video_from_file(vid_filepath):
  return cv2.VideoCapture(vid_filepath)

def split_video_on_frames(video, num_frames=10):
  return m_split_video_on_frames.video_to_frames(video, num_frames=num_frames)

def frames_to_text(frames, batched_proc):
  if batched_proc:
    frames_offset = [int(frame_offset) for frame, frame_offset in frames]
    frames = [frame for frame, frame_offset in frames]
    return dict(zip(frames_offset, image_to_text.list_images_to_text(frames)))
  result = {
    int(frame_offset): image_to_text.image_to_text(frame)
    for frame, frame_offset in frames
  }
  return result

def video_to_text(video_filepath, batched_proc=True, save_frames=False):
  video = read_video_from_file(video_filepath)
  frames = split_video_on_frames(video, num_frames=7) # 15
  if save_frames:
    frames_dest_base_path = video_filepath.split('/')[-1].replace('.mp4', '')
    m_split_video_on_frames.save_frames(frames, frames_dest_base_path)
  frames_text = frames_to_text(frames, batched_proc)
  tokens_text = post_proc_text.frames_text_to_tokens_text('\n'.join(frames_text.values()))
  try:
    model_handled_text = post_proc_text.proc_text_llama3_8b(tokens_text)
  except Exception as error:
    print(error)
    return tokens_text
  return model_handled_text

if __name__ == '__main__':
  import sys, os
  from pprint import pprint
  # Single video handler
  '''
  video_filepath = sys.argv[1]
  print(f'{video_filepath=}')
  #text = video_to_text(video_filepath, batched_proc=False)
  text = video_to_text(video_filepath, save_frames=True)
  pprint(text)
  '''
  # Walk through videos
  '''
  videos_dir = sys.argv[1]
  for root, dirs, files in os.walk(videos_dir, topdown=False):
    for n, file in enumerate(files):
      if n == 10: break
      video_filepath = os.path.join(root, file)
      print(video_filepath)
      text = video_to_text(video_filepath, save_frames=False)
      pprint(text)
      print()
  '''
  # Random video
  import glob, random
  videos_dir = sys.argv[1]
  videos = glob.glob(f'{videos_dir}/*')
  video_filepath = random.choice(videos)
  print(f'{video_filepath=}')
  text = video_to_text(video_filepath, save_frames=False)
  pprint(text)
