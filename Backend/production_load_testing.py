#!/usr/bin/env python3
"""
Production-Level Load Testing and Performance Optimization for Flirrt.ai
Implements comprehensive load testing, performance monitoring, and optimization
"""

import os
import json
import time
import asyncio
import threading
import statistics
from typing import Dict, List, Any, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import sys

# Add Backend to path for imports
sys.path.append(str(Path(__file__).parent))

from advanced_ai_service import AdvancedFlirrtAI, AnalysisContext

@dataclass
class LoadTestConfig:
    concurrent_users: int
    requests_per_user: int
    test_duration_seconds: int
    ramp_up_seconds: int
    target_response_time: float
    target_success_rate: float

@dataclass
class PerformanceMetrics:
    response_times: List[float]
    success_count: int
    error_count: int
    start_time: float
    end_time: float
    concurrent_users: int

class ProductionLoadTester:
    def __init__(self, results_dir: str = "load_test_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize AI service
        self.ai_service = AdvancedFlirrtAI()
        
        # Load test configurations
        self.test_configs = {
            "light_load": LoadTestConfig(
                concurrent_users=5,
                requests_per_user=10,
                test_duration_seconds=60,
                ramp_up_seconds=10,
                target_response_time=5.0,
                target_success_rate=0.95
            ),
            "moderate_load": LoadTestConfig(
                concurrent_users=20,
                requests_per_user=15,
                test_duration_seconds=120,
                ramp_up_seconds=20,
                target_response_time=8.0,
                target_success_rate=0.90
            ),
            "heavy_load": LoadTestConfig(
                concurrent_users=50,
                requests_per_user=20,
                test_duration_seconds=300,
                ramp_up_seconds=30,
                target_response_time=12.0,
                target_success_rate=0.85
            ),
            "stress_test": LoadTestConfig(
                concurrent_users=100,
                requests_per_user=25,
                test_duration_seconds=600,
                ramp_up_seconds=60,
                target_response_time=20.0,
                target_success_rate=0.80
            )
        }
        
        # Performance tracking
        self.performance_history = []
        self.optimization_results = {}
        
        # Test data
        self.test_image_data = self.load_test_image()
        self.test_contexts = self.create_test_contexts()
    
    def load_test_image(self) -> str:
        """Load a test image for load testing"""
        # Create a minimal test image in base64
        import base64
        
        # 1x1 pixel PNG in base64
        test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        return test_image
    
    def create_test_contexts(self) -> List[AnalysisContext]:
        """Create diverse test contexts for load testing"""
        contexts = []
        
        # Generate diverse contexts
        genders = ["male", "female"]
        age_ranges = ["20-25", "25-30", "30-35", "35+"]
        apps = ["Tinder", "Bumble", "Hinge", "Instagram"]
        
        for user_gender in genders:
            for target_gender in genders:
                for age_range in age_ranges:
                    for app in apps:
                        context = AnalysisContext(
                            user_gender=user_gender,
                            target_gender=target_gender,
                            age_range=age_range,
                            app_type=app
                        )
                        contexts.append(context)
        
        return contexts
    
    def single_request_test(self, context: AnalysisContext, request_id: int) -> Dict[str, Any]:
        """Perform a single AI analysis request"""
        start_time = time.time()
        
        try:
            result = self.ai_service.hybrid_analysis(context, self.test_image_data)
            end_time = time.time()
            
            response_time = end_time - start_time
            success = result.get("final_suggestions") is not None and len(result.get("final_suggestions", [])) > 0
            
            return {
                "request_id": request_id,
                "response_time": response_time,
                "success": success,
                "error": None,
                "suggestions_count": len(result.get("final_suggestions", [])),
                "models_used": result.get("models_used", []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            end_time = time.time()
            return {
                "request_id": request_id,
                "response_time": end_time - start_time,
                "success": False,
                "error": str(e),
                "suggestions_count": 0,
                "models_used": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def user_simulation(self, user_id: int, config: LoadTestConfig, 
                       start_delay: float) -> List[Dict[str, Any]]:
        """Simulate a single user's requests"""
        
        # Wait for ramp-up delay
        time.sleep(start_delay)
        
        user_results = []
        
        for request_num in range(config.requests_per_user):
            # Select random context
            import random
            context = random.choice(self.test_contexts)
            
            # Perform request
            request_id = f"user_{user_id}_req_{request_num}"
            result = self.single_request_test(context, request_id)
            result["user_id"] = user_id
            user_results.append(result)
            
            # Small delay between requests from same user
            time.sleep(0.1)
        
        return user_results
    
    def run_load_test(self, test_name: str, config: LoadTestConfig) -> Dict[str, Any]:
        """Run a complete load test"""
        
        print(f"🚀 Starting Load Test: {test_name}")
        print(f"   Concurrent Users: {config.concurrent_users}")
        print(f"   Requests per User: {config.requests_per_user}")
        print(f"   Total Requests: {config.concurrent_users * config.requests_per_user}")
        print(f"   Test Duration: {config.test_duration_seconds}s")
        print(f"   Ramp-up Time: {config.ramp_up_seconds}s")
        
        start_time = time.time()
        all_results = []
        
        # Calculate ramp-up delays
        ramp_up_delay = config.ramp_up_seconds / config.concurrent_users
        
        # Use ThreadPoolExecutor for concurrent users
        with ThreadPoolExecutor(max_workers=config.concurrent_users) as executor:
            # Submit user simulations
            futures = []
            for user_id in range(config.concurrent_users):
                start_delay = user_id * ramp_up_delay
                future = executor.submit(
                    self.user_simulation, 
                    user_id, 
                    config, 
                    start_delay
                )
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    user_results = future.result()
                    all_results.extend(user_results)
                    print(f"   ✓ User completed: {len(user_results)} requests")
                except Exception as e:
                    print(f"   ✗ User failed: {e}")
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Analyze results
        analysis = self.analyze_load_test_results(all_results, config, total_duration)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.results_dir / f"load_test_{test_name}_{timestamp}.json"
        
        test_report = {
            "test_name": test_name,
            "config": {
                "concurrent_users": config.concurrent_users,
                "requests_per_user": config.requests_per_user,
                "test_duration_seconds": config.test_duration_seconds,
                "ramp_up_seconds": config.ramp_up_seconds,
                "target_response_time": config.target_response_time,
                "target_success_rate": config.target_success_rate
            },
            "results": all_results,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(results_file, 'w') as f:
            json.dump(test_report, f, indent=2)
        
        print(f"💾 Load test results saved to: {results_file}")
        
        return analysis
    
    def analyze_load_test_results(self, results: List[Dict[str, Any]], 
                                 config: LoadTestConfig, 
                                 total_duration: float) -> Dict[str, Any]:
        """Analyze load test results"""
        
        if not results:
            return {"error": "No results to analyze"}
        
        # Basic statistics
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        response_times = [r["response_time"] for r in successful_results]
        
        # Performance metrics
        total_requests = len(results)
        success_rate = len(successful_results) / total_requests if total_requests > 0 else 0
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)] if len(response_times) > 1 else response_times[0]
            p99_response_time = sorted(response_times)[int(len(response_times) * 0.99)] if len(response_times) > 1 else response_times[0]
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = median_response_time = p95_response_time = p99_response_time = 0
            min_response_time = max_response_time = 0
        
        # Throughput
        requests_per_second = total_requests / total_duration if total_duration > 0 else 0
        successful_requests_per_second = len(successful_results) / total_duration if total_duration > 0 else 0
        
        # Target compliance
        response_time_compliance = avg_response_time <= config.target_response_time
        success_rate_compliance = success_rate >= config.target_success_rate
        
        # Error analysis
        error_types = {}
        for result in failed_results:
            error = result.get("error", "Unknown error")
            error_types[error] = error_types.get(error, 0) + 1
        
        # Model usage analysis
        all_models_used = []
        for result in successful_results:
            all_models_used.extend(result.get("models_used", []))
        
        model_usage = {}
        for model in all_models_used:
            model_usage[model] = model_usage.get(model, 0) + 1
        
        # Performance grade
        performance_grade = self.calculate_performance_grade(
            success_rate, avg_response_time, config
        )
        
        return {
            "performance_summary": {
                "total_requests": total_requests,
                "successful_requests": len(successful_results),
                "failed_requests": len(failed_results),
                "success_rate": round(success_rate, 3),
                "total_duration": round(total_duration, 2),
                "performance_grade": performance_grade
            },
            "response_time_metrics": {
                "average": round(avg_response_time, 3),
                "median": round(median_response_time, 3),
                "p95": round(p95_response_time, 3),
                "p99": round(p99_response_time, 3),
                "min": round(min_response_time, 3),
                "max": round(max_response_time, 3)
            },
            "throughput_metrics": {
                "requests_per_second": round(requests_per_second, 2),
                "successful_requests_per_second": round(successful_requests_per_second, 2)
            },
            "target_compliance": {
                "response_time_target": config.target_response_time,
                "response_time_actual": round(avg_response_time, 3),
                "response_time_compliance": response_time_compliance,
                "success_rate_target": config.target_success_rate,
                "success_rate_actual": round(success_rate, 3),
                "success_rate_compliance": success_rate_compliance,
                "overall_compliance": response_time_compliance and success_rate_compliance
            },
            "error_analysis": {
                "error_types": error_types,
                "most_common_error": max(error_types.items(), key=lambda x: x[1])[0] if error_types else None
            },
            "model_usage_analysis": {
                "model_usage_count": model_usage,
                "most_used_model": max(model_usage.items(), key=lambda x: x[1])[0] if model_usage else None
            },
            "recommendations": self.generate_performance_recommendations(
                success_rate, avg_response_time, config, error_types
            )
        }
    
    def calculate_performance_grade(self, success_rate: float, 
                                   avg_response_time: float, 
                                   config: LoadTestConfig) -> str:
        """Calculate overall performance grade"""
        
        # Success rate scoring (0-50 points)
        if success_rate >= 0.95:
            success_score = 50
        elif success_rate >= 0.90:
            success_score = 40
        elif success_rate >= 0.80:
            success_score = 30
        elif success_rate >= 0.70:
            success_score = 20
        else:
            success_score = 10
        
        # Response time scoring (0-50 points)
        if avg_response_time <= config.target_response_time * 0.5:
            response_score = 50
        elif avg_response_time <= config.target_response_time * 0.75:
            response_score = 40
        elif avg_response_time <= config.target_response_time:
            response_score = 30
        elif avg_response_time <= config.target_response_time * 1.5:
            response_score = 20
        else:
            response_score = 10
        
        total_score = success_score + response_score
        
        if total_score >= 90:
            return "A+ (Excellent)"
        elif total_score >= 80:
            return "A (Very Good)"
        elif total_score >= 70:
            return "B (Good)"
        elif total_score >= 60:
            return "C (Acceptable)"
        elif total_score >= 50:
            return "D (Poor)"
        else:
            return "F (Failing)"
    
    def generate_performance_recommendations(self, success_rate: float, 
                                           avg_response_time: float,
                                           config: LoadTestConfig,
                                           error_types: Dict[str, int]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Success rate recommendations
        if success_rate < 0.8:
            recommendations.append("🚨 CRITICAL: Success rate below 80%. Investigate error handling and API reliability.")
        elif success_rate < 0.9:
            recommendations.append("⚠️ Success rate below 90%. Improve error handling and fallback mechanisms.")
        
        # Response time recommendations
        if avg_response_time > config.target_response_time * 2:
            recommendations.append("🐌 CRITICAL: Response time significantly exceeds target. Consider caching, model optimization, or infrastructure scaling.")
        elif avg_response_time > config.target_response_time:
            recommendations.append("⏱️ Response time exceeds target. Optimize prompts, implement caching, or consider faster models.")
        
        # Error-specific recommendations
        if error_types:
            most_common_error = max(error_types.items(), key=lambda x: x[1])[0]
            if "timeout" in most_common_error.lower():
                recommendations.append("⏰ Implement timeout handling and retry mechanisms.")
            elif "rate limit" in most_common_error.lower():
                recommendations.append("🚦 Implement rate limiting and request queuing.")
            elif "api" in most_common_error.lower():
                recommendations.append("🔌 Improve API error handling and fallback strategies.")
        
        # Load-specific recommendations
        if config.concurrent_users >= 50:
            recommendations.append("🏗️ Consider implementing connection pooling and async processing for high-load scenarios.")
        
        if not recommendations:
            recommendations.append("✅ Performance is excellent! Continue monitoring and maintain current optimization level.")
        
        return recommendations
    
    def run_comprehensive_load_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive load test suite across all configurations"""
        
        print("🧪 Running Comprehensive Load Test Suite")
        print("=" * 60)
        
        suite_results = {}
        
        for test_name, config in self.test_configs.items():
            print(f"\n🔬 Running {test_name.upper()} test...")
            
            try:
                analysis = self.run_load_test(test_name, config)
                suite_results[test_name] = analysis
                
                # Print summary
                summary = analysis["performance_summary"]
                print(f"   ✓ Success Rate: {summary['success_rate']}")
                print(f"   ✓ Avg Response Time: {analysis['response_time_metrics']['average']}s")
                print(f"   ✓ Performance Grade: {summary['performance_grade']}")
                print(f"   ✓ Throughput: {analysis['throughput_metrics']['requests_per_second']} req/s")
                
            except Exception as e:
                print(f"   ✗ Test failed: {e}")
                suite_results[test_name] = {"error": str(e)}
        
        # Generate comprehensive report
        comprehensive_report = self.generate_comprehensive_load_report(suite_results)
        
        # Save comprehensive results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suite_file = self.results_dir / f"load_test_suite_{timestamp}.json"
        
        with open(suite_file, 'w') as f:
            json.dump({
                "suite_results": suite_results,
                "comprehensive_report": comprehensive_report,
                "test_timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n💾 Comprehensive load test results saved to: {suite_file}")
        
        return comprehensive_report
    
    def generate_comprehensive_load_report(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive load test report"""
        
        successful_tests = {k: v for k, v in suite_results.items() if "error" not in v}
        
        if not successful_tests:
            return {"error": "No successful load tests to analyze"}
        
        # Aggregate metrics
        all_success_rates = [test["performance_summary"]["success_rate"] for test in successful_tests.values()]
        all_response_times = [test["response_time_metrics"]["average"] for test in successful_tests.values()]
        all_throughputs = [test["throughput_metrics"]["requests_per_second"] for test in successful_tests.values()]
        
        # Performance trends
        performance_trend = {}
        for test_name, results in successful_tests.items():
            performance_trend[test_name] = {
                "success_rate": results["performance_summary"]["success_rate"],
                "avg_response_time": results["response_time_metrics"]["average"],
                "throughput": results["throughput_metrics"]["requests_per_second"],
                "grade": results["performance_summary"]["performance_grade"]
            }
        
        # Scalability analysis
        scalability_analysis = self.analyze_scalability(successful_tests)
        
        # Overall assessment
        overall_assessment = self.generate_overall_assessment(successful_tests)
        
        return {
            "suite_summary": {
                "total_tests": len(suite_results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(suite_results) - len(successful_tests),
                "overall_success_rate": round(statistics.mean(all_success_rates), 3),
                "overall_avg_response_time": round(statistics.mean(all_response_times), 3),
                "overall_throughput": round(statistics.mean(all_throughputs), 2)
            },
            "performance_trend": performance_trend,
            "scalability_analysis": scalability_analysis,
            "overall_assessment": overall_assessment,
            "production_readiness": self.assess_production_readiness(successful_tests),
            "optimization_priorities": self.identify_optimization_priorities(successful_tests)
        }
    
    def analyze_scalability(self, successful_tests: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scalability characteristics"""
        
        # Extract load levels and performance
        load_performance = []
        for test_name, results in successful_tests.items():
            config = self.test_configs[test_name]
            load_performance.append({
                "test_name": test_name,
                "concurrent_users": config.concurrent_users,
                "success_rate": results["performance_summary"]["success_rate"],
                "avg_response_time": results["response_time_metrics"]["average"],
                "throughput": results["throughput_metrics"]["requests_per_second"]
            })
        
        # Sort by load level
        load_performance.sort(key=lambda x: x["concurrent_users"])
        
        # Analyze trends
        if len(load_performance) > 1:
            # Response time degradation
            response_times = [lp["avg_response_time"] for lp in load_performance]
            response_time_increase = response_times[-1] / response_times[0] if response_times[0] > 0 else 1
            
            # Success rate degradation
            success_rates = [lp["success_rate"] for lp in load_performance]
            success_rate_decrease = success_rates[0] - success_rates[-1]
            
            # Throughput scaling
            throughputs = [lp["throughput"] for lp in load_performance]
            throughput_scaling = throughputs[-1] / throughputs[0] if throughputs[0] > 0 else 1
            
            scalability_grade = self.calculate_scalability_grade(
                response_time_increase, success_rate_decrease, throughput_scaling
            )
        else:
            response_time_increase = 1.0
            success_rate_decrease = 0.0
            throughput_scaling = 1.0
            scalability_grade = "Insufficient data"
        
        return {
            "load_performance_data": load_performance,
            "response_time_increase_factor": round(response_time_increase, 2),
            "success_rate_decrease": round(success_rate_decrease, 3),
            "throughput_scaling_factor": round(throughput_scaling, 2),
            "scalability_grade": scalability_grade,
            "scalability_recommendations": self.generate_scalability_recommendations(
                response_time_increase, success_rate_decrease, throughput_scaling
            )
        }
    
    def calculate_scalability_grade(self, response_time_increase: float, 
                                   success_rate_decrease: float, 
                                   throughput_scaling: float) -> str:
        """Calculate scalability grade"""
        
        score = 0
        
        # Response time scaling (0-40 points)
        if response_time_increase <= 1.5:
            score += 40
        elif response_time_increase <= 2.0:
            score += 30
        elif response_time_increase <= 3.0:
            score += 20
        else:
            score += 10
        
        # Success rate stability (0-30 points)
        if success_rate_decrease <= 0.05:
            score += 30
        elif success_rate_decrease <= 0.10:
            score += 20
        elif success_rate_decrease <= 0.20:
            score += 10
        else:
            score += 0
        
        # Throughput scaling (0-30 points)
        if throughput_scaling >= 0.8:
            score += 30
        elif throughput_scaling >= 0.6:
            score += 20
        elif throughput_scaling >= 0.4:
            score += 10
        else:
            score += 0
        
        if score >= 90:
            return "Excellent Scalability"
        elif score >= 75:
            return "Good Scalability"
        elif score >= 60:
            return "Acceptable Scalability"
        elif score >= 45:
            return "Poor Scalability"
        else:
            return "Critical Scalability Issues"
    
    def generate_scalability_recommendations(self, response_time_increase: float,
                                           success_rate_decrease: float,
                                           throughput_scaling: float) -> List[str]:
        """Generate scalability recommendations"""
        recommendations = []
        
        if response_time_increase > 3.0:
            recommendations.append("🚨 Response time degrades severely under load. Implement caching, optimize algorithms, or scale infrastructure.")
        elif response_time_increase > 2.0:
            recommendations.append("⚠️ Response time increases significantly under load. Consider performance optimizations.")
        
        if success_rate_decrease > 0.15:
            recommendations.append("🚨 Success rate drops significantly under load. Improve error handling and resource management.")
        elif success_rate_decrease > 0.05:
            recommendations.append("⚠️ Success rate decreases under load. Strengthen error handling mechanisms.")
        
        if throughput_scaling < 0.4:
            recommendations.append("🚨 Throughput scaling is poor. Consider horizontal scaling or async processing.")
        elif throughput_scaling < 0.6:
            recommendations.append("⚠️ Throughput scaling could be improved. Optimize resource utilization.")
        
        if not recommendations:
            recommendations.append("✅ Excellent scalability characteristics. System handles load well.")
        
        return recommendations
    
    def generate_overall_assessment(self, successful_tests: Dict[str, Any]) -> str:
        """Generate overall performance assessment"""
        
        # Calculate average grades
        grades = [test["performance_summary"]["performance_grade"] for test in successful_tests.values()]
        
        # Count grade distribution
        grade_counts = {}
        for grade in grades:
            grade_letter = grade.split()[0]  # Extract letter grade
            grade_counts[grade_letter] = grade_counts.get(grade_letter, 0) + 1
        
        # Determine overall assessment
        if grade_counts.get("A+", 0) + grade_counts.get("A", 0) >= len(grades) * 0.8:
            return "🎉 EXCELLENT: System demonstrates outstanding performance across all load levels. Ready for production deployment."
        elif grade_counts.get("A+", 0) + grade_counts.get("A", 0) + grade_counts.get("B", 0) >= len(grades) * 0.8:
            return "✅ GOOD: System shows solid performance with minor optimization opportunities. Suitable for production with monitoring."
        elif grade_counts.get("C", 0) + grade_counts.get("D", 0) >= len(grades) * 0.5:
            return "⚠️ ACCEPTABLE: System performance is adequate but requires optimization before production deployment."
        else:
            return "🚨 CRITICAL: System performance is below acceptable standards. Major optimization required before production."
    
    def assess_production_readiness(self, successful_tests: Dict[str, Any]) -> Dict[str, Any]:
        """Assess production readiness"""
        
        readiness_criteria = {
            "light_load_success": False,
            "moderate_load_success": False,
            "heavy_load_acceptable": False,
            "stress_test_survival": False,
            "overall_reliability": False
        }
        
        # Check each criterion
        for test_name, results in successful_tests.items():
            success_rate = results["performance_summary"]["success_rate"]
            compliance = results["target_compliance"]["overall_compliance"]
            
            if test_name == "light_load" and success_rate >= 0.95 and compliance:
                readiness_criteria["light_load_success"] = True
            elif test_name == "moderate_load" and success_rate >= 0.90 and compliance:
                readiness_criteria["moderate_load_success"] = True
            elif test_name == "heavy_load" and success_rate >= 0.80:
                readiness_criteria["heavy_load_acceptable"] = True
            elif test_name == "stress_test" and success_rate >= 0.70:
                readiness_criteria["stress_test_survival"] = True
        
        # Overall reliability check
        all_success_rates = [test["performance_summary"]["success_rate"] for test in successful_tests.values()]
        avg_success_rate = statistics.mean(all_success_rates)
        readiness_criteria["overall_reliability"] = avg_success_rate >= 0.85
        
        # Calculate readiness score
        readiness_score = sum(readiness_criteria.values()) / len(readiness_criteria)
        
        # Determine readiness level
        if readiness_score >= 0.8:
            readiness_level = "PRODUCTION READY"
        elif readiness_score >= 0.6:
            readiness_level = "NEARLY READY"
        elif readiness_score >= 0.4:
            readiness_level = "NEEDS OPTIMIZATION"
        else:
            readiness_level = "NOT READY"
        
        return {
            "readiness_criteria": readiness_criteria,
            "readiness_score": round(readiness_score, 2),
            "readiness_level": readiness_level,
            "production_recommendations": self.generate_production_recommendations(readiness_criteria, readiness_score)
        }
    
    def generate_production_recommendations(self, criteria: Dict[str, bool], score: float) -> List[str]:
        """Generate production deployment recommendations"""
        recommendations = []
        
        if score >= 0.8:
            recommendations.extend([
                "🚀 System is ready for production deployment",
                "📊 Implement comprehensive monitoring and alerting",
                "🔄 Set up automated scaling based on load patterns",
                "📈 Monitor performance metrics continuously"
            ])
        elif score >= 0.6:
            recommendations.extend([
                "🔧 Address remaining performance issues before full deployment",
                "🧪 Consider staged rollout with monitoring",
                "⚡ Optimize identified bottlenecks",
                "📊 Implement enhanced monitoring"
            ])
        else:
            recommendations.extend([
                "🚨 Major optimization required before production",
                "🔍 Conduct detailed performance profiling",
                "🏗️ Consider infrastructure improvements",
                "🧪 Repeat load testing after optimizations"
            ])
        
        # Specific recommendations based on failed criteria
        if not criteria["light_load_success"]:
            recommendations.append("🎯 Fix basic performance issues - system fails under light load")
        if not criteria["moderate_load_success"]:
            recommendations.append("⚡ Optimize for moderate load handling")
        if not criteria["heavy_load_acceptable"]:
            recommendations.append("🏗️ Improve heavy load performance and error handling")
        if not criteria["overall_reliability"]:
            recommendations.append("🛡️ Enhance overall system reliability and error recovery")
        
        return recommendations
    
    def identify_optimization_priorities(self, successful_tests: Dict[str, Any]) -> List[str]:
        """Identify optimization priorities"""
        priorities = []
        
        # Analyze common issues across tests
        all_recommendations = []
        for test in successful_tests.values():
            all_recommendations.extend(test.get("recommendations", []))
        
        # Count recommendation frequency
        recommendation_counts = {}
        for rec in all_recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        # Sort by frequency
        sorted_recommendations = sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Extract top priorities
        for rec, count in sorted_recommendations[:5]:
            if count > 1:  # Only include recommendations that appear multiple times
                priorities.append(f"{rec} (appears in {count} tests)")
        
        if not priorities:
            priorities.append("✅ No critical optimization priorities identified. System performing well.")
        
        return priorities

def main():
    """Main function to run production load testing"""
    print("🚀 Flirrt.ai Production Load Testing and Performance Optimization")
    print("=" * 80)
    
    load_tester = ProductionLoadTester()
    
    # Run comprehensive load test suite
    print("🧪 Running comprehensive load test suite...")
    comprehensive_report = load_tester.run_comprehensive_load_test_suite()
    
    if "error" in comprehensive_report:
        print(f"❌ Load testing failed: {comprehensive_report['error']}")
        return
    
    print("\n📊 COMPREHENSIVE LOAD TEST RESULTS")
    print("=" * 50)
    
    # Suite summary
    suite_summary = comprehensive_report["suite_summary"]
    print(f"📈 Overall Performance:")
    print(f"   Success Rate: {suite_summary['overall_success_rate']}")
    print(f"   Avg Response Time: {suite_summary['overall_avg_response_time']}s")
    print(f"   Throughput: {suite_summary['overall_throughput']} req/s")
    
    # Performance trend
    print(f"\n📊 Performance by Load Level:")
    for test_name, performance in comprehensive_report["performance_trend"].items():
        print(f"   {test_name.upper()}:")
        print(f"     Success Rate: {performance['success_rate']}")
        print(f"     Response Time: {performance['avg_response_time']}s")
        print(f"     Grade: {performance['grade']}")
    
    # Scalability analysis
    scalability = comprehensive_report["scalability_analysis"]
    print(f"\n🔄 Scalability Analysis:")
    print(f"   Grade: {scalability['scalability_grade']}")
    print(f"   Response Time Increase: {scalability['response_time_increase_factor']}x")
    print(f"   Success Rate Decrease: {scalability['success_rate_decrease']}")
    
    # Production readiness
    readiness = comprehensive_report["production_readiness"]
    print(f"\n🚀 Production Readiness:")
    print(f"   Level: {readiness['readiness_level']}")
    print(f"   Score: {readiness['readiness_score']}/1.0")
    
    # Overall assessment
    print(f"\n🎯 Overall Assessment:")
    print(f"   {comprehensive_report['overall_assessment']}")
    
    # Top optimization priorities
    priorities = comprehensive_report["optimization_priorities"]
    if priorities:
        print(f"\n🔧 Top Optimization Priorities:")
        for priority in priorities[:3]:
            print(f"   • {priority}")
    
    print(f"\n✅ Production load testing complete!")
    print(f"📁 Detailed results saved in: {load_tester.results_dir}")

if __name__ == "__main__":
    main()

