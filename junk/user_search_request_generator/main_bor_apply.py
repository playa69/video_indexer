import marisa_trie
import sys
import pickle

# marisa-trie==1.2.0
# python3.12

def read_bor(filepath):
  with open(filepath, 'rb') as f:
    loaded_trie = pickle.load(f)
    return loaded_trie

def bor_search(word):
  bor_filepath = 'gpt_google_final_20k_bor.pickle'
  trie = read_bor(bor_filepath)
  result = trie.keys(word)
  return result

if __name__ == '__main__':
  test_words = [
    'ban', 'роб', 'смо', 'как', 'что',
    'ham', 'кто', 'откуда', 'зачем', 'сколько', 'до', 'густо',
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
    'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
    'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
    'э', 'ю', 'я',
  ]
  for word in test_words:
    result = bor_search(word)
    result = [w for w in result[:8] if len(w) > 3]
    print(word, result)
