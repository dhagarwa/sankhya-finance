import React, { useEffect, useState } from 'react';
// We will use Babel standalone to transform the string code into runnable JS
import { transform } from '@babel/standalone';

// Recharts (or any other libraries you expect the server code to use)
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  // Add any other Recharts components as needed
} from 'recharts';

interface DynamicVisualizationProps {
  visualizationCode: string; // The code string returned by your API, e.g. the "```typescript ...```" snippet
  data: any;                // The JSON data returned by your API
}

const DynamicVisualization: React.FC<DynamicVisualizationProps> = ({
  visualizationCode,
  data
}) => {
  const [RenderedComponent, setRenderedComponent] = useState<React.FC | null>(
    null
  );

  useEffect(() => {
    if (!visualizationCode) return;

    try {
      // 1. Strip out possible markdown fences (```typescript ...```) to get raw TS/JS code
      const codeWithoutFences = visualizationCode.replace(/```[^`]*```/g, (match) => {
        // Attempt to remove just the triple backticks. If your server always returns the code
        // in a consistent format, you can customize logic here as needed.
        return match.replace(/```typescript|```js|```/g, '');
      });

      // 2. Transform code from TypeScript/JSX -> plain JS that can run in the browser
      // Using presets: ['typescript', 'react'] if the code is indeed TypeScript
      // If your code is plain JavaScript/JSX, you can omit 'typescript'.
      const transformedCode = transform(codeWithoutFences, {
        presets: ['typescript', 'react'],
        filename: 'file.tsx', // or 'file.tsx'
      }).code;
      

      // 3. Create a new Function and return the default or named component
      //    We'll assume the server code defines a component called "CompanyGrowth"
      //    and exports it as default or returns it at the end.
      //    Adapt the variable name to match the component name from your server code.
      //
      //    We also inject references to React, Recharts, and "data" in the arguments
      //    so that the server code can reference them if needed.
      const componentFactory = new Function(
        'React',
        'BarChart',
        'Bar',
        'XAxis',
        'YAxis',
        'Tooltip',
        'Legend',
        'data',
        `${transformedCode}\n\nreturn CompanyGrowth;`
      );

      // 4. Invoke the factory to retrieve the component
      const ComponentFromServer = componentFactory(
        React,
        BarChart,
        Bar,
        XAxis,
        YAxis,
        Tooltip,
        Legend,
        data
      );

      // 5. Set the component to local state so we can render it
      setRenderedComponent(() => ComponentFromServer);
    } catch (error) {
      console.error('Error dynamically generating component:', error);
      setRenderedComponent(null);
    }
  }, [visualizationCode, data]);

  // If we haven't successfully created a component, show nothing or a fallback
  if (!RenderedComponent) {
    return null;
  }

  // Render the dynamically-created component
  return <RenderedComponent />;
};

export default DynamicVisualization;
