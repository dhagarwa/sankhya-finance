#!/usr/bin/env python3
"""
Sankhya Finance API - Authentication Demo
Shows how to use the API with proper authentication headers
"""

import requests
import json

# API Configuration
API_BASE_URL = "https://sankhya-finance-api-141555278601.us-central1.run.app"
API_KEY = "sk-sankhya-finance-2025"  # Default demo key

def test_health_check():
    """Test health endpoint (no auth required)"""
    print("🏥 Testing health endpoint...")
    
    response = requests.get(f"{API_BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed: {data}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_streaming_analysis():
    """Test streaming analysis with authentication"""
    print("\n🔄 Testing streaming analysis...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": "What is Apple's current stock price?",
        "debug_mode": False
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            headers=headers,
            json=payload,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Successfully connected to streaming endpoint")
            print("📡 Receiving streaming data...\n")
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])
                            message_type = data.get('type', 'unknown')
                            message_data = data.get('data', {})
                            message = message_data.get('message', '')
                            
                            print(f"📨 [{message_type.upper()}] {message}")
                            
                            # Stop after a few messages for demo
                            if message_type == 'step_completed':
                                print("\n🛑 Demo stopped early - API is working!")
                                break
                                
                        except json.JSONDecodeError:
                            print(f"⚠️  Couldn't parse: {line_str}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_simple_analysis():
    """Test simple analysis endpoint"""
    print("\n📊 Testing simple analysis...")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": "What is Tesla's current stock price?",
        "debug_mode": False
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze-simple",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Simple analysis completed")
            print(f"Query: {data.get('query')}")
            print(f"Status: {data.get('result', {}).get('status')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_without_auth():
    """Test what happens without authentication"""
    print("\n🚫 Testing without authentication...")
    
    payload = {
        "query": "What is Apple's current stock price?",
        "debug_mode": False
    }
    
    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def main():
    print("🚀 SANKHYA FINANCE API - AUTHENTICATION DEMO")
    print("=" * 60)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY}")
    print("=" * 60)
    
    # Test 1: Health check (no auth required)
    health_ok = test_health_check()
    
    if health_ok:
        # Test 2: Streaming with auth
        test_streaming_analysis()
        
        # Test 3: Simple analysis with auth
        test_simple_analysis()
        
        # Test 4: What happens without auth
        test_without_auth()
    
    print("\n📋 CURL Examples:")
    print("=" * 40)
    print("Health check (no auth):")
    print(f'curl "{API_BASE_URL}/health"')
    
    print("\nStreaming analysis (with auth):")
    print(f'''curl -X POST "{API_BASE_URL}/analyze" \\
  -H "Authorization: Bearer {API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{{"query": "What is Apple\'s current stock price?", "debug_mode": false}}' \\
  --no-buffer''')
    
    print("\nSimple analysis (with auth):")
    print(f'''curl -X POST "{API_BASE_URL}/analyze-simple" \\
  -H "Authorization: Bearer {API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{{"query": "What is Tesla\'s current stock price?", "debug_mode": false}}' ''')

if __name__ == "__main__":
    main() 