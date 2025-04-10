'use client';

import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import { checkHealth, generateModel, getResultFileUrl } from '../services/api';
import type { UploadResult } from '../services/api';

export default function Page() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [floorPlans, setFloorPlans] = useState<UploadResult[]>([]);
  const [elevations, setElevations] = useState<UploadResult[]>([]);
  const [modelResult, setModelResult] = useState<{ modelFile: string; gbxmlFile: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Check API health on component mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        await checkHealth();
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
        setError('API is offline. Please start the backend server.');
      }
    };

    checkApiHealth();
  }, []);

  const handleFloorPlanUpload = (result: UploadResult) => {
    setFloorPlans([...floorPlans, result]);
    setError(null);
  };

  const handleElevationUpload = (result: UploadResult) => {
    setElevations([...elevations, result]);
    setError(null);
  };

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleGenerateModel = async () => {
    if (floorPlans.length === 0) {
      setError('Please upload at least one floor plan');
      return;
    }

    if (elevations.length === 0) {
      setError('Please upload at least one elevation');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await generateModel(
        floorPlans.map(fp => fp.result_file),
        elevations.map(el => el.result_file)
      );

      setModelResult({
        modelFile: result.model_file,
        gbxmlFile: result.gbxml_file,
      });
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to generate model');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Building to 3D Models</h1>
      
      {apiStatus === 'checking' && <p>Checking API status...</p>}
      
      {apiStatus === 'offline' && (
        <div className="error-message">
          <p>API is offline. Please start the backend server.</p>
        </div>
      )}
      
      {apiStatus === 'online' && (
        <>
          <div className="upload-section">
            <div className="upload-container">
              <FileUpload
                fileType="floorPlan"
                onUploadSuccess={handleFloorPlanUpload}
                onUploadError={handleUploadError}
                floorLevel={0}
              />
              
              {floorPlans.length > 0 && (
                <div className="uploaded-files">
                  <h4>Uploaded Floor Plans:</h4>
                  <ul>
                    {floorPlans.map((plan, index) => (
                      <li key={index}>
                        {plan.filename} (Floor {plan.floor_level})
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            
            <div className="upload-container">
              <FileUpload
                fileType="elevation"
                onUploadSuccess={handleElevationUpload}
                onUploadError={handleUploadError}
                orientation="north"
              />
              
              {elevations.length > 0 && (
                <div className="uploaded-files">
                  <h4>Uploaded Elevations:</h4>
                  <ul>
                    {elevations.map((elevation, index) => (
                      <li key={index}>
                        {elevation.filename} ({elevation.orientation})
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
          
          <div className="generate-section">
            <button
              onClick={handleGenerateModel}
              disabled={loading || floorPlans.length === 0 || elevations.length === 0}
            >
              {loading ? 'Generating...' : 'Generate 3D Model'}
            </button>
            
            {error && <div className="error-message">{error}</div>}
            
            {modelResult && (
              <div className="model-result">
                <h3>Generated Model:</h3>
                <p>
                  <a
                    href={getResultFileUrl(modelResult.modelFile)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download 3D Model
                  </a>
                </p>
                <p>
                  <a
                    href={getResultFileUrl(modelResult.gbxmlFile)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download gbXML File
                  </a>
                </p>
              </div>
            )}
          </div>
        </>
      )}
    </main>
  );
}