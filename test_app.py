import requests
import threading
import time
from movieRecommendation import app
import sys

def start_server():
    app.run(port=5000)

def test_app():
    # Start server in a separate thread
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    
    # Give server a moment to start
    time.sleep(2)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test 1: Main page load
        print("Testing generic page load...")
        resp = requests.get(base_url)
        if resp.status_code == 200:
            print("PASS: Main page loaded successfully.")
        else:
            print(f"FAIL: Main page returned {resp.status_code}")

        # Test 2: Search API with lowercase
        print("\nTesting search API (lowercase)...")
        search_term = "star wa"
        resp = requests.get(f"{base_url}/search?q={search_term}")
        if resp.status_code == 200:
            results = resp.json()
            if len(results) > 0:
                print(f"PASS: Search returned {len(results)} results for '{search_term}'.")
                print(f"Sample: {results[0]}")
            else:
                print("FAIL: Search returned empty list (unexpected for 'star wa').")
        else:
            print(f"FAIL: Search API returned {resp.status_code}")

        # Test 3: Recommendation (POST)
        print("\nTesting recommendation (lowercase input)...")
        movie_name = "star wars: the force awakens" # Correct lowercase title
        resp = requests.post(base_url, data={'movie': movie_name})
        if resp.status_code == 200 and "Recommended for You" in resp.text:
            print(f"PASS: Recommendation page loaded for '{movie_name}'.")
        else:
            print(f"FAIL: Recommendation page failed or did not show results for '{movie_name}'.")
            
    except Exception as e:
        print(f"FAIL: An error occurred: {e}")

if __name__ == "__main__":
    test_app()
