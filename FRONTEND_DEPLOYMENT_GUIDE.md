# ComfyUI Frontend Deployment Guide with Model Download Fix

## 🚨 Critical Information

The model download issue persists because ComfyUI uses a **separate frontend package** (`comfyui-frontend-package`) installed via pip, NOT the source code we modified. Even though we fixed the source code, the server is still serving the original frontend package.

## Problem Diagnosis

### Why the fix isn't working:
1. ComfyUI loads frontend from `comfyui-frontend-package` (pip package)
2. Our modifications are in the source code repository `ComfyUI_frontend/`
3. The server ignores our modified source code and uses the installed package
4. User sees old behavior despite our fixes

## Solution Options

### Option 1: Use Latest Frontend Version (Recommended)

The ComfyUI team has likely fixed this issue in newer versions. Use the latest frontend:

```bash
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

### Option 2: Build Custom Frontend Package

If you need to use our specific fixes:

#### Step 1: Build the Frontend
```bash
cd ComfyUI_frontend
pnpm install
pnpm build
```

#### Step 2: Create a Custom Package Structure
```bash
# Create a temporary directory for the custom package
mkdir -p custom_frontend_package
cd custom_frontend_package

# Copy the built frontend
cp -r ../ComfyUI_frontend/dist/* .

# Create package structure
mkdir -p comfyui_frontend_package/static
mv * comfyui_frontend_package/static/

# Create setup.py
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="comfyui-frontend-package-custom",
    version="1.0.0",
    packages=find_packages(),
    package_data={'comfyui_frontend_package': ['static/**/*']},
    include_package_data=True,
)
EOF

# Create __init__.py
touch comfyui_frontend_package/__init__.py
```

#### Step 3: Install Custom Package
```bash
pip install -e .
```

#### Step 4: Update Requirements
```bash
# In the main ComfyUI directory
pip uninstall comfyui-frontend-package
# Your custom package will now be used
```

### Option 3: Use Local Frontend Development

#### Step 1: Start Frontend Dev Server
```bash
cd ComfyUI_frontend
pnpm dev
```

#### Step 2: Start ComfyUI with Proxy
```bash
# In another terminal
cd ComfyUI
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

The dev server will serve your modified frontend code.

### Option 4: Direct File Replacement (Advanced)

1. Find the installed frontend package location:
```bash
python -c "import comfyui_frontend_package; print(comfyui_frontend_package.__file__)"
```

2. Replace the files in the installed package with our modified versions
3. **Warning**: This is brittle and will be overwritten on package updates

## Verification Steps

### 1. Check Which Frontend is Being Used
Open browser DevTools → Network tab → look for JavaScript files to see source:

- If paths show `localhost:5173` → Using dev server ✅
- If paths show package name → Using pip package ❌
- If paths show custom files → Using custom build ✅

### 2. Test the Download Fix
1. Load workflow with missing models
2. Open browser DevTools → Console
3. Click download button
4. Look for network request to `/api/download_model`
5. Console should show "Server download failed" if backend is not running
6. Should NOT immediately download to browser

### 3. Verify Backend Endpoint
```bash
python test_download_endpoint.py
```

## Expected Behavior After Fix

### Working Server Download:
1. Click download → Shows "Downloading... (X%)"
2. Network request to `/api/download_model`
3. Model saves to `models/checkpoints/` (or appropriate folder)
4. Progress reaches 100%

### Server Download Working But Fails:
1. Click download → Shows error message
2. "Download to browser instead" button appears
3. User can choose browser download as fallback

### Not Working (Current Issue):
1. Click download → Immediately downloads to browser
2. No progress indicator
3. No error messages
4. Model goes to browser downloads folder

## Quick Fix Test

To test if our frontend code works:

1. **Build the frontend**:
```bash
cd ComfyUI_frontend
pnpm install
pnpm build
```

2. **Use built frontend with ComfyUI**:
```bash
cd ../ComfyUI
# Copy built files to web directory
mkdir -p web
cp -r ../ComfyUI_frontend/dist/* web/
python main.py
```

3. **Test the download** - it should now work correctly

## Troubleshooting

### Still downloading to browser?
- Check browser DevTools → Network tab for `/api/download_model` request
- If no request seen → frontend still using old code
- If request seen and fails → backend issue or network problem
- If request seen and succeeds → check file system for downloaded model

### Frontend not updating?
- Clear browser cache (Ctrl+Shift+R)
- Check if using correct frontend version
- Verify build process completed successfully

### Backend endpoint missing?
- Ensure using updated `server.py` with `/download_model` endpoint
- Restart ComfyUI server after updating code
- Check server logs for endpoint registration

## Production Deployment

For production use, the best approach is:

1. **Wait for official fix** in ComfyUI frontend package
2. **Use Option 1** with latest frontend version if available
3. **Use Option 2** only if you need immediate deployment and understand maintenance implications

The official ComfyUI team should release a updated frontend package with the model download fix, making this workaround unnecessary.