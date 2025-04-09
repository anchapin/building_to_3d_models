#!/bin/bash

# Run all tests for the Building-to-3D Conversion Application

# Create output directories
mkdir -p tests/output/image_processing
mkdir -p tests/output/reconstruction
mkdir -p tests/output/gbxml
mkdir -p tests/output/integration
mkdir -p tests/output/frontend
mkdir -p tests/output/deployment
mkdir -p tests/output/end_to_end

# Run module tests
echo "Running module tests..."
python3 tests/test_modules.py

# Run deployment tests
echo "Running deployment tests..."
python3 tests/test_deployment.py

echo "All tests completed."
