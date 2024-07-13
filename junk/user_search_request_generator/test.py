import requests
import json
import concurrent.futures
import csv

def get_autocompleted_words(query, depth=1, lang='ru'):
  if depth == 0:
      return
  response = requests.get('https://clients1.google.ru/complete/search', params={
    'client': 'hp',
    'hl': lang,
    'q': query
  })
  print(response.status_code)
  response = response.text

  data = response[response.index('(') + 1:-1]
  o = json.loads(data)
  for result in o[1]:
    suggestion = result[0].replace('<b>', '').replace('</b>', '')
    if depth == 1:
      yield suggestion
    if depth > 1:
      for s in get_autocompleted_words(suggestion, depth - 1, lang):
        yield s

def get_autocompleted_words_to_list(*args, **kwargs):
  result = list(get_autocompleted_words(*args, **kwargs))
  return result

def generate_words_to_autocomplete():
  searches = list()
  with open('user_search_examples.csv', 'r', encoding='utf-8')as file:
    reader = csv.reader(file)
    for row in reader:
      searches.extend(row) 
  searches_words = list({w for w in [x for srch in searches for x in srch.split(' ') if len(x)>2]})
  return searches, searches_words

def save_result(data, filepath):
  with open(filepath, 'w', encoding='utf-8')as file:
    writer = csv.writer(file)
    for row in data:
      writer.writerow((row,)) 

def test_result():
  import glob
  def read_one_csv(filepath):
    result = list()
    with open(filepath, 'r', encoding='utf-8')as file:
      reader = csv.reader(file)
      for row in reader:
        result.extend(row) 
    return result
  result = list()
  for filepath in glob.glob('result*'):
    print(filepath)
    result.extend(read_one_csv(filepath))
  print(len(result))
  print(len(set(result)))
  res = set(result)
  save_result(res, 'final_20k.csv')

def fetch_words(words):
  result = list()
  with concurrent.futures.ThreadPoolExecutor() as executor:
    jobs = {
      executor.submit(get_autocompleted_words_to_list, word, depth=2): word
      for word in words
    }
    for done_job in concurrent.futures.as_completed(jobs):
      try:
        job_result = done_job.result()
        result.extend(job_result)
      except Exception as error:
        raise error
        print(error)
  return result

def main():
  import time
  init_searches, words = generate_words_to_autocomplete()
  print(f'{len(words)=}')
  #words = words[:50]
  n = 7
  batched_words = [words[i:i+n] for i in range(0, len(words), n)]
  result = init_searches
  for n, words_batch in enumerate(batched_words):
    result.extend(fetch_words(words_batch))
    time.sleep(2)
    save_result(result, f'result_{n}.csv')

if __name__ == '__main__':
  #main()
  test_result()
