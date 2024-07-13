import requests
import re

def frames_text_to_tokens_text(text):
  tokens = [token for line in text.split('\n') for token in line.split(' ')]
  unique_tokens = list()
  seen_tokens = set()
  for token in tokens:
    if token == '': continue
    if token in seen_tokens: continue
    unique_tokens.append(token)
  result_text = ' '.join(unique_tokens)
  return result_text

def create_text_assistant(ollama_url_api, from_model='llama3:8b'):
  dest_model_name = f'{from_model}-text-assistant'
  url = f"{ollama_url_api}/create"
  payload = {
    'name': dest_model_name,
    "modelfile": f"FROM {from_model}\nSYSTEM Ты ассистент по обработке текста. Ты отвечаешь в формате 'Обработанный текст: <text>'. Отвечаешь на русском языке. Твоя основная задача убрать непонятные слова из текста. Исправить слова с ошибками. Убрать символы, которые мешают читабельности текста. В твоем ответе должен быть только 'Обработанный текст: <text>' и ничего больше. Если ты не можешь обработать текст, то отвечай 'Обработанный текст: пусто'. Если ты ответишь что-то кроме обработанного текста, то программа не сработает, все сломается. ОЧЕНЬ ВАЖНО ОТВЕЧАТЬ ТОЛЬКО ОБРАБОТАННЫЙ ТЕКСТ ПО ШАБЛОНУ 'Обработанный текст: <text>' или 'Обработанный текст: пусто'."
  }
  response = requests.post(url, json=payload)
  print('Status code', response.status_code)
  print(response.text)
  return dest_model_name

def load_model(ollama_url_api, model_name_to_load='llama3:8b-text-assistant'):
  url = f"{ollama_url_api}/generate" 
  payload = {
    'model': model_name_to_load,
  }
  response = requests.post(url, json=payload)
  print('Load model response', response.status_code)

def model_query(prompt, ollama_url_api, model_name='llama3:8b-text-assistant'):
  url = f"{ollama_url_api}/generate" 
  options = {
    'seed': 444,
    'temperature': 0,
  }
  payload = {
    'model': model_name,
    'prompt': prompt,
    'options': options,
    'stream': False,
  }
  response = requests.post(url, json=payload)
  response_text = response.json()
  return response_text['response']

def proc_model_response(model_response):
  model_response = model_response.lower()
  if 'пусто' in model_response: return ''
  model_response = model_response.replace('обработанный текст:', '')
  model_response = re.compile(r"[^\w\s\-\.,;:?!]").sub('', model_response)
  model_response = frames_text_to_tokens_text(model_response)
  return model_response

def proc_text_llama3_8b(text, create_text_assistant_model=False, load_model_to_memory=True):
  ollama_url_api = "http://localhost:11434/api"
  src_model_name = 'llama3:8b'
  text_assistant_model_name = 'llama3:8b-text-assistant'
  if create_text_assistant_model:
    create_text_assistant(ollama_url_api, src_model_name)
  if load_model_to_memory:
    load_model(ollama_url_api, text_assistant_model_name)
  prompt = f"Текст который ты должен обработать: {text}"
  response = model_query(prompt, ollama_url_api, text_assistant_model_name)
  result = proc_model_response(response)
  return result

if __name__ == '__main__':
  from pprint import pprint
  from .junk.legacy._legacy_gen_prompt_test_dataset import read_random_15_results
  res = read_random_15_results()
  for video_filepath, video_text in res.items():
    print('*' * 50)
    text = '\n'.join(video_text.values())
    tokens_text = frames_text_to_tokens_text(text)
    result = proc_text_llama3_8b(tokens_text)
    print(repr(result))
    print()
    print('*' * 50)

