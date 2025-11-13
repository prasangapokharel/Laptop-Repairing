import orjson
data = {"user": "godsu", "message": "Hello, world!"}
json_bytes = orjson.dumps(data)
print(json_bytes)