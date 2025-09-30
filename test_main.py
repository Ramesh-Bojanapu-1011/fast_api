"""
Comprehensive test suite for FastAPI application using pytest.
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health and basic endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World"
        assert data["status"] == "active"
        assert data["service"] == "Search API"
    
    def test_hello_endpoint_valid_name(self):
        """Test hello endpoint with valid name"""
        response = client.get("/hello/TestUser")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello TestUser"
        assert data["status"] == "success"
    
    def test_hello_endpoint_empty_name(self):
        """Test hello endpoint with empty name"""
        response = client.get("/hello/ ")
        assert response.status_code == 400
        data = response.json()
        assert "Name cannot be empty" in data["detail"]
    
    def test_health_check_endpoint(self):
        """Test the detailed health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Search API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data


class TestSearchEndpoints:
    """Test search functionality endpoints"""
    
    def test_youtube_search_valid_request(self):
        """Test YouTube search with valid request"""
        payload = {
            "search_text": "Python tutorial",
            "num_results": 3
        }
        response = client.post("/find/youtube/videos", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "data" in data
        assert "message" in data
    
    def test_youtube_search_invalid_num_results(self):
        """Test YouTube search with invalid num_results"""
        payload = {
            "search_text": "Python tutorial",
            "num_results": 100  # Should be max 50
        }
        response = client.post("/find/youtube/videos", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_youtube_search_empty_text(self):
        """Test YouTube search with empty search text"""
        payload = {
            "search_text": "",
            "num_results": 3
        }
        response = client.post("/find/youtube/videos", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_youtube_search_missing_text(self):
        """Test YouTube search with missing search text"""
        payload = {
            "num_results": 3
        }
        response = client.post("/find/youtube/videos", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_actor_search_valid_request(self):
        """Test actor search with valid request"""
        payload = {
            "name": "Test Actor",
            "craft": "actor"
        }
        response = client.post("/find/person/wiki_url", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_actor_search_empty_name(self):
        """Test actor search with empty name"""
        payload = {
            "name": "",
            "craft": "actor"
        }
        response = client.post("/find/person/wiki_url", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_actor_search_empty_craft(self):
        """Test actor search with empty craft"""
        payload = {
            "name": "Test Actor",
            "craft": ""
        }
        response = client.post("/find/person/wiki_url", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_actor_search_missing_fields(self):
        """Test actor search with missing required fields"""
        payload = {
            "name": "Test Actor"
            # Missing craft field
        }
        response = client.post("/find/person/wiki_url", json=payload)
        assert response.status_code == 422  # Validation error


class TestResponseModels:
    """Test response structure and data types"""
    
    def test_search_response_structure(self):
        """Test that search responses have correct structure"""
        payload = {
            "name": "Test Actor",
            "craft": "actor"
        }
        response = client.post("/find/person/wiki_url", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "data" in data
        assert isinstance(data["status"], bool)
        assert isinstance(data["data"], list)
        
        # Optional message field
        if "message" in data:
            assert isinstance(data["message"], str)
    
    def test_youtube_response_structure(self):
        """Test that YouTube responses have correct structure"""
        payload = {
            "search_text": "Test query",
            "num_results": 2
        }
        response = client.post("/find/youtube/videos", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "data" in data
        assert isinstance(data["status"], bool)
        assert isinstance(data["data"], dict)


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_nonexistent_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_wrong_http_method(self):
        """Test using wrong HTTP method"""
        response = client.get("/find/youtube/videos")  # Should be POST
        assert response.status_code == 405  # Method not allowed
    
    def test_invalid_json(self):
        """Test sending invalid JSON"""
        response = client.post(
            "/find/youtube/videos",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])