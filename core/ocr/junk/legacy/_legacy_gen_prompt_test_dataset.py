from video_to_text import video_to_text

def save_to_json(data, filepath):
  import json
  with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

def read_json(filepath):
  import json
  with open(filepath, 'r') as f:
    data = json.load(f)
  return data

def random_video_to_text_result():
  import glob, random
  from pprint import pprint
  videos_dir = 'videos'
  videos = glob.glob(f'{videos_dir}/*')
  video_filepath = random.choice(videos)
  print(f'{video_filepath=}')
  text = video_to_text(video_filepath, save_frames=False)
  pprint(text)
  return text, video_filepath

def gen_random_15_video_to_text_results():
  result = {
    video_filepath: result
    for result, video_filepath in (random_video_to_text_result() for i in range(15))
  }
  return result

def read_random_15_results():
  from pprint import pprint
  results = read_json('random_15_datasets.json')
  '''
  for k, v in results.items():
    print(k)
    pprint(v)
  '''
  return results

if __name__ == '__main__':
  '''
  random_15_datasets = gen_random_15_video_to_text_results()
  save_to_json(random_15_datasets, 'random_15_datasets.json')
  '''
  read_random_15_results()
  pass
  
