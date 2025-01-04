import os
from dotenv import load_dotenv
from visualization_agent import VisualizationAgent

# Load environment variables
load_dotenv()

# Initialize the agent with Gemini key
agent = VisualizationAgent(api_key=os.getenv('GOOGLE_API_KEY'))

# Example usage
data = {
    'company': ['Apple', 'Microsoft', 'Amazon'],
    '2022': [280, 250, 260],
    '2023': [300, 280, 280]
}

visualization_code = agent.generate_visualization_code(
    prompt="Compare company growth between 2022 and 2023",
    data=data
)
print(visualization_code)