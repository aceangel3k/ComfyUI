# ComfyUI Model Download Fix - Troubleshooting Guide

## Issue: Downloads still going to browser instead of ComfyUI models folder

If you've implemented the fix but downloads are still going to the browser downloads folder, follow these troubleshooting steps:

## Step 1: Verify the Backend is Working

First, test if the backend endpoint is working correctly:

```bash
python test_download_endpoint_simple.py
```

Expected output should show:
```
✅ SUCCESS: Download endpoint is working!
Response: {
  "success": true,
  "message": "Model downloaded to /path/to/models/vae/test_vae.bin",
  "path": "/path/to/models/vae/test_vae.bin"
}
```

If this fails:
- Check the server logs for errors
- Make sure ComfyUI started without errors
- Verify the server.py changes were applied correctly

## Step 2: Verify You're Using the Updated Frontend

The most common issue is that you're still using the old frontend. Check your ComfyUI startup command:

### Option A: Use Latest Frontend (Recommended)
```bash
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

### Option B: Build Custom Frontend
If you need to use custom frontend changes:

1. Navigate to the ComfyUI_frontend directory:
```bash
cd ../ComfyUI_frontend
```

2. Install dependencies and build:
```bash
npm install
npm run build
```

3. Copy the built frontend to ComfyUI:
```bash
cp -r dist/* ../ComfyUI/web/
```

### Option C: Check Current Frontend Version
Check which frontend version you're using by looking at the ComfyUI startup logs. You should see something like:
```
[Prompt Server] web root: /path/to/comfyui/web
```

## Step 3: Check Browser Developer Tools

1. Open the browser developer tools (F12)
2. Go to the Network tab
3. Click the download button in the missing models dialog
4. Look for a request to `/download/download_model`

**If you see a request to `/download/download_model`:**
- The frontend is updated correctly
- Check the response status and error messages

**If you see NO network request or a direct download:**
- The frontend is not using the updated code
- You need to update the frontend (see Step 2)

## Step 4: Verify Frontend Code

Check that the frontend files contain our changes:

### Check useDownload.ts
The file should contain:
```typescript
const response = await fetch('/download/download_model', {
```
NOT:
```typescript
const response = await fetch('/api/download_model', {
```

### Check FileDownload.vue
The file should call `triggerServerDownload` when modelType is provided (lines 95-97).

## Step 5: Clear Browser Cache

Sometimes the browser caches the old frontend JavaScript:

1. Clear browser cache and cookies
2. Hard refresh (Ctrl+F5 or Cmd+Shift+R)
3. Restart ComfyUI
4. Try the download again

## Step 6: Check for Multiple ComfyUI Instances

Make sure you don't have multiple ComfyUI instances running:

```bash
ps aux | grep python
# or on Windows:
tasklist | findstr python
```

Kill any extra instances and restart with the correct command.

## Common Issues and Solutions

### Issue: "Unknown user: default" error
**Solution**: This should be fixed with our sub-application approach. If you still see this, verify the server.py changes were applied correctly.

### Issue: "Added route will never be executed" error
**Solution**: This should be fixed. If you still see this, make sure there are no duplicate route registrations.

### Issue: Frontend shows but downloads still go to browser
**Solution**: You're using the old frontend. Follow Step 2 to update the frontend.

### Issue: Endpoint returns 404 Not Found
**Solution**: The backend changes weren't applied correctly. Verify the server.py changes and restart ComfyUI.

## Verification

Once everything is working:

1. Backend test should pass (Step 1)
2. Browser network tab should show request to `/download/download_model`
3. Model should appear in the correct ComfyUI models folder (e.g., `models/vae/`)
4. No files should be downloaded to the browser's default downloads folder

## If Issues Persist

If you've followed all these steps and still have issues:

1. Check the exact startup command you're using
2. Verify frontend files contain our changes
3. Check server logs for any errors
4. Try with a completely fresh browser profile
5. Make sure no other ComfyUI instances are running

The most common issue is using an outdated frontend. The backend changes are usually easier to apply correctly.