from typing import Union, Dict, Any
import pandas as pd
import google.generativeai as genai

class VisualizationAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def _format_data(self, data: Union[pd.DataFrame, str, Dict[str, Any]]) -> str:
        """Convert different data formats to a string representation"""
        if isinstance(data, pd.DataFrame):
            return data.to_json(orient='records')
        elif isinstance(data, dict):
            return str(data)
        return str(data)
    
    def generate_visualization_code(
        self, 
        prompt: str, 
        data: Union[pd.DataFrame, str, Dict[str, Any]]
    ) -> str:
        # Convert data to a consistent format
        data_description = self._format_data(data)
        
        # Construct the prompt
        system_prompt = """
        You are a visualization expert. Generate a React component using Recharts library that:
        1. Is named 'Chart'
        2. Accepts no props (data is available in scope as 'data' variable)
        3. Returns a single visualization wrapped in ResponsiveContainer
        4. Uses appropriate chart type based on the data and goal
        5. DO NOT include imports or data declarations
        6. DO NOT export the component
        
        Example format:
        const Chart = () => {
          return (
            <ResponsiveContainer width="100%" height="100%">
              {/* Chart implementation here */}
            </ResponsiveContainer>
          );
        };
        """
        
        full_prompt = f"""
        {system_prompt}
        
        Visualization Goal: {prompt}
        
        Data Structure: {data_description}
        
        Generate only the Chart component code.
        """
        
        # Get response from Gemini
        response = self.model.generate_content(full_prompt)
        
        return response.text 