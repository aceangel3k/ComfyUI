# Frontend Implementation Guide for Model Download Fix

## Overview
This guide provides the necessary changes needed in the ComfyUI frontend repository to use the new `/download_model` backend endpoint instead of direct browser downloads.

## Files to Modify
Since the frontend code is in the separate `ComfyUI_frontend` repository, the following files will likely need to be modified:

1. **Missing Models Dialog Component** - The component that shows the missing models dialog
2. **Download Button Handler** - The function that handles download button clicks
3. **API Service** - The service that handles API calls to the backend

## Implementation Steps

### 1. Update the Download Handler Function
Replace the current browser download logic with API calls to the new endpoint:

```typescript
// Previous code (likely existing):
const downloadModel = (url: string, filename: string) => {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

// New implementation:
const downloadModel = async (url: string, filename: string, modelType: string) => {
  try {
    // Show loading state
    setIsDownloading(true);
    
    const response = await fetch('/api/download_model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        filename: filename,
        model_type: modelType
      })
    });
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      // Show success message
      showMessage('Model downloaded successfully!', 'success');
      // Trigger model list refresh
      await refreshModelList();
    } else {
      // Show error message
      showMessage(result.error || 'Download failed', 'error');
    }
  } catch (error) {
    showMessage('Download failed: ' + error.message, 'error');
  } finally {
    setIsDownloading(false);
  }
};
```

### 2. Update the Missing Models Dialog Component
Modify the dialog to pass the model type to the download handler:

```typescript
// In the missing models dialog component where download buttons are rendered:

const MissingModelsDialog = ({ missingModels, onClose }) => {
  const [downloadingModels, setDownloadingModels] = useState(new Set());
  
  const handleDownload = async (model) => {
    setDownloadingModels(prev => new Set(prev).add(model.id));
    
    try {
      await downloadModel(
        model.downloadUrl,
        model.filename,
        model.type // e.g., 'checkpoints', 'vae', 'loras', etc.
      );
    } finally {
      setDownloadingModels(prev => {
        const newSet = new Set(prev);
        newSet.delete(model.id);
        return newSet;
      });
    }
  };
  
  return (
    <Dialog>
      {/* Dialog header */}
      <DialogBody>
        {missingModels.map(model => (
          <div key={model.id} className="missing-model-item">
            <div className="model-info">
              <h3>{model.name}</h3>
              <p>Type: {model.type}</p>
              <p>Size: {model.size}</p>
            </div>
            <Button 
              onClick={() => handleDownload(model)}
              disabled={downloadingModels.has(model.id)}
              variant="primary"
            >
              {downloadingModels.has(model.id) ? 'Downloading...' : 'Download'}
            </Button>
          </div>
        ))}
      </DialogBody>
    </Dialog>
  );
};
```

### 3. Add Progress Indicator (Optional)
For better UX, add a progress indicator for large model downloads:

```typescript
// Enhanced version with progress tracking:
const downloadModelWithProgress = async (url: string, filename: string, modelType: string, onProgress?: (progress: number) => void) => {
  try {
    setIsDownloading(true);
    
    const response = await fetch('/api/download_model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        filename: filename,
        model_type: modelType
      })
    });
    
    const result = await response.json();
    
    if (response.ok && result.success) {
      showMessage('Model downloaded successfully!', 'success');
      await refreshModelList();
    } else {
      showMessage(result.error || 'Download failed', 'error');
    }
  } catch (error) {
    showMessage('Download failed: ' + error.message, 'error');
  } finally {
    setIsDownloading(false);
  }
};
```

### 4. Update CSS Styles
Add styles for the download states:

```css
.missing-model-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.model-info h3 {
  margin: 0;
  font-weight: 600;
}

.model-info p {
  margin: 0.25rem 0;
  color: var(--text-secondary);
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.download-progress {
  width: 100%;
  height: 4px;
  background-color: var(--background-secondary);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.download-progress-bar {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}
```

### 5. Add Toast/Message Service
Implement a toast notification system for user feedback:

```typescript
// Message service implementation:
const useMessageService = () => {
  const [messages, setMessages] = useState([]);
  
  const showMessage = (text: string, type: 'success' | 'error' | 'info') => {
    const id = Date.now().toString();
    setMessages(prev => [...prev, { id, text, type }]);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      setMessages(prev => prev.filter(msg => msg.id !== id));
    }, 5000);
  };
  
  return { messages, showMessage };
};
```

## Required Props for Model Objects
Ensure each model object in the missing models array has the following structure:

```typescript
interface MissingModel {
  id: string;
  name: string;
  type: string; // 'checkpoints', 'vae', 'loras', etc.
  filename: string;
  downloadUrl: string;
  size?: string;
  description?: string;
}
```

## Model Type Mapping
Map the model types correctly from the backend to frontend:

```typescript
const MODEL_TYPE_MAP = {
  'checkpoints': 'Stable Diffusion Models',
  'vae': 'VAE',
  'loras': 'LoRA',
  'text_encoders': 'Text Encoders',
  'clip_vision': 'CLIP Vision',
  'controlnet': 'ControlNet',
  'unet': 'UNet',
  // Add other model types as needed
};

const getModelDisplayName = (type: string) => {
  return MODEL_TYPE_MAP[type] || type;
};
```

## Testing Checklist
- [ ] Verify download buttons are present in missing models dialog
- [ ] Test download with different model types
- [ ] Verify progress indicators work correctly
- [ ] Test error handling (invalid URLs, network errors)
- [ ] Confirm models appear in correct folders after download
- [ ] Test with large model files (>1GB)
- [ ] Verify concurrent downloads work properly

## Error Scenarios to Handle
1. **Network connectivity issues**
2. **Invalid model URLs**
3. **Insufficient disk space**
4. **Permission issues**
5. **Server errors**

## Migration Notes
- This change requires the backend fix to be deployed first
- The frontend should gracefully fallback to browser downloads if the new endpoint is not available (for backwards compatibility)
- Consider adding a feature flag to enable/disable the new download behavior

## Additional Improvements
1. **Resume capability** for interrupted downloads
2. **Parallel download** support for multiple models
3. **Download queue** to manage concurrent downloads
4. **Hash verification** to ensure model integrity
5. **Extract metadata** from downloaded models

## Files in ComfyUI_frontend Repository
Look for these files in the ComfyUI_frontend repository:
- `src/components/MissingModelsDialog.vue` or similar
- `src/services/api.js` or `src/utils/api.js`
- `src/stores/modelStore.js` or similar
- `src/components/DownloadButton.vue` or similar

This implementation will ensure that model downloads from the missing models dialog are saved to the correct ComfyUI models folders instead of the browser's default download location.