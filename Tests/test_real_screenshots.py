#!/usr/bin/env python3
"""
Real Screenshot Analysis Test for Flirrt.ai
Tests AI analysis and flirting suggestions on actual dating app screenshots
"""

import os
import sys
import json
import base64
import requests
import time
from pathlib import Path

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def encode_image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Error encoding image {image_path}: {e}")
        return None

def categorize_screenshot(image_path):
    """Categorize screenshot based on filename and content analysis"""
    filename = os.path.basename(image_path)
    
    # Basic categorization based on patterns we can observe
    categories = {
        'tinder_profile': [],
        'instagram_profile': [],
        'dating_conversation': [],
        'social_media': [],
        'other': []
    }
    
    # For now, we'll categorize based on visual analysis
    # In a real implementation, we'd use AI to categorize
    return 'dating_profile'  # Default category

def analyze_screenshot_with_ai(image_path, context="dating_profile"):
    """Analyze screenshot using our AI service"""
    print(f"\n🔍 Analyzing: {os.path.basename(image_path)}")
    
    # Encode image
    image_b64 = encode_image_to_base64(image_path)
    if not image_b64:
        return None
    
    # Prepare request
    payload = {
        "image_data": image_b64,
        "current_text": "Hey! How's your day going?",
        "context": context
    }
    
    try:
        # Send to AI service
        response = requests.post(
            "http://localhost:5000/api/ai/analyze-screenshot",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ AI analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error calling AI service: {e}")
        return None

def test_real_screenshots():
    """Test AI analysis on all real screenshots"""
    print("🎯 Real Screenshot Analysis Test")
    print("=" * 60)
    
    screenshots_dir = "/home/ubuntu/Fliirt/Tests/real_screenshots"
    
    if not os.path.exists(screenshots_dir):
        print(f"❌ Screenshots directory not found: {screenshots_dir}")
        return False
    
    # Get all screenshot files
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not screenshot_files:
        print(f"❌ No screenshot files found in {screenshots_dir}")
        return False
    
    print(f"📱 Found {len(screenshot_files)} screenshots to analyze")
    
    results = []
    successful_analyses = 0
    
    # Test first 5 screenshots for detailed analysis
    test_files = screenshot_files[:5]
    
    for i, filename in enumerate(test_files, 1):
        print(f"\n{'='*20} Test {i}/{len(test_files)} {'='*20}")
        
        image_path = os.path.join(screenshots_dir, filename)
        
        # Analyze with AI
        start_time = time.time()
        result = analyze_screenshot_with_ai(image_path)
        end_time = time.time()
        
        if result and result.get('success'):
            successful_analyses += 1
            
            print(f"✅ Analysis successful in {end_time - start_time:.2f}s")
            print(f"📊 Visual Analysis: {result.get('visual_analysis', 'N/A')[:150]}...")
            
            suggestions = result.get('suggestions', [])
            print(f"\n💕 Generated {len(suggestions)} flirting suggestions:")
            for j, suggestion in enumerate(suggestions, 1):
                print(f"   {j}. {suggestion}")
            
            # Evaluate suggestion quality
            quality_score = evaluate_suggestion_quality(suggestions, result.get('visual_analysis', ''))
            print(f"\n🎯 Suggestion Quality Score: {quality_score}/10")
            
            results.append({
                'filename': filename,
                'success': True,
                'suggestions': suggestions,
                'quality_score': quality_score,
                'processing_time': end_time - start_time,
                'visual_analysis': result.get('visual_analysis', '')
            })
        else:
            print(f"❌ Analysis failed for {filename}")
            results.append({
                'filename': filename,
                'success': False,
                'error': 'AI analysis failed'
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🏁 Real Screenshot Analysis Results")
    print(f"📊 Total Screenshots Tested: {len(test_files)}")
    print(f"✅ Successful Analyses: {successful_analyses}")
    print(f"📈 Success Rate: {(successful_analyses/len(test_files)*100):.1f}%")
    
    if successful_analyses > 0:
        avg_quality = sum(r.get('quality_score', 0) for r in results if r.get('success')) / successful_analyses
        avg_time = sum(r.get('processing_time', 0) for r in results if r.get('success')) / successful_analyses
        print(f"🎯 Average Quality Score: {avg_quality:.1f}/10")
        print(f"⏱️ Average Processing Time: {avg_time:.2f}s")
    
    # Save detailed results
    save_analysis_results(results)
    
    return successful_analyses > 0

def evaluate_suggestion_quality(suggestions, visual_analysis):
    """Evaluate the quality of generated suggestions"""
    if not suggestions:
        return 0
    
    score = 0
    max_score = 10
    
    # Check basic requirements
    if len(suggestions) >= 3:
        score += 2  # Has required number of suggestions
    
    # Check for variety
    if len(set(suggestions)) == len(suggestions):
        score += 1  # All suggestions are unique
    
    # Check length appropriateness
    appropriate_length = sum(1 for s in suggestions if 20 <= len(s) <= 120)
    score += min(2, appropriate_length)  # Up to 2 points for appropriate length
    
    # Check for engagement elements
    engagement_words = ['?', '!', 'love', 'amazing', 'beautiful', 'gorgeous', 'stunning', 'wow']
    engagement_count = sum(1 for s in suggestions if any(word in s.lower() for word in engagement_words))
    score += min(2, engagement_count)  # Up to 2 points for engagement
    
    # Check for personalization (if visual analysis mentions specific details)
    if visual_analysis and len(visual_analysis) > 50:
        # Look for references to specific details
        personal_words = ['photo', 'picture', 'style', 'look', 'outfit', 'smile', 'eyes']
        personal_count = sum(1 for s in suggestions if any(word in s.lower() for word in personal_words))
        score += min(2, personal_count)  # Up to 2 points for personalization
    
    # Check for appropriate tone (not too aggressive, not too bland)
    tone_score = 0
    for suggestion in suggestions:
        if any(word in suggestion.lower() for word in ['hey', 'hi', 'love', 'like', 'beautiful']):
            tone_score += 1
    score += min(1, tone_score)  # 1 point for appropriate tone
    
    return min(score, max_score)

def save_analysis_results(results):
    """Save analysis results to file"""
    results_file = "/home/ubuntu/Fliirt/Tests/real_screenshot_analysis_results.json"
    
    try:
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_tested': len(results),
                'successful': sum(1 for r in results if r.get('success')),
                'results': results
            }, f, indent=2)
        
        print(f"📄 Detailed results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")

def test_specific_scenarios():
    """Test specific dating scenarios with targeted suggestions"""
    print(f"\n{'='*60}")
    print("🎭 Testing Specific Dating Scenarios")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Fitness Enthusiast Profile',
            'context': 'Profile shows gym photos and fitness content',
            'expected_themes': ['fitness', 'workout', 'gym', 'active', 'health']
        },
        {
            'name': 'Travel Lover Profile', 
            'context': 'Profile shows travel photos and adventure content',
            'expected_themes': ['travel', 'adventure', 'explore', 'places', 'journey']
        },
        {
            'name': 'Professional Profile',
            'context': 'Profile shows professional photos and career content',
            'expected_themes': ['career', 'professional', 'ambitious', 'success', 'goals']
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Testing: {scenario['name']}")
        print(f"📝 Context: {scenario['context']}")
        
        # For now, we'll use mock analysis since we need actual AI integration
        # In real implementation, this would analyze actual screenshots
        mock_suggestions = generate_mock_suggestions_for_scenario(scenario)
        
        print(f"💕 Generated suggestions:")
        for i, suggestion in enumerate(mock_suggestions, 1):
            print(f"   {i}. {suggestion}")
        
        # Check if suggestions match expected themes
        theme_matches = sum(1 for suggestion in mock_suggestions 
                          if any(theme in suggestion.lower() for theme in scenario['expected_themes']))
        
        print(f"🎯 Theme relevance: {theme_matches}/{len(mock_suggestions)} suggestions match expected themes")

def generate_mock_suggestions_for_scenario(scenario):
    """Generate mock suggestions for testing scenarios"""
    scenario_suggestions = {
        'Fitness Enthusiast Profile': [
            "I see you're into fitness! What's your favorite workout routine? 💪",
            "Your dedication to staying healthy is inspiring! Gym buddies? 😊",
            "Love the active lifestyle! What's your next fitness goal? 🏃‍♀️"
        ],
        'Travel Lover Profile': [
            "Your travel photos are amazing! What's been your favorite destination? ✈️",
            "I love your adventurous spirit! Where's next on your bucket list? 🌍",
            "Those travel shots are incredible! Any hidden gems you'd recommend? 📸"
        ],
        'Professional Profile': [
            "Your professional success is impressive! What drives your passion? 💼",
            "Love the ambitious energy! What's exciting in your career right now? 🚀",
            "Your achievements are inspiring! Coffee to discuss goals? ☕"
        ]
    }
    
    return scenario_suggestions.get(scenario['name'], [
        "Hey! Your profile caught my attention 😊",
        "I'd love to get to know you better!",
        "You seem like someone with great stories to tell ✨"
    ])

def main():
    """Run all real screenshot tests"""
    print("🚀 Flirrt.ai Real Screenshot Analysis Test Suite")
    print("=" * 70)
    
    # Check if AI service is running
    try:
        response = requests.get("http://localhost:5000/api/ai/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI service is running and healthy")
        else:
            print("⚠️ AI service responded but may have issues")
    except:
        print("❌ AI service not available - using mock analysis")
        return False
    
    # Run tests
    tests = [
        ("Real Screenshot Analysis", test_real_screenshots),
        ("Specific Scenario Testing", test_specific_scenarios)
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
    
    print(f"\n{'='*70}")
    print(f"🏁 Real Screenshot Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All real screenshot tests passed! AI analysis is working with real data.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

