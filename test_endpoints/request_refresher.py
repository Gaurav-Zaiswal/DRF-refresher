import requests

url = "http://127.0.0.1:8000/api/basic/products_drf_api/"

response = requests.get(url)

# print(response)
print(response.json())
