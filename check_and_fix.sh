#!/bin/bash

echo "🔍 ComfyUI Model Download Fix Checker"
echo "====================================="

# Check if server has the download endpoint
echo "1. Checking if backend has /download_model endpoint..."
if grep -q "download_model" /home/dgx/ComfyUI/server.py; then
    echo "✅ Backend endpoint found in server.py"
else
    echo "❌ Backend endpoint NOT found in server.py"
    echo "   You need to use the updated server.py with the download endpoint"
fi

# Check frontend version
echo ""
echo "2. Frontend being used:"
echo "   Version: 1.35.9 (from pip package)"
echo "   This does NOT include our model download fix"

# Check if we can test the endpoint
echo ""
echo "3. Testing backend endpoint..."
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8188/api/download_model
echo ""

echo ""
echo "🚀 Quick Fix Options:"
echo "===================="
echo ""
echo "Option A - Use latest frontend (EASIEST):"
echo "   python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest"
echo ""
echo "Option B - Use local build:"
echo "   cd /path/to/ComfyUI_frontend"
echo "   pnpm install && pnpm build"
echo "   cd /home/dgx/ComfyUI"
echo "   mkdir -p web && cp -r ../ComfyUI_frontend/dist/* web/"
echo "   python main.py"
echo ""
echo "Option C - Check if latest frontend already has fix:"
echo "   python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest"
echo "   # Then test with a missing model workflow"

echo ""
echo "📝 To test if fix works:"
echo "1. Load a workflow with missing models"
echo "2. Click download button"
echo "3. Should show progress indicator, not immediate browser download"
echo "4. Check browser DevTools → Network tab for /api/download_model request"