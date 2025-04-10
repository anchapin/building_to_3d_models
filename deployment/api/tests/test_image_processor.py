import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import cv2
import tempfile

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_processing.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.image_processor = ImageProcessor()
        
        # Create a simple test image
        self.test_image = np.ones((100, 100), dtype=np.uint8) * 255
        
        # Draw a simple rectangle to represent a room
        cv2.rectangle(self.test_image, (20, 20), (80, 80), 0, 2)
        
        # Create a temporary directory for output
        self.temp_dir = tempfile.mkdtemp()
        
        # Save the test image to a temporary file
        self.test_image_path = os.path.join(self.temp_dir, 'test_image.png')
        cv2.imwrite(self.test_image_path, self.test_image)
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('image_processing.edge_detector.EdgeDetector.detect_architectural_elements')
    @patch('image_processing.feature_extractor.FeatureExtractor.extract_features')
    def test_process_building_plan(self, mock_extract_features, mock_detect_elements):
        """Test processing a building plan image."""
        # Mock the detect_architectural_elements method
        mock_detect_elements.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60
                },
                {
                    'type': 'wall',
                    'points': [(80, 20), (80, 80)],
                    'length': 60
                },
                {
                    'type': 'wall',
                    'points': [(80, 80), (20, 80)],
                    'length': 60
                },
                {
                    'type': 'wall',
                    'points': [(20, 80), (20, 20)],
                    'length': 60
                }
            ]
        }
        
        # Mock the extract_features method
        mock_extract_features.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 0,
                    'orientation': 'horizontal'
                },
                {
                    'type': 'wall',
                    'points': [(80, 20), (80, 80)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 90,
                    'orientation': 'vertical'
                },
                {
                    'type': 'wall',
                    'points': [(80, 80), (20, 80)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 180,
                    'orientation': 'horizontal'
                },
                {
                    'type': 'wall',
                    'points': [(20, 80), (20, 20)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 270,
                    'orientation': 'vertical'
                }
            ],
            'rooms': [
                {
                    'type': 'room',
                    'points': [(20, 20), (80, 20), (80, 80), (20, 80)],
                    'area': 3600,
                    'centroid': (50, 50),
                    'label': 1
                }
            ]
        }
        
        # Process the test image
        result = self.image_processor.process_building_plan(
            self.test_image_path,
            output_dir=self.temp_dir
        )
        
        # Check that the result contains the expected keys
        self.assertIn('image_id', result)
        self.assertIn('file_path', result)
        self.assertIn('vector_data', result)
        self.assertIn('features', result)
        
        # Check that the vector data contains the expected keys
        vector_data = result['vector_data']
        self.assertIn('width', vector_data)
        self.assertIn('height', vector_data)
        self.assertIn('paths', vector_data)
        
        # Check that the features match the mocked features
        self.assertEqual(result['features'], mock_extract_features.return_value)
        
        # Check that the output file was created
        output_path = os.path.join(self.temp_dir, f"{os.path.basename(self.test_image_path)}_processed.json")
        self.assertTrue(os.path.exists(output_path))
    
    @patch('image_processing.edge_detector.EdgeDetector.detect_architectural_elements')
    @patch('image_processing.feature_extractor.FeatureExtractor.extract_features')
    def test_process_floor_plan(self, mock_extract_features, mock_detect_elements):
        """Test processing a floor plan specifically."""
        # Mock the detect_architectural_elements method
        mock_detect_elements.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60
                }
            ]
        }
        
        # Mock the extract_features method
        mock_extract_features.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 0,
                    'orientation': 'horizontal'
                }
            ],
            'rooms': [
                {
                    'type': 'room',
                    'points': [(20, 20), (80, 20), (80, 80), (20, 80)],
                    'area': 3600,
                    'centroid': (50, 50),
                    'label': 1
                }
            ]
        }
        
        # Process the test image as a floor plan
        result = self.image_processor.process_floor_plan(
            self.test_image_path,
            output_dir=self.temp_dir
        )
        
        # Check that the result contains the floor plan specific data
        self.assertIn('floor_plan_data', result)
        self.assertIn('room_connections', result['floor_plan_data'])
        self.assertIn('level', result['floor_plan_data'])
    
    @patch('image_processing.edge_detector.EdgeDetector.detect_architectural_elements')
    @patch('image_processing.feature_extractor.FeatureExtractor.extract_features')
    @patch('image_processing.edge_detector.EdgeDetector._hough_line_detection')
    def test_process_elevation_view(self, mock_hough_line, mock_extract_features, mock_detect_elements):
        """Test processing an elevation view."""
        # Mock the detect_architectural_elements method
        mock_detect_elements.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60
                }
            ]
        }
        
        # Mock the extract_features method
        mock_extract_features.return_value = {
            'walls': [
                {
                    'type': 'wall',
                    'points': [(20, 20), (80, 20)],
                    'length': 60,
                    'thickness': 2,
                    'angle': 0,
                    'orientation': 'horizontal'
                }
            ]
        }
        
        # Mock the _hough_line_detection method
        mock_hough_line.return_value = (None, np.array([[[20, 30, 80, 30]]]))
        
        # Process the test image as an elevation view
        result = self.image_processor.process_elevation_view(
            self.test_image_path,
            output_dir=self.temp_dir
        )
        
        # Check that the result contains the elevation specific data
        self.assertIn('elevation_data', result)
        self.assertIn('floor_levels', result['elevation_data'])
        self.assertIn('orientation', result['elevation_data'])
        
        # Check that floor levels were detected
        self.assertTrue(len(result['elevation_data']['floor_levels']) > 0)

if __name__ == '__main__':
    unittest.main()