'use client';

import { useState } from 'react';

interface ScaleConfigurationToolProps {
  imageId: string;
  onSetScale: (imageId: string, pixelLength: number, realLength: number, unit: string) => void;
}

export function ScaleConfigurationTool({ imageId, onSetScale }: ScaleConfigurationToolProps) {
  const [pixelLength, setPixelLength] = useState<number>(100);
  const [realLength, setRealLength] = useState<number>(5);
  const [unit, setUnit] = useState<string>('meters');
  const [isSettingScale, setIsSettingScale] = useState(false);
  
  const handleSetScale = async () => {
    try {
      setIsSettingScale(true);
      await onSetScale(imageId, pixelLength, realLength, unit);
    } finally {
      setIsSettingScale(false);
    }
  };
  
  return (
    <div className="flex flex-col space-y-2">
      <div className="flex items-center space-x-2">
        <input
          type="number"
          value={pixelLength}
          onChange={(e) => setPixelLength(Number(e.target.value))}
          className="border rounded px-2 py-1 w-20"
          placeholder="Pixels"
        />
        <span>pixels =</span>
        <input
          type="number"
          value={realLength}
          onChange={(e) => setRealLength(Number(e.target.value))}
          className="border rounded px-2 py-1 w-20"
          placeholder="Length"
        />
        <select
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
          className="border rounded px-2 py-1"
        >
          <option value="meters">meters</option>
          <option value="feet">feet</option>
          <option value="inches">inches</option>
        </select>
      </div>
      <button
        onClick={handleSetScale}
        disabled={isSettingScale || pixelLength <= 0 || realLength <= 0}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded text-sm disabled:opacity-50"
      >
        {isSettingScale ? 'Setting Scale...' : 'Set Scale'}
      </button>
    </div>
  );
}
