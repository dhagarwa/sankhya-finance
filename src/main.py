"""
Sankhya Finance - Modern AI-Powered Financial Analysis
Using OpenAI O3 reasoning model with Financial Datasets MCP Server
"""

import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.o3_query_decomposer import O3QueryDecomposer, QueryPatterns
from agents.yfinance_client import FinanceToolRegistry


async def analyze_financial_query(query: str, debug_mode: bool = False) -> dict:
    """
    Main analysis function using O3 reasoning and MCP server
    """
    print("\n" + "="*80)
    print(f"🚀 SANKHYA FINANCE - AI Financial Analysis")
    print(f"Query: {query}")
    print("="*80)
    
    # Get API keys
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key or "placeholder" in openai_api_key:
        print("❌ Error: OPENAI_API_KEY not found or is placeholder")
        return {"error": "Missing OpenAI API key - YFinance data will work but no AI analysis"}
    
    try:
        # Initialize O3 Query Decomposer with YFinance client
        async with O3QueryDecomposer(openai_api_key) as decomposer:
            
            # Step 1: Analyze query patterns
            print("\n📊 Step 1: Query Pattern Analysis")
            query_type = QueryPatterns.detect_query_type(query)
            tickers = QueryPatterns.extract_tickers(query, decomposer.intelligent_ticker_extractor)
            print(f"   Query Type: {query_type}")
            print(f"   Detected Tickers: {tickers if tickers else 'None detected'}")
            
            # Step 2: O3 Decomposition and Execution
            print("\n🧠 Step 2: O3 Reasoning & YFinance Execution")
            decomposition = await decomposer.decompose_query(query, debug_mode)
            
            # Step 3: Results Summary
            print("\n📈 Step 3: Analysis Results")
            print("-" * 50)
            
            successful_steps = [s for s in decomposition.steps if s.status == "completed"]
            failed_steps = [s for s in decomposition.steps if s.status == "failed"]
            
            print(f"✅ Successful Steps: {len(successful_steps)}")
            print(f"❌ Failed Steps: {len(failed_steps)}")
            
            if failed_steps:
                print("\nFailed Steps:")
                for step in failed_steps:
                    print(f"   • {step.step_id}: {step.error}")
            
            # Step 4: Final Analysis
            if decomposition.final_analysis:
                print("\n🎯 Final Analysis:")
                print("-" * 50)
                print(decomposition.final_analysis)
            
            return {
                "status": decomposition.status,
                "query": query,
                "query_type": query_type,
                "detected_tickers": tickers,
                "reasoning": decomposition.reasoning,
                "steps_executed": len(successful_steps),
                "steps_failed": len(failed_steps),
                "final_analysis": decomposition.final_analysis,
                "raw_data": {
                    step.step_id: step.result 
                    for step in decomposition.steps 
                    if step.status == "completed" and step.result
                }
            }
            
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        return {
            "error": str(e),
            "query": query
        }


async def interactive_mode():
    """Interactive mode for testing queries"""
    print("\n🎯 SANKHYA FINANCE - Interactive Mode")
    print("="*50)
    print("Enter financial queries to analyze (type 'quit' to exit)")
    print("Examples:")
    print("  • What is Apple's current stock price?")
    print("  • Compare MSFT and GOOGL revenue growth over last 4 quarters")
    print("  • Show me Tesla's cash flow statements")
    print("  • Get recent news about NVDA")
    print("-"*50)
    
    # Ask for debug mode preference
    debug_choice = input("\n🔍 Enable debug mode to see detailed O3 reasoning and YFinance responses? (y/n): ").strip().lower()
    debug_mode = debug_choice in ['y', 'yes', '1', 'true']
    
    if debug_mode:
        print("🐛 Debug mode enabled - you'll see detailed execution information")
    else:
        print("📊 Standard mode - showing summary information only")
    
    while True:
        try:
            query = input("\n💬 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Analyze the query
            result = await analyze_financial_query(query, debug_mode)
            
            # Brief summary
            if "error" not in result:
                print(f"\n📊 Query processed: {result['status']}")
                print(f"🔍 Analysis complete with {result['steps_executed']} successful steps")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def run_test_queries():
    """Run predefined test queries to demonstrate capabilities with interactive control"""
    test_queries = [
        "What is Apple's current stock price?",
        "Get Microsoft's income statements for the last 4 quarters",
        "Compare TSLA and NVDA revenue growth",
        "Show me recent news about Amazon",
        "What are Google's balance sheet metrics?",
    ]
    
    print(f"\n🧪 Running {len(test_queries)} test queries (Interactive Mode)...")
    print("After each query, you'll be asked whether to continue to the next one.")
    
    results = []
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*20} Test Query {i}/{len(test_queries)} {'='*20}")
        
        # Run the query with debug mode
        result = await analyze_financial_query(query, debug_mode=True)
        results.append(result)
        
        # Interactive control - ask user if they want to continue
        if i < len(test_queries):
            print(f"\n{'='*60}")
            print(f"🎯 Query {i} completed!")
            choice = input(f"Continue to next query ({i+1}/{len(test_queries)})? (y/n/q): ").strip().lower()
            
            if choice in ['n', 'no']:
                print("⏸️  Stopping at user request.")
                break
            elif choice in ['q', 'quit']:
                print("🛑 Quitting test sequence.")
                break
            elif choice in ['y', 'yes', '']:
                print("▶️  Continuing to next query...")
                continue
            else:
                print("❓ Invalid choice, continuing anyway...")
                continue
    
    # Summary
    print(f"\n📊 TEST RESULTS SUMMARY")
    print("="*50)
    successful = len([r for r in results if "error" not in r and r.get("status") == "completed"])
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {len(results) - successful}/{len(results)}")
    
    return results


async def show_available_tools():
    """Display available MCP tools"""
    print("\n🛠️  AVAILABLE FINANCIAL DATA TOOLS")
    print("="*50)
    print(FinanceToolRegistry.format_tools_for_llm())


async def test_ticker_detection():
    """Test the ticker detection functionality"""
    print("\n🔍 TICKER DETECTION TEST")
    print("="*50)
    
    test_queries = [
        "What is Apple's current stock price?",
        "Compare TSLA and NVDA revenue growth",
        "Show me Microsoft's financials",
        "Get Google and Amazon earnings",
        "AAPL vs MSFT analysis",
        "How is Netflix performing?",
        "Meta stock analysis",
        "Intel and AMD comparison"
    ]
    
    for query in test_queries:
        query_type = QueryPatterns.detect_query_type(query)
        tickers = QueryPatterns.extract_tickers(query)
        
        print(f"\n📝 Query: {query}")
        print(f"   Type: {query_type}")
        print(f"   Tickers: {tickers if tickers else 'None detected'}")
    
    print("\n✅ Ticker detection test completed!")


async def main():
    """Main entry point"""
    print("\n🚀 SANKHYA FINANCE")
    print("AI-Powered Financial Analysis with O3 Reasoning")
    print("="*60)
    
    # Check environment setup
    openai_key = os.getenv("OPENAI_API_KEY")
    financial_key = os.getenv("FINANCIAL_DATASETS_API_KEY")
    
    if not openai_key or "placeholder" in openai_key:
        print("⚠️  Missing OPENAI_API_KEY in environment variables")
        print("For full functionality, get one at: https://platform.openai.com/api-keys")
        print("Continuing in DEMO MODE (limited functionality)...")
        demo_mode = True
    else:
        demo_mode = False
    
    # YFinance doesn't need API keys, so we're good to go!
    print("✅ Using YFinance for financial data (no API key required)")
    
    print("✅ Environment variables loaded")
    
    if demo_mode:
        print("\n🔧 DEMO MODE: Some features may be limited without API keys")
    
    # Menu
    while True:
        print("\n📋 OPTIONS:")
        print("1. Interactive Query Mode")
        print("2. Run Test Queries") 
        print("3. Show Available Tools")
        print("4. Test Ticker Detection (Demo)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            await interactive_mode()
        elif choice == "2":
            await run_test_queries()
        elif choice == "3":
            await show_available_tools()
        elif choice == "4":
            await test_ticker_detection()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    print("🌟 Starting Sankhya Finance Analysis System...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 System stopped by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")