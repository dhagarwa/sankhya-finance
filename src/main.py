import asyncio
from agents.query_decomposer import QueryDecomposer
from agents.data_retrieval_agent import DataRetrievalAgent
import json
import pandas as pd

async def analyze_query(query: str):
    print("\n" + "="*80)
    print(f"Starting analysis for query: {query}")
    print("="*80)
    
    # Initialize agents
    print("\n1. Initializing agents...")
    decomposer = QueryDecomposer()
    retriever = DataRetrievalAgent()
    print("✓ Agents initialized successfully")
    
    try:
        # Step 1: Decompose the query
        print("\n2. Decomposing query...")
        decomposed = await decomposer.decompose_query(query)
        
        if not decomposed:
            print("✗ Query decomposition failed")
            raise ValueError("Query decomposition failed")
            
        print("✓ Query successfully decomposed into steps:")
        print(json.dumps(decomposed, indent=2))
        
        # Step 2: Execute the plan
        print("\n3. Executing data retrieval plan...")
        results = await retriever.execute_plan(decomposed)
        print("✓ Data retrieval completed")
        
        # Step 3: Process results
        print("\n4. Processing results:")
        for result in results:
            print(f"\nStep {result['step_number']}: {result['description']}")
            if result['error']:
                print(f"✗ Error: {result['error']}")
            elif isinstance(result['data'], pd.DataFrame):
                print("✓ Data retrieved (showing first 5 rows):")
                print("-"*40)
                print(result['data'].head())
                print("-"*40)
            elif isinstance(result['data'], dict):
                print("✓ Historical data retrieved for tickers:", list(result['data'].keys()))
                for ticker, df in result['data'].items():
                    print(f"\n{ticker} data (showing first 3 rows):")
                    print(df.head(3))
            else:
                print("✓ Result:", result['data'])
                
        return results
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {str(e)}")
        return None
    finally:
        print("\n" + "="*80)

async def main():
    print("\nSankhya Finance Analysis System")
    print("="*40)
    
    test_queries = [
        "Compare the revenue growth rates of AAPL and MSFT over the last 4 quarters",
        "What is the current PE ratio and market cap of NVDA?",
        "Show me the dividend yield trends for PG over the last 5 years"
    ]
    
    print(f"\nProcessing {len(test_queries)} test queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}/{len(test_queries)}")
        await analyze_query(query)

if __name__ == "__main__":
    print("Starting Sankhya Finance analysis...")
    asyncio.run(main())