import os
import base64
import json
from flask import Blueprint, request, jsonify
from openai import OpenAI
import requests
from xai_sdk import Client as XAIClient
import google.generativeai as genai

ai_bp = Blueprint('ai', __name__)

# Initialize AI clients
openai_client = OpenAI()
xai_client = XAIClient(api_key=os.getenv('XAI_API_KEY'))
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@ai_bp.route('/analyze-screenshot', methods=['POST'])
def analyze_screenshot():
    """
    Analyze a screenshot and generate flirting suggestions
    
    Expected payload:
    {
        "image_data": "base64_encoded_image",
        "current_text": "optional_current_message_text",
        "context": "optional_additional_context"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image_data' not in data:
            return jsonify({'error': 'Missing image_data in request'}), 400
        
        image_data = data['image_data']
        current_text = data.get('current_text', '')
        context = data.get('context', '')
        
        # Step 1: Visual Analysis with GPT-4o
        visual_analysis = analyze_image_with_openai(image_data, current_text, context)
        
        if not visual_analysis:
            # Fallback to Gemini for visual analysis
            visual_analysis = analyze_image_with_gemini(image_data, current_text, context)
        
        if not visual_analysis:
            return jsonify({'error': 'Failed to analyze image'}), 500
        
        # Step 2: Generate flirting suggestions with OpenAI (skip Grok for now)
        flirting_suggestions = generate_flirting_with_openai(visual_analysis, current_text)
        
        if not flirting_suggestions:
            # Fallback to mock suggestions
            flirting_suggestions = [
                "Hey! I love your style 😍",
                "That photo is amazing! Where was it taken?",
                "You seem like someone I'd love to get to know better ✨"
            ]
        
        return jsonify({
            'success': True,
            'visual_analysis': visual_analysis,
            'suggestions': flirting_suggestions,
            'timestamp': data.get('timestamp', ''),
            'model_used': {
                'visual': 'gpt-4o',
                'flirting': 'gpt-4o'
            }
        })
        
    except Exception as e:
        print(f"❌ Error in analyze_screenshot: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def analyze_image_with_openai(image_data, current_text, context):
    """Analyze image using OpenAI GPT-5/4o for visual understanding"""
    try:
        # Prepare the image for OpenAI API
        image_url = f"data:image/jpeg;base64,{image_data}"
        
        prompt = f"""
        Analyze this dating app screenshot and extract key information for generating personalized flirting suggestions.

        Current message context: "{current_text}"
        Additional context: "{context}"

        Please analyze:
        1. Profile information visible (name, age, bio, interests, photos)
        2. Previous conversation context if visible
        3. Visual cues about personality, interests, lifestyle
        4. Any specific details that could be used for personalized conversation starters
        5. The overall vibe/energy of the person's profile

        Provide a detailed analysis that will help generate authentic, personalized flirting suggestions.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o as GPT-5 may not be available yet
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ OpenAI visual analysis error: {str(e)}")
        return None

def analyze_image_with_gemini(image_data, current_text, context):
    """Fallback visual analysis using Google Gemini"""
    try:
        # Convert base64 to bytes for Gemini
        image_bytes = base64.b64decode(image_data)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""
        Analyze this dating app screenshot for generating personalized flirting suggestions.

        Current message: "{current_text}"
        Context: "{context}"

        Extract: profile details, interests, conversation context, personality cues, and any specific details for personalized conversation starters.
        """
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        
        return response.text
        
    except Exception as e:
        print(f"❌ Gemini visual analysis error: {str(e)}")
        return None

def generate_flirting_with_grok(visual_analysis, current_text):
    """Generate flirting suggestions using Grok 4 for human-like charm"""
    try:
        prompt = f"""
        Based on this visual analysis of a dating app profile, generate 3 charming, witty flirting suggestions.

        Visual Analysis: {visual_analysis}
        Current message context: "{current_text}"

        Requirements:
        1. Be authentic and personalized based on the analysis
        2. Use a confident, playful, and charming tone
        3. Reference specific details from their profile when possible
        4. Keep each suggestion under 100 characters for easy typing
        5. Make them conversation starters that invite response
        6. Be respectful but bold and engaging
        7. Use humor and wit when appropriate

        Return exactly 3 suggestions as a JSON array of strings.
        """
        
        response = xai_client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        suggestions_text = response.choices[0].message.content
        
        # Try to parse as JSON, fallback to manual parsing
        try:
            suggestions = json.loads(suggestions_text)
            if isinstance(suggestions, list) and len(suggestions) >= 3:
                return suggestions[:3]
        except:
            # Manual parsing if JSON fails
            lines = suggestions_text.strip().split('\n')
            suggestions = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('[') and not line.startswith(']'):
                    # Remove quotes and numbering
                    clean_line = line.strip('"').strip("'").strip()
                    if clean_line.startswith(('1.', '2.', '3.', '-', '*')):
                        clean_line = clean_line[2:].strip()
                    if clean_line:
                        suggestions.append(clean_line)
            
            return suggestions[:3] if len(suggestions) >= 3 else None
        
        return None
        
    except Exception as e:
        print(f"❌ Grok flirting generation error: {str(e)}")
        return None

def generate_flirting_with_openai(visual_analysis, current_text):
    """Fallback flirting generation using OpenAI"""
    try:
        prompt = f"""
        Generate 3 charming flirting suggestions based on this dating profile analysis.

        Analysis: {visual_analysis}
        Current message: "{current_text}"

        Make them personalized, witty, under 100 characters each, and conversation-starting.
        Return as JSON array of 3 strings.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        suggestions = result.get('suggestions', [])
        
        return suggestions[:3] if len(suggestions) >= 3 else None
        
    except Exception as e:
        print(f"❌ OpenAI flirting generation error: {str(e)}")
        return None

@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'flirrt-ai-analysis',
        'models_available': {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'grok': bool(os.getenv('XAI_API_KEY')),
            'gemini': bool(os.getenv('GEMINI_API_KEY'))
        }
    })

@ai_bp.route('/test-suggestions', methods=['POST'])
def test_suggestions():
    """Test endpoint for generating mock suggestions"""
    try:
        data = request.get_json()
        context = data.get('context', 'general')
        
        mock_suggestions = [
            "Hey! Your smile is absolutely captivating 😊",
            "I love your style! Where's your favorite place to explore?",
            "You seem like someone with amazing stories to tell ✨"
        ]
        
        return jsonify({
            'success': True,
            'suggestions': mock_suggestions,
            'context': context,
            'model_used': 'mock'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

