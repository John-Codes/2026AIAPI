"""
REAL ENDPOINT TESTS - NO MOCKS ALLOWED

This file contains real HTTP endpoint tests using httpx.
These tests make actual requests to a running FastAPI server on localhost:8000.
NO MOCK TESTS ARE EVER ALLOWED IN THIS FILE.

To run these tests:
1. Start the FastAPI server: uvicorn app:app --host 0.0.0.0 --port 8000
2. Set your OpenRouter API key: export OpenRouter=your_api_key_here
3. Run tests: pytest test_real_endpoints.py -v
"""

import pytest
import httpx
import json
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0

# Test API key - replace with your actual OpenRouter API key
TEST_API_KEY = os.getenv("OpenRouter", "sk-or-xxxx")
TEST_MODEL = os.getenv("Model_Name", "z-ai/glm-4.5-air:free")

class TestRealEndpoints:
    """Real endpoint tests - no mocks allowed"""
    
    @pytest.fixture(scope="session")
    def client(self):
        """HTTP client for real endpoint testing"""
        return httpx.Client(timeout=TIMEOUT)
    
    @pytest.fixture(scope="session")
    def is_server_running(self, client):
        """Check if the FastAPI server is running"""
        try:
            response = client.get(f"{BASE_URL}/heartbeat")
            return response.status_code == 200
        except httpx.ConnectError:
            return False
    
    def test_heartbeat_endpoint(self, client, is_server_running):
        """Test the heartbeat endpoint returns healthy status"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        response = client.get(f"{BASE_URL}/heartbeat")
        
        # Verify response status
        assert response.status_code == 200
        
        # Verify response structure
        data = response.json()
        assert "status" in data
        assert "message" in data
        assert data["status"] == "healthy"
        assert data["message"] == "API is running"
    
    def test_generate_endpoint_text_only(self, client, is_server_running):
        """Test generate endpoint with text input only"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        # Skip if using default test API key (invalid)
        if TEST_API_KEY == "sk-or-xxxx":
            pytest.skip("Please set a valid OpenRouter API key")
        
        payload = {
            "text": "Hello, can you tell me what 2+2 equals?",
            "api_key": TEST_API_KEY,
            "model_name": TEST_MODEL
        }
        
        response = client.post(f"{BASE_URL}/generate", json=payload)
        
        # Verify response status
        assert response.status_code == 200
        
        # Verify response structure
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
    
    def test_generate_endpoint_with_invalid_api_key(self, client, is_server_running):
        """Test generate endpoint with invalid API key"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        payload = {
            "text": "Hello, world!",
            "api_key": "invalid-api-key-12345"
        }
        
        response = client.post(f"{BASE_URL}/generate", json=payload)
        
        # Should return 200 but with error message in response
        assert response.status_code == 200
        
        data = response.json()
        assert "response" in data
        # Should contain error message
        assert "error" in data["response"].lower() or "failed" in data["response"].lower()
    
    def test_generate_endpoint_missing_text_field(self, client, is_server_running):
        """Test generate endpoint with missing required text field"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        payload = {
            "api_key": TEST_API_KEY
            # Missing required "text" field
        }
        
        response = client.post(f"{BASE_URL}/generate", json=payload)
        
        # Should return 422 for validation error
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data
    
    def test_generate_endpoint_with_image_url(self, client, is_server_running):
        """Test generate endpoint with image URL (if available)"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        if TEST_API_KEY == "sk-or-xxxx":
            pytest.skip("Please set a valid OpenRouter API key")
        
        payload = {
            "text": "Describe this image",
            "image_url": "https://via.placeholder.com/300x200.png?text=Test+Image",
            "api_key": TEST_API_KEY,
            "model_name": TEST_MODEL
        }
        
        response = client.post(f"{BASE_URL}/generate", json=payload)
        
        # Verify response status
        assert response.status_code == 200
        
        # Verify response structure
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
    
    def test_server_connection_error(self, client):
        """Test handling when server is not running"""
        # This test should be run when server is not running
        # We'll simulate by trying to connect to a non-existent port
        
        try:
            response = client.get("http://localhost:8001/heartbeat")  # Wrong port
            pytest.fail("Should have raised ConnectError")
        except httpx.ConnectError:
            # Expected behavior
            pass
    
    def test_timeout_handling(self, client, is_server_running):
        """Test timeout handling for slow responses"""
        if not is_server_running:
            pytest.skip("FastAPI server is not running on localhost:8000")
        
        # Create a client with very short timeout
        short_timeout_client = httpx.Client(timeout=0.1)
        
        try:
            response = short_timeout_client.get(f"{BASE_URL}/heartbeat")
            # If we get a response quickly, that's fine too
            assert response.status_code == 200
        except httpx.TimeoutException:
            # Expected for very short timeout
            pass
        finally:
            short_timeout_client.close()


# Test runner utilities
def check_server_status():
    """Check if the server is running and return status"""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{BASE_URL}/heartbeat")
            if response.status_code == 200:
                print("✅ FastAPI server is running on localhost:8000")
                return True
            else:
                print("❌ FastAPI server responded with unexpected status code")
                return False
    except httpx.ConnectError:
        print("❌ FastAPI server is not running on localhost:8000")
        print("   Please start it with: uvicorn app:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error checking server status: {e}")
        return False


def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("OpenRouter")
    if api_key and api_key != "sk-or-xxxx":
        print("✅ OpenRouter API key is configured")
        return True
    else:
        print("⚠️  OpenRouter API key not configured or using default")
        print("   Set your API key: export OpenRouter=your_actual_api_key")
        return False


if __name__ == "__main__":
    print("🔍 Checking prerequisites for real endpoint tests...")
    print()
    
    server_ok = check_server_status()
    api_key_ok = check_api_key()
    
    print()
    if server_ok and api_key_ok:
        print("✅ All prerequisites met. Run tests with: pytest test_real_endpoints.py -v")
    else:
        print("❌ Please fix the issues above before running tests")