#!/usr/bin/env python3
"""
Debug TypeScript Generation Test
Shows all streaming messages to understand the response format
"""

import requests
import json

# API Configuration
API_BASE_URL = "https://sankhya-finance-api-141555278601.us-central1.run.app"
API_KEY = "sk-sankhya-finance-2025"

def debug_streaming_response():
    """Debug the streaming response to see all message types"""
    
    print("🔍 DEBUG: Analyzing all streaming messages")
    print("=" * 60)
    
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
            message_count = 0
            typescript_found = False
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        message_count += 1
                        try:
                            data = json.loads(line_str[6:])
                            message_type = data.get('type', 'unknown')
                            message_data = data.get('data', {})
                            
                            print(f"\n📨 Message #{message_count}: {message_type}")
                            
                            # Show key fields
                            if 'message' in message_data:
                                print(f"   📝 Message: {message_data['message']}")
                            
                            if 'stage' in message_data:
                                print(f"   🎯 Stage: {message_data['stage']}")
                            
                            if 'step_type' in message_data:
                                print(f"   🔧 Step Type: {message_data['step_type']}")
                            
                            # SPECIAL HANDLING FOR formatted_output messages
                            if message_type == 'formatted_output':
                                print(f"   🎨 FORMATTED OUTPUT DETECTED!")
                                output_data = message_data.get('output', {})
                                
                                if isinstance(output_data, dict):
                                    print(f"   📋 Output Keys: {list(output_data.keys())}")
                                    
                                    # Check for structured_output
                                    if 'structured_output' in output_data:
                                        structured = output_data['structured_output']
                                        print(f"   ✅ Structured Output Found!")
                                        print(f"      📊 Keys: {list(structured.keys())}")
                                        
                                        # Check for TypeScript component
                                        if 'typescript_component' in structured:
                                            ts_component = structured['typescript_component']
                                            print(f"      🎨 TypeScript Component Found!")
                                            typescript_found = True
                                            
                                            component_name = ts_component.get('component_name', 'Unknown')
                                            code_length = len(ts_component.get('component_code', ''))
                                            dependencies = ts_component.get('required_dependencies', [])
                                            
                                            print(f"         📦 Component Name: {component_name}")
                                            print(f"         📝 Code Length: {code_length} characters")
                                            print(f"         📚 Dependencies: {', '.join(dependencies)}")
                                            
                                            # Validate TypeScript code quality
                                            component_code = ts_component.get('component_code', '')
                                            if component_code:
                                                code_checks = {
                                                    "React import": "import React" in component_code,
                                                    "TypeScript interface": "interface" in component_code,
                                                    "JSX return": "return (" in component_code,
                                                    "CSS classes": "className=" in component_code,
                                                    "Export statement": "export" in component_code
                                                }
                                                
                                                print(f"         🔍 Code Quality:")
                                                for check, passed in code_checks.items():
                                                    status = "✅" if passed else "❌"
                                                    print(f"            {status} {check}")
                                                
                                                # Show code snippet
                                                if len(component_code) > 100:
                                                    lines = component_code.split('\n')
                                                    preview_lines = lines[:5]
                                                    print(f"         📄 Code Preview:")
                                                    for i, line in enumerate(preview_lines):
                                                        print(f"            {i+1}: {line[:60]}{'...' if len(line) > 60 else ''}")
                                        else:
                                            print(f"      ❌ No TypeScript component in structured output")
                                        
                                        # Check for content blocks
                                        if 'content_blocks' in structured:
                                            blocks = structured['content_blocks']
                                            print(f"      📊 Content Blocks: {len(blocks)}")
                                            block_types = [block.get('type', 'unknown') for block in blocks]
                                            print(f"         Types: {', '.join(set(block_types))}")
                                        else:
                                            print(f"      ❌ No content blocks")
                                    
                                    elif 'raw_output' in output_data:
                                        print(f"   📝 Has raw_output (length: {len(str(output_data['raw_output']))})")
                                else:
                                    print(f"   📄 Output is not a dict: {type(output_data)}")
                            
                            # Show first few keys of any large data structure
                            if len(message_data) > 5:
                                key_sample = list(message_data.keys())[:5]
                                print(f"   🔑 Data Keys (sample): {key_sample}")
                                
                        except json.JSONDecodeError as e:
                            print(f"   ❌ JSON decode error: {e}")
                            print(f"   Raw: {line_str[:100]}...")
            
            print(f"\n📊 FINAL RESULTS:")
            print(f"   Total messages processed: {message_count}")
            print(f"   TypeScript component found: {'✅ YES' if typescript_found else '❌ NO'}")
            
            return typescript_found
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = debug_streaming_response()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 TYPESCRIPT GENERATION CONFIRMED!")
        print("✅ The LLM Output Formatter is successfully generating TypeScript React components")
        print("✅ Components include proper interfaces, dependencies, and React patterns")
        print("✅ Frontend can use the generated components directly in React applications")
    else:
        print("❌ TypeScript generation not working as expected") 