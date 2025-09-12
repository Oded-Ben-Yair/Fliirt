#!/usr/bin/env python3
"""
Iterative Testing and Quality Scoring System for Flirrt.ai
Implements comprehensive testing with real screenshots and automated quality assessment
"""

import os
import json
import base64
import time
import random
from typing import Dict, List, Any, Tuple
from pathlib import Path
from datetime import datetime
import statistics
import sys

# Add Backend to path for imports
sys.path.append(str(Path(__file__).parent.parent / "Backend"))

from advanced_ai_service import AdvancedFlirrtAI, AnalysisContext
from dataset_builder import FlirrtDatasetBuilder

class IterativeTestingSystem:
    def __init__(self, dataset_dir: str = "dataset"):
        self.dataset_dir = Path(dataset_dir)
        self.results_dir = self.dataset_dir / "test_results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.ai_service = AdvancedFlirrtAI()
        self.dataset_builder = FlirrtDatasetBuilder(str(self.dataset_dir))
        
        # Test configuration
        self.test_scenarios = self.dataset_builder.create_test_scenarios()
        self.quality_thresholds = {
            "excellent": 0.8,
            "good": 0.6,
            "acceptable": 0.4,
            "poor": 0.0
        }
        
        # Performance tracking
        self.iteration_history = []
        self.best_scores = {}
        self.improvement_targets = {}
    
    def get_test_images(self) -> List[str]:
        """Get all test images from dataset"""
        image_files = []
        
        # Get user screenshots
        user_dir = self.dataset_dir / "user_screenshots"
        if user_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                image_files.extend(user_dir.glob(ext))
        
        # Get web screenshots
        web_dir = self.dataset_dir / "web_screenshots"
        if web_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                image_files.extend(web_dir.glob(ext))
        
        return [str(img) for img in image_files]
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image {image_path}: {e}")
            return ""
    
    def create_test_context(self, scenario: Dict[str, Any], image_path: str) -> AnalysisContext:
        """Create test context from scenario and image"""
        
        # Determine genders based on scenario or randomize
        if scenario["user_gender"] == "any":
            user_gender = random.choice(["male", "female"])
        else:
            user_gender = scenario["user_gender"]
        
        if scenario["target_gender"] == "any":
            target_gender = random.choice(["male", "female"])
        else:
            target_gender = scenario["target_gender"]
        
        # Determine app type based on image name or randomize
        image_name = Path(image_path).name.lower()
        if "tinder" in image_name:
            app_type = "Tinder"
        elif "bumble" in image_name:
            app_type = "Bumble"
        elif "hinge" in image_name:
            app_type = "Hinge"
        else:
            app_type = random.choice(["Tinder", "Bumble", "Hinge", "Instagram"])
        
        return AnalysisContext(
            user_gender=user_gender,
            target_gender=target_gender,
            age_range=scenario["age_range"],
            app_type=app_type,
            current_text="",
            conversation_history=[]
        )
    
    def enhanced_quality_scoring(self, suggestions: List[Dict[str, Any]], 
                                context: AnalysisContext, 
                                scenario: Dict[str, Any],
                                image_path: str) -> Dict[str, Any]:
        """Enhanced quality scoring with multiple criteria"""
        
        if not suggestions:
            return {
                "overall_score": 0.0,
                "detailed_scores": {},
                "quality_grade": "poor",
                "issues": ["No suggestions generated"]
            }
        
        all_scores = []
        detailed_metrics = {
            "relevance": [],
            "creativity": [],
            "appropriateness": [],
            "engagement": [],
            "specificity": [],
            "gender_appropriateness": [],
            "context_awareness": []
        }
        
        expected_themes = scenario.get("expected_themes", [])
        
        for suggestion in suggestions:
            suggestion_text = suggestion.get("text", "").lower()
            
            # Basic scoring from dataset_builder
            basic_scores = self.dataset_builder.quality_score_suggestion(
                suggestion.get("text", ""), 
                {"expected_themes": expected_themes}
            )
            
            # Enhanced scoring criteria
            enhanced_scores = self.calculate_enhanced_scores(
                suggestion, context, scenario, image_path
            )
            
            # Combine scores
            combined_scores = {**basic_scores, **enhanced_scores}
            
            # Calculate weighted overall score
            weights = {
                "relevance": 0.25,
                "creativity": 0.15,
                "appropriateness": 0.20,
                "engagement": 0.15,
                "specificity": 0.10,
                "gender_appropriateness": 0.10,
                "context_awareness": 0.05
            }
            
            suggestion_score = sum(
                combined_scores.get(metric, 0) * weight 
                for metric, weight in weights.items()
            )
            
            all_scores.append(suggestion_score)
            
            # Track detailed metrics
            for metric in detailed_metrics:
                detailed_metrics[metric].append(combined_scores.get(metric, 0))
        
        # Calculate aggregate scores
        overall_score = statistics.mean(all_scores) if all_scores else 0.0
        
        # Calculate detailed metric averages
        avg_detailed_scores = {
            metric: statistics.mean(scores) if scores else 0.0
            for metric, scores in detailed_metrics.items()
        }
        
        # Determine quality grade
        quality_grade = self.determine_quality_grade(overall_score)
        
        # Identify issues
        issues = self.identify_issues(suggestions, avg_detailed_scores, context)
        
        return {
            "overall_score": round(overall_score, 3),
            "detailed_scores": {k: round(v, 3) for k, v in avg_detailed_scores.items()},
            "individual_scores": [round(score, 3) for score in all_scores],
            "quality_grade": quality_grade,
            "issues": issues,
            "suggestion_count": len(suggestions),
            "best_suggestion_score": round(max(all_scores), 3) if all_scores else 0.0,
            "score_variance": round(statistics.variance(all_scores), 3) if len(all_scores) > 1 else 0.0
        }
    
    def calculate_enhanced_scores(self, suggestion: Dict[str, Any], 
                                 context: AnalysisContext, 
                                 scenario: Dict[str, Any],
                                 image_path: str) -> Dict[str, float]:
        """Calculate enhanced scoring criteria"""
        suggestion_text = suggestion.get("text", "").lower()
        
        scores = {}
        
        # Gender appropriateness scoring
        gender_score = self.score_gender_appropriateness(suggestion_text, context)
        scores["gender_appropriateness"] = gender_score
        
        # Context awareness scoring
        context_score = self.score_context_awareness(suggestion_text, context, scenario)
        scores["context_awareness"] = context_score
        
        return scores
    
    def score_gender_appropriateness(self, suggestion_text: str, context: AnalysisContext) -> float:
        """Score gender appropriateness based on research findings"""
        
        # Research-based gender strategies
        if context.user_gender == "male":
            # Males should focus on conversation, compliments, humor
            positive_indicators = ["question", "?", "what", "how", "tell me", "love", "amazing", "interesting"]
            negative_indicators = ["hey", "hi", "sup", "sexy", "hot"]
        else:  # female
            # Females should be direct, acknowledge humor, show interest
            positive_indicators = ["funny", "laugh", "haha", "love", "interesting", "tell me", "?"]
            negative_indicators = ["hey", "hi", "cute", "handsome"]
        
        positive_count = sum(1 for indicator in positive_indicators if indicator in suggestion_text)
        negative_count = sum(1 for indicator in negative_indicators if indicator in suggestion_text)
        
        # Calculate score
        score = min(positive_count * 0.3, 1.0) - (negative_count * 0.2)
        return max(0.0, min(1.0, score))
    
    def score_context_awareness(self, suggestion_text: str, 
                               context: AnalysisContext, 
                               scenario: Dict[str, Any]) -> float:
        """Score context awareness"""
        
        score = 0.5  # Base score
        
        # App-specific appropriateness
        if context.app_type.lower() in suggestion_text:
            score += 0.1
        
        # Age-appropriate language
        age_range = scenario.get("age_range", "25-30")
        if "20-25" in age_range:
            # Younger audience - more casual language acceptable
            if any(word in suggestion_text for word in ["cool", "awesome", "vibe"]):
                score += 0.1
        elif "35+" in age_range:
            # Older audience - more mature language
            if any(word in suggestion_text for word in ["interesting", "fascinating", "appreciate"]):
                score += 0.1
        
        return min(1.0, score)
    
    def determine_quality_grade(self, score: float) -> str:
        """Determine quality grade from score"""
        if score >= self.quality_thresholds["excellent"]:
            return "excellent"
        elif score >= self.quality_thresholds["good"]:
            return "good"
        elif score >= self.quality_thresholds["acceptable"]:
            return "acceptable"
        else:
            return "poor"
    
    def identify_issues(self, suggestions: List[Dict[str, Any]], 
                       detailed_scores: Dict[str, float],
                       context: AnalysisContext) -> List[str]:
        """Identify specific issues with suggestions"""
        issues = []
        
        # Check for common problems
        if detailed_scores.get("relevance", 0) < 0.5:
            issues.append("Low relevance to profile content")
        
        if detailed_scores.get("creativity", 0) < 0.5:
            issues.append("Generic or unoriginal suggestions")
        
        if detailed_scores.get("appropriateness", 0) < 0.8:
            issues.append("Potentially inappropriate content")
        
        if detailed_scores.get("engagement", 0) < 0.5:
            issues.append("Low engagement potential")
        
        if detailed_scores.get("gender_appropriateness", 0) < 0.6:
            issues.append(f"Not optimized for {context.user_gender} communication style")
        
        # Check suggestion diversity
        suggestion_texts = [s.get("text", "") for s in suggestions]
        if len(set(suggestion_texts)) < len(suggestion_texts):
            issues.append("Duplicate or very similar suggestions")
        
        # Check length appropriateness
        avg_length = sum(len(s.get("text", "")) for s in suggestions) / len(suggestions)
        if avg_length < 20:
            issues.append("Suggestions too short")
        elif avg_length > 200:
            issues.append("Suggestions too long")
        
        return issues
    
    def run_single_test(self, image_path: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test with an image and scenario"""
        
        print(f"  Testing: {Path(image_path).name} with {scenario['name']}")
        
        # Create context
        context = self.create_test_context(scenario, image_path)
        
        # Encode image
        image_data = self.encode_image(image_path)
        if not image_data:
            return {
                "error": "Failed to encode image",
                "image_path": image_path,
                "scenario": scenario["name"]
            }
        
        # Run AI analysis
        start_time = time.time()
        try:
            result = self.ai_service.hybrid_analysis(context, image_data)
            processing_time = time.time() - start_time
        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "image_path": image_path,
                "scenario": scenario["name"],
                "processing_time": time.time() - start_time
            }
        
        # Extract suggestions
        suggestions = result.get("final_suggestions", [])
        
        # Score quality
        quality_scores = self.enhanced_quality_scoring(
            suggestions, context, scenario, image_path
        )
        
        # Compile test result
        test_result = {
            "image_path": image_path,
            "scenario": scenario["name"],
            "context": {
                "user_gender": context.user_gender,
                "target_gender": context.target_gender,
                "age_range": context.age_range,
                "app_type": context.app_type
            },
            "ai_result": result,
            "suggestions": suggestions,
            "quality_scores": quality_scores,
            "processing_time": round(processing_time, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        return test_result
    
    def run_comprehensive_test_suite(self, max_tests_per_scenario: int = 5) -> Dict[str, Any]:
        """Run comprehensive test suite across all scenarios and images"""
        
        print("🧪 Running Comprehensive Test Suite")
        print("=" * 60)
        
        test_images = self.get_test_images()
        if not test_images:
            return {"error": "No test images found"}
        
        print(f"📊 Found {len(test_images)} test images")
        print(f"🎯 Testing {len(self.test_scenarios)} scenarios")
        
        all_results = []
        scenario_results = {}
        
        for scenario in self.test_scenarios:
            print(f"\n🔬 Testing Scenario: {scenario['name']}")
            
            # Select random images for this scenario
            scenario_images = random.sample(
                test_images, 
                min(max_tests_per_scenario, len(test_images))
            )
            
            scenario_test_results = []
            
            for image_path in scenario_images:
                result = self.run_single_test(image_path, scenario)
                scenario_test_results.append(result)
                all_results.append(result)
                
                # Print quick result
                if "error" not in result:
                    score = result["quality_scores"]["overall_score"]
                    grade = result["quality_scores"]["quality_grade"]
                    print(f"    ✓ Score: {score} ({grade})")
                else:
                    print(f"    ✗ Error: {result['error']}")
            
            scenario_results[scenario['name']] = scenario_test_results
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report(all_results, scenario_results)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"test_suite_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                "test_suite_results": all_results,
                "scenario_results": scenario_results,
                "comprehensive_report": report,
                "test_configuration": {
                    "max_tests_per_scenario": max_tests_per_scenario,
                    "total_images": len(test_images),
                    "total_scenarios": len(self.test_scenarios),
                    "total_tests": len(all_results)
                }
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        return report
    
    def generate_comprehensive_report(self, all_results: List[Dict[str, Any]], 
                                    scenario_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        # Filter successful results
        successful_results = [r for r in all_results if "error" not in r]
        
        if not successful_results:
            return {"error": "No successful tests to analyze"}
        
        # Overall statistics
        all_scores = [r["quality_scores"]["overall_score"] for r in successful_results]
        
        overall_stats = {
            "total_tests": len(all_results),
            "successful_tests": len(successful_results),
            "success_rate": round(len(successful_results) / len(all_results), 3),
            "average_score": round(statistics.mean(all_scores), 3),
            "median_score": round(statistics.median(all_scores), 3),
            "score_std_dev": round(statistics.stdev(all_scores), 3) if len(all_scores) > 1 else 0.0,
            "min_score": round(min(all_scores), 3),
            "max_score": round(max(all_scores), 3)
        }
        
        # Score distribution
        score_distribution = {
            "excellent (0.8+)": sum(1 for s in all_scores if s >= 0.8),
            "good (0.6-0.8)": sum(1 for s in all_scores if 0.6 <= s < 0.8),
            "acceptable (0.4-0.6)": sum(1 for s in all_scores if 0.4 <= s < 0.6),
            "poor (<0.4)": sum(1 for s in all_scores if s < 0.4)
        }
        
        # Detailed metrics analysis
        metrics = ["relevance", "creativity", "appropriateness", "engagement", "specificity", 
                  "gender_appropriateness", "context_awareness"]
        
        metric_analysis = {}
        for metric in metrics:
            metric_scores = [r["quality_scores"]["detailed_scores"].get(metric, 0) for r in successful_results]
            metric_analysis[metric] = {
                "average": round(statistics.mean(metric_scores), 3),
                "min": round(min(metric_scores), 3),
                "max": round(max(metric_scores), 3),
                "std_dev": round(statistics.stdev(metric_scores), 3) if len(metric_scores) > 1 else 0.0
            }
        
        # Scenario performance
        scenario_performance = {}
        for scenario_name, results in scenario_results.items():
            successful_scenario_results = [r for r in results if "error" not in r]
            if successful_scenario_results:
                scenario_scores = [r["quality_scores"]["overall_score"] for r in successful_scenario_results]
                scenario_performance[scenario_name] = {
                    "average_score": round(statistics.mean(scenario_scores), 3),
                    "test_count": len(successful_scenario_results),
                    "success_rate": round(len(successful_scenario_results) / len(results), 3),
                    "best_score": round(max(scenario_scores), 3),
                    "worst_score": round(min(scenario_scores), 3)
                }
        
        # Performance analysis
        avg_processing_time = statistics.mean([r.get("processing_time", 0) for r in successful_results])
        
        performance_analysis = {
            "average_processing_time": round(avg_processing_time, 2),
            "total_processing_time": round(sum(r.get("processing_time", 0) for r in successful_results), 2),
            "fastest_test": round(min(r.get("processing_time", 0) for r in successful_results), 2),
            "slowest_test": round(max(r.get("processing_time", 0) for r in successful_results), 2)
        }
        
        # Issue analysis
        all_issues = []
        for result in successful_results:
            all_issues.extend(result["quality_scores"].get("issues", []))
        
        issue_frequency = {}
        for issue in all_issues:
            issue_frequency[issue] = issue_frequency.get(issue, 0) + 1
        
        # Generate recommendations
        recommendations = self.generate_improvement_recommendations(
            overall_stats, metric_analysis, scenario_performance, issue_frequency
        )
        
        return {
            "overall_statistics": overall_stats,
            "score_distribution": score_distribution,
            "metric_analysis": metric_analysis,
            "scenario_performance": scenario_performance,
            "performance_analysis": performance_analysis,
            "common_issues": dict(sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True)),
            "recommendations": recommendations,
            "test_timestamp": datetime.now().isoformat()
        }
    
    def generate_improvement_recommendations(self, overall_stats: Dict[str, Any],
                                           metric_analysis: Dict[str, Any],
                                           scenario_performance: Dict[str, Any],
                                           issue_frequency: Dict[str, int]) -> List[str]:
        """Generate specific improvement recommendations"""
        recommendations = []
        
        # Overall performance recommendations
        avg_score = overall_stats["average_score"]
        if avg_score < 0.6:
            recommendations.append("🚨 CRITICAL: Overall performance below acceptable threshold. Major prompt engineering overhaul needed.")
        elif avg_score < 0.7:
            recommendations.append("⚠️ Overall performance needs improvement. Focus on prompt optimization and model tuning.")
        
        # Metric-specific recommendations
        for metric, analysis in metric_analysis.items():
            if analysis["average"] < 0.6:
                if metric == "relevance":
                    recommendations.append("🎯 Improve visual analysis to better identify profile elements for relevant suggestions.")
                elif metric == "creativity":
                    recommendations.append("💡 Enhance creativity by avoiding generic phrases and generating more original content.")
                elif metric == "appropriateness":
                    recommendations.append("🛡️ Strengthen content filters to ensure all suggestions are appropriate for dating context.")
                elif metric == "engagement":
                    recommendations.append("💬 Include more questions and conversation starters to improve engagement potential.")
                elif metric == "gender_appropriateness":
                    recommendations.append("👥 Better implement gender-specific communication strategies from research.")
        
        # Issue-based recommendations
        top_issues = list(issue_frequency.keys())[:3]
        for issue in top_issues:
            if "relevance" in issue.lower():
                recommendations.append("🔍 Implement better visual element detection and analysis.")
            elif "generic" in issue.lower():
                recommendations.append("🎨 Add more diverse suggestion templates and avoid repetitive patterns.")
            elif "inappropriate" in issue.lower():
                recommendations.append("🔒 Strengthen content moderation and appropriateness checking.")
        
        # Scenario-specific recommendations
        worst_scenarios = sorted(scenario_performance.items(), key=lambda x: x[1]["average_score"])[:2]
        for scenario_name, performance in worst_scenarios:
            if performance["average_score"] < 0.6:
                recommendations.append(f"📊 Focus improvement efforts on '{scenario_name}' scenario - consistently underperforming.")
        
        # Performance recommendations
        if overall_stats.get("success_rate", 1.0) < 0.9:
            recommendations.append("🔧 Improve error handling and fallback mechanisms to increase success rate.")
        
        if not recommendations:
            recommendations.append("✅ Performance is good! Continue fine-tuning for optimal results.")
        
        return recommendations
    
    def run_iterative_improvement_cycle(self, iterations: int = 3, tests_per_iteration: int = 10) -> Dict[str, Any]:
        """Run iterative improvement cycle with multiple test rounds"""
        
        print("🔄 Starting Iterative Improvement Cycle")
        print("=" * 60)
        
        iteration_results = []
        
        for iteration in range(1, iterations + 1):
            print(f"\n🔄 Iteration {iteration}/{iterations}")
            
            # Run test suite
            report = self.run_comprehensive_test_suite(max_tests_per_scenario=tests_per_iteration)
            
            if "error" in report:
                print(f"❌ Iteration {iteration} failed: {report['error']}")
                continue
            
            # Track iteration
            iteration_data = {
                "iteration": iteration,
                "report": report,
                "timestamp": datetime.now().isoformat()
            }
            
            iteration_results.append(iteration_data)
            self.iteration_history.append(iteration_data)
            
            # Print iteration summary
            overall_stats = report["overall_statistics"]
            print(f"📊 Iteration {iteration} Results:")
            print(f"   Average Score: {overall_stats['average_score']}")
            print(f"   Success Rate: {overall_stats['success_rate']}")
            print(f"   Score Distribution: {report['score_distribution']}")
            
            # Show top recommendations
            recommendations = report["recommendations"][:3]
            print(f"🎯 Top Recommendations:")
            for rec in recommendations:
                print(f"   {rec}")
            
            # Check for improvement
            if iteration > 1:
                prev_score = iteration_results[-2]["report"]["overall_statistics"]["average_score"]
                current_score = overall_stats["average_score"]
                improvement = current_score - prev_score
                
                if improvement > 0:
                    print(f"📈 Improvement: +{improvement:.3f}")
                else:
                    print(f"📉 Decline: {improvement:.3f}")
        
        # Generate final improvement report
        final_report = self.generate_improvement_cycle_report(iteration_results)
        
        # Save iteration results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cycle_file = self.results_dir / f"improvement_cycle_{timestamp}.json"
        
        with open(cycle_file, 'w') as f:
            json.dump({
                "iteration_results": iteration_results,
                "improvement_cycle_report": final_report,
                "cycle_configuration": {
                    "iterations": iterations,
                    "tests_per_iteration": tests_per_iteration
                }
            }, f, indent=2)
        
        print(f"\n💾 Improvement cycle results saved to: {cycle_file}")
        
        return final_report
    
    def generate_improvement_cycle_report(self, iteration_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate report on improvement cycle"""
        
        if not iteration_results:
            return {"error": "No iteration results to analyze"}
        
        # Extract scores over time
        scores_over_time = []
        success_rates_over_time = []
        
        for iteration_data in iteration_results:
            stats = iteration_data["report"]["overall_statistics"]
            scores_over_time.append(stats["average_score"])
            success_rates_over_time.append(stats["success_rate"])
        
        # Calculate improvement metrics
        initial_score = scores_over_time[0]
        final_score = scores_over_time[-1]
        total_improvement = final_score - initial_score
        
        # Trend analysis
        if len(scores_over_time) > 1:
            improvements = [scores_over_time[i] - scores_over_time[i-1] for i in range(1, len(scores_over_time))]
            avg_improvement_per_iteration = statistics.mean(improvements)
            consistent_improvement = all(imp >= 0 for imp in improvements)
        else:
            avg_improvement_per_iteration = 0
            consistent_improvement = True
        
        return {
            "cycle_summary": {
                "total_iterations": len(iteration_results),
                "initial_score": round(initial_score, 3),
                "final_score": round(final_score, 3),
                "total_improvement": round(total_improvement, 3),
                "improvement_percentage": round((total_improvement / initial_score) * 100, 1) if initial_score > 0 else 0,
                "avg_improvement_per_iteration": round(avg_improvement_per_iteration, 3),
                "consistent_improvement": consistent_improvement
            },
            "performance_trend": {
                "scores_over_time": [round(s, 3) for s in scores_over_time],
                "success_rates_over_time": [round(s, 3) for s in success_rates_over_time],
                "best_iteration": scores_over_time.index(max(scores_over_time)) + 1,
                "worst_iteration": scores_over_time.index(min(scores_over_time)) + 1
            },
            "final_assessment": self.generate_final_assessment(total_improvement, final_score, consistent_improvement),
            "next_steps": self.generate_next_steps(iteration_results[-1]["report"])
        }
    
    def generate_final_assessment(self, total_improvement: float, final_score: float, consistent_improvement: bool) -> str:
        """Generate final assessment of improvement cycle"""
        
        if final_score >= 0.8:
            if total_improvement > 0.1:
                return "🎉 EXCELLENT: Significant improvement achieved with high final performance. System ready for production."
            else:
                return "✅ GOOD: High performance maintained. System ready for production with minor optimizations."
        elif final_score >= 0.6:
            if total_improvement > 0.05:
                return "📈 IMPROVING: Good progress made. Continue optimization to reach production readiness."
            else:
                return "⚠️ STABLE: Acceptable performance but limited improvement. Consider new optimization strategies."
        else:
            if total_improvement > 0:
                return "🔧 DEVELOPING: Some improvement shown but performance still below target. Major optimization needed."
            else:
                return "🚨 CONCERNING: No improvement or declining performance. Fundamental approach review required."
    
    def generate_next_steps(self, final_report: Dict[str, Any]) -> List[str]:
        """Generate next steps based on final iteration results"""
        
        next_steps = []
        
        final_score = final_report["overall_statistics"]["average_score"]
        
        if final_score >= 0.8:
            next_steps.extend([
                "🚀 Proceed to production load testing",
                "📊 Implement real-time monitoring and quality tracking",
                "🎯 Fine-tune for specific edge cases and scenarios"
            ])
        elif final_score >= 0.6:
            next_steps.extend([
                "🔧 Focus on top-performing scenarios and replicate success patterns",
                "📈 Implement targeted improvements for underperforming metrics",
                "🧪 Run additional focused testing on problem areas"
            ])
        else:
            next_steps.extend([
                "🔄 Major prompt engineering overhaul required",
                "🧠 Consider alternative model configurations or approaches",
                "📚 Review and implement additional research findings"
            ])
        
        # Add specific recommendations from final report
        recommendations = final_report.get("recommendations", [])[:2]
        next_steps.extend(recommendations)
        
        return next_steps

def main():
    """Main function to run iterative testing system"""
    print("🧪 Flirrt.ai Iterative Testing and Quality Scoring System")
    print("=" * 70)
    
    testing_system = IterativeTestingSystem()
    
    # Run comprehensive test suite
    print("🔬 Running initial comprehensive test suite...")
    initial_report = testing_system.run_comprehensive_test_suite(max_tests_per_scenario=3)
    
    if "error" in initial_report:
        print(f"❌ Initial testing failed: {initial_report['error']}")
        return
    
    print("\n📊 Initial Test Results:")
    overall_stats = initial_report["overall_statistics"]
    print(f"   Average Score: {overall_stats['average_score']}")
    print(f"   Success Rate: {overall_stats['success_rate']}")
    print(f"   Total Tests: {overall_stats['total_tests']}")
    
    # Show score distribution
    print(f"\n📈 Score Distribution:")
    for grade, count in initial_report["score_distribution"].items():
        print(f"   {grade}: {count}")
    
    # Show top issues
    common_issues = initial_report.get("common_issues", {})
    if common_issues:
        print(f"\n⚠️ Most Common Issues:")
        for issue, count in list(common_issues.items())[:3]:
            print(f"   {issue}: {count} occurrences")
    
    # Show recommendations
    recommendations = initial_report.get("recommendations", [])
    if recommendations:
        print(f"\n🎯 Top Recommendations:")
        for rec in recommendations[:3]:
            print(f"   {rec}")
    
    print(f"\n✅ Iterative testing system ready for optimization cycles!")
    print(f"📁 Results saved in: {testing_system.results_dir}")

if __name__ == "__main__":
    main()

