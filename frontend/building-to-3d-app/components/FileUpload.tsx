'use client';

import { useState } from 'react';

interface FileUploadProps {
  onUploadSuccess: (result: any) => void;
  onUploadError: (error: string) => void;
  fileType: 'floorPlan' | 'elevation';
  orientation?: string;
  floorLevel?: number;
}

export default function FileUpload({
  onUploadSuccess,
  onUploadError,
  fileType,
  orientation = 'north',
  floorLevel = 0,
}: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      onUploadError('Please select a file to upload');
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', fileType);
      
      if (fileType === 'elevation' && orientation) {
        formData.append('orientation', orientation);
      }
      
      if (fileType === 'floorPlan' && floorLevel !== undefined) {
        formData.append('floorLevel', floorLevel.toString());
      }

      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const result = await response.json();
      onUploadSuccess(result);
    } catch (error) {
      onUploadError(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <h3>{fileType === 'floorPlan' ? 'Floor Plan' : 'Elevation'} Upload</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor={`file-${fileType}`}>
            Select {fileType === 'floorPlan' ? 'Floor Plan' : 'Elevation'} File:
          </label>
          <input
            type="file"
            id={`file-${fileType}`}
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileChange}
            disabled={uploading}
          />
        </div>
        
        {fileType === 'elevation' && (
          <div className="form-group">
            <label htmlFor="orientation">Orientation:</label>
            <select
              id="orientation"
              value={orientation}
              onChange={(e) => orientation = e.target.value}
              disabled={uploading}
            >
              <option value="north">North</option>
              <option value="east">East</option>
              <option value="south">South</option>
              <option value="west">West</option>
            </select>
          </div>
        )}
        
        {fileType === 'floorPlan' && (
          <div className="form-group">
            <label htmlFor="floorLevel">Floor Level:</label>
            <input
              type="number"
              id="floorLevel"
              value={floorLevel}
              onChange={(e) => floorLevel = parseInt(e.target.value, 10)}
              disabled={uploading}
            />
          </div>
        )}
        
        <button type="submit" disabled={uploading}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}