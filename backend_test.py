import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any

class OceanHazardAPITester:
    def __init__(self, base_url="https://pdf-blueprint-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer mock_jwt_token'
        }
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASSED {details}")
        else:
            self.failed_tests.append(f"{name}: {details}")
            print(f"❌ {name}: FAILED {details}")

    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.api_url}/health", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Response: {data.get('status', 'N/A')}"
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False

    def test_dashboard_stats(self):
        """Test dashboard stats endpoint"""
        try:
            response = requests.get(f"{self.api_url}/dashboard/stats", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                required_fields = ['total_reports', 'verified_reports', 'pending_reports', 'active_alerts']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    success = False
                    details += f", Missing fields: {missing_fields}"
                else:
                    details += f", Total reports: {data.get('total_reports', 0)}"
            self.log_test("Dashboard Stats", success, details)
            return success
        except Exception as e:
            self.log_test("Dashboard Stats", False, f"Exception: {str(e)}")
            return False

    def test_get_reports(self):
        """Test get hazard reports endpoint"""
        try:
            response = requests.get(f"{self.api_url}/reports", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f", Reports count: {len(data)}"
                    if len(data) > 0:
                        # Check first report structure
                        first_report = data[0]
                        required_fields = ['id', 'title', 'description', 'hazard_type', 'severity', 'location']
                        missing_fields = [field for field in required_fields if field not in first_report]
                        if missing_fields:
                            details += f", Missing fields in report: {missing_fields}"
                else:
                    success = False
                    details += ", Response is not a list"
            self.log_test("Get Reports", success, details)
            return success
        except Exception as e:
            self.log_test("Get Reports", False, f"Exception: {str(e)}")
            return False

    def test_create_report(self):
        """Test create hazard report endpoint"""
        try:
            test_report = {
                "title": "Test Hazard Report",
                "description": "This is a test hazard report created by automated testing",
                "hazard_type": "high_waves",
                "severity": "medium",
                "location": {
                    "latitude": 19.0760,
                    "longitude": 72.8777,
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "country": "India"
                },
                "contact_info": "test@example.com",
                "language": "en",
                "tags": ["test", "automated"]
            }
            
            response = requests.post(f"{self.api_url}/reports", 
                                   json=test_report, 
                                   headers=self.headers, 
                                   timeout=15)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if 'id' in data:
                    details += f", Created report ID: {data['id']}"
                    return data['id']  # Return ID for further testing
                else:
                    success = False
                    details += ", No ID in response"
            
            self.log_test("Create Report", success, details)
            return data['id'] if success and 'id' in data else None
            
        except Exception as e:
            self.log_test("Create Report", False, f"Exception: {str(e)}")
            return None

    def test_get_single_report(self, report_id: str):
        """Test get single report by ID"""
        if not report_id:
            self.log_test("Get Single Report", False, "No report ID provided")
            return False
            
        try:
            response = requests.get(f"{self.api_url}/reports/{report_id}", 
                                  headers=self.headers, 
                                  timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if data.get('id') == report_id:
                    details += f", Retrieved report: {data.get('title', 'N/A')}"
                else:
                    success = False
                    details += ", Report ID mismatch"
            
            self.log_test("Get Single Report", success, details)
            return success
            
        except Exception as e:
            self.log_test("Get Single Report", False, f"Exception: {str(e)}")
            return False

    def test_social_media_posts(self):
        """Test social media posts endpoint"""
        try:
            response = requests.get(f"{self.api_url}/social-media", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f", Posts count: {len(data)}"
                    if len(data) > 0:
                        first_post = data[0]
                        required_fields = ['id', 'platform', 'content', 'author']
                        missing_fields = [field for field in required_fields if field not in first_post]
                        if missing_fields:
                            details += f", Missing fields: {missing_fields}"
                else:
                    success = False
                    details += ", Response is not a list"
            
            self.log_test("Social Media Posts", success, details)
            return success
            
        except Exception as e:
            self.log_test("Social Media Posts", False, f"Exception: {str(e)}")
            return False

    def test_map_hazards(self):
        """Test map hazards endpoint"""
        try:
            response = requests.get(f"{self.api_url}/map/hazards", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f", Map hazards count: {len(data)}"
                    if len(data) > 0:
                        first_hazard = data[0]
                        required_fields = ['id', 'latitude', 'longitude', 'hazard_type', 'severity']
                        missing_fields = [field for field in required_fields if field not in first_hazard]
                        if missing_fields:
                            details += f", Missing fields: {missing_fields}"
                else:
                    success = False
                    details += ", Response is not a list"
            
            self.log_test("Map Hazards", success, details)
            return success
            
        except Exception as e:
            self.log_test("Map Hazards", False, f"Exception: {str(e)}")
            return False

    def test_alerts(self):
        """Test alerts endpoint"""
        try:
            response = requests.get(f"{self.api_url}/alerts", headers=self.headers, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if isinstance(data, list):
                    details += f", Alerts count: {len(data)}"
                    if len(data) > 0:
                        first_alert = data[0]
                        required_fields = ['id', 'title', 'message', 'severity']
                        missing_fields = [field for field in required_fields if field not in first_alert]
                        if missing_fields:
                            details += f", Missing fields: {missing_fields}"
                else:
                    success = False
                    details += ", Response is not a list"
            
            self.log_test("Alerts", success, details)
            return success
            
        except Exception as e:
            self.log_test("Alerts", False, f"Exception: {str(e)}")
            return False

    def test_social_media_analyze(self):
        """Test social media analysis endpoint"""
        try:
            response = requests.post(f"{self.api_url}/social-media/analyze", 
                                   headers=self.headers, 
                                   timeout=20)  # Longer timeout for AI processing
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                if 'analyzed_posts' in data:
                    details += f", Analyzed posts: {data['analyzed_posts']}"
                else:
                    details += f", Response: {data}"
            
            self.log_test("Social Media Analysis", success, details)
            return success
            
        except Exception as e:
            self.log_test("Social Media Analysis", False, f"Exception: {str(e)}")
            return False

    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        # Test login
        try:
            login_data = {
                "username": "demo_user",
                "password": "demo_password"
            }
            response = requests.post(f"{self.api_url}/auth/login", 
                                   json=login_data, 
                                   headers={'Content-Type': 'application/json'}, 
                                   timeout=10)
            success = response.status_code == 200
            details = f"Login Status: {response.status_code}"
            
            if success:
                data = response.json()
                if 'access_token' in data:
                    details += ", Token received"
                else:
                    details += ", No token in response"
            
            self.log_test("Authentication Login", success, details)
            return success
            
        except Exception as e:
            self.log_test("Authentication Login", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🌊 Starting Ocean Hazard Platform API Tests")
        print("=" * 50)
        
        # Basic connectivity
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return self.print_summary()
        
        # Core endpoints
        self.test_dashboard_stats()
        self.test_get_reports()
        
        # Create and retrieve report
        report_id = self.test_create_report()
        if report_id:
            self.test_get_single_report(report_id)
        
        # Other endpoints
        self.test_social_media_posts()
        self.test_map_hazards()
        self.test_alerts()
        self.test_social_media_analyze()
        self.test_auth_endpoints()
        
        return self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("🧪 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for failure in self.failed_tests:
                print(f"  - {failure}")
        
        print("\n" + "=" * 50)
        return len(self.failed_tests) == 0

def main():
    tester = OceanHazardAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
