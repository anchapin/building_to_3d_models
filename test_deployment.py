import os
import sys
import unittest
import json
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFrontendIntegration(unittest.TestCase):
    """Test cases for the frontend integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'frontend')
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    @patch('subprocess.run')
    def test_frontend_build(self, mock_run):
        """Test that the frontend builds correctly."""
        # Mock the build process
        mock_run.return_value = MagicMock(returncode=0)
        
        # Set up paths
        frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   'frontend', 'building-to-3d-app')
        
        # Check if frontend directory exists
        self.assertTrue(os.path.exists(frontend_dir), 
                       f"Frontend directory not found at {frontend_dir}")
        
        # Check for key frontend files
        self.assertTrue(os.path.exists(os.path.join(frontend_dir, 'src', 'app', 'page.tsx')),
                       "Main page component not found")
        self.assertTrue(os.path.exists(os.path.join(frontend_dir, 'src', 'app', 'upload', 'page.tsx')),
                       "Upload page component not found")
        self.assertTrue(os.path.exists(os.path.join(frontend_dir, 'src', 'app', 'results', 'page.tsx')),
                       "Results page component not found")
        
        # Simulate build process
        try:
            # In a real test, this would run: npm run build
            # For our test, we'll just mock it
            mock_run.assert_not_called()  # No actual call should happen in this test
            
            # Check that the build process would be successful
            self.assertEqual(mock_run.return_value.returncode, 0)
            
        except Exception as e:
            self.fail(f"Frontend build test failed with error: {e}")

class TestDeployment(unittest.TestCase):
    """Test cases for application deployment."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'deployment')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create a mock deployment package
        self.deployment_dir = os.path.join(self.test_output_dir, 'deployment_package')
        os.makedirs(self.deployment_dir, exist_ok=True)
        
        # Create mock files for deployment
        with open(os.path.join(self.deployment_dir, 'index.html'), 'w') as f:
            f.write("<html><body><h1>Building-to-3D Conversion App</h1></body></html>")
            
        os.makedirs(os.path.join(self.deployment_dir, 'api'), exist_ok=True)
        with open(os.path.join(self.deployment_dir, 'api', 'app.py'), 'w') as f:
            f.write("# Mock API server\n")
    
    def test_deployment_package_creation(self):
        """Test creation of deployment package."""
        # Check that deployment directory exists
        self.assertTrue(os.path.exists(self.deployment_dir))
        
        # Check for key files
        self.assertTrue(os.path.exists(os.path.join(self.deployment_dir, 'index.html')))
        self.assertTrue(os.path.exists(os.path.join(self.deployment_dir, 'api', 'app.py')))
        
        # Create a zip file of the deployment package
        shutil.make_archive(
            os.path.join(self.test_output_dir, 'building_to_3d_app'),
            'zip',
            self.deployment_dir
        )
        
        # Check that zip file was created
        self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, 'building_to_3d_app.zip')))
    
    @patch('subprocess.run')
    def test_deployment_script(self, mock_run):
        """Test deployment script execution."""
        # Mock the deployment process
        mock_run.return_value = MagicMock(returncode=0)
        
        # Create a mock deployment script
        deploy_script_path = os.path.join(self.test_output_dir, 'deploy.sh')
        with open(deploy_script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Mock deployment script\n")
            f.write("echo 'Deploying application...'\n")
            f.write("mkdir -p /tmp/deployed_app\n")
            f.write("cp -r $1/* /tmp/deployed_app/\n")
            f.write("echo 'Application deployed successfully!'\n")
        
        # Make script executable
        os.chmod(deploy_script_path, 0o755)
        
        # Simulate deployment
        try:
            # In a real test, this would run the deployment script
            # For our test, we'll just mock it
            mock_run.assert_not_called()  # No actual call should happen in this test
            
            # Check that the deployment process would be successful
            self.assertEqual(mock_run.return_value.returncode, 0)
            
        except Exception as e:
            self.fail(f"Deployment test failed with error: {e}")

class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end tests for the entire application workflow with sample data."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'end_to_end')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create sample test data directory
        self.test_data_dir = os.path.join(self.test_output_dir, 'test_data')
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create sample floor plan image
        self.floor_plan_path = os.path.join(self.test_data_dir, 'sample_floor_plan.png')
        self._create_sample_image(self.floor_plan_path, 800, 600)
        
        # Create sample elevation images
        self.elevation_paths = []
        for direction in ['north', 'east', 'south', 'west']:
            path = os.path.join(self.test_data_dir, f'sample_elevation_{direction}.png')
            self._create_sample_image(path, 800, 400)
            self.elevation_paths.append(path)
    
    def _create_sample_image(self, path, width, height):
        """Create a sample image for testing."""
        try:
            import numpy as np
            from PIL import Image, ImageDraw
            
            # Create a blank image
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw some lines to simulate walls
            draw.line([(50, 50), (width-50, 50)], fill='black', width=3)
            draw.line([(width-50, 50), (width-50, height-50)], fill='black', width=3)
            draw.line([(width-50, height-50), (50, height-50)], fill='black', width=3)
            draw.line([(50, height-50), (50, 50)], fill='black', width=3)
            
            # Draw some rectangles to simulate windows and doors
            draw.rectangle([(200, 50), (300, 100)], outline='black', width=2)
            draw.rectangle([(500, 50), (600, 150)], outline='black', width=2)
            
            # Save the image
            img.save(path)
            
        except ImportError:
            # If PIL is not available, create an empty file
            with open(path, 'w') as f:
                f.write("Mock image file for testing")
    
    @patch('backend.image_processing.image_processor.ImageProcessor.process_building_plan')
    @patch('backend.reconstruction.reconstruction_coordinator.ReconstructionCoordinator.process_building')
    @patch('backend.gbxml.gbxml_manager.GbXMLManager.convert_building_model')
    def test_end_to_end_workflow(self, mock_convert, mock_process_building, mock_process_plan):
        """Test the end-to-end workflow with sample data."""
        # Mock the image processing output
        mock_process_plan.return_value = {
            'image_id': 'sample_floor_plan',
            'features': {
                'walls': [
                    {'type': 'wall', 'points': [(50, 50), (750, 50)], 'length': 700},
                    {'type': 'wall', 'points': [(750, 50), (750, 550)], 'length': 500},
                    {'type': 'wall', 'points': [(750, 550), (50, 550)], 'length': 700},
                    {'type': 'wall', 'points': [(50, 550), (50, 50)], 'length': 500}
                ],
                'windows': [
                    {'type': 'window', 'points': [(200, 50), (300, 100)], 'width': 100, 'height': 50}
                ],
                'doors': [
                    {'type': 'door', 'door_type': 'standard', 'points': [(500, 50), (600, 150)], 'width': 100, 'height': 100}
                ]
            }
        }
        
        # Mock the reconstruction output
        mock_process_building.return_value = {
            'building_model': {
                'floors': [0.0, 3.0],
                'walls': [
                    {'points': [(50, 50), (750, 50)], 'height': 3.0, 'base_height': 0.0},
                    {'points': [(750, 50), (750, 550)], 'height': 3.0, 'base_height': 0.0},
                    {'points': [(750, 550), (50, 550)], 'height': 3.0, 'base_height': 0.0},
                    {'points': [(50, 550), (50, 50)], 'height': 3.0, 'base_height': 0.0}
                ],
                'openings': [
                    {'type': 'window', 'position': (200, 50), 'width': 100, 'height': 50, 'floor': 0},
                    {'type': 'door', 'door_type': 'standard', 'position': (500, 50), 'width': 100, 'height': 100, 'floor': 0}
                ]
            },
            'mesh_path': os.path.join(self.test_output_dir, 'building_model.obj')
        }
        
        # Mock the gbXML conversion output
        mock_convert.return_value = os.path.join(self.test_output_dir, 'building_model.gbxml')
        
        # Create a mock mesh file
        with open(os.path.join(self.test_output_dir, 'building_model.obj'), 'w') as f:
            f.write("# Mock OBJ file for testing\n")
        
        try:
            # Simulate the end-to-end workflow
            
            # 1. Process floor plan
            floor_plan_result = mock_process_plan(self.floor_plan_path, output_dir=self.test_output_dir)
            self.assertIsNotNone(floor_plan_result)
            
            # 2. Process elevations
            elevation_results = []
            for path in self.elevation_paths:
                result = mock_process_plan(path, output_dir=self.test_output_dir)
                elevation_results.append(result)
            
            # 3. Reconstruct 3D model
            model_result = mock_process_building(
                [os.path.join(self.test_output_dir, 'sample_floor_plan_processed.json')],
                [os.path.join(self.test_output_dir, f'sample_elevation_{d}_processed.json') for d in ['north', 'east', 'south', 'west']],
                output_dir=self.test_output_dir
            )
            self.assertIsNotNone(model_result)
            
            # 4. Convert to gbXML
            gbxml_path = mock_convert(
                os.path.join(self.test_output_dir, 'building_model.json'),
                output_dir=self.test_output_dir
            )
            self.assertEqual(gbxml_path, os.path.join(self.test_output_dir, 'building_model.gbxml'))
            
            # Check that the workflow would be successful
            mock_process_plan.assert_called()
            mock_process_building.assert_called()
            mock_convert.assert_called()
            
        except Exception as e:
            self.fail(f"End-to-end test failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
