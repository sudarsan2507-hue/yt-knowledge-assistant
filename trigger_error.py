
import requests
import time
import sys

# Wait for server
time.sleep(2)

url = "http://127.0.0.1:8080/process_video"
payload = {"url": "https://youtu.be/fLeJJPxua3E"}

print(f"Sending request to {url}...")
try:
    resp = requests.post(url, json=payload)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Request failed: {e}")
