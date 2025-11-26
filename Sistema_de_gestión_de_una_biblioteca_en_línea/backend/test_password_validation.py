"""
Quick test script to verify password validation error handling.
This script tests that invalid passwords return HTTP 400 instead of 500.
"""

import requests
import json

BASE_URL = "http://localhost:8009"

def test_invalid_password_missing_uppercase():
    """Test password validation with missing uppercase letter."""
    print("\n🧪 Test 1: Password missing uppercase letter")
    print("=" * 60)
    
    payload = {
        "name": "Test User 1",
        "email": "test1@example.com",
        "password": "password123!",  # Missing uppercase
        "user_type": "general"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✅ PASS: Returns 400 Bad Request")
    else:
        print(f"❌ FAIL: Expected 400, got {response.status_code}")
    
    return response.status_code == 400


def test_invalid_password_missing_special():
    """Test password validation with missing special character."""
    print("\n🧪 Test 2: Password missing special character")
    print("=" * 60)
    
    payload = {
        "name": "Test User 2",
        "email": "test2@example.com",
        "password": "Password123",  # Missing special character
        "user_type": "general"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✅ PASS: Returns 400 Bad Request")
    else:
        print(f"❌ FAIL: Expected 400, got {response.status_code}")
    
    return response.status_code == 400


def test_valid_password():
    """Test with a valid password."""
    print("\n🧪 Test 3: Valid password")
    print("=" * 60)
    
    payload = {
        "name": "Test User 3",
        "email": "test3@example.com",
        "password": "Password123!",  # Valid password
        "user_type": "general"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code in [200, 201]:
        print("✅ PASS: User created successfully")
    else:
        print(f"❌ FAIL: Expected 200/201, got {response.status_code}")
    
    return response.status_code in [200, 201]


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PASSWORD VALIDATION ERROR HANDLING TEST")
    print("=" * 60)
    
    try:
        test1 = test_invalid_password_missing_uppercase()
        test2 = test_invalid_password_missing_special()
        test3 = test_valid_password()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Test 1 (Missing uppercase): {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Test 2 (Missing special): {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"Test 3 (Valid password): {'✅ PASS' if test3 else '❌ FAIL'}")
        
        if all([test1, test2, test3]):
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️  Some tests failed")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API. Is the server running?")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
