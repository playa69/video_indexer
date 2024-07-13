from from_yappy_hackaton_2024_400k_csv import save_csv, read_csv 

def join_csv(src_csv, dest_filepath):
  result = set()
  for filepath in src_csv:
    for (row,) in read_csv(filepath):
      row = row.replace('#','')
      row = [w for w in row.split(' ') if len(w) > 3]
      #result.add(row)
      result.update(row)
  save_csv(result, dest_filepath)

if __name__ == '__main__':
  #csv_to_join = ['final_20k.csv', 'hashtags_from_yappy_top_15k.csv']
  #join_csv(csv_to_join, 'final_union_search_requests_yappy_15k.csv')

  #csv_to_join = ['final_20k.csv', 'hashtags_from_yappy.csv']
  #join_csv(csv_to_join, 'final_union_search_requests.csv')

  csv_to_join = ['final_20k.csv', 'gpt_final_union_search_requests.csv']
  join_csv(csv_to_join, 'gpt_final_union_search_requests_final_20k.csv')
