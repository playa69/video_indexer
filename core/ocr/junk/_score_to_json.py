import glob

def save_to_json(data, filepath):
  import json
  with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

def read_json(filepath):
  import json
  with open(filepath, 'r') as f:
    data = json.load(f)
  return data

def read_file_text(filepath):
  with open(filepath, 'r') as f:
    data = f.read()
  return data

def collect_text_to_json():
  text_from_video_files = glob.glob('text_from_video_score/*.txt')
  result = dict()
  for filepath in text_from_video_files:
    #print(filepath)
    _file = filepath.split('/')[-1]
    video_original_url = 'https://cdn-st.rutubelist.ru/media/' + _file.replace('_', '/').replace('.txt', '.mp4')
    #print(video_original_url)
    file_text = read_file_text(filepath)
    result[video_original_url] = file_text
    #print(file_text)
    #print()
  save_to_json(result, 'score_text_from_videos.json')
  print(len(result))

collect_text_to_json()
#print(read_file_text('score_text_from_videos.json'))
