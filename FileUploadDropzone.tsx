'use client';

import { useState } from 'react';

export default function FileUploadDropzone({ accept, multiple, onFilesSelected, label }) {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState([]);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragging) {
      setIsDragging(true);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) {
      handleFiles(droppedFiles);
    }
  };

  const handleFileInputChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
      handleFiles(selectedFiles);
    }
  };

  const handleFiles = (selectedFiles) => {
    // Filter files based on accept prop if provided
    let filteredFiles = selectedFiles;
    if (accept) {
      const acceptedTypes = accept.split(',').map(type => type.trim());
      filteredFiles = selectedFiles.filter(file => {
        return acceptedTypes.some(type => {
          if (type.startsWith('.')) {
            // Check file extension
            return file.name.toLowerCase().endsWith(type.toLowerCase());
          } else {
            // Check MIME type
            return file.type.match(new RegExp(type.replace('*', '.*')));
          }
        });
      });
    }

    // Handle multiple files or just take the first one
    const newFiles = multiple ? [...files, ...filteredFiles] : filteredFiles.slice(0, 1);
    
    setFiles(newFiles);
    if (onFilesSelected) {
      onFilesSelected(newFiles);
    }
  };

  const removeFile = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
    if (onFilesSelected) {
      onFilesSelected(newFiles);
    }
  };

  return (
    <div className="w-full">
      <div 
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleFileInputChange}
          className="hidden"
          id="file-upload"
        />
        <label 
          htmlFor="file-upload"
          className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded cursor-pointer inline-block mb-4"
        >
          {label || 'Select Files'}
        </label>
        <p className="text-sm text-gray-500">
          or drag and drop files here
        </p>
        {accept && (
          <p className="text-xs text-gray-400 mt-2">
            Accepted file types: {accept}
          </p>
        )}
      </div>

      {files.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-medium mb-2">Selected Files:</h4>
          <ul className="text-sm">
            {files.map((file, index) => (
              <li key={index} className="flex justify-between items-center py-1">
                <div>
                  {file.name} ({(file.size / 1024).toFixed(1)} KB)
                </div>
                <button 
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700"
                  type="button"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
