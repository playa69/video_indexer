import requests
import sys
from pprint import pprint
query = 'dogs' if len(sys.argv) == 1 else sys.argv[1]
payload = {'query': query}
response = requests.get('http://176.109.105.121/api/search', params=payload)
print(response)
print(response.url)
print('Response time seconds', response.elapsed.total_seconds())
pprint(response.json())

