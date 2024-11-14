from typing import Dict
import requests
import json
import os
from datetime import datetime

class QueryDecomposer:
    """
    A conversational agent that breaks down complex stock-related queries into steps
    using Gemini Flash API.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.system_prompt = """You are a financial query decomposition expert. Break down complex stock-related queries into logical steps.

For each query, provide:
1. A list of sequential steps needed to answer the query
2. For each step, specify what data is needed
3. Time period and frequency of data required

Available data types from our Polygon.io API:
- Stock prices (daily/quarterly closing prices)
- Financial statements (quarterly income statements, balance sheets)
- Basic company info (market cap, sector)

Format your response as JSON with this structure:
{
    "query": "original query",
    "steps": [
        {
            "step_number": 1,
            "description": "what needs to be done",
            "required_data": ["list of data points needed"],
            "time_period": "required time range",
            "frequency": "data frequency"
        }
    ]
}

Ensure your response is ONLY the JSON object, with no additional text."""

    def call_gemini_api(self, prompt: str) -> Dict:
        """Call Gemini Flash API with the given prompt."""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{self.system_prompt}\n\nQuery to decompose: {prompt}"
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            f"{url}?key={self.api_key}", 
            headers=headers, 
            json=data
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API call failed: {response.status_code}, {response.text}")

    async def decompose_query(self, query: str) -> Dict:
        """Decompose a natural language query into structured steps."""
        try:
            # Call Gemini API
            response = self.call_gemini_api(query)
            
            # Extract the JSON response from Gemini's output
            # Assuming the response contains the text in the first candidate's content
            text_response = response['candidates'][0]['content']['parts'][0]['text']
            
            # Parse the text response into JSON
            # Remove any potential markdown formatting
            json_str = text_response.strip('```json').strip('```').strip()
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error decomposing query: {str(e)}")
            return None 