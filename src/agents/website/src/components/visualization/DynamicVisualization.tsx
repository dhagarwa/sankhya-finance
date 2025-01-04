import React, { useEffect, useState } from 'react';
import { transform } from '@babel/standalone';
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
  CartesianGrid
} from 'recharts';

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

  useEffect(() => {
    if (!visualizationCode) return;

    try {
      // Clean the code - remove markdown and imports
      const cleanCode = visualizationCode
        .replace(/```[^`]*```/g, (match) => match.replace(/```typescript|```jsx|```/g, ''))
        .replace(/import.*?;?\n/g, '')
        .replace(/export default/g, '')
        .trim();

      // Transform the code
      const transformedCode = transform(cleanCode, {
        presets: ['react', 'typescript'],
        filename: 'dynamic.tsx'
      }).code;

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
        'chartData',
        `
        const data = chartData;
        ${transformedCode}
        return typeof Chart !== 'undefined' ? Chart : CompanyGrowthChart;
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
        data
      );

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
