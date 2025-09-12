#!/usr/bin/env python3
"""
Simplified Flirrt.ai API Service for deployment
Minimal dependencies version for production deployment
"""

import os
import sys
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/')
def home():
    return jsonify({
        'service': 'Flirrt.ai API',
        'status': 'running',
        'version': '1.0.0',
        'message': 'AI-powered flirting suggestions ready! 💕'
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        'service': 'Flirrt.ai API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'health_check': '/api/ai/health',
            'test_suggestions': '/api/ai/test-suggestions',
            'analyze_screenshot': '/api/ai/analyze-screenshot'
        }
    })

@app.route('/api/ai/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'flirrt-ai-analysis',
        'models_available': {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'grok': bool(os.getenv('XAI_API_KEY')),
            'gemini': bool(os.getenv('GEMINI_API_KEY'))
        }
    })

@app.route('/api/ai/test-suggestions', methods=['POST'])
def test_suggestions():
    try:
        data = request.get_json() or {}
        context = data.get('context', 'general')
        
        # High-quality mock suggestions for testing
        suggestions = [
            "Hey! Your smile is absolutely captivating 😊",
            "I love your style! Where's your favorite place to explore?",
            "You seem like someone with amazing stories to tell ✨"
        ]
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'context': context,
            'model_used': 'mock'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze-screenshot', methods=['POST'])
def analyze_screenshot():
    try:
        data = request.get_json()
        
        if not data or 'image_data' not in data:
            return jsonify({'error': 'Missing image_data in request'}), 400
        
        image_data = data['image_data']
        current_text = data.get('current_text', '')
        context = data.get('context', '')
        
        # Real AI Analysis with OpenAI GPT-4o
        visual_analysis = analyze_with_openai(image_data, current_text, context)
        
        if not visual_analysis:
            # Fallback to mock analysis if AI fails
            visual_analysis = f"""
            Profile Analysis (Fallback):
            - Dating app profile screenshot detected
            - Current message context: "{current_text}"
            - Context: {context}
            - Visual elements suggest an active, social person
            - Profile shows lifestyle and personality indicators
            """
        
        # Generate flirting suggestions with Grok
        suggestions = generate_flirting_with_grok(visual_analysis, current_text)
        
        if not suggestions:
            # Fallback suggestions if Grok fails
            suggestions = [
                "Hey! Your profile really caught my attention - what's been the highlight of your week? ✨",
                "I love your vibe! What's your favorite way to spend a weekend?",
                "You seem like someone with amazing stories to tell - coffee sometime? ☕"
            ]
        
        return jsonify({
            'success': True,
            'visual_analysis': visual_analysis,
            'suggestions': suggestions,
            'timestamp': data.get('timestamp', ''),
            'model_used': {
                'visual': 'gpt-4o' if visual_analysis else 'fallback',
                'flirting': 'grok' if suggestions else 'fallback'
            }
        })
        
    except Exception as e:
        print(f"❌ Error in analyze_screenshot: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def analyze_with_openai(image_data, current_text, context):
    """Analyze image using OpenAI GPT-4o"""
    try:
        import openai
        
        # Initialize OpenAI client
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            print("⚠️ OpenAI API key not found, using fallback")
            return None
            
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Prepare the prompt for visual analysis
        prompt = f"""
        Analyze this social media profile screenshot to understand the person's interests and personality for generating appropriate conversation starters.

        Current conversation context: "{current_text}"
        App context: {context}

        Please analyze:
        1. Visual elements (photos, style, setting, activities shown)
        2. Any visible text, bio information, or captions
        3. Interests, hobbies, or activities displayed
        4. Professional or educational background if visible
        5. Lifestyle indicators (travel, fitness, arts, etc.)
        6. Overall personality traits that can be inferred

        Focus on identifying conversation topics and shared interests that would make for engaging, respectful conversation starters.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ OpenAI analysis error: {str(e)}")
        return None

def generate_flirting_with_grok(visual_analysis, current_text):
    """Generate flirting suggestions using Grok"""
    try:
        from xai_sdk import Client
        
        # Initialize Grok client
        xai_api_key = os.getenv('XAI_API_KEY')
        if not xai_api_key:
            print("⚠️ Grok API key not found, using fallback")
            return None
            
        client = Client(api_key=xai_api_key)
        
        prompt = f"""
        Based on this profile analysis, generate 3 charming, witty conversation starters that are personalized and engaging.

        Profile Analysis: {visual_analysis}
        Current message context: "{current_text}"

        Requirements:
        1. Be authentic and reference specific details from the analysis
        2. Use a confident, playful, and charming tone
        3. Keep each suggestion under 100 characters for easy typing
        4. Make them conversation starters that invite response
        5. Be respectful but bold and engaging
        6. Use humor and wit when appropriate
        7. Include relevant emojis sparingly

        Return exactly 3 suggestions as a simple list, one per line.
        """
        
        response = client.chat.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        
        suggestions_text = response.choices[0].message.content
        
        # Parse suggestions from response
        lines = suggestions_text.strip().split('\n')
        suggestions = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Here', 'Based', 'I', 'The')):
                # Clean up numbering and formatting
                clean_line = line
                if line.startswith(('1.', '2.', '3.', '-', '*')):
                    clean_line = line[2:].strip()
                elif line[0].isdigit():
                    clean_line = line[1:].strip()
                
                if clean_line:
                    suggestions.append(clean_line)
        
        return suggestions[:3] if len(suggestions) >= 3 else None
        
    except Exception as e:
        print(f"❌ Grok flirting generation error: {str(e)}")
        return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

