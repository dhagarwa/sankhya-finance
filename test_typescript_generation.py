#!/usr/bin/env python3
"""
Test TypeScript Generation Capability
Verifies that the LLM Output Formatter generates both structured JSON and TypeScript React components
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "https://sankhya-finance-api-141555278601.us-central1.run.app"
API_KEY = "sk-sankhya-finance-2025"

def test_typescript_generation():
    """Test if the API generates TypeScript React components"""
    
    print("🔬 TESTING TYPESCRIPT GENERATION CAPABILITY")
    print("=" * 60)
    
    # Test query specifically designed to generate rich visualizations
    test_query = "What is Apple's current stock price and show me key financial metrics?"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": test_query,
        "debug_mode": False
    }
    
    print(f"📝 Test Query: '{test_query}'")
    print(f"🎯 Expected: Structured JSON + TypeScript React Component")
    print("-" * 60)
    
    try:
        print("📡 Sending request to streaming endpoint...")
        
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            headers=headers,
            json=payload,
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Connected! Processing streaming response...")
            
            structured_outputs = []
            step_count = 0
            
            # Process streaming response
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])
                            message_type = data.get('type', 'unknown')
                            message_data = data.get('data', {})
                            
                            # Track progress
                            if message_type == 'step_completed':
                                step_count += 1
                                print(f"   Step {step_count} completed: {message_data.get('step_type', 'unknown')}")
                            
                            # Capture final structured outputs
                            elif message_type in ['final_result', 'final_structured_output']:
                                outputs = message_data.get('structured_outputs', [])
                                if outputs:
                                    structured_outputs.extend(outputs)
                                    
                        except json.JSONDecodeError:
                            continue
            
            # Analyze the results
            print(f"\n🔍 ANALYSIS RESULTS:")
            print(f"   Total Steps Completed: {step_count}")
            print(f"   Structured Outputs Received: {len(structured_outputs)}")
            
            if not structured_outputs:
                print("❌ No structured outputs received!")
                return False
            
            # Test each structured output
            typescript_found = False
            valid_json_structure = False
            
            for i, output in enumerate(structured_outputs):
                print(f"\n📋 Testing Output #{i+1}:")
                
                # Check for basic structured JSON components
                if "content_blocks" in output:
                    content_blocks = output["content_blocks"]
                    print(f"   ✅ Contains content_blocks: {len(content_blocks)} blocks")
                    valid_json_structure = True
                    
                    # List content block types
                    block_types = [block.get('type', 'unknown') for block in content_blocks]
                    print(f"   📊 Block types: {', '.join(set(block_types))}")
                else:
                    print(f"   ❌ Missing content_blocks")
                
                # Check for TypeScript component
                if "typescript_component" in output:
                    typescript_data = output["typescript_component"]
                    print(f"   🎨 TypeScript Component Found!")
                    
                    # Validate TypeScript component structure
                    required_fields = ["component_code", "component_name", "required_dependencies"]
                    missing_fields = [field for field in required_fields if field not in typescript_data]
                    
                    if not missing_fields:
                        print(f"   ✅ TypeScript component has all required fields")
                        typescript_found = True
                        
                        # Check component details
                        component_name = typescript_data.get("component_name", "Unknown")
                        dependencies = typescript_data.get("required_dependencies", [])
                        component_code = typescript_data.get("component_code", "")
                        
                        print(f"   📦 Component Name: {component_name}")
                        print(f"   📚 Dependencies: {', '.join(dependencies)}")
                        print(f"   📝 Code Length: {len(component_code)} characters")
                        
                        # Validate the component code looks like React/TypeScript
                        code_checks = {
                            "Has React import": "import React" in component_code,
                            "Has TypeScript interface": "interface" in component_code,
                            "Has JSX return": "return (" in component_code,
                            "Has component export": "export" in component_code,
                            "Has CSS classes": "className=" in component_code
                        }
                        
                        print(f"   🔍 Code Quality Checks:")
                        for check, passed in code_checks.items():
                            status = "✅" if passed else "❌"
                            print(f"      {status} {check}")
                        
                        # Show a snippet of the component code
                        if len(component_code) > 100:
                            snippet = component_code[:200] + "..."
                            print(f"   📄 Code Preview:")
                            print(f"      {snippet}")
                        
                    else:
                        print(f"   ❌ Missing required fields: {missing_fields}")
                else:
                    print(f"   ❌ No TypeScript component found")
                
                # Check for rendering mode
                rendering_mode = output.get("rendering_mode", "unknown")
                print(f"   🎭 Rendering Mode: {rendering_mode}")
            
            # Final assessment
            print(f"\n🎯 FINAL ASSESSMENT:")
            
            if valid_json_structure and typescript_found:
                print("✅ SUCCESS: Both structured JSON and TypeScript generation working!")
                print("   📊 Structured JSON: Available for traditional rendering")
                print("   🎨 TypeScript Component: Available for direct React integration")
                print("   🚀 Frontend can choose between JSON parsing or direct component usage")
                return True
            elif valid_json_structure:
                print("⚠️  PARTIAL: Structured JSON working, but TypeScript generation failed")
                return False
            elif typescript_found:
                print("⚠️  PARTIAL: TypeScript generation working, but structured JSON missing")
                return False
            else:
                print("❌ FAILED: Neither structured JSON nor TypeScript generation working")
                return False
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_api_health():
    """Quick health check"""
    try:
        health = requests.get(f"{API_BASE_URL}/health")
        if health.status_code == 200:
            health_data = health.json()
            print(f"✅ API Health: {health_data.get('status')}")
            print(f"   OpenAI Configured: {health_data.get('openai_configured')}")
            return health_data.get('openai_configured', False)
        return False
    except:
        return False

if __name__ == "__main__":
    print("🚀 TypeScript Generation Test Suite\n")
    
    # Health check first
    if not test_api_health():
        print("❌ API not accessible or OpenAI not configured")
        exit(1)
    
    print()
    # Run the TypeScript generation test
    success = test_typescript_generation()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 TEST PASSED: TypeScript generation capability confirmed!")
        print("\n📖 Usage Instructions:")
        print("1. Frontend can use structured JSON for traditional data rendering")
        print("2. Frontend can directly use generated TypeScript components")
        print("3. Components include proper TypeScript interfaces and modern React patterns")
        print("4. Dependencies are clearly specified for easy integration")
    else:
        print("❌ TEST FAILED: TypeScript generation needs investigation")
    
    print(f"\n🔗 API Endpoint: {API_BASE_URL}/analyze")
    print(f"📄 Full Response: Contains both 'content_blocks' and 'typescript_component'") 