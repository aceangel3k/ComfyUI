#!/usr/bin/env python3
"""
Simple test script to verify the download endpoint is working
"""

import asyncio
import aiohttp
import json

async def test_download_endpoint():
    """Test the /download/download_model endpoint"""
    
    # Test data
    test_url = "https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-image-vae/resolve/main/vae/diffusion_pytorch_model.bin"
    test_filename = "test_vae.bin"
    test_model_type = "vae"
    
    # Endpoint URL
    endpoint_url = "http://localhost:8188/download/download_model"
    
    print(f"Testing download endpoint: {endpoint_url}")
    print(f"Test URL: {test_url}")
    print(f"Model type: {test_model_type}")
    print(f"Filename: {test_filename}")
    print("-" * 50)
    
    # Test data
    payload = {
        "url": test_url,
        "model_type": test_model_type,
        "filename": test_filename
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint_url, json=payload) as response:
                print(f"Response status: {response.status}")
                print(f"Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ SUCCESS: Download endpoint is working!")
                    print(f"Response: {json.dumps(result, indent=2)}")
                else:
                    error_text = await response.text()
                    print("❌ FAILED: Download endpoint returned error")
                    print(f"Error response: {error_text}")
                    
    except aiohttp.ClientConnectorError:
        print("❌ FAILED: Cannot connect to ComfyUI server")
        print("Make sure ComfyUI is running on localhost:8188")
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_download_endpoint())