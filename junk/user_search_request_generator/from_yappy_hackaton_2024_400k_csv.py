import csv
from pprint import pprint
import re
from collections import Counter

def save_csv(data, filepath):
  with open(filepath, 'w', encoding='utf-8')as file:
    writer = csv.writer(file)
    for row in data:
      writer.writerow((row,)) 

def read_csv(filepath):
  result = list()
  with open(filepath, 'r', encoding='utf-8')as file:
    reader = csv.reader(file)
    for row in reader:
      yield row
      #result.extend(row) 
  #return result

def extract_hashtags(text):
  hashtags = re.findall(r'#\w+', text)
  return hashtags

def select_most_popular(hashtags, top=15_000):
  hashtags_cntr = Counter(hashtags) 
  print(f'{len(hashtags_cntr)=}')
  #pprint(hashtags_cntr.most_common(100))
  hashtags = [hashtag for hashtag, cnt in hashtags_cntr.most_common(100)]
  return hashtags

def main():
  rows = read_csv('yappy_hackaton_2024_400k.csv')
  #hashtags = set()
  hashtags = list()
  rows_cnt = 0
  for n, (url, desc) in enumerate(rows):
    rows_cnt += 1
    #hashtags.update(extract_hashtags(desc))
    hashtags.extend(extract_hashtags(desc))
  print(f'{len(hashtags)=}')
  print(f'{rows_cnt=}')
  hashtags = select_most_popular(hashtags, top=15_000)
  save_csv(hashtags, 'hashtags_from_yappy_top_15k.csv')

if __name__ == '__main__':
  main()
