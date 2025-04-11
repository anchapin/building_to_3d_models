'use client';

import { useState } from 'react';
import { FileUploadDropzone } from '@/components/FileUploadDropzone';
import { ScaleConfigurationTool } from '@/components/ScaleConfigurationTool';
import Link from 'next/link';
import { uploadFile, setScale, generateModel } from '@/lib/api';

export default function UploadPage() {
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationResult, setGenerationResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File, type: string, orientation?: string, floorLevel?: number) => {
    try {
      setError(null);
      const result = await uploadFile(file, type, orientation, floorLevel);
      
      setUploadedFiles(prev => [...prev, {
        ...result,
        type,
        orientation,
        floorLevel,
        hasScale: false
      }]);
    } catch (err: any) {
      setError(err.message || 'Failed to upload file');
    }
  };

  const handleSetScale = async (imageId: string, pixelLength: number, realLength: number, unit: string = 'meters') => {
    try {
      setError(null);
      await setScale(imageId, pixelLength, realLength, unit);
      
      // Update the file's scale status
      setUploadedFiles(prev => prev.map(file => 
        file.filename.startsWith(imageId) ? { ...file, hasScale: true } : file
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to set scale');
    }
  };

  const handleGenerateModel = async () => {
    try {
      setError(null);
      setIsGenerating(true);
      
      const floorPlans = uploadedFiles
        .filter(file => file.file_type === 'floorPlan')
        .map(file => file.result_file);
        
      const elevations = uploadedFiles
        .filter(file => file.file_type === 'elevation')
        .map(file => file.result_file);
      
      if (floorPlans.length === 0) {
        throw new Error('At least one floor plan is required');
      }
      
      const result = await generateModel(floorPlans, elevations);
      setGenerationResult(result);
    } catch (err: any) {
      setError(err.message || 'Failed to generate model');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col p-8">
      <h1 className="text-3xl font-bold mb-8">Upload Building Plans</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div>
          <h2 className="text-xl font-bold mb-4">Floor Plans</h2>
          <FileUploadDropzone 
            onUpload={(file) => handleFileUpload(file, 'floorPlan', undefined, 0)}
            acceptedFileTypes={['image/png', 'image/jpeg', 'application/pdf']}
            label="Upload Floor Plan"
            fileType="floorPlan"
          />
        </div>
        
        <div>
          <h2 className="text-xl font-bold mb-4">Elevations</h2>
          <FileUploadDropzone 
            onUpload={(file) => handleFileUpload(file, 'elevation', 'north')}
            acceptedFileTypes={['image/png', 'image/jpeg', 'application/pdf']}
            label="Upload North Elevation"
            fileType="elevation"
            orientation="north"
          />
          <div className="mt-4">
            <FileUploadDropzone 
              onUpload={(file) => handleFileUpload(file, 'elevation', 'east')}
              acceptedFileTypes={['image/png', 'image/jpeg', 'application/pdf']}
              label="Upload East Elevation"
              fileType="elevation"
              orientation="east"
            />
          </div>
        </div>
      </div>
      
      {uploadedFiles.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-bold mb-4">Uploaded Files</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border">
              <thead>
                <tr>
                  <th className="py-2 px-4 border">Filename</th>
                  <th className="py-2 px-4 border">Type</th>
                  <th className="py-2 px-4 border">Details</th>
                  <th className="py-2 px-4 border">Scale</th>
                </tr>
              </thead>
              <tbody>
                {uploadedFiles.map((file, index) => (
                  <tr key={index}>
                    <td className="py-2 px-4 border">{file.filename}</td>
                    <td className="py-2 px-4 border">{file.file_type}</td>
                    <td className="py-2 px-4 border">
                      {file.file_type === 'floorPlan' ? `Floor Level: ${file.floor_level}` : `Orientation: ${file.orientation}`}
                    </td>
                    <td className="py-2 px-4 border">
                      {file.hasScale ? (
                        <span className="text-green-500">✓ Scale Set</span>
                      ) : (
                        <ScaleConfigurationTool 
                          imageId={file.filename.split('.')[0]}
                          onSetScale={handleSetScale}
                        />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {uploadedFiles.length > 0 && uploadedFiles.every(file => file.hasScale) && (
        <div className="flex justify-center mb-8">
          <button
            onClick={handleGenerateModel}
            disabled={isGenerating}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            {isGenerating ? 'Generating...' : 'Generate 3D Model'}
          </button>
        </div>
      )}
      
      {generationResult && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          <h3 className="font-bold">Model Generated Successfully!</h3>
          <p className="mt-2">You can now download the generated files:</p>
          <div className="mt-4 flex space-x-4">
            <a 
              href={`http://localhost:5000/api/results/${generationResult.model_file}`}
              download
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Download 3D Model (.obj)
            </a>
            <a 
              href={`http://localhost:5000/api/results/${generationResult.gbxml_file}`}
              download
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Download gbXML
            </a>
          </div>
        </div>
      )}
      
      <div className="mt-8">
        <Link href="/" className="text-blue-500 hover:underline">
          ← Back to Home
        </Link>
      </div>
    </main>
  );
}
