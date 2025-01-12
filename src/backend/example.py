import os
from src.agents.visualization_agent import VisualizationAgent


# Initialize the agent with Gemini key
agent = VisualizationAgent()

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