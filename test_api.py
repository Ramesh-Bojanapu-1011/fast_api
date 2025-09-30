#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI endpoints are working correctly.
"""

import requests

BASE_URL = "http://127.0.0.1:8001/"

def test_health_endpoint():
    """Test the basic health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health Endpoint Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_hello_endpoint():
    """Test the hello endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/hello/World")
        print(f"Hello Endpoint Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing hello endpoint: {e}")
        return False

def test_health_check_endpoint():
    """Test the detailed health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check Endpoint Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health check endpoint: {e}")
        return False

def test_youtube_search():
    """Test the YouTube search endpoint"""
    try:
        data = {
            "search_text": "FastAPI tutorial",
            "num_results": 3
        }
        response = requests.post(
            f"{BASE_URL}/find/youtube/videos",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"YouTube Search Status: {response.status_code}")
        print(f"Response keys: {list(response.json().keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing YouTube search: {e}")
        return False

def test_actor_search():
    """Test the actor search endpoint"""
    try:
        data = {
            "name": "Chiranjeevi",
            "craft": "actor"
        }
        response = requests.post(
            f"{BASE_URL}/find/person/wiki_url",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Actor Search Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing actor search: {e}")
        return False

if __name__ == "__main__":
    print("Testing FastAPI endpoints...")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Hello Endpoint", test_hello_endpoint),
        ("Health Check Endpoint", test_health_check_endpoint),
        ("YouTube Search", test_youtube_search),
        ("Actor Search", test_actor_search)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print(f"✅ {test_name}: {'PASSED' if result else 'FAILED'}")
        print("-" * 30)
    
    print("\n📊 Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above for details.")