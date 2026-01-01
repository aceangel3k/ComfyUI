# Model Download Fix for Missing Models Dialog

## Problem
When loading a template with missing models (LLM/diffusion models, not 3D), the missing models dialog shows download buttons. However, when clicked in the web UI, these buttons were downloading models via the web browser instead of saving them to the ComfyUI models folder. This worked correctly in the Mac app but not in the web UI.

## Root Cause
The web UI was missing a server-side endpoint to handle model downloads. The frontend was likely using direct browser downloads, which download to the user's default download folder instead of the ComfyUI models folder.

## Solution
Added a new API endpoint `/download_model` to the server that handles model downloads and saves them to the appropriate ComfyUI models folder.

### Changes Made

#### server.py
1. **Added import**: Added `from pathlib import Path` for path operations.

2. **Added new endpoint**: Created `/download_model` POST endpoint that:
   - Accepts JSON payload with `url`, `model_type`, and `filename`
   - Validates the model type exists in ComfyUI's folder_paths
   - Validates filename for security (prevents path traversal)
   - Downloads the model from the provided URL
   - Saves it to the correct models folder based on model_type
   - Returns success/error response

### API Endpoint Details

**Endpoint**: `POST /download_model`

**Request Body**:
```json
{
  "url": "https://example.com/model.safetensors",
  "model_type": "checkpoints",  // or "vae", "loras", etc.
  "filename": "my_model.safetensors"
}
```

**Response** (Success):
```json
{
  "success": true,
  "message": "Model downloaded to /path/to/models/checkpoints/my_model.safetensors",
  "path": "/path/to/models/checkpoints/my_model.safetensors"
}
```

**Response** (Error):
```json
{
  "error": "Error message description"
}
```

### Security Features
1. **Filename validation**: Prevents path traversal attacks by checking for `/`, `..`, and `\` in filename
2. **Model type validation**: Only allows download to valid ComfyUI model directories
3. **Path verification**: Ensures the target file path is within the intended model directory
4. **Error handling**: Comprehensive error handling with appropriate HTTP status codes

### Usage
The frontend missing models dialog should now be updated to:
1. Detect when a download button is clicked
2. Extract the model URL, type, and filename
3. Make a POST request to `/download_model` instead of using browser download
4. Show progress/completion status to the user
5. Update the model list after successful download

## Supported Model Types
The endpoint supports all model types defined in ComfyUI's `folder_paths.folder_names_and_paths`, including:
- `checkpoints` (main diffusion models)
- `vae`
- `loras`
- `text_encoders`
- `clip_vision`
- `controlnet`
- `unet`
- And more...

## Testing
To test the fix:
1. Start ComfyUI with a missing model in a workflow
2. Open the missing models dialog
3. Click the download button
4. Verify the model is downloaded to the correct models folder instead of the browser download folder

## Notes
- The endpoint is available at both `/download_model` and `/api/download_model`
- Downloads are streamed in 1MB chunks to handle large model files efficiently
- The endpoint uses the existing aiohttp client session for consistent connection handling
- Error logging is implemented for debugging download issues