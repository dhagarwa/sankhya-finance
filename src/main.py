import asyncio
from agents.query_decomposer import QueryDecomposer
import json

async def test_query_decomposition():
    # Sample queries to test decomposition
    test_queries = [
        "Compare revenue growth rates of AAPL, MSFT, and GOOGL over the last 4 quarters",
        "Calculate the market cap weighted index of ADBE, CRM, and NOW for the past 5 years, showing quarterly returns",
        "Which of the top 10 S&P 500 companies had the highest operating margin in the last quarter?",
        # Add more test queries here
    ]
    
    # Initialize the decomposer
    decomposer = QueryDecomposer()
    
    # Process each query
    for query in test_queries:
        print(f"\nProcessing query: {query}")
        print("=" * 80)
        
        try:
            # Decompose the query
            result = await decomposer.decompose_query(query)
            
            if result:
                # Pretty print the result
                print("\nDecomposed steps:")
                print(json.dumps(result, indent=2))
            else:
                print("Failed to decompose query")
                
        except Exception as e:
            print(f"Error processing query: {str(e)}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(test_query_decomposition()) 