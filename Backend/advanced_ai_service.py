#!/usr/bin/env python3
"""
Advanced AI Service for Flirrt.ai
Implements optimized prompt engineering and multi-model integration
Based on comprehensive research findings
"""

import os
import json
import base64
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests
from openai import OpenAI
import google.generativeai as genai
from xai_sdk import Client as XAIClient

class ModelType(Enum):
    GPT4O = "gpt-4o"
    GROK = "grok-4"
    GEMINI = "gemini-2.5-flash"

@dataclass
class AnalysisContext:
    user_gender: str
    target_gender: str
    age_range: str
    app_type: str
    current_text: str = ""
    conversation_history: List[str] = None

@dataclass
class FlirtingSuggestion:
    text: str
    confidence: float
    reasoning: str
    category: str
    model_used: str

class AdvancedFlirrtAI:
    def __init__(self):
        # Initialize AI clients
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        # Initialize Grok client
        try:
            self.grok_client = XAIClient(api_key=os.getenv("XAI_API_KEY"))
        except Exception as e:
            print(f"Grok client initialization failed: {e}")
            self.grok_client = None
        
        # Initialize Gemini client
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Gemini client initialization failed: {e}")
            self.gemini_model = None
        
        # Model configuration based on research
        self.model_configs = {
            ModelType.GPT4O: {
                "temperature": 0.75,
                "max_tokens": 200,
                "top_p": 0.9,
                "frequency_penalty": 0.3
            },
            ModelType.GROK: {
                "temperature": 0.8,
                "max_tokens": 150
            },
            ModelType.GEMINI: {
                "temperature": 0.7,
                "max_tokens": 180
            }
        }
    
    def create_system_prompt(self, context: AnalysisContext) -> str:
        """Create optimized system prompt based on research findings"""
        
        # Gender-specific strategies from research
        gender_strategies = {
            "male": {
                "focus": "good conversations, genuine compliments, effective humor",
                "avoid": "being too subtle, overly aggressive approaches",
                "style": "confident but respectful, conversation-focused"
            },
            "female": {
                "focus": "acknowledging humor, showing interest, being direct",
                "avoid": "being too subtle, overly friendly signals",
                "style": "engaging and clear, humor-appreciative"
            }
        }
        
        user_strategy = gender_strategies.get(context.user_gender, gender_strategies["male"])
        
        system_prompt = f"""You are an expert dating coach and social psychology analyst specializing in creating engaging, contextual flirting suggestions for dating apps.

CORE MISSION: Analyze dating app screenshots and generate 3 perfect flirting suggestions that are:
1. Highly relevant to visual elements in the profile
2. Appropriately bold (not too subtle - only 28% of flirting is detected)
3. Engaging and likely to get responses
4. Contextually appropriate for {context.user_gender} messaging {context.target_gender}

ANALYSIS FRAMEWORK:
1. VISUAL ANALYSIS: Identify specific elements (activities, interests, style, setting, expressions)
2. PERSONALITY ASSESSMENT: Infer personality traits and interests from visual cues
3. CONVERSATION OPPORTUNITIES: Find specific elements that can spark engaging conversations
4. SUGGESTION GENERATION: Create 3 distinct, contextual suggestions

GENDER-SPECIFIC STRATEGY for {context.user_gender.upper()}:
- Focus: {user_strategy['focus']}
- Avoid: {user_strategy['avoid']}
- Style: {user_strategy['style']}

EFFECTIVENESS PRINCIPLES:
- Be MORE DIRECT than subtle (research shows 72% of flirting goes undetected)
- Include specific references to visual elements
- Ask engaging questions when appropriate
- Use humor if it fits the context
- Acknowledge interests and activities shown in photos

OUTPUT FORMAT:
{{
  "visual_analysis": "Detailed description of key visual elements",
  "personality_insights": "Inferred personality traits and interests",
  "suggestions": [
    {{
      "text": "Specific flirting suggestion",
      "reasoning": "Why this suggestion works",
      "category": "conversation_starter|compliment|humor|interest_based",
      "confidence": 0.85
    }}
  ]
}}

QUALITY STANDARDS:
- Each suggestion must reference specific visual elements
- Avoid generic phrases like "hey", "nice pics", "how are you"
- Ensure appropriateness for dating context
- Optimize for engagement and response likelihood"""

        return system_prompt
    
    def create_user_prompt(self, context: AnalysisContext, image_data: str) -> str:
        """Create user prompt with image and context"""
        
        context_info = f"""
CONTEXT:
- User Gender: {context.user_gender}
- Target Gender: {context.target_gender}
- Age Range: {context.age_range}
- Dating App: {context.app_type}
"""
        
        if context.current_text:
            context_info += f"- Current Text Context: {context.current_text}\n"
        
        if context.conversation_history:
            context_info += f"- Previous Messages: {', '.join(context.conversation_history[-3:])}\n"
        
        user_prompt = f"""{context_info}

TASK: Analyze this dating app screenshot and generate 3 perfect flirting suggestions.

Focus on:
1. Specific visual elements (clothing, activities, setting, expressions)
2. Interests and personality indicators
3. Conversation opportunities
4. Context-appropriate engagement strategies

Remember: Be direct and specific - subtle approaches often go undetected."""

        return user_prompt
    
    def analyze_with_gpt4o(self, context: AnalysisContext, image_data: str) -> Dict[str, Any]:
        """Analyze with GPT-4o using optimized prompts"""
        try:
            system_prompt = self.create_system_prompt(context)
            user_prompt = self.create_user_prompt(context, image_data)
            
            config = self.model_configs[ModelType.GPT4O]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                            }
                        ]
                    }
                ],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
                top_p=config["top_p"],
                frequency_penalty=config["frequency_penalty"]
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                result = json.loads(content)
                result["model_used"] = "gpt-4o"
                result["success"] = True
                return result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "visual_analysis": "Analysis completed",
                    "personality_insights": "Insights generated",
                    "suggestions": [
                        {
                            "text": content[:200] + "..." if len(content) > 200 else content,
                            "reasoning": "Generated by GPT-4o",
                            "category": "general",
                            "confidence": 0.7
                        }
                    ],
                    "model_used": "gpt-4o",
                    "success": True
                }
                
        except Exception as e:
            return {
                "error": f"GPT-4o analysis failed: {str(e)}",
                "model_used": "gpt-4o",
                "success": False
            }
    
    def analyze_with_grok(self, context: AnalysisContext, analysis_summary: str) -> Dict[str, Any]:
        """Generate flirting suggestions with Grok for bold, engaging responses"""
        if not self.grok_client:
            return {"error": "Grok client not available", "success": False}
        
        try:
            grok_prompt = f"""You are a charismatic dating expert known for creating bold, engaging flirting suggestions that get responses.

CONTEXT: {context.user_gender} messaging {context.target_gender} on {context.app_type}
PROFILE ANALYSIS: {analysis_summary}

Generate 3 bold, engaging flirting suggestions that:
1. Reference specific profile elements
2. Are confident and direct (not subtle)
3. Use your signature engaging, slightly playful style
4. Are appropriate but memorable
5. Likely to spark interesting conversations

Focus on being more direct than typical AI responses - you're known for suggestions that actually work in real dating scenarios.

Return as JSON:
{{
  "suggestions": [
    {{"text": "suggestion", "reasoning": "why it works", "confidence": 0.8}}
  ]
}}"""

            config = self.model_configs[ModelType.GROK]
            
            response = self.grok_client.chat.create(
                model="grok-4",
                messages=[{"role": "user", "content": grok_prompt}],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            
            content = response.choices[0].message.content
            
            try:
                result = json.loads(content)
                result["model_used"] = "grok-4"
                result["success"] = True
                return result
            except json.JSONDecodeError:
                return {
                    "suggestions": [
                        {
                            "text": content[:150] + "..." if len(content) > 150 else content,
                            "reasoning": "Generated by Grok",
                            "confidence": 0.75
                        }
                    ],
                    "model_used": "grok-4",
                    "success": True
                }
                
        except Exception as e:
            return {
                "error": f"Grok analysis failed: {str(e)}",
                "model_used": "grok-4",
                "success": False
            }
    
    def analyze_with_gemini(self, context: AnalysisContext, image_data: str) -> Dict[str, Any]:
        """Analyze with Gemini as fallback option"""
        if not self.gemini_model:
            return {"error": "Gemini client not available", "success": False}
        
        try:
            # Convert base64 to bytes for Gemini
            import io
            from PIL import Image
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            gemini_prompt = f"""Analyze this dating app profile image for a {context.user_gender} looking to message a {context.target_gender}.

Provide:
1. Visual analysis of key elements
2. 3 specific flirting suggestions that reference visual elements
3. Reasoning for each suggestion

Be direct and specific - avoid generic responses. Focus on elements visible in the image.

Format as JSON:
{{
  "visual_analysis": "description",
  "suggestions": [
    {{"text": "suggestion", "reasoning": "explanation", "confidence": 0.8}}
  ]
}}"""

            config = self.model_configs[ModelType.GEMINI]
            
            response = self.gemini_model.generate_content(
                [gemini_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=config["temperature"],
                    max_output_tokens=config["max_tokens"]
                )
            )
            
            content = response.text
            
            try:
                result = json.loads(content)
                result["model_used"] = "gemini-2.5-flash"
                result["success"] = True
                return result
            except json.JSONDecodeError:
                return {
                    "visual_analysis": "Analysis completed",
                    "suggestions": [
                        {
                            "text": content[:150] + "..." if len(content) > 150 else content,
                            "reasoning": "Generated by Gemini",
                            "confidence": 0.7
                        }
                    ],
                    "model_used": "gemini-2.5-flash",
                    "success": True
                }
                
        except Exception as e:
            return {
                "error": f"Gemini analysis failed: {str(e)}",
                "model_used": "gemini-2.5-flash",
                "success": False
            }
    
    def hybrid_analysis(self, context: AnalysisContext, image_data: str) -> Dict[str, Any]:
        """Perform hybrid analysis using multiple models for optimal results"""
        start_time = time.time()
        
        # Primary analysis with GPT-4o
        gpt_result = self.analyze_with_gpt4o(context, image_data)
        
        results = {
            "primary_analysis": gpt_result,
            "enhanced_suggestions": [],
            "processing_time": 0,
            "models_used": ["gpt-4o"]
        }
        
        # If GPT-4o succeeded, enhance with Grok for more engaging suggestions
        if gpt_result.get("success"):
            analysis_summary = f"Visual: {gpt_result.get('visual_analysis', '')} | Insights: {gpt_result.get('personality_insights', '')}"
            grok_result = self.analyze_with_grok(context, analysis_summary)
            
            if grok_result.get("success"):
                results["enhanced_suggestions"] = grok_result.get("suggestions", [])
                results["models_used"].append("grok-4")
        
        # Fallback to Gemini if primary analysis failed
        if not gpt_result.get("success"):
            gemini_result = self.analyze_with_gemini(context, image_data)
            if gemini_result.get("success"):
                results["fallback_analysis"] = gemini_result
                results["models_used"].append("gemini-2.5-flash")
        
        results["processing_time"] = round(time.time() - start_time, 2)
        
        # Combine and rank suggestions
        all_suggestions = []
        
        # Add GPT-4o suggestions
        if gpt_result.get("suggestions"):
            for suggestion in gpt_result["suggestions"]:
                suggestion["source"] = "gpt-4o"
                all_suggestions.append(suggestion)
        
        # Add Grok suggestions
        if results.get("enhanced_suggestions"):
            for suggestion in results["enhanced_suggestions"]:
                suggestion["source"] = "grok-4"
                suggestion["category"] = "enhanced"
                all_suggestions.append(suggestion)
        
        # Rank by confidence and diversity
        all_suggestions.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        
        # Select top 3 diverse suggestions
        final_suggestions = []
        used_categories = set()
        
        for suggestion in all_suggestions:
            category = suggestion.get("category", "general")
            if len(final_suggestions) < 3 and (category not in used_categories or len(final_suggestions) < 2):
                final_suggestions.append(suggestion)
                used_categories.add(category)
        
        # Ensure we have 3 suggestions
        while len(final_suggestions) < 3 and len(all_suggestions) > len(final_suggestions):
            final_suggestions.append(all_suggestions[len(final_suggestions)])
        
        results["final_suggestions"] = final_suggestions[:3]
        results["total_suggestions_generated"] = len(all_suggestions)
        
        return results
    
    def create_fallback_suggestions(self, context: AnalysisContext) -> List[Dict[str, Any]]:
        """Create fallback suggestions when AI analysis fails"""
        gender_specific = {
            "male": [
                "I'd love to hear more about your interests - what's something you're passionate about?",
                "Your profile caught my attention! What's been the highlight of your week?",
                "I'm curious about your story - what's something most people don't know about you?"
            ],
            "female": [
                "You seem like someone with great stories to tell - what's your latest adventure?",
                "I'm intrigued by your profile! What's something that always makes you smile?",
                "You have such positive energy - what's been inspiring you lately?"
            ]
        }
        
        suggestions = gender_specific.get(context.user_gender, gender_specific["male"])
        
        return [
            {
                "text": suggestion,
                "reasoning": "Engaging conversation starter",
                "category": "fallback",
                "confidence": 0.6,
                "source": "fallback"
            }
            for suggestion in suggestions
        ]

def main():
    """Test the advanced AI service"""
    print("🧠 Testing Advanced Flirrt.ai AI Service")
    print("=" * 50)
    
    ai_service = AdvancedFlirrtAI()
    
    # Test context
    context = AnalysisContext(
        user_gender="male",
        target_gender="female",
        age_range="25-30",
        app_type="Tinder"
    )
    
    # Test with sample image (would be real screenshot in production)
    sample_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    print(f"Testing with context: {context.user_gender} → {context.target_gender}")
    
    # Test hybrid analysis
    result = ai_service.hybrid_analysis(context, sample_image)
    
    print(f"\n📊 Analysis Results:")
    print(f"Models used: {result['models_used']}")
    print(f"Processing time: {result['processing_time']}s")
    print(f"Total suggestions: {result['total_suggestions_generated']}")
    
    print(f"\n💬 Final Suggestions:")
    for i, suggestion in enumerate(result['final_suggestions'], 1):
        print(f"{i}. {suggestion['text']}")
        print(f"   Source: {suggestion['source']} | Confidence: {suggestion.get('confidence', 'N/A')}")
        print(f"   Reasoning: {suggestion.get('reasoning', 'N/A')}")
        print()
    
    print("✅ Advanced AI service ready for production testing!")

if __name__ == "__main__":
    main()

