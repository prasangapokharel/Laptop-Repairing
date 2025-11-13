import orjson
import requests


url = "http://localhost:8000/v1/users"

response = requests.get(url)
data = orjson.loads(response.content)

print(data)


