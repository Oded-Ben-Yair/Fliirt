#!/usr/bin/env python3
"""
Comprehensive test suite for Flirrt.ai AI service
Tests all endpoints, AI model integrations, and error handling
"""

import requests
import json
import base64
import time
import sys
import os
from PIL import Image
import io

# Test configuration
BASE_URL = "http://localhost:5000"
AI_BASE_URL = f"{BASE_URL}/api/ai"

def create_test_image():
    """Create a simple test image for API testing"""
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_data = buffer.getvalue()
    
    return base64.b64encode(img_data).decode('utf-8')

def test_service_health():
    """Test if the AI service is running and healthy"""
    print("🔍 Testing AI service health...")
    
    try:
        response = requests.get(f"{AI_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service healthy: {data['service']}")
            print(f"📊 Models available: {data['models_available']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_mock_suggestions():
    """Test the mock suggestions endpoint"""
    print("\n🧪 Testing mock suggestions endpoint...")
    
    try:
        payload = {"context": "test"}
        response = requests.post(
            f"{AI_BASE_URL}/test-suggestions",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get('suggestions', [])
            print(f"✅ Mock suggestions received: {len(suggestions)} items")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
            return True
        else:
            print(f"❌ Mock suggestions failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Mock suggestions error: {e}")
        return False

def test_screenshot_analysis():
    """Test the screenshot analysis endpoint with a test image"""
    print("\n🖼️ Testing screenshot analysis endpoint...")
    
    try:
        # Create test image
        test_image_b64 = create_test_image()
        
        payload = {
            "image_data": test_image_b64,
            "current_text": "Hey there!",
            "context": "dating_app_test"
        }
        
        print("📤 Sending analysis request...")
        response = requests.post(
            f"{AI_BASE_URL}/analyze-screenshot",
            json=payload,
            timeout=30  # Longer timeout for AI processing
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis successful!")
            print(f"🔍 Visual analysis: {data.get('visual_analysis', 'N/A')[:100]}...")
            
            suggestions = data.get('suggestions', [])
            print(f"💕 Suggestions received: {len(suggestions)} items")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
                
            models = data.get('model_used', {})
            print(f"🤖 Models used: Visual={models.get('visual', 'N/A')}, Flirting={models.get('flirting', 'N/A')}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n🚨 Testing error handling...")
    
    # Test missing image data
    try:
        response = requests.post(
            f"{AI_BASE_URL}/analyze-screenshot",
            json={"current_text": "test"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Correctly handled missing image data")
        else:
            print(f"❌ Unexpected response for missing image: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    # Test invalid JSON
    try:
        response = requests.post(
            f"{AI_BASE_URL}/analyze-screenshot",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [400, 500]:
            print("✅ Correctly handled invalid JSON")
        else:
            print(f"❌ Unexpected response for invalid JSON: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Invalid JSON test failed: {e}")
        return False
    
    return True

def test_api_status():
    """Test the main API status endpoint"""
    print("\n📊 Testing main API status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"📋 Service: {data['service']}")
            print(f"🔗 Endpoints: {list(data['endpoints'].keys())}")
            return True
        else:
            print(f"❌ API status failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API status error: {e}")
        return False

def run_performance_test():
    """Run a basic performance test"""
    print("\n⚡ Running performance test...")
    
    try:
        start_time = time.time()
        
        # Test multiple mock suggestion requests
        for i in range(5):
            response = requests.post(
                f"{AI_BASE_URL}/test-suggestions",
                json={"context": f"test_{i}"},
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Performance test failed at request {i+1}")
                return False
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 5
        
        print(f"✅ Performance test completed")
        print(f"⏱️ Total time: {total_time:.2f}s")
        print(f"📈 Average per request: {avg_time:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Flirrt.ai AI Service Test Suite")
    print("=" * 50)
    
    tests = [
        ("Service Health", test_service_health),
        ("API Status", test_api_status),
        ("Mock Suggestions", test_mock_suggestions),
        ("Screenshot Analysis", test_screenshot_analysis),
        ("Error Handling", test_error_handling),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "="*50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI service is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

