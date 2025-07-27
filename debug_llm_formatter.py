#!/usr/bin/env python3
"""
Debug LLM Formatter
Tests the LLM formatter separately to understand the JSON parsing error
"""

import asyncio
import json
import sys
import os

# Add src to path to import modules
sys.path.append('./src')

from agents.llm_output_formatter import LLMOutputFormatter

async def debug_llm_formatter():
    """Debug the LLM formatter to understand the JSON parsing error"""
    
    print("🔍 DEBUG: LLM Output Formatter")
    print("=" * 50)
    
    # Use the OpenAI API key from environment or default
    openai_api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    if "placeholder" in openai_api_key or len(openai_api_key) < 20:
        print("❌ No valid OpenAI API key found")
        print("Set OPENAI_API_KEY environment variable")
        return
    
    formatter = LLMOutputFormatter(openai_api_key)
    
    # Simulate the same data that would cause the error
    test_raw_output = """
    Microsoft Income Statements - Last 4 Quarters
    
    Q4 2023: Revenue $62.0B, Net Income $18.3B
    Q3 2023: Revenue $56.2B, Net Income $18.4B 
    Q2 2023: Revenue $51.9B, Net Income $16.4B
    Q1 2023: Revenue $52.9B, Net Income $16.4B
    
    Key metrics show consistent revenue growth and strong profitability.
    """
    
    test_step_data = {
        "step_1": {
            "totalRevenue": 62000000000,
            "netIncome": 18300000000,
            "grossMargins": 0.69,
            "ticker": "MSFT"
        }
    }
    
    test_query = "Display Microsoft's income statements for the last 4 quarters"
    
    try:
        print("🧪 Testing Structured JSON Generation...")
        
        # Test the _generate_structured_json method directly
        try:
            structured_result = await formatter._generate_structured_json(
                test_raw_output, 
                test_step_data, 
                test_query
            )
            print("✅ Structured JSON generation successful!")
            print(f"   Keys: {list(structured_result.keys())}")
            print(f"   Content blocks: {len(structured_result.get('content_blocks', []))}")
            
        except Exception as e:
            print(f"❌ Structured JSON generation failed: {e}")
            
            # Let's try to see what the raw response looks like
            print("\n🔬 Debugging the raw OpenAI response...")
            
            # Manually create the prompt that would be sent
            data_context = formatter._prepare_data_context(test_step_data)
            
            formatting_prompt = f"""
You are an expert financial data visualization specialist. Your task is to convert raw financial analysis results into a perfectly structured JSON format that a frontend can use to create beautiful, interactive displays.

ORIGINAL USER QUERY: "{test_query}"

RAW ANALYSIS OUTPUT:
{test_raw_output}

UNDERLYING DATA:
{json.dumps(data_context, indent=2, default=str)}

Your task is to create a JSON response with the following EXACT structure:

{{
  "summary": "A clear, concise 1-2 sentence summary of the key findings",
  "content_blocks": [
    {{
      "type": "metric",
      "title": "Descriptive Title",
      "data": {{
        "value": "Formatted value (e.g., $156.23, 15.4%, 2.3x)",
        "label": "What this metric represents",
        "trend": "up/down/neutral (if applicable)",
        "context": "Brief context about this metric"
      }}
    }}
  ],
  "key_insights": [
    "Most important insight from the analysis",
    "Second most important insight"
  ],
  "recommendations": [
    "Actionable recommendation based on analysis"
  ],
  "metadata": {{
    "query_type": "financial_metrics",
    "confidence": "high"
  }}
}}

CRITICAL FORMATTING RULES:
1. Return ONLY valid JSON, no additional text
2. Include 2-4 key insights that directly answer the user's question
3. Format all financial values appropriately

Based on the user's query "{test_query}", intelligently select and structure the most relevant content blocks that directly address what they asked for.
"""

            print(f"\n📝 Prompt being sent (first 500 chars):")
            print(f"{formatting_prompt[:500]}...")
            
            # Try to make the API call manually to see the response
            try:
                response = await formatter.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a financial data visualization expert. You convert raw financial analysis into perfectly structured JSON for frontend display. Always return valid JSON only."},
                        {"role": "user", "content": formatting_prompt}
                    ],
                    temperature=0.1,
                    max_completion_tokens=3000
                )
                
                raw_response = response.choices[0].message.content.strip()
                print(f"\n📥 Raw OpenAI Response:")
                print(f"   Length: {len(raw_response)} characters")
                print(f"   First 200 chars: {raw_response[:200]}")
                print(f"   Last 200 chars: {raw_response[-200:]}")
                
                # Try to parse the JSON
                try:
                    parsed_json = json.loads(raw_response)
                    print("✅ Raw response is valid JSON!")
                    print(f"   Top-level keys: {list(parsed_json.keys())}")
                except json.JSONDecodeError as json_err:
                    print(f"❌ Raw response is invalid JSON: {json_err}")
                    print("🔍 Analyzing response content...")
                    
                    if not raw_response:
                        print("   Response is empty!")
                    elif raw_response.startswith('{'):
                        print("   Response starts with { but has JSON errors")
                    else:
                        print(f"   Response doesn't start with JSON: '{raw_response[:50]}'")
                        
            except Exception as api_err:
                print(f"❌ OpenAI API call failed: {api_err}")
        
        print("\n🧪 Testing TypeScript Generation...")
        
        # Test the TypeScript generation
        try:
            typescript_result = await formatter._generate_typescript_component(
                test_raw_output,
                test_step_data, 
                test_query
            )
            print("✅ TypeScript generation successful!")
            print(f"   Component name: {typescript_result.get('component_name')}")
            print(f"   Code length: {len(typescript_result.get('component_code', ''))}")
            
        except Exception as e:
            print(f"❌ TypeScript generation failed: {e}")
        
        print("\n🧪 Testing Full Format for Frontend...")
        
        # Test the complete format_for_frontend method
        try:
            full_result = await formatter.format_for_frontend(
                test_raw_output,
                test_step_data,
                test_query
            )
            print("✅ Full formatting successful!")
            print(f"   Has structured output: {'content_blocks' in full_result}")
            print(f"   Has TypeScript: {'typescript_component' in full_result}")
            print(f"   Rendering mode: {full_result.get('rendering_mode')}")
            
        except Exception as e:
            print(f"❌ Full formatting failed: {e}")
            
    except Exception as e:
        print(f"❌ General error: {e}")

async def main():
    await debug_llm_formatter()

if __name__ == "__main__":
    asyncio.run(main()) 