from enum import Enum
from typing import Dict, Tuple

class AgentType(Enum):
    DATA_RETRIEVAL = "data_retrieval"
    CALCULATION = "calculation"
    VISUALIZATION = "visualization"
    NONE = "none"

class StepClassifier:
    """Classifies decomposed steps to determine appropriate agent"""
    
    @staticmethod
    def classify_step(step: Dict) -> Tuple[AgentType, str]:
        description = step["description"].lower()
        required_data = step["required_data"]
        
        # Data Retrieval steps
        if any(keyword in description for keyword in ["get", "fetch", "retrieve", "find"]):
            return AgentType.DATA_RETRIEVAL, "Fetch required data from YFinance"
            
        # Calculation steps
        # elif any(keyword in description for keyword in ["calculate", "compute", "compare", "analyze"]):
        #     if not required_data:  # If we already have the data
        #         return AgentType.CALCULATION, "Perform calculations on existing data"
        #     return AgentType.DATA_RETRIEVAL, "Need to fetch data first"
            
        # # Visualization steps
        # elif any(keyword in description for keyword in ["plot", "graph", "visualize", "show"]):
        #     return AgentType.VISUALIZATION, "Create visualization"
            
        return AgentType.NONE, "No suitable agent available yet" 