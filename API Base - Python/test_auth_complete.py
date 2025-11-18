#!/usr/bin/env python3
"""
Complete authentication pipeline test
Tests: token generation, protected route access with token, and 401 without token
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_auth_pipeline():
    print("=" * 60)
    print("TESTING COMPLETE AUTHENTICATION PIPELINE")
    print("=" * 60)
    
    # Wait a moment for the server to be ready
    time.sleep(1)
    
    # Test 1: Generate token
    print("\n[1] Generating authentication token...")
    try:
        token_response = requests.post(
            f"{BASE_URL}/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        print(f"    Status: {token_response.status_code}")
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            token = token_data.get('access_token')
            print(f"    ✓ Token generated successfully")
            print(f"    Token preview: {token[:50]}...")
        else:
            print(f"    ✗ Failed: {token_response.text}")
            return
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return
    
    # Test 2: Access protected route WITH token
    print("\n[2] Testing protected route WITH valid token...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        contacts_response = requests.get(
            f"{BASE_URL}/api/contacts/",
            headers=headers
        )
        print(f"    Status: {contacts_response.status_code}")
        print(f"    Response: {contacts_response.text[:100]}")
        
        if contacts_response.status_code == 200:
            print(f"    ✓ Successfully accessed protected route!")
        else:
            print(f"    ✗ Unexpected status code")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Test 3: Access protected route WITHOUT token (should fail)
    print("\n[3] Testing protected route WITHOUT token (should be 401)...")
    try:
        contacts_response = requests.get(f"{BASE_URL}/api/contacts/")
        print(f"    Status: {contacts_response.status_code}")
        
        if contacts_response.status_code == 401:
            print(f"    ✓ Correctly rejected unauthorized request")
            print(f"    Response: {contacts_response.text[:100]}")
        else:
            print(f"    ✗ Expected 401, got {contacts_response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION PIPELINE TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_auth_pipeline()
