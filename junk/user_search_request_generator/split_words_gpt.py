import requests
import concurrent.futures
import os 
import json
from from_yappy_hackaton_2024_400k_csv import save_csv, read_csv 
import time
import datetime

EDENAI_TOKEN = os.getenv("EDENAI_TOKEN")

def chat(promt):
    headers = {"Authorization": f"Bearer {EDENAI_TOKEN}"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": promt,
        "chatbot_global_action": '''Ты бот-помощник! Твоя задача разделить слова, которые написаны слитно. Например "запеченнаятыква" это "запеченная тыква". Учитывай, что не все слова написаны слитно, некоторые раздельно и их трогать не надо. Выдай в ответ список сиправленных слов.''',
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 2000,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']

def join_batch(batch):
  return ' '.join(batch)

def proc_batch_of_batch(batch_of_batch):
  result = list()
  with concurrent.futures.ThreadPoolExecutor() as executor:
    jobs = {
      executor.submit(chat, join_batch(batch)): batch
      for batch in batch_of_batch
    }
    for done_job in concurrent.futures.as_completed(jobs):
      try:
        job_result = done_job.result()
        result.append(job_result)
      except Exception as error:
        raise error
        print(error)
  return result

def save_result(result, filepath):
  with open(filepath, 'w', encoding='utf-8') as file:
    file.write(result)

def main():
  filepath = 'final_union_search_requests.csv'
  words = list({row for (row,) in read_csv(filepath)})
  print(f'{len(words)=}')
  n_batch = 700
  batches = [words[i:i+n_batch] for i in range(0, len(words), n_batch)]
  print(f'{len(batches)=}')
  n_batch_batch = 5
  batches_of_batches = [batches[i:i+n_batch_batch] for i in range(0, len(batches), n_batch_batch)]
  print(f'{len(batches_of_batches)=}')
  for n, batch_of_batch in enumerate(batches_of_batches):
    print(n, datetime.datetime.now())
    result = proc_batch_of_batch(batch_of_batch) 
    save_result(join_batch(result), f'result_batch_{n}.txt')
    time.sleep(3)

if __name__ == '__main__':
  main()

