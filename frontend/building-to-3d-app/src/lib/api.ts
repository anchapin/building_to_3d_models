const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Check the health of the API server
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error('API server is not responding');
  }
  
  return await response.json();
}

/**
 * Upload a file to the server
 */
export async function uploadFile(
  file: File, 
  type: string, 
  orientation?: string, 
  floorLevel?: number
) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);
  
  if (type === 'elevation' && orientation) {
    formData.append('orientation', orientation);
  }
  
  if (type === 'floorPlan' && floorLevel !== undefined) {
    formData.append('floorLevel', floorLevel.toString());
  }
  
  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to upload file');
  }
  
  return await response.json();
}

/**
 * Set the scale for an image
 */
export async function setScale(
  imageId: string, 
  pixelLength: number, 
  realLength: number, 
  unit: string = 'meters'
) {
  const response = await fetch(`${API_BASE_URL}/set-scale`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      imageId,
      pixelLength,
      realLength,
      unit,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to set scale');
  }
  
  return await response.json();
}

/**
 * Generate a 3D model from processed files
 */
export async function generateModel(floorPlans: string[], elevations: string[]) {
  const response = await fetch(`${API_BASE_URL}/generate-model`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      floorPlans,
      elevations,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to generate model');
  }
  
  return await response.json();
}
