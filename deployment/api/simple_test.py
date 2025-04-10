#!/usr/bin/env python3
"""
Simple test script to verify the API is working.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the app
from app import app

class SimpleTest(unittest.TestCase):
    """Simple test case for the API."""
    
    def setUp(self):
        """Set up the test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ok')

if __name__ == '__main__':
    unittest.main()