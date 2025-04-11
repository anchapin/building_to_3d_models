'use client';

import { useState, useCallback } from 'react';

interface FileUploadDropzoneProps {
  onUpload: (file: File) => void;
  acceptedFileTypes: string[];
  label: string;
  fileType: 'floorPlan' | 'elevation';
  orientation?: string;
  floorLevel?: number;
}

export function FileUploadDropzone({
  onUpload,
  acceptedFileTypes,
  label,
  fileType,
  orientation,
  floorLevel
}: FileUploadDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  
  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);
  
  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);
  
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);
  
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (acceptedFileTypes.includes(file.type)) {
        handleFileUpload(file);
      }
    }
  }, [acceptedFileTypes]);
  
  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      handleFileUpload(file);
    }
  }, []);
  
  const handleFileUpload = async (file: File) => {
    try {
      setIsUploading(true);
      await onUpload(file);
    } finally {
      setIsUploading(false);
    }
  };
  
  return (
    <div
      className={`border-2 border-dashed rounded-lg p-6 text-center ${
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <label className="block cursor-pointer">
        <span className="text-gray-700">{label}</span>
        <input
          type="file"
          className="hidden"
          accept={acceptedFileTypes.join(',')}
          onChange={handleFileChange}
          disabled={isUploading}
        />
        <div className="mt-2 text-sm text-gray-500">
          {isUploading ? (
            'Uploading...'
          ) : (
            <>
              Drag and drop a file here, or click to select a file
              <br />
              Accepted file types: {acceptedFileTypes.map(type => type.split('/')[1]).join(', ')}
            </>
          )}
        </div>
      </label>
    </div>
  );
}
