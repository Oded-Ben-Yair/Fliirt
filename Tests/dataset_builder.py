#!/usr/bin/env python3
"""
Comprehensive Dataset Builder and Testing Framework for Flirrt.ai
Builds diverse testing dataset and implements quality scoring system
"""

import os
import json
import base64
import random
from typing import Dict, List, Any, Tuple
from pathlib import Path
import requests
from datetime import datetime

class FlirrtDatasetBuilder:
    def __init__(self, dataset_dir: str = "Tests/dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.user_screenshots_dir = self.dataset_dir / "user_screenshots"
        self.web_screenshots_dir = self.dataset_dir / "web_screenshots"
        self.test_results_dir = self.dataset_dir / "test_results"
        
        # Create directories
        for dir_path in [self.user_screenshots_dir, self.web_screenshots_dir, self.test_results_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def categorize_screenshots(self) -> Dict[str, List[str]]:
        """Categorize screenshots by type and demographics"""
        categories = {
            "male_profiles": [],
            "female_profiles": [],
            "group_photos": [],
            "activity_photos": [],
            "conversation_screenshots": [],
            "bio_heavy": [],
            "photo_heavy": []
        }
        
        # Get all image files
        all_images = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            all_images.extend(self.user_screenshots_dir.glob(ext))
            all_images.extend(self.web_screenshots_dir.glob(ext))
        
        # Basic categorization (would be enhanced with AI analysis)
        for img_path in all_images:
            filename = img_path.name.lower()
            
            # Simple heuristic categorization
            if 'male' in filename or 'man' in filename:
                categories["male_profiles"].append(str(img_path))
            elif 'female' in filename or 'woman' in filename:
                categories["female_profiles"].append(str(img_path))
            elif 'group' in filename:
                categories["group_photos"].append(str(img_path))
            elif 'activity' in filename or 'sport' in filename:
                categories["activity_photos"].append(str(img_path))
            elif 'chat' in filename or 'conversation' in filename:
                categories["conversation_screenshots"].append(str(img_path))
            else:
                # Default categorization
                if len(categories["male_profiles"]) <= len(categories["female_profiles"]):
                    categories["male_profiles"].append(str(img_path))
                else:
                    categories["female_profiles"].append(str(img_path))
        
        return categories
    
    def create_test_scenarios(self) -> List[Dict[str, Any]]:
        """Create diverse test scenarios for comprehensive testing"""
        scenarios = [
            {
                "name": "Young Professional Male",
                "user_gender": "male",
                "target_gender": "female",
                "age_range": "25-30",
                "context": "Professional photos, office/business setting",
                "expected_themes": ["career", "ambition", "lifestyle"]
            },
            {
                "name": "Active Female",
                "user_gender": "female", 
                "target_gender": "male",
                "age_range": "22-28",
                "context": "Outdoor activities, sports, fitness",
                "expected_themes": ["fitness", "adventure", "outdoors"]
            },
            {
                "name": "Creative Artist",
                "user_gender": "any",
                "target_gender": "any",
                "age_range": "20-35",
                "context": "Art, music, creative pursuits",
                "expected_themes": ["creativity", "art", "culture"]
            },
            {
                "name": "Travel Enthusiast",
                "user_gender": "any",
                "target_gender": "any", 
                "age_range": "25-40",
                "context": "Travel photos, different locations",
                "expected_themes": ["travel", "adventure", "culture"]
            },
            {
                "name": "Pet Lover",
                "user_gender": "any",
                "target_gender": "any",
                "age_range": "20-45",
                "context": "Photos with pets, animals",
                "expected_themes": ["pets", "animals", "care"]
            },
            {
                "name": "Foodie",
                "user_gender": "any",
                "target_gender": "any",
                "age_range": "22-40",
                "context": "Food photos, restaurants, cooking",
                "expected_themes": ["food", "cooking", "restaurants"]
            }
        ]
        return scenarios
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 for API calls"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def quality_score_suggestion(self, suggestion: str, context: Dict[str, Any]) -> Dict[str, float]:
        """Score a flirting suggestion based on multiple criteria"""
        scores = {
            "relevance": 0.0,      # How relevant to the profile
            "creativity": 0.0,     # How creative/original
            "appropriateness": 0.0, # How appropriate for dating
            "engagement": 0.0,     # Likely to get a response
            "specificity": 0.0     # How specific vs generic
        }
        
        suggestion_lower = suggestion.lower()
        
        # Relevance scoring
        expected_themes = context.get("expected_themes", [])
        theme_matches = sum(1 for theme in expected_themes if theme in suggestion_lower)
        scores["relevance"] = min(theme_matches / max(len(expected_themes), 1), 1.0)
        
        # Creativity scoring (avoid generic phrases)
        generic_phrases = ["hey", "hi", "how are you", "what's up", "nice pics"]
        generic_count = sum(1 for phrase in generic_phrases if phrase in suggestion_lower)
        scores["creativity"] = max(0.0, 1.0 - (generic_count * 0.3))
        
        # Appropriateness scoring (avoid inappropriate content)
        inappropriate_words = ["sexy", "hot", "body", "bed", "night"]
        inappropriate_count = sum(1 for word in inappropriate_words if word in suggestion_lower)
        scores["appropriateness"] = max(0.0, 1.0 - (inappropriate_count * 0.5))
        
        # Engagement scoring (questions and conversation starters)
        engagement_indicators = ["?", "what", "how", "where", "when", "tell me"]
        engagement_count = sum(1 for indicator in engagement_indicators if indicator in suggestion_lower)
        scores["engagement"] = min(engagement_count * 0.3, 1.0)
        
        # Specificity scoring (specific details vs generic)
        if len(suggestion.split()) > 10:  # Longer, more detailed suggestions
            scores["specificity"] = 0.8
        elif len(suggestion.split()) > 5:
            scores["specificity"] = 0.5
        else:
            scores["specificity"] = 0.2
        
        return scores
    
    def calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        weights = {
            "relevance": 0.3,
            "creativity": 0.2,
            "appropriateness": 0.25,
            "engagement": 0.15,
            "specificity": 0.1
        }
        
        overall = sum(scores[metric] * weights[metric] for metric in weights)
        return round(overall, 3)
    
    def generate_test_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(test_results)
        if total_tests == 0:
            return {"error": "No test results to analyze"}
        
        # Calculate aggregate statistics
        all_scores = [result["overall_score"] for result in test_results]
        avg_score = sum(all_scores) / len(all_scores)
        
        # Score distribution
        excellent = sum(1 for score in all_scores if score >= 0.8)
        good = sum(1 for score in all_scores if 0.6 <= score < 0.8)
        fair = sum(1 for score in all_scores if 0.4 <= score < 0.6)
        poor = sum(1 for score in all_scores if score < 0.4)
        
        # Metric analysis
        metrics = ["relevance", "creativity", "appropriateness", "engagement", "specificity"]
        metric_averages = {}
        for metric in metrics:
            metric_scores = [result["detailed_scores"][metric] for result in test_results]
            metric_averages[metric] = sum(metric_scores) / len(metric_scores)
        
        # Performance by scenario
        scenario_performance = {}
        for result in test_results:
            scenario = result.get("scenario", "unknown")
            if scenario not in scenario_performance:
                scenario_performance[scenario] = []
            scenario_performance[scenario].append(result["overall_score"])
        
        for scenario in scenario_performance:
            scores = scenario_performance[scenario]
            scenario_performance[scenario] = {
                "average_score": sum(scores) / len(scores),
                "test_count": len(scores),
                "best_score": max(scores),
                "worst_score": min(scores)
            }
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "average_score": round(avg_score, 3),
                "score_distribution": {
                    "excellent (0.8+)": excellent,
                    "good (0.6-0.8)": good,
                    "fair (0.4-0.6)": fair,
                    "poor (<0.4)": poor
                }
            },
            "metric_analysis": {metric: round(score, 3) for metric, score in metric_averages.items()},
            "scenario_performance": scenario_performance,
            "recommendations": self.generate_recommendations(metric_averages, avg_score),
            "timestamp": datetime.now().isoformat()
        }
        
        return report
    
    def generate_recommendations(self, metric_averages: Dict[str, float], avg_score: float) -> List[str]:
        """Generate improvement recommendations based on test results"""
        recommendations = []
        
        if avg_score < 0.6:
            recommendations.append("Overall performance needs significant improvement. Focus on prompt engineering.")
        
        if metric_averages["relevance"] < 0.6:
            recommendations.append("Improve visual analysis to better identify profile elements for relevant suggestions.")
        
        if metric_averages["creativity"] < 0.6:
            recommendations.append("Enhance creativity by avoiding generic phrases and generating more original content.")
        
        if metric_averages["appropriateness"] < 0.8:
            recommendations.append("Review content filters to ensure all suggestions are appropriate for dating context.")
        
        if metric_averages["engagement"] < 0.6:
            recommendations.append("Include more questions and conversation starters to improve engagement potential.")
        
        if metric_averages["specificity"] < 0.6:
            recommendations.append("Generate more detailed, specific suggestions rather than generic responses.")
        
        if not recommendations:
            recommendations.append("Performance is good! Continue fine-tuning for optimal results.")
        
        return recommendations
    
    def save_dataset_info(self):
        """Save dataset information and statistics"""
        categories = self.categorize_screenshots()
        scenarios = self.create_test_scenarios()
        
        dataset_info = {
            "total_images": sum(len(files) for files in categories.values()),
            "categories": {cat: len(files) for cat, files in categories.items()},
            "test_scenarios": len(scenarios),
            "created_at": datetime.now().isoformat(),
            "scenarios": scenarios
        }
        
        info_path = self.dataset_dir / "dataset_info.json"
        with open(info_path, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        print(f"Dataset info saved to {info_path}")
        print(f"Total images: {dataset_info['total_images']}")
        print(f"Categories: {dataset_info['categories']}")
        
        return dataset_info

def main():
    """Main function to build and validate dataset"""
    print("🔬 Building Flirrt.ai Testing Dataset and Framework")
    print("=" * 60)
    
    builder = FlirrtDatasetBuilder()
    
    # Build dataset information
    dataset_info = builder.save_dataset_info()
    
    # Create sample test scenarios
    scenarios = builder.create_test_scenarios()
    print(f"\n📋 Created {len(scenarios)} test scenarios:")
    for scenario in scenarios:
        print(f"  - {scenario['name']}: {scenario['context']}")
    
    # Demonstrate quality scoring
    print(f"\n🎯 Quality Scoring Framework:")
    sample_suggestions = [
        "Hey, how's it going?",
        "I love your hiking photos! What's your favorite trail?",
        "Your dog is adorable! What's their name?",
        "I see you're into photography - that sunset shot is amazing! Do you have a favorite spot for golden hour shots?"
    ]
    
    sample_context = {
        "expected_themes": ["hiking", "photography", "pets"],
        "scenario": "Active Female"
    }
    
    for suggestion in sample_suggestions:
        scores = builder.quality_score_suggestion(suggestion, sample_context)
        overall = builder.calculate_overall_score(scores)
        print(f"  '{suggestion[:50]}...' → Score: {overall}")
    
    print(f"\n✅ Dataset framework ready for AI testing!")
    print(f"📁 Dataset location: {builder.dataset_dir}")
    print(f"🧪 Ready to test with {dataset_info['total_images']} images across {len(scenarios)} scenarios")

if __name__ == "__main__":
    main()

