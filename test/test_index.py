index_data = [
	['https://cdn-st.rutubelist.ru/media/bf/6a/f040f0dd4afc90b8eb12c8d76571/fhd.mp4', ''],
 	['https://cdn-st.rutubelist.ru/media/73/48/47a9e25b4b36bc6254d29f42787a/fhd.mp4', '#boobs , #bigass , #girls , #pussy , #еда , #готовка , #рецепт , #кукинг , #мистика , #страшилка , #horror , #бизнес , #инвестиции'],
	['https://cdn-st.rutubelist.ru/media/fe/86/ab9d0a504c2a892c88dc02b79b56/fhd.mp4', '#путешествия #journey #туризм #обучениезаграницей #языковаяшкола'],
]

import requests
def index(url, description):
  try:
    payload = {'link': url, 'description': description}
    response = requests.post('http://176.109.105.121/api/index', json=payload)
    print(response.url)
    print(response)
    print(response.text)
  except Exception as error:
    print(error)

import random
url, desc = random.choice(index_data)
index(url, desc)
