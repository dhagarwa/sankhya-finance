from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import os

class Step(BaseModel):
    """Schema for each decomposition step"""
    step_number: int = Field(description="The order number of this step")
    description: str = Field(description="What needs to be done")
    required_data: List[str] = Field(description="List of data points needed")
    time_period: str = Field(description="Required time range")
    frequency: str = Field(description="Data frequency")

class QueryDecomposition(BaseModel):
    """Schema for the complete decomposition"""
    query: str = Field(description="Original query")
    steps: List[Step] = Field(description="List of decomposition steps")

class QueryDecomposer:
    """
    A conversational agent that breaks down complex stock-related queries into steps
    using Gemini Flash API via LangChain.
    """
    
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        
        # Initialize the output parser
        self.parser = JsonOutputParser(pydantic_object=QueryDecomposition)
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial query decomposition expert. Break down complex stock-related queries into logical steps.

Available data types from our Polygon.io API:
- Stock prices (daily/quarterly closing prices)
- Financial statements (quarterly income statements, balance sheets)
- Basic company info (market cap, sector)

{format_instructions}"""),
            ("user", "{query}")
        ])

    async def decompose_query(self, query: str) -> Dict:
        """Decompose a natural language query into structured steps."""
        try:
            # Create the chain
            chain = self.prompt | self.llm | self.parser
            
            # Run the chain
            result = await chain.ainvoke({
                "query": query,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            return result
            
        except Exception as e:
            print(f"Error decomposing query: {str(e)}")
            return None 