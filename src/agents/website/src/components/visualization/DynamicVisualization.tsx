import React, { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ScatterChart,
  Scatter
} from 'recharts';
import { transform } from '@babel/standalone';

interface DynamicVisualizationProps {
  visualizationCode: string;
  data: Record<string, any[]>;
}

const DynamicVisualization: React.FC<DynamicVisualizationProps> = ({
  visualizationCode,
  data
}) => {
  const [error, setError] = useState<string | null>(null);
  const [RenderedComponent, setRenderedComponent] = useState<React.FC | null>(null);

  const transformData = (record: Record<string, any[]>): any[] => {
    const keys = Object.keys(record);
    if (keys.length === 0) return [];
    
    return record[keys[0]].map((_, index) => {
      const item: Record<string, any> = {};
      keys.forEach(key => {
        item[key] = record[key][index];
      });
      return item;
    });
  };

  useEffect(() => {
    if (!visualizationCode) return;

    try {
      // Clean the code
      const cleanCode = visualizationCode
        .replace(/```[^`]*```/g, (match) => match.replace(/```typescript|```jsx|```/g, ''))
        .replace(/import.*?;?\n/g, '')
        .replace(/export default/g, '')
        .trim();

      console.log('Clean code:', cleanCode);

      // Transform JSX to JavaScript using Babel
      const transformedCode = transform(cleanCode, {
        presets: [['react', { runtime: 'classic' }]],
        filename: 'dynamic.jsx',
        configFile: false,
        babelrc: false
      }).code;

      console.log('Transformed code:', transformedCode);

      const transformedData = transformData(data);
      console.log('Transformed data:', transformedData);

      // Create the component factory
      const componentFactory = new Function(
        'React',
        'ResponsiveContainer',
        'BarChart',
        'Bar',
        'LineChart',
        'Line',
        'XAxis',
        'YAxis',
        'Tooltip',
        'Legend',
        'CartesianGrid',
        'ScatterChart',
        'Scatter',
        'chartData',
        `
        "use strict";
        const data = chartData;
        ${transformedCode}
        return Chart;
        `
      );

      // Execute the factory with dependencies
      const Component = componentFactory(
        React,
        ResponsiveContainer,
        BarChart,
        Bar,
        LineChart,
        Line,
        XAxis,
        YAxis,
        Tooltip,
        Legend,
        CartesianGrid,
        ScatterChart,
        Scatter,
        transformedData
      );

      if (!Component) {
        throw new Error('Component creation failed');
      }

      setRenderedComponent(() => Component);
      setError(null);
    } catch (err) {
      console.error('Error creating visualization:', err);
      setError(`Failed to create visualization: ${err.message}`);
    }
  }, [visualizationCode, data]);

  if (error) {
    return (
      <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
        {error}
      </div>
    );
  }

  if (!RenderedComponent) {
    return (
      <div className="p-4 text-purple-200 animate-pulse">
        Loading visualization...
      </div>
    );
  }

  return (
    <div className="w-full h-[500px] bg-white/5 backdrop-blur-md rounded-xl p-4">
      <RenderedComponent />
    </div>
  );
};

export default DynamicVisualization;
