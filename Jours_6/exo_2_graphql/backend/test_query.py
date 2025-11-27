import urllib.request
import json

url = "http://localhost:8001/graphql"
query = """
query {
  users {
    name
    email
  }
}
"""

data = json.dumps({'query': query}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        print("Response:")
        print(json.dumps(json.loads(response.read()), indent=2))
except Exception as e:
    print(f"Error: {e}")
