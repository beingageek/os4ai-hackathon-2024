import requests
import json

# Get your API key from https://www.rainforestapi.com
params = {
    'api_key': '',
    'amazon_domain': 'amazon.com',
    'category_id': '3760931',
    'type': 'search',
    'search_term': 'toothpaste',
    'max_page': 5
}

# make the http GET request to Rainforest API
api_result = requests.get('https://api.rainforestapi.com/request', params)

# print the JSON response from Rainforest API
print(json.dumps(api_result.json()))

with open('data/amazon_search_results.json', 'w') as f:
    json.dump(api_result.json(), f)