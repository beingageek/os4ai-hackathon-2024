import google.generativeai as genai
import pandas as pd
from typing_extensions import TypedDict

GOOGLE_API_KEY = ''

with open('data/amazon_search_results.json') as f:
    res_data = f.read()

import json
data = json.loads(res_data)

price_list = []
brands = ["Colgate", "Crest", "Sensodyne", "Tom's", "Arm & Hammer",
          "Whole Foods Market", "Hello", "Dr. Sheffield", "Marvis",
          "SEAGO", "COSLUS", "Boka", "PerioSciences", "Cocofloss", "Lumineux", "Coconut"]

for item in data['search_results']:
    title = item['title']
    item_brand = "--"
    for brand in brands:
        if brand in title:
            item_brand = brand
            break
    rating = "na"
    if 'rating' in item:
        rating = item['rating']
    rating_count = "na"
    if 'ratings_total' in item:
        rating_count = item['ratings_total']
    price = item['price']['raw']
    unit_price = "--"
    if 'list_price' in item['price']:
        unit_price = item['price']['list_price']
    recent_sales = 0
    if 'recent_sales' in item:
        recent_sales = item['recent_sales']
        recent_sales = recent_sales.replace("K+ bought in past month", "000").replace("+ bought in past month", "")
    price_list.append([item_brand, title, rating, rating_count, price, recent_sales, unit_price])

df = pd.DataFrame(price_list, columns=['brand', 'title', 'rating', 'rating_count', 'price', 'recent_sales', 'unit_price'])

df.sort_values(by=['brand', 'title', 'price'], ascending=True, inplace=True)
df.reset_index(drop=True, inplace=True)

df.to_csv('data/amazon_results_table.csv', index=False, header=True)

df.drop_duplicates(['brand', 'title', 'price'], inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.to_markdown())

with open('data/amazon_results_simplified.json', 'w') as f:
    json.dump(df.to_dict('records'), f)

json_data = df.to_dict('records')
titles = []
for raw in json_data:
    titles.append(raw['title'] + ", Unit Price = " + raw['unit_price'])

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

analyzePrompt = """
This array contains search data about the brand, unit size, unit count and unit price of a product. Parse all the data as described in the pricing schema
Return output in list format. 
"""


class Response(TypedDict):
    brands: list[str]
    sizeUnits: list[float]
    countUnits: list[int]
    price: list[float]


response = model.generate_content(
    [analyzePrompt, str(titles)],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=Response))

productInfo = json.loads(response.text)

print(json.dumps(productInfo, indent=4))