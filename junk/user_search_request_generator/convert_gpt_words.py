from from_yappy_hackaton_2024_400k_csv import save_csv, read_csv 
import glob

def read(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    return f.read()

def convert_gpt_words(filepath):
  results_filepath = glob.glob('result_batch_*')
  result = set()
  for filepath in results_filepath:
    file_str = read(filepath)
    file_str = file_str.replace(',', '').replace('-', '').replace('->', '').replace('\n', ' ')
    proc = {word.lower() for word in file_str.split() if word !='' and len(word) >= 3}
    print(f'{len(proc)=}')
    result.update(proc)
  print(f'{len(result)=}')
  save_csv(result, 'gpt_final_union_search_requests.csv')
  
if __name__ == '__main__':
  convert_gpt_words(0)
