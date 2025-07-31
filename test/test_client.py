#!/usr/bin/env python3
"""
Test client for the MicroFocus Tools API
Demonstrates how to interact with the FastAPI server endpoints
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_list_tools():
    """Test the /tools endpoint to get all available tools"""
    print("🔧 Testing /tools endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/tools")
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Found {len(data['tools'])} tools:")
        for tool in data['tools'][:5]:  # Show first 5 tools
            print(f"   • {tool['tool_name']}: {tool['description']}")
        if len(data['tools']) > 5:
            print(f"   ... and {len(data['tools']) - 5} more tools")
        print()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_tool_details(tool_name):
    """Test the /tool/{tool_name} endpoint to get specific tool details"""
    print(f"🔍 Testing /tool/{tool_name} endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/tool/{tool_name}")
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Tool details for '{tool_name}':")
        print(f"   Description: {data['description']}")
        print(f"   Usage: {data['usage_template']}")
        print(f"   Categories: {', '.join(data['categories'])}")
        print(f"   Arguments: {len(data['arguments'])}")
        print(f"   Options: {len(data['options'])}")
        print(f"   Examples: {len(data['examples'])}")
        print()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_handling():
    """Test error handling with non-existent tool"""
    print("🚫 Testing error handling with non-existent tool...")
    try:
        response = requests.get(f"{BASE_URL}/tool/nonexistent")
        if response.status_code == 404:
            error_data = response.json()
            print(f"✅ Proper error handling: {error_data['detail']}")
            print()
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def interactive_tool_search():
    """Interactive tool search and details viewer"""
    print("🔍 Interactive Tool Search")
    print("Enter a tool name to see details, or 'list' to see all tools, 'quit' to exit:")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'list':
                response = requests.get(f"{BASE_URL}/tools")
                response.raise_for_status()
                data = response.json()
                print("\n📋 Available tools:")
                for i, tool in enumerate(data['tools'], 1):
                    print(f"{i:2d}. {tool['tool_name']} - {tool['description']}")
            elif user_input:
                response = requests.get(f"{BASE_URL}/tool/{user_input}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"\n📖 {data['tool_name']} - {data['description']}")
                    print(f"Usage: {data['usage_template']}")
                    print(f"Categories: {', '.join(data['categories'])}")
                    
                    if data['arguments']:
                        print("\nArguments:")
                        for arg in data['arguments']:
                            req = "required" if arg['required'] else "optional"
                            print(f"  • {arg['name']} ({req}): {arg['description']}")
                    
                    if data['options']:
                        print("\nOptions:")
                        for opt in data['options'][:3]:  # Show first 3 options
                            param = f" <{opt['parameter_name']}>" if opt['has_parameter'] else ""
                            print(f"  • {opt['flag']}{param}: {opt['description']}")
                        if len(data['options']) > 3:
                            print(f"  ... and {len(data['options']) - 3} more options")
                    
                    if data['examples']:
                        print("\nExamples:")
                        for ex in data['examples'][:2]:  # Show first 2 examples
                            print(f"  • {ex['command']}")
                            print(f"    {ex['description']}")
                else:
                    error_data = response.json()
                    print(f"❌ {error_data['detail']}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Goodbye!")

def main():
    print("🚀 MicroFocus Tools API Test Client")
    print("=" * 50)
    
    # Run basic tests
    tests_passed = 0
    total_tests = 0
    
    # Test 1: List all tools
    total_tests += 1
    if test_list_tools():
        tests_passed += 1
    
    # Test 2: Get details for specific tools
    test_tools = ['dslist', 'mfcopy', 'xtrace']
    for tool in test_tools:
        total_tests += 1
        if test_get_tool_details(tool):
            tests_passed += 1
    
    # Test 3: Error handling
    total_tests += 1
    if test_error_handling():
        tests_passed += 1
    
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        print("\n" + "=" * 50)
        interactive_tool_search()

if __name__ == "__main__":
    main()