import asyncio
from agents.query_decomposer import QueryDecomposer
import json

async def main():
    # Sample queries to test decomposition
    test_queries = [
        "Compare revenue growth rates of AAPL, MSFT, and GOOGL over the last 4 quarters",
        "Calculate the market cap weighted index of ADBE, CRM, and NOW for the past 5 years, showing quarterly returns",
        "Which of the top 10 S&P 500 companies had the highest operating margin in the last quarter?"
    ]
    
    decomposer = QueryDecomposer()
    
    for query in test_queries:
        print(f"\nProcessing query: {query}")
        print("=" * 50)
        
        result = await decomposer.decompose_query(query)
        if result:
            print(json.dumps(result, indent=2))
        print("\n")

if __name__ == "__main__":
    asyncio.run(main()) 