'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function ThreeDViewer() {
  // In a real implementation, this would use Three.js to render a 3D model
  // For now, we'll create a placeholder component
  
  const [viewMode, setViewMode] = useState('solid');
  const [showElements, setShowElements] = useState({
    walls: true,
    windows: true,
    doors: true,
    roofs: true
  });
  
  return (
    <div className="w-full h-full">
      <div className="bg-gray-800 rounded-lg p-4 h-96 flex items-center justify-center mb-4">
        <div className="text-center text-white">
          <div className="border-2 border-dashed border-gray-600 p-12 rounded-lg">
            <h3 className="text-xl mb-4">3D Model Viewer</h3>
            <p className="text-gray-400 mb-6">
              This is a placeholder for the Three.js 3D model viewer.
            </p>
            <p className="text-sm text-gray-500">
              In the actual implementation, this would display an interactive 3D model
              of the building created from the uploaded plans.
            </p>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <h3 className="font-medium mb-2">View Controls</h3>
          <div className="flex flex-wrap gap-2">
            <button 
              className={`px-3 py-1 rounded ${viewMode === 'solid' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
              onClick={() => setViewMode('solid')}
            >
              Solid
            </button>
            <button 
              className={`px-3 py-1 rounded ${viewMode === 'wireframe' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
              onClick={() => setViewMode('wireframe')}
            >
              Wireframe
            </button>
            <button 
              className={`px-3 py-1 rounded ${viewMode === 'xray' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
              onClick={() => setViewMode('xray')}
            >
              X-Ray
            </button>
            <button className="px-3 py-1 rounded bg-gray-200">
              Reset View
            </button>
          </div>
        </div>
        
        <div>
          <h3 className="font-medium mb-2">Show/Hide Elements</h3>
          <div className="flex flex-wrap gap-2">
            <label className="flex items-center">
              <input 
                type="checkbox" 
                checked={showElements.walls}
                onChange={() => setShowElements({...showElements, walls: !showElements.walls})}
                className="mr-1"
              />
              Walls
            </label>
            <label className="flex items-center">
              <input 
                type="checkbox" 
                checked={showElements.windows}
                onChange={() => setShowElements({...showElements, windows: !showElements.windows})}
                className="mr-1"
              />
              Windows
            </label>
            <label className="flex items-center">
              <input 
                type="checkbox" 
                checked={showElements.doors}
                onChange={() => setShowElements({...showElements, doors: !showElements.doors})}
                className="mr-1"
              />
              Doors
            </label>
            <label className="flex items-center">
              <input 
                type="checkbox" 
                checked={showElements.roofs}
                onChange={() => setShowElements({...showElements, roofs: !showElements.roofs})}
                className="mr-1"
              />
              Roofs
            </label>
          </div>
        </div>
      </div>
      
      <div className="text-sm text-gray-500">
        <p>Current view mode: <span className="font-medium">{viewMode}</span></p>
        <p>Visible elements: {Object.entries(showElements)
          .filter(([_, isVisible]) => isVisible)
          .map(([element]) => element)
          .join(', ')}
        </p>
      </div>
    </div>
  );
}
