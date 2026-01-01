import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
VIDEO_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # Me at the zoo (19s)

def test_pipeline():
    print(f"Testing connectivity to {BASE_URL}...")
    try:
        # Check if root/docs is accessible (FastAPI default)
        requests.get(f"{BASE_URL}/docs", timeout=5)
        print("[OK] Backend is reachable.")
    except Exception as e:
        print(f"[FAIL] Backend not reachable: {e}")
        sys.exit(1)

    print(f"\nSubmitting video for processing: {VIDEO_URL}")
    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}/process_video", json={"url": VIDEO_URL}, timeout=300)
        if response.status_code == 200:
            data = response.json()
            elapsed = time.time() - start_time
            print(f"[OK] Processing complete in {elapsed:.2f}s")
            print(f"   Title: {data.get('title')}")
            print(f"   Summary: {data.get('summary')}")
            if 'error' in data:
                print(f"[FAIL] API returned error: {data['error']}")
                sys.exit(1)
        else:
            print(f"[FAIL] Request failed: {response.status_code} - {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Exception during processing: {e}")
        sys.exit(1)

    print("\nTesting Q&A...")
    try:
        q_response = requests.post(f"{BASE_URL}/ask", json={"question": "What is reliable?"}) # Context specific
        if q_response.status_code == 200:
            ans_data = q_response.json()
            print(f"[OK] Q&A Success. Answer: {ans_data.get('answer')}")
        else:
            print(f"[FAIL] Q&A failed: {q_response.status_code}")
    except Exception as e:
        print(f"[FAIL] Exception during Q&A: {e}")

if __name__ == "__main__":
    test_pipeline()
