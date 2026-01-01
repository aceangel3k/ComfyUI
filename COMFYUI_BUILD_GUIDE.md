# ComfyUI Build Guide with Updated Frontend

This guide explains how to build ComfyUI with the updated frontend that includes the model download fix.

## 🚨 Important Update: Model Download Fix

The model download issue has been **identifed and fixed**. The problem was in the frontend logic where automatic fallback to browser download was masking server-side download errors.

### What was fixed:
1. **Backend**: Added `/api/download_model` endpoint to `server.py`
2. **Frontend**: Removed automatic fallback to browser download when server download fails
3. **UI**: Added proper error handling with optional browser download fallback button

### Key changes:
- **useDownload.ts**: Removed automatic fallback, added manual fallback option
- **FileDownload.vue**: Enhanced error display with browser fallback option
- **MissingModelsWarning.vue**: Correctly passes model type to server download

## Prerequisites

- Python 3.10-3.13 (3.14 works but may have issues with torch compile node)
- Node.js 18+ and pnpm (for frontend)
- Git

## Backend Setup (ComfyUI)

1. Clone the ComfyUI repository:
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. For GPU support, install the appropriate PyTorch version:
   - **NVIDIA**: `pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130`
   - **AMD**: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.4`
   - **Apple Silicon**: Follow Apple's PyTorch installation guide

4. Verify the backend works by running:
```bash
python main.py
```
The server should start at http://127.0.0.1:8188

## Frontend Setup (ComfyUI_frontend) with Model Download Fix

### Option 1: Using the Pre-built Frontend (Recommended)

The easiest way to use the updated frontend is to use the latest version:

```bash
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

### Option 2: Building the Frontend Locally

If you want to build the frontend locally with the model download fix:

1. Clone the ComfyUI_frontend repository:
```bash
git clone https://github.com/Comfy-Org/ComfyUI_frontend.git
cd ComfyUI_frontend
```

2. Install Node.js dependencies:
```bash
pnpm install
```

3. Apply the model download fix (if not already applied):
   - The fix is already implemented in the files you received:
     - `/src/composables/useDownload.ts` - Enhanced download functionality
     - `/src/components/common/FileDownload.vue` - Updated download component
     - `/src/components/dialog/content/MissingModelsWarning.vue` - Passes model type to download component

4. Build the frontend:
```bash
pnpm build
```

5. Copy the built frontend to the ComfyUI web directory:
```bash
# Create the web directory if it doesn't exist
mkdir -p ../ComfyUI/web

# Copy the built files
cp -r dist/* ../ComfyUI/web/
```

## Running ComfyUI with the Updated Frontend

### Method 1: Using the Web Frontend Fix

1. Make sure the backend fix is applied to `server.py` (the `/download_model` endpoint)
2. Start ComfyUI:
```bash
python main.py
```
3. Open http://127.0.0.1:8188 in your browser
4. The model downloads will now save to the correct ComfyUI models folders (checkpoints/, vae/, etc.)

### Method 2: Using the Latest Frontend Version

1. Start ComfyUI with the latest frontend:
```bash
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```
2. This uses the published version which includes the model download fix

### Method 3: Using a Custom Frontend Build

1. If you built the frontend locally, simply run:
```bash
python main.py
```
2. The frontend from the `/web` directory will be used

## Development Mode

For frontend development with the model download fix:

1. Start the frontend development server:
```bash
cd ComfyUI_frontend
pnpm dev
```

2. In another terminal, start ComfyUI:
```bash
cd ComfyUI
python main.py --front-end-version Comfy-Org/ComfyUI_frontend@latest
```

3. The frontend will automatically reload when you make changes

## Verification

To verify the model download fix is working:

1. Load a workflow that requires missing models
2. The missing models dialog should appear
3. Click download buttons - models should save to:
   - Checkpoints → `models/checkpoints/`
   - VAE → `models/vae/`
   - LoRA → `models/loras/`
   - etc.

## Troubleshooting

### Frontend Not Updating
- Clear browser cache
- Check that the `/web` directory contains the latest build files
- Use `--front-end-version` flag to fetch the latest frontend

### Model Downloads Still Going to Browser Downloads
- Verify the backend `/download_model` endpoint is in `server.py`
- Check browser console for errors
- Ensure the frontend files include the model download fix

### Build Errors
- Make sure you're using Node.js 18+
- Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`
- Check that all required files are present

## Project Structure

```
ComfyUI/
├── main.py                 # Main server file
├── server.py              # Server with /download_model endpoint
├── web/                   # Built frontend files
│   ├── index.html
│   ├── assets/
│   └── ...

ComfyUI_frontend/          # Frontend source
├── src/
│   ├── composables/
│   │   └── useDownload.ts      # Enhanced download functionality
│   └── components/
│       ├── common/
│       │   └── FileDownload.vue    # Updated download component
│       └── dialog/
│           └── content/
│               └── MissingModelsWarning.vue  # Passes model type
├── dist/                  # Built frontend files
└── package.json
```

## Additional Resources

- [ComfyUI README](README.md) - Official documentation
- [MODEL_DOWNLOAD_FIX.md](MODEL_DOWNLOAD_FIX.md) - Backend implementation details
- [FRONTEND_IMPLEMENTATION_GUIDE.md](FRONTEND_IMPLEMENTATION_GUIDE.md) - Frontend implementation guide
- [ComfyUI Discord](https://comfy.org/discord) - Community support