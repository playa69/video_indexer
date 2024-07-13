import requests

model = 'llama3:8b'

def load_model():
  url = "http://localhost:11434/api/generate"
  payload = {
    'model': model,
  }
  response = requests.post(url, json=payload)
  print('Load model response', response.status_code)

def query(prompt):
  url = "http://localhost:11434/api/generate" 
  options = {
    'seed': 444,
    'temperature': 0,
  }
  payload = {
    'model': model,
    'prompt': prompt,
    'options': options,
    'stream': False,
  }
  response = requests.post(url, json=payload)
  response_text = response.json()
  '''
  print(response.url)
  print(response.status_code)
  from pprint import pprint
  del response_text['context']
  print(response_text['response'])
  '''
  return response_text['response']

def preproc_text(video_to_text):
  import re
  lines = video_to_text.values()
  unique_lines = list()
  seen_lines = set()
  for line in lines:
    if line in seen_lines: continue
    cleaned_line = re.sub(r'[^а-яА-Яa-zA-Z0-9\s.,!?-]', '', line)
    cleaned_line = ' '.join(cleaned_line.split())
    if cleaned_line == '': continue
    unique_lines.append(cleaned_line)
  result_text = '\n'.join(unique_lines)
  return result_text

def handle_text(video_to_text):
  proc_text = preproc_text(video_to_text)
  prompt = f"""
Ты ассистент по обработке текста с кадров видео. Твоя задача заключается в следующем:
1. Выделить только важную информацию из текста.
2. Исправить ошибки и удалить ненужные символы.
3. Перевести текст на русский язык, сохраняя названия чего-либо (например, имен собственных, торговых марок, терминов) на английском.
4. Вернуть результат на русском языке в читабельном виде.
5. Не добавлять никакой дополнительной информации, такой как "Вот ваш результат" или другие пояснения.

Вот текст для обработки:
{proc_text}
	"""
  print('*'*40, 'prompt', '*'*40)
  print(prompt)
  try:
    result = query(prompt)
    return result
  except Exception as error:
    print(error)

if __name__ == '__main__':
  from pprint import pprint
  from _gen_prompt_test_dataset import read_random_15_results
  load_model()
  res =  read_random_15_results()
  for video_filepath, video_text in res.items():
    print(repr(video_filepath))
    res = handle_text(video_text)
    print('*'*40, 'answer', '*'*40)
    print(res)
    print('\n' * 3)

