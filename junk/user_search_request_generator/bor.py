from from_yappy_hackaton_2024_400k_csv import save_csv, read_csv 
import marisa_trie
import sys
import pickle

# marisa-trie==1.2.0
# python3.12

def create_bor(filepath):
  words = {row for (row,) in read_csv(filepath)}
  print(f'{len(words)=}')
  trie = marisa_trie.Trie(words)
  return trie

def save_bor(trie, filepath):
  # Сериализация три
  with open(filepath, 'wb') as f:
    pickle.dump(trie, f)

def read_bor(filepath):
  # Десериализация три
  with open(filepath, 'rb') as f:
    loaded_trie = pickle.load(f)
    return loaded_trie

def test():
  #trie, bor_filepath = create_bor('final_union_search_requests.csv'), 'google_yappy_hashtags_bor.pickle'
  #trie, bor_filepath = create_bor('gpt_final_union_search_requests.csv'), 'gpt_google_yappy_hashtags_bor.pickle'
  trie, bor_filepath = create_bor('gpt_final_union_search_requests_final_20k.csv'), 'gpt_google_final_20k_bor.pickle'
  #trie, bor_filepath = create_bor('final_20k.csv'), 'google_bor.pickle'
  #trie, bor_filepath = create_bor('final_union_search_requests_yappy_15k.csv'), 'google_yappy_top15k_hashtags_bor.pickle'
  print(f'{bor_filepath=}')
  save_bor(trie, bor_filepath)
  trie = read_bor(bor_filepath)
  test_words = [
    'ban', 'роб', 'смо', 'как', 'что',
    'ham', 'кто', 'откуда', 'зачем', 'сколько', 'до', 'густо',
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
    'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
    'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
    'э', 'ю', 'я',
  ]
  for word in test_words:
    result = trie.keys(word)
    result = [w for w in result[:8] if len(w) > 3]
    print(word, result)

if __name__ == '__main__':
  test()
