
import requests
import json
import time

API_URL = "http://127.0.0.1:8000"
VIDEO_URL = "https://youtu.be/fLeJJPxua3E"

print(f"--- STARTING FINAL VERIFICATION ---")
print(f"Target: {API_URL}")
print(f"Video: {VIDEO_URL}")

def test_process():
    print("\n1. Testing /process_video endpoint...")
    print("   Sending request (this takes time)...")
    start = time.time()
    try:
        response = requests.post(f"{API_URL}/process_video", json={"url": VIDEO_URL})
        duration = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            print(f"   SUCCESS! (took {duration:.1f}s)")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Summary: {data.get('summary', 'N/A')[:100]}...")
            print(f"   Topics Found: {len(data.get('topics', []))}")
            return True
        else:
            print(f"   FAILED: Status {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"   CRITICAL ERROR: {e}")
        return False

def test_ask():
    print("\n2. Testing /ask endpoint...")
    question = "What is this video about?"
    try:
        response = requests.post(f"{API_URL}/ask", json={"question": question})
        if response.status_code == 200:
            data = response.json()
            print(f"   SUCCESS!")
            print(f"   Question: {question}")
            print(f"   Answer: {data.get('answer', 'N/A')[:100]}...")
            return True
        else:
            print(f"   FAILED: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"   CRITICAL ERROR: {e}")
        return False

if __name__ == "__main__":
    if test_process():
        test_ask()
    else:
        print("\nSkipping Q&A test due to processing failure.")
    print("\n--- VERIFICATION COMPLETE ---")
