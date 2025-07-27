#!/usr/bin/env python3
"""
Test script for Sankhya Finance Streaming API
Demonstrates real-time streaming of the agentic chain
"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_streaming_api():
    """Test the streaming API endpoint"""
    
    # Test query
    test_query = "What is Apple's current stock price?"
    
    print("🧪 Testing Sankhya Finance Streaming API")
    print("=" * 50)
    print(f"Query: {test_query}")
    print("=" * 50)
    
    url = "http://localhost:8000/analyze"
    payload = {
        "query": test_query,
        "debug_mode": True
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status != 200:
                    print(f"❌ Error: HTTP {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
                    return
                
                print("📡 Receiving streaming data...\n")
                
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])
                            message_type = data.get('type', 'unknown')
                            message_data = data.get('data', {})
                            
                            # Format the output based on message type
                            timestamp = message_data.get('timestamp', '')
                            message = message_data.get('message', '')
                            
                            if message_type == 'status':
                                stage = message_data.get('stage', '')
                                print(f"🔄 [{stage.upper()}] {message}")
                                
                            elif message_type == 'pattern_result':
                                tickers = message_data.get('detected_tickers', [])
                                query_type = message_data.get('query_type', '')
                                print(f"📊 {message}")
                                print(f"   Type: {query_type}")
                                print(f"   Tickers: {tickers}")
                                
                            elif message_type == 'decomposition_result':
                                reasoning = message_data.get('reasoning', '')
                                steps = message_data.get('steps', [])
                                print(f"🧠 {message}")
                                print(f"   Reasoning: {reasoning[:200]}...")
                                print(f"   Steps:")
                                for step in steps:
                                    print(f"     • {step['step_id']} ({step['step_type']}): {step['description']}")
                                
                            elif message_type == 'step_start':
                                step_type = message_data.get('step_type', '')
                                print(f"🔧 [{step_type}] {message}")
                                
                            elif message_type == 'step_progress':
                                print(f"⚙️  {message}")
                                
                            elif message_type == 'step_completed':
                                print(f"✅ {message}")
                                
                            elif message_type == 'step_failed':
                                error = message_data.get('error', '')
                                print(f"❌ {message}")
                                print(f"   Error: {error}")
                                
                            elif message_type == 'formatted_output':
                                output = message_data.get('output', '')
                                print(f"🎨 FORMATTED OUTPUT:")
                                print("-" * 40)
                                print(output)
                                print("-" * 40)
                                
                            elif message_type == 'final_summary':
                                print(f"🏁 {message}")
                                analysis = message_data.get('final_analysis', '')
                                if analysis:
                                    print(f"   Final Analysis: {analysis}")
                                
                            elif message_type == 'error':
                                print(f"❌ ERROR: {message}")
                                
                            else:
                                print(f"🔍 [{message_type.upper()}] {message}")
                            
                            print()  # Empty line for readability
                            
                        except json.JSONDecodeError as e:
                            print(f"⚠️  Failed to parse JSON: {e}")
                            print(f"   Raw line: {line_str}")
    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("\n💡 Make sure the API server is running:")
        print("   cd src/api && python main.py")


async def test_health_endpoint():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data}")
                    return True
                else:
                    print(f"❌ Health check failed: HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


async def main():
    """Main test function"""
    print("🧪 SANKHYA FINANCE API TEST SUITE")
    print("=" * 60)
    
    # Check if API key is configured
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key or "placeholder" in openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not configured")
        print("   The API will return an error, but streaming format will still be tested")
    else:
        print("✅ OpenAI API key configured")
    
    print()
    
    # Test health endpoint first
    health_ok = await test_health_endpoint()
    print()
    
    if health_ok:
        # Test streaming analysis
        await test_streaming_api()
    else:
        print("❌ Skipping streaming test due to health check failure")
    
    print("\n🎯 Test completed!")
    print("\n💡 To test with the HTML client, visit:")
    print("   http://localhost:8000/static/index.html")


if __name__ == "__main__":
    asyncio.run(main()) 