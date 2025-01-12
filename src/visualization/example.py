import os
from dotenv import load_dotenv
from src.agents.visualization_agent import VisualizationAgent

# Load environment variables
load_dotenv()

# Initialize the agent with Gemini key
agent = VisualizationAgent(api_key=os.getenv('GOOGLE_API_KEY'))

# Example usage
data = {
    'company': ['Apple', 'Microsoft', 'Amazon'],
    'revenue 2022': [280, 250, 260],
    'revenue 2023': [300, 280, 280]
}

visualization_code = agent.generate_visualization_code(
    prompt="Plot Apple revenue in 2022 and 2023",
    data=data
)
print(visualization_code)