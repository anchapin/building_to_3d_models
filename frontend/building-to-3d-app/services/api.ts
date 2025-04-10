const API_BASE_URL = 'http://localhost:5000/api';

export interface UploadResult {
  success: boolean;
  filename: string;
  result_file: string;
  file_type: string;
  orientation?: string;
  floor_level?: number;
}

export interface ModelGenerationResult {
  success: boolean;
  model_file: string;
  gbxml_file: string;
}

export interface ScaleResult {
  success: boolean;
  scale_factor: number;
}

/**
 * Upload a building plan file (floor plan or elevation)
 */
export async function uploadFile(
  file: File,
  type: 'floorPlan' | 'elevation',
  options?: { orientation?: string; floorLevel?: number }
): Promise<UploadResult> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);
  
  if (type === 'elevation' && options?.orientation) {
    formData.append('orientation', options.orientation);
  }
  
  if (type === 'floorPlan' && options?.floorLevel !== undefined) {
    formData.append('floorLevel', options.floorLevel.toString());
  }

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Set scale for an image
 */
export async function setScale(
  imageId: string,
  pixelLength: number,
  realLength: number,
  unit: string = 'meters'
): Promise<ScaleResult> {
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
    throw new Error(`Setting scale failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Generate 3D model from processed files
 */
export async function generateModel(
  floorPlans: string[],
  elevations: string[]
): Promise<ModelGenerationResult> {
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
    throw new Error(`Model generation failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get a result file
 */
export function getResultFileUrl(filename: string): string {
  return `${API_BASE_URL}/results/${filename}`;
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }
  
  return response.json();
}