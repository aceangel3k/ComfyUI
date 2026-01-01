#!/usr/bin/env python3
"""
Test script to verify the /api/download_model endpoint is working correctly.
Run this while ComfyUI server is running.
"""

import requests
import json
import sys

def test_download_endpoint():
    """Test the download model endpoint"""
    url = "http://127.0.0.1:8188/api/download_model"
    
    # Test data
    test_payload = {
        "url": "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors",
        "filename": "test_model.safetensors",
        "model_type": "checkpoints"
    }
    
    print("Testing /api/download_model endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")
    
    try:
        response = requests.post(url, json=test_payload, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Body (raw): {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Endpoint is working correctly!")
            if 'path' in response_data:
                print(f"✅ Model downloaded to: {response_data.get('path')}")
        else:
            print(f"\n❌ Endpoint returned error status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection failed. Make sure ComfyUI server is running on http://127.0.0.1:8188")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timed out. Server might be busy or endpoint might be stuck.")
        return False
    except Exception as e:
        print(f"\n❌ Request failed with error: {str(e)}")
        return False
    
    return True

def test_endpoint_with_invalid_model_type():
    """Test the endpoint with invalid model type"""
    url = "http://127.0.0.1:8188/api/download_model"
    
    test_payload = {
        "url": "https://example.com/test.safetensors",
        "filename": "test.safetensors", 
        "model_type": "invalid_type"
    }
    
    print("\n\nTesting with invalid model type...")
    
    try:
        response = requests.post(url, json=test_payload, timeout=10)
        
        if response.status_code == 400:
            print("✅ correctly rejected invalid model type")
            return True
        else:
            print(f"❌ Should have returned 400 for invalid model type, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 ComfyUI Download Endpoint Test")
    print("=" * 50)
    
    success = test_download_endpoint()
    if success:
        test_endpoint_with_invalid_model_type()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Tests failed!")
        sys.exit(1)