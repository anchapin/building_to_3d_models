import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Create temporary directories for uploads and results
        self.temp_upload_dir = tempfile.mkdtemp()
        self.temp_results_dir = tempfile.mkdtemp()
        
        # Mock the upload and results folders
        self.upload_folder_patcher = patch('app.UPLOAD_FOLDER', self.temp_upload_dir)
        self.results_folder_patcher = patch('app.RESULTS_FOLDER', self.temp_results_dir)
        
        self.upload_folder_patcher.start()
        self.results_folder_patcher.start()
    
    def tearDown(self):
        # Stop patches
        self.upload_folder_patcher.stop()
        self.results_folder_patcher.stop()
        
        # Clean up temporary directories
        import shutil
        shutil.rmtree(self.temp_upload_dir)
        shutil.rmtree(self.temp_results_dir)
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
    
    @patch('app.ImageProcessor')
    def test_upload_file_no_file(self, mock_image_processor):
        """Test upload endpoint with no file."""
        response = self.client.post('/api/upload')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No file part')
    
    @patch('app.ImageProcessor')
    def test_upload_file_empty_filename(self, mock_image_processor):
        """Test upload endpoint with empty filename."""
        response = self.client.post('/api/upload', data={
            'file': (tempfile.NamedTemporaryFile(), ''),
            'type': 'floorPlan'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No selected file')
    
    @patch('app.ImageProcessor')
    def test_upload_file_invalid_type(self, mock_image_processor):
        """Test upload endpoint with invalid file type."""
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
            response = self.client.post('/api/upload', data={
                'file': (temp_file, 'test.pdf'),
                'type': 'invalid'
            })
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Invalid file type')
    
    @patch('app.ImageProcessor')
    def test_upload_floor_plan(self, mock_image_processor):
        """Test upload endpoint with floor plan."""
        # Mock the process_building_plan method
        mock_instance = mock_image_processor.return_value
        mock_instance.process_building_plan.return_value = {
            'floor_level': 0
        }
        
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
            response = self.client.post('/api/upload', data={
                'file': (temp_file, 'test.pdf'),
                'type': 'floorPlan',
                'floorLevel': '0'
            })
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['file_type'], 'floorPlan')
            self.assertEqual(data['floor_level'], '0')
    
    @patch('app.ImageProcessor')
    def test_upload_elevation(self, mock_image_processor):
        """Test upload endpoint with elevation."""
        # Mock the process_building_plan method
        mock_instance = mock_image_processor.return_value
        mock_instance.process_building_plan.return_value = {}
        
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_file:
            response = self.client.post('/api/upload', data={
                'file': (temp_file, 'test.pdf'),
                'type': 'elevation',
                'orientation': 'north'
            })
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['file_type'], 'elevation')
            self.assertEqual(data['orientation'], 'north')
    
    @patch('app.ImageProcessor')
    def test_set_scale(self, mock_image_processor):
        """Test set scale endpoint."""
        # Mock the scale_converter.set_scale method
        mock_instance = mock_image_processor.return_value
        mock_instance.scale_converter.set_scale.return_value = 0.01
        
        response = self.client.post('/api/set-scale', json={
            'imageId': 'test.pdf',
            'pixelLength': 100,
            'realLength': 1,
            'unit': 'meters'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['scale_factor'], 0.01)
    
    @patch('app.ReconstructionCoordinator')
    @patch('app.GbXMLManager')
    def test_generate_model(self, mock_gbxml_manager, mock_reconstruction_coordinator):
        """Test generate model endpoint."""
        # Mock the process_building method
        mock_recon_instance = mock_reconstruction_coordinator.return_value
        mock_recon_instance.process_building.return_value = {}
        
        # Mock the convert_building_model method
        mock_gbxml_instance = mock_gbxml_manager.return_value
        mock_gbxml_instance.convert_building_model.return_value = 'building_model.gbxml'
        
        response = self.client.post('/api/generate-model', json={
            'floorPlans': ['floor1.json', 'floor2.json'],
            'elevations': ['north.json', 'south.json']
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['model_file'], 'building_model.obj')
        self.assertEqual(data['gbxml_file'], 'building_model.gbxml')
    
    def test_get_result_file_not_found(self):
        """Test get result file endpoint with non-existent file."""
        response = self.client.get('/api/results/nonexistent.json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'File not found')

if __name__ == '__main__':
    unittest.main()