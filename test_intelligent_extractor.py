#!/usr/bin/env python3
"""
Test script for the Intelligent Ticker Extractor
Tests natural language to S&P 500 ticker translation
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from openai import OpenAI
from agents.intelligent_ticker_extractor import IntelligentTickerExtractor
from agents.o3_query_decomposer import QueryPatterns

def test_intelligent_extraction():
    """Test the intelligent ticker extraction with various natural language queries"""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    # Initialize the intelligent extractor
    client = OpenAI(api_key=openai_api_key)
    extractor = IntelligentTickerExtractor(client)
    
    # Test queries that demonstrate intelligent understanding
    test_queries = [
        # Sector-based queries
        "car manufacturers in SP500",
        "all tech companies",
        "energy companies",
        "banks and financial institutions",
        
        # Business category queries  
        "artificial intelligence companies",
        "social media platforms",
        "cloud computing providers",
        "pharmaceutical companies",
        
        # Complex natural language queries
        "companies with revenue growth over 20%",
        "top streaming services",
        "electric vehicle makers",
        "companies that make semiconductors",
        "home improvement retailers",
        
        # Specific company mentions
        "Apple and Microsoft analysis", 
        "Compare Tesla with Ford",
        "How is Amazon doing?",
    ]
    
    print("🧪 Testing Intelligent Ticker Extraction")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 50)
        
        try:
            # Test with intelligent extractor
            tickers = extractor.extract_tickers(query)
            
            if tickers:
                print(f"✅ Found {len(tickers)} companies: {tickers[:10]}{'...' if len(tickers) > 10 else ''}")
                
                # Get detailed explanation
                explanation = extractor.get_extraction_explanation(query, tickers)
                print(f"📝 Explanation:\n{explanation[:300]}{'...' if len(explanation) > 300 else ''}")
            else:
                print("❌ No companies found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
            # Test fallback
            print("🔄 Trying fallback method...")
            fallback_tickers = QueryPatterns.extract_tickers(query)
            print(f"📋 Fallback result: {fallback_tickers}")
    
    print("\n" + "=" * 60)
    print("✅ Intelligent ticker extraction test completed!")

def test_comparison():
    """Compare intelligent vs heuristic extraction"""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    client = OpenAI(api_key=openai_api_key)
    extractor = IntelligentTickerExtractor(client)
    
    comparison_queries = [
        "car manufacturers in SP500",
        "tech companies with high growth", 
        "all energy companies",
        "companies that make semiconductors"
    ]
    
    print("\n🔍 Intelligent vs Heuristic Comparison")
    print("=" * 60)
    
    for query in comparison_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 40)
        
        # Intelligent extraction
        try:
            intelligent_tickers = extractor.extract_tickers(query)
            print(f"🧠 Intelligent: {intelligent_tickers[:5]}{'...' if len(intelligent_tickers) > 5 else ''} ({len(intelligent_tickers)} total)")
        except Exception as e:
            print(f"🧠 Intelligent: Error - {e}")
            intelligent_tickers = []
        
        # Heuristic extraction
        heuristic_tickers = QueryPatterns.extract_tickers(query)
        print(f"📋 Heuristic:   {heuristic_tickers} ({len(heuristic_tickers)} total)")
        
        # Analysis
        if len(intelligent_tickers) > len(heuristic_tickers):
            print("💡 Intelligent found more relevant companies")
        elif len(intelligent_tickers) == len(heuristic_tickers):
            print("⚖️  Same number of companies found")
        else:
            print("🤔 Heuristic found more (may include false positives)")

if __name__ == "__main__":
    test_intelligent_extraction()
    test_comparison() 