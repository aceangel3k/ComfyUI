#!/usr/bin/env python3
"""
Basic test to verify the download endpoint is properly registered
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_import():
    """Test that we can import the server and that our download route exists"""
    try:
        print("Testing backend import...")
        
        # Try to import the main server module
        import server
        
        print("✅ Server module imported successfully")
        
        # Check if our download_model method exists
        if hasattr(server, 'PromptServer'):
            prompt_server = server.PromptServer
            if hasattr(prompt_server, 'download_model'):
                print("✅ download_model method exists")
            else:
                print("❌ download_model method not found")
                return False
                
            # Check if it's properly defined as a method
            import inspect
            if inspect.ismethod(prompt_server.download_model) or inspect.isfunction(prompt_server.download_model):
                print("✅ download_model is properly defined")
            else:
                print("❌ download_model is not properly defined")
                return False
        else:
            print("❌ PromptServer class not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error importing server: {e}")
        return False

def test_route_registration():
    """Test that the download route would be properly registered"""
    try:
        print("\nTesting route registration structure...")
        
        # Read the server.py file to check our changes
        with open('server.py', 'r') as f:
            content = f.read()
            
        # Check for our download endpoint
        if 'def download_model(self' in content:
            print("✅ download_model method definition found")
        else:
            print("❌ download_model method definition not found")
            return False
            
        # Check for the sub-application creation
        if 'download_app = web.Application()' in content:
            print("✅ download sub-application creation found")
        else:
            print("❌ download sub-application creation not found")
            return False
            
        # Check for the route registration
        if 'download_app.router.add_post("/download_model"' in content:
            print("✅ download route registration found")
        else:
            print("❌ download route registration not found")
            return False
            
        # Check for sub-app addition
        if "self.app.add_subapp('/download'" in content:
            print("✅ sub-app addition to main app found")
        else:
            print("❌ sub-app addition to main app not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking route registration: {e}")
        return False

def main():
    print("=== ComfyUI Model Download Fix - Basic Backend Test ===\n")
    
    # Test 1: Backend import
    test1_passed = test_backend_import()
    
    # Test 2: Route registration
    test2_passed = test_route_registration()
    
    print(f"\n=== Test Results ===")
    print(f"Backend Import: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Route Registration: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print(f"\n🎉 All tests passed! The backend implementation appears to be correctly set up.")
        print(f"\nNext steps:")
        print(f"1. Start ComfyUI server: python main.py")
        print(f"2. Open web UI and test model download in missing models dialog")
        print(f"3. Models should now download to the correct ComfyUI models folder")
        return True
    else:
        print(f"\n❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)