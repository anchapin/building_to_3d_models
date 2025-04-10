import os
import requests
import json

def test_health_endpoint():
    """Test the health check endpoint."""
    response = requests.get('http://localhost:5000/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
    print("Health check endpoint test passed!")

def main():
    """Run all tests."""
    print("Testing API endpoints...")
    test_health_endpoint()
    print("All tests passed!")

if __name__ == '__main__':
    main()