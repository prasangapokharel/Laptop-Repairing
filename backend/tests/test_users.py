import orjson
import requests

base_url = "http://localhost:8000"

def test_users():
    url = f"{base_url}/v1/users"
    response = requests.get(url)
    data = orjson.loads(response.content)
    print("Full Name: ",  ["full_name"])
test_users()