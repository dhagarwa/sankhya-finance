#!/usr/bin/env python3
"""
Sankhya Finance API - LLM-Enhanced Structured Output Demo
Shows how the API now returns beautiful, structured JSON for frontend display
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "https://sankhya-finance-api-141555278601.us-central1.run.app"
API_KEY = "sk-sankhya-finance-2025"

def demo_structured_output():
    """Demo the new LLM-enhanced structured output"""
    
    print("🎨 SANKHYA FINANCE - LLM-ENHANCED STRUCTURED OUTPUT DEMO")
    print("=" * 70)
    print(f"API URL: {API_BASE_URL}")
    print("=" * 70)
    
    # Test queries that showcase different output types
    demo_queries = [
        {
            "name": "📊 Current Stock Price Query",
            "query": "What is Apple's current stock price?",
            "expected_blocks": ["metric", "insight"]
        },
        {
            "name": "🆚 Company Comparison Query", 
            "query": "Compare Apple and Microsoft revenue growth",
            "expected_blocks": ["table", "comparison", "chart"]
        },
        {
            "name": "📈 Financial Metrics Query",
            "query": "Show me Tesla's key financial metrics including P/E ratio and market cap",
            "expected_blocks": ["metric", "table", "insight"]
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n🔹 DEMO {i}: {demo['name']}")
        print(f"Query: '{demo['query']}'")
        print("-" * 50)
        
        # Make the API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": demo['query'],
            "debug_mode": False
        }
        
        try:
            print("📡 Sending request and streaming response...")
            
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                headers=headers,
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                print("✅ Connected! Streaming analysis...")
                
                structured_outputs = []
                final_result = None
                
                # Process streaming response
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('data: '):
                            try:
                                data = json.loads(line_str[6:])
                                message_type = data.get('type', 'unknown')
                                message_data = data.get('data', {})
                                
                                # Show key progress messages
                                if message_type in ['status', 'step_completed']:
                                    print(f"   {message_data.get('message', '')}")
                                
                                # Capture structured outputs
                                elif message_type == 'final_result':
                                    final_result = message_data
                                    structured_outputs = message_data.get('structured_outputs', [])
                                
                                elif message_type == 'final_structured_output':
                                    structured_outputs = message_data.get('structured_outputs', [])
                                    
                            except json.JSONDecodeError:
                                continue
                
                # Display the structured output
                if structured_outputs:
                    print("\n🎨 STRUCTURED OUTPUT GENERATED:")
                    print("=" * 40)
                    
                    for j, output in enumerate(structured_outputs):
                        print(f"\n📋 Output Block #{j+1}:")
                        print(f"   Summary: {output.get('summary', 'N/A')}")
                        
                        content_blocks = output.get('content_blocks', [])
                        print(f"   Content Blocks: {len(content_blocks)}")
                        
                        for k, block in enumerate(content_blocks):
                            block_type = block.get('type', 'unknown')
                            block_title = block.get('title', 'Untitled')
                            print(f"      {k+1}. {block_type.upper()}: {block_title}")
                            
                            # Show preview of data structure
                            if block_type == 'metric':
                                data = block.get('data', {})
                                value = data.get('value', 'N/A')
                                print(f"         Value: {value}")
                            
                            elif block_type == 'table':
                                data = block.get('data', {})
                                headers = data.get('headers', [])
                                rows = data.get('rows', [])
                                print(f"         Table: {len(headers)} columns, {len(rows)} rows")
                                if headers:
                                    print(f"         Headers: {', '.join(headers[:3])}{'...' if len(headers) > 3 else ''}")
                            
                            elif block_type == 'chart':
                                data = block.get('data', {})
                                chart_type = data.get('chart_type', 'unknown')
                                datasets = data.get('datasets', [])
                                print(f"         Chart: {chart_type} with {len(datasets)} dataset(s)")
                            
                            elif block_type == 'comparison':
                                data = block.get('data', {})
                                items = data.get('items', [])
                                print(f"         Comparison: {len(items)} items")
                        
                        # Show insights
                        insights = output.get('key_insights', [])
                        if insights:
                            print(f"   Key Insights ({len(insights)}):")
                            for insight in insights[:2]:  # Show first 2
                                print(f"      • {insight}")
                        
                        # Show metadata
                        metadata = output.get('metadata', {})
                        if metadata:
                            query_type = metadata.get('query_type', 'unknown')
                            confidence = metadata.get('confidence', 'unknown')
                            print(f"   Metadata: Type={query_type}, Confidence={confidence}")
                
                print(f"\n✅ Demo {i} completed successfully!")
                
                # Validate expected content blocks
                if structured_outputs and demo['expected_blocks']:
                    found_types = []
                    for output in structured_outputs:
                        for block in output.get('content_blocks', []):
                            found_types.append(block.get('type'))
                    
                    expected = set(demo['expected_blocks'])
                    found = set(found_types)
                    
                    if expected.intersection(found):
                        print(f"✅ Expected content types found: {list(expected.intersection(found))}")
                    else:
                        print(f"⚠️  Expected {expected}, but found {found}")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error in demo {i}: {e}")
        
        # Small delay between demos
        if i < len(demo_queries):
            print(f"\n⏸️  Waiting 2 seconds before next demo...")
            time.sleep(2)
    
    print("\n🎉 ALL DEMOS COMPLETED!")
    print("\n📖 Frontend Display Guide:")
    print("=" * 40)
    print("The structured JSON contains these content block types that your frontend can render:")
    print("📊 METRIC blocks: Display as cards/tiles with large numbers")
    print("📋 TABLE blocks: Render as sortable tables")  
    print("📈 CHART blocks: Create interactive charts (line, bar, pie)")
    print("⚖️  COMPARISON blocks: Show as comparison cards/lists")
    print("💡 INSIGHT blocks: Display as highlighted insight boxes")
    print("📝 TEXT blocks: Render as formatted text sections")
    
    print("\n🎨 Example Frontend Rendering:")
    print("- Metrics → Large number cards with trend indicators")
    print("- Tables → Sortable, filterable data tables")
    print("- Charts → Interactive visualizations using Chart.js/D3")
    print("- Insights → Highlighted callout boxes")
    print("- Comparisons → Side-by-side comparison cards")

def quick_test():
    """Quick test to verify API is working"""
    print("🔍 Quick API Test...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test health endpoint
        health = requests.get(f"{API_BASE_URL}/health")
        if health.status_code == 200:
            health_data = health.json()
            print(f"✅ API Health: {health_data.get('status')}")
            print(f"   OpenAI Configured: {health_data.get('openai_configured')}")
            print(f"   Auth Required: {health_data.get('auth_required')}")
            return True
        else:
            print(f"❌ Health check failed: {health.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Sankhya Finance Structured Output Demo\n")
    
    # Quick health check first
    if quick_test():
        print("\n" + "="*70)
        demo_structured_output()
    else:
        print("❌ API not accessible. Please check the service status.")
    
    print(f"\n📝 To use this API in your frontend:")
    print(f"   1. Send requests to: {API_BASE_URL}/analyze")
    print(f"   2. Include header: Authorization: Bearer {API_KEY}")
    print(f"   3. Stream the response and look for 'final_structured_output' messages")
    print(f"   4. Use the structured JSON to render beautiful UI components")
    print(f"\nAPI Documentation: {API_BASE_URL}/docs") 