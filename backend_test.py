#!/usr/bin/env python3
"""
Context Engineering Framework Backend API Tests
===============================================

Comprehensive test suite for the Context Engineering demo server running on port 8001.
Tests all endpoints and functionality as specified in the review request.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List, Optional

class ContextEngineAPITester:
    """Test suite for Context Engineering Framework API"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        self.session.timeout = 30
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time()
        }
        if response_data:
            result["response_data"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()
    
    def test_server_connectivity(self) -> bool:
        """Test 1: Basic server connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                self.log_test(
                    "Server Connectivity", 
                    True, 
                    f"Server responding on port 8001, status: {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    "Server Connectivity", 
                    False, 
                    f"Unexpected status code: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test(
                "Server Connectivity", 
                False, 
                f"Connection failed: {str(e)}"
            )
            return False
    
    def test_main_demo_page(self) -> bool:
        """Test 2: Main demo page (GET /)"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                content = response.text
                # Check for key elements in the HTML
                required_elements = [
                    "Context Engineering Demo",
                    "Interactive Demo",
                    "System Status",
                    "Architecture Components",
                    "processQuery()",
                    "loadStatus()"
                ]
                
                missing_elements = [elem for elem in required_elements if elem not in content]
                
                if not missing_elements:
                    self.log_test(
                        "Main Demo Page", 
                        True, 
                        f"HTML page loaded successfully with all required elements"
                    )
                    return True
                else:
                    self.log_test(
                        "Main Demo Page", 
                        False, 
                        f"Missing elements: {missing_elements}"
                    )
                    return False
            else:
                self.log_test(
                    "Main Demo Page", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Main Demo Page", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_status_endpoint(self) -> bool:
        """Test 3: Status endpoint (GET /api/status)"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = ["status", "components", "version"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        self.log_test(
                            "Status Endpoint", 
                            True, 
                            f"Status: {data['status']}, Components: {data['components']}, Version: {data['version']}"
                        )
                        return True
                    else:
                        self.log_test(
                            "Status Endpoint", 
                            False, 
                            f"Missing fields: {missing_fields}",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Status Endpoint", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Status Endpoint", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Status Endpoint", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_demo_api_endpoint(self) -> bool:
        """Test 4: Demo API endpoint (GET /api/demo)"""
        try:
            response = self.session.get(f"{self.base_url}/api/demo")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = ["message", "endpoints"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields and isinstance(data["endpoints"], list):
                        self.log_test(
                            "Demo API Endpoint", 
                            True, 
                            f"Message: {data['message']}, Endpoints: {len(data['endpoints'])} listed"
                        )
                        return True
                    else:
                        self.log_test(
                            "Demo API Endpoint", 
                            False, 
                            f"Missing fields: {missing_fields} or invalid endpoints format",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Demo API Endpoint", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Demo API Endpoint", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Demo API Endpoint", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_reasoning_endpoint_basic(self) -> bool:
        """Test 5: Basic reasoning endpoint (POST /api/reason)"""
        try:
            test_query = "What is artificial intelligence?"
            payload = {"query": test_query}
            
            response = self.session.post(
                f"{self.base_url}/api/reason",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check required fields
                    required_fields = [
                        "success", "query", "response", "confidence", 
                        "processing_time", "components_used", "reasoning_trace"
                    ]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        # Validate data types and values
                        validations = [
                            (data["success"] == True, "success should be True"),
                            (data["query"] == test_query, "query should match input"),
                            (isinstance(data["response"], str) and len(data["response"]) > 0, "response should be non-empty string"),
                            (isinstance(data["confidence"], int) and 0 <= data["confidence"] <= 100, "confidence should be 0-100"),
                            (isinstance(data["processing_time"], str), "processing_time should be string"),
                            (isinstance(data["components_used"], int) and data["components_used"] > 0, "components_used should be positive integer"),
                            (isinstance(data["reasoning_trace"], list), "reasoning_trace should be list")
                        ]
                        
                        failed_validations = [msg for valid, msg in validations if not valid]
                        
                        if not failed_validations:
                            self.log_test(
                                "Reasoning Endpoint - Basic", 
                                True, 
                                f"Query processed successfully. Confidence: {data['confidence']}%, Time: {data['processing_time']}s, Components: {data['components_used']}"
                            )
                            return True
                        else:
                            self.log_test(
                                "Reasoning Endpoint - Basic", 
                                False, 
                                f"Validation failures: {failed_validations}",
                                data
                            )
                            return False
                    else:
                        self.log_test(
                            "Reasoning Endpoint - Basic", 
                            False, 
                            f"Missing fields: {missing_fields}",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Reasoning Endpoint - Basic", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Reasoning Endpoint - Basic", 
                    False, 
                    f"Status code: {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reasoning Endpoint - Basic", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_reasoning_endpoint_complex_query(self) -> bool:
        """Test 6: Complex philosophical query"""
        try:
            test_query = "What are the fundamental principles of consciousness and how do they relate to artificial intelligence systems?"
            payload = {"query": test_query}
            
            response = self.session.post(
                f"{self.base_url}/api/reason",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    if data.get("success") and len(data.get("response", "")) > 100:
                        self.log_test(
                            "Reasoning Endpoint - Complex Query", 
                            True, 
                            f"Complex query processed. Response length: {len(data['response'])} chars, Confidence: {data.get('confidence', 'N/A')}%"
                        )
                        return True
                    else:
                        self.log_test(
                            "Reasoning Endpoint - Complex Query", 
                            False, 
                            f"Insufficient response or failed processing",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Reasoning Endpoint - Complex Query", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Reasoning Endpoint - Complex Query", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reasoning Endpoint - Complex Query", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_reasoning_endpoint_empty_query(self) -> bool:
        """Test 7: Empty query edge case"""
        try:
            payload = {"query": ""}
            
            response = self.session.post(
                f"{self.base_url}/api/reason",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Should still process but might use default query
                    if data.get("success") is not None:
                        self.log_test(
                            "Reasoning Endpoint - Empty Query", 
                            True, 
                            f"Empty query handled gracefully. Success: {data['success']}"
                        )
                        return True
                    else:
                        self.log_test(
                            "Reasoning Endpoint - Empty Query", 
                            False, 
                            "Unexpected response format",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Reasoning Endpoint - Empty Query", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Reasoning Endpoint - Empty Query", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reasoning Endpoint - Empty Query", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_reasoning_endpoint_no_query_field(self) -> bool:
        """Test 8: Missing query field"""
        try:
            payload = {"message": "test without query field"}
            
            response = self.session.post(
                f"{self.base_url}/api/reason",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Should handle missing query field gracefully
                    if data.get("success") is not None:
                        self.log_test(
                            "Reasoning Endpoint - No Query Field", 
                            True, 
                            f"Missing query field handled. Success: {data['success']}"
                        )
                        return True
                    else:
                        self.log_test(
                            "Reasoning Endpoint - No Query Field", 
                            False, 
                            "Unexpected response format",
                            data
                        )
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test(
                        "Reasoning Endpoint - No Query Field", 
                        False, 
                        "Invalid JSON response",
                        response.text
                    )
                    return False
            else:
                self.log_test(
                    "Reasoning Endpoint - No Query Field", 
                    False, 
                    f"Status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Reasoning Endpoint - No Query Field", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_malformed_json_request(self) -> bool:
        """Test 9: Malformed JSON request"""
        try:
            # Send malformed JSON
            response = self.session.post(
                f"{self.base_url}/api/reason",
                data='{"query": "test", invalid json}',
                headers={"Content-Type": "application/json"}
            )
            
            # Should return error response
            if response.status_code in [400, 500]:
                self.log_test(
                    "Malformed JSON Request", 
                    True, 
                    f"Malformed JSON properly rejected with status {response.status_code}"
                )
                return True
            elif response.status_code == 200:
                # Check if it's an error response
                try:
                    data = response.json()
                    if data.get("success") == False:
                        self.log_test(
                            "Malformed JSON Request", 
                            True, 
                            f"Malformed JSON handled with error response: {data.get('error', 'Unknown error')}"
                        )
                        return True
                except:
                    pass
                
                self.log_test(
                    "Malformed JSON Request", 
                    False, 
                    "Malformed JSON should not return success",
                    response.text
                )
                return False
            else:
                self.log_test(
                    "Malformed JSON Request", 
                    False, 
                    f"Unexpected status code: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Malformed JSON Request", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_invalid_endpoint(self) -> bool:
        """Test 10: Invalid endpoint (should return 404)"""
        try:
            response = self.session.get(f"{self.base_url}/api/nonexistent")
            
            if response.status_code == 404:
                self.log_test(
                    "Invalid Endpoint", 
                    True, 
                    "Invalid endpoint properly returns 404"
                )
                return True
            else:
                self.log_test(
                    "Invalid Endpoint", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Invalid Endpoint", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_cors_headers(self) -> bool:
        """Test 11: CORS headers presence"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            
            cors_header = response.headers.get('Access-Control-Allow-Origin')
            if cors_header:
                self.log_test(
                    "CORS Headers", 
                    True, 
                    f"CORS header present: {cors_header}"
                )
                return True
            else:
                self.log_test(
                    "CORS Headers", 
                    False, 
                    "Missing Access-Control-Allow-Origin header"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "CORS Headers", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def test_performance_timing(self) -> bool:
        """Test 12: Performance and response timing"""
        try:
            test_queries = [
                "What is machine learning?",
                "Explain quantum computing",
                "How does neural network training work?"
            ]
            
            response_times = []
            
            for query in test_queries:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/api/reason",
                    json={"query": query},
                    headers={"Content-Type": "application/json"}
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append(end_time - start_time)
                else:
                    self.log_test(
                        "Performance Timing", 
                        False, 
                        f"Request failed for query: {query}"
                    )
                    return False
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # Consider performance acceptable if average < 5s and max < 10s
            if avg_response_time < 5.0 and max_response_time < 10.0:
                self.log_test(
                    "Performance Timing", 
                    True, 
                    f"Average response time: {avg_response_time:.2f}s, Max: {max_response_time:.2f}s"
                )
                return True
            else:
                self.log_test(
                    "Performance Timing", 
                    False, 
                    f"Performance issues - Average: {avg_response_time:.2f}s, Max: {max_response_time:.2f}s"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Performance Timing", 
                False, 
                f"Error: {str(e)}"
            )
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary"""
        print("🧠 Context Engineering Framework Backend API Tests")
        print("=" * 60)
        print()
        
        # List of all test methods
        test_methods = [
            self.test_server_connectivity,
            self.test_main_demo_page,
            self.test_status_endpoint,
            self.test_demo_api_endpoint,
            self.test_reasoning_endpoint_basic,
            self.test_reasoning_endpoint_complex_query,
            self.test_reasoning_endpoint_empty_query,
            self.test_reasoning_endpoint_no_query_field,
            self.test_malformed_json_request,
            self.test_invalid_endpoint,
            self.test_cors_headers,
            self.test_performance_timing
        ]
        
        # Run all tests
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            try:
                if test_method():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
        
        # Generate summary
        success_rate = (passed_tests / total_tests) * 100
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 80:
            print("🎉 OVERALL STATUS: GOOD - Backend API is functioning well")
        elif success_rate >= 60:
            print("⚠️  OVERALL STATUS: ACCEPTABLE - Some issues found but core functionality works")
        else:
            print("❌ OVERALL STATUS: POOR - Significant issues found")
        
        print()
        print("🔍 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"]:
                print(f"    {result['details']}")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "detailed_results": self.test_results
        }

def main():
    """Main test execution"""
    print("Starting Context Engineering Framework Backend Tests...")
    print()
    
    # Initialize tester
    tester = ContextEngineAPITester()
    
    # Run all tests
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    if results["success_rate"] >= 80:
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)