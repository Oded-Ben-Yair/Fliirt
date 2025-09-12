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
        
        # For deployment, use mock analysis and suggestions
        # In production, this would integrate with actual AI models
        
        mock_analysis = f"""
        Based on the provided screenshot analysis:
        
        Profile Analysis:
        - The image appears to be a dating app profile
        - Current message context: "{current_text}"
        - Context: {context}
        
        Key observations for personalized suggestions:
        - Profile shows someone who values authenticity
        - Interests appear to include lifestyle and social activities
        - The conversation context suggests a casual, friendly approach would work well
        
        Recommendation: Use warm, engaging openers that reference shared interests or ask thoughtful questions.
        """
        
        # High-quality flirting suggestions
        suggestions = [
            "Hey! I love your vibe - what's been the highlight of your week? ✨",
            "Your profile caught my eye! What's your favorite way to spend a weekend?",
            "Hi there! You seem like someone who knows how to have fun 😊"
        ]
        
        return jsonify({
            'success': True,
            'visual_analysis': mock_analysis,
            'suggestions': suggestions,
            'timestamp': data.get('timestamp', ''),
            'model_used': {
                'visual': 'mock-analysis',
                'flirting': 'mock-suggestions'
            }
        })
        
    except Exception as e:
        print(f"❌ Error in analyze_screenshot: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

