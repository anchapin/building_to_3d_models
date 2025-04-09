'use client';

import { useState } from 'react';

export default function ScaleConfigurationTool({ imageUrl, onScaleSet }) {
  const [startPoint, setStartPoint] = useState(null);
  const [endPoint, setEndPoint] = useState(null);
  const [realWorldLength, setRealWorldLength] = useState('');
  const [unit, setUnit] = useState('feet');
  const [step, setStep] = useState(1);

  const handleImageClick = (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    if (step === 1) {
      setStartPoint({ x, y });
      setStep(2);
    } else if (step === 2) {
      setEndPoint({ x, y });
      setStep(3);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!startPoint || !endPoint || !realWorldLength) {
      alert('Please complete all steps');
      return;
    }
    
    // Calculate pixel distance
    const pixelDistance = Math.sqrt(
      Math.pow(endPoint.x - startPoint.x, 2) + 
      Math.pow(endPoint.y - startPoint.y, 2)
    );
    
    // Calculate scale (units per pixel)
    const scale = parseFloat(realWorldLength) / pixelDistance;
    
    // Call the callback with the scale information
    onScaleSet({
      scale,
      unit,
      pixelDistance,
      realWorldLength: parseFloat(realWorldLength)
    });
    
    // Reset for next use
    setStartPoint(null);
    setEndPoint(null);
    setRealWorldLength('');
    setStep(1);
  };

  const resetSelection = () => {
    setStartPoint(null);
    setEndPoint(null);
    setStep(1);
  };

  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-lg font-medium mb-2">Scale Configuration Tool</h3>
      
      <div className="mb-4">
        <p className="text-sm text-gray-600 mb-2">
          {step === 1 && 'Step 1: Click on the first point of a known dimension'}
          {step === 2 && 'Step 2: Click on the second point of the same dimension'}
          {step === 3 && 'Step 3: Enter the real-world length of this dimension'}
        </p>
        
        <div 
          className="relative border bg-gray-100 h-64 flex items-center justify-center cursor-crosshair"
          onClick={step < 3 ? handleImageClick : null}
        >
          {imageUrl ? (
            <img 
              src={imageUrl} 
              alt="Building plan" 
              className="max-h-full max-w-full object-contain"
            />
          ) : (
            <div className="text-gray-400">Image preview</div>
          )}
          
          {startPoint && (
            <div 
              className="absolute h-4 w-4 bg-red-500 rounded-full -ml-2 -mt-2"
              style={{ left: startPoint.x, top: startPoint.y }}
            ></div>
          )}
          
          {endPoint && (
            <>
              <div 
                className="absolute h-4 w-4 bg-red-500 rounded-full -ml-2 -mt-2"
                style={{ left: endPoint.x, top: endPoint.y }}
              ></div>
              <div 
                className="absolute bg-red-500 h-0.5"
                style={{
                  left: Math.min(startPoint.x, endPoint.x),
                  top: startPoint.y + (endPoint.y - startPoint.y) / 2,
                  width: Math.abs(endPoint.x - startPoint.x),
                  transform: `rotate(${Math.atan2(endPoint.y - startPoint.y, endPoint.x - startPoint.x) * 180 / Math.PI}deg)`,
                  transformOrigin: 'left center'
                }}
              ></div>
            </>
          )}
        </div>
      </div>
      
      {step === 3 && (
        <form onSubmit={handleSubmit} className="mb-4">
          <div className="flex items-center">
            <label className="mr-2">Real-world length:</label>
            <input
              type="number"
              step="0.01"
              min="0.1"
              value={realWorldLength}
              onChange={(e) => setRealWorldLength(e.target.value)}
              required
              className="border rounded px-2 py-1 w-20 mr-2"
            />
            <select 
              value={unit}
              onChange={(e) => setUnit(e.target.value)}
              className="border rounded px-2 py-1"
            >
              <option value="feet">feet</option>
              <option value="meters">meters</option>
              <option value="inches">inches</option>
              <option value="cm">centimeters</option>
            </select>
          </div>
          
          <div className="flex mt-4 space-x-2">
            <button
              type="button"
              onClick={resetSelection}
              className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded"
            >
              Reset Points
            </button>
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
            >
              Set Scale
            </button>
          </div>
        </form>
      )}
      
      <div className="text-xs text-gray-500">
        <p>Instructions:</p>
        <ol className="list-decimal ml-4">
          <li>Click on the first point of a known dimension (e.g., door width)</li>
          <li>Click on the second point of the same dimension</li>
          <li>Enter the real-world length of this dimension</li>
        </ol>
      </div>
    </div>
  );
}
