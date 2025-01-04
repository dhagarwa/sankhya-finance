import React, { useState } from 'react';
import DynamicVisualization from './DynamicVisualization';

export default function VisualizationPage() {
  const [prompt, setPrompt] = useState('');
  const [visualizationCode, setVisualizationCode] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVisualizationRequest = async () => {
    try {
      setLoading(true);
      const response = await fetch('api/generate-visualization', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      console.log('Response:', result);
      setVisualizationCode(result.visualizationCode);
      setData(result.data);
    } catch (error) {
      console.error('Error fetching visualization:', error);
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="p-4">
      <div className="mb-4">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your visualization prompt..."
          className="w-full p-2 border rounded"
        />
        <button
          onClick={handleVisualizationRequest}
          disabled={loading}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          {loading ? 'Generating...' : 'Generate Visualization'}
        </button>
      </div>

      {visualizationCode && data && (
        <div className="border rounded p-4">
          <DynamicVisualization
            visualizationCode={visualizationCode}
            data={data}
          />
        </div>
      )}
    </div>
  );
} 