import React, { useState } from 'react';
import DynamicVisualization from './DynamicVisualization';

export default function VisualizationPage() {
  const [prompt, setPrompt] = useState('');
  const [visualizationCode, setVisualizationCode] = useState('');
  const [data, setData] = useState<Record<string, any[]> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVisualizationRequest = async () => {
    if (!prompt.trim()) {
      setError('Please enter a visualization prompt');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/generate-visualization', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }

      setVisualizationCode(result.visualizationCode);
      setData(result.data);
    } catch (err) {
      console.error('Error fetching visualization:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="space-y-6">
        {/* Input Section */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-purple-200">
            Data Visualization
          </h2>
          <div className="flex gap-4">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the visualization you want..."
              className="flex-1 p-3 rounded-xl bg-white/5 border border-purple-500/20 
                         text-purple-100 placeholder-purple-400/50 focus:outline-none 
                         focus:border-purple-500/50"
            />
            <button
              onClick={handleVisualizationRequest}
              disabled={loading}
              className="px-6 py-3 bg-purple-500/20 hover:bg-purple-500/30 
                       text-purple-200 rounded-xl border border-purple-500/30
                       disabled:opacity-50 disabled:cursor-not-allowed
                       transition-all duration-200"
            >
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
            {error}
          </div>
        )}

        {/* Visualization Output */}
        {visualizationCode && data && (
          <div className="border border-purple-500/20 rounded-xl overflow-hidden">
            <DynamicVisualization
              visualizationCode={visualizationCode}
              data={data}
            />
          </div>
        )}
      </div>
    </div>
  );
} 