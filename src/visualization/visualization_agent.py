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
        You are a visualization expert. Given data and a user's intent:
        1. Analyze the data structure and the visualization goal
        2. Choose the most appropriate visualization type
        3. Generate TypeScript code using a visualization library (preferably Recharts or Chart.js)
        4. Include all necessary imports and typing
        Provide only the complete, working TypeScript code without explanations.
        """
        
        full_prompt = f"""
        {system_prompt}
        
        Visualization Goal: {prompt}
        
        Data: {data_description}
        
        Generate TypeScript code for the most appropriate visualization.
        """
        
        # Get response from Gemini
        response = self.model.generate_content(full_prompt)
        
        return response.text 