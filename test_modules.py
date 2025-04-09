import os
import sys
import unittest
import json

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.image_processing.image_processor import ImageProcessor
from backend.reconstruction.building_reconstructor import BuildingReconstructor
from backend.reconstruction.reconstruction_coordinator import ReconstructionCoordinator
from backend.gbxml.gbxml_converter import GbXMLConverter
from backend.gbxml.gbxml_manager import GbXMLManager

class TestImageProcessingModule(unittest.TestCase):
    """Test cases for the image processing module."""
    
    def setUp(self):
        """Set up test environment."""
        self.image_processor = ImageProcessor()
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'image_processing')
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_image_processor_initialization(self):
        """Test that the image processor initializes correctly."""
        self.assertIsNotNone(self.image_processor)
        self.assertIsNotNone(self.image_processor.pdf_converter)
        self.assertIsNotNone(self.image_processor.edge_detector)
        self.assertIsNotNone(self.image_processor.feature_extractor)
        self.assertIsNotNone(self.image_processor.scale_converter)
    
    def test_scale_conversion(self):
        """Test scale conversion functionality."""
        # Set a scale
        image_id = "test_image"
        pixel_length = 100
        real_length = 5.0  # 5 meters
        unit = "meters"
        
        scale_factor = self.image_processor.scale_converter.set_scale(
            image_id, pixel_length, real_length, unit
        )
        
        # Test conversion from pixels to real-world units
        real_world_length = self.image_processor.scale_converter.pixels_to_real_world(
            image_id, 200, "meters"
        )
        
        # 200 pixels should be 10 meters (twice the scale reference)
        self.assertAlmostEqual(real_world_length, 10.0, places=2)
        
        # Test conversion from real-world units to pixels
        pixels = self.image_processor.scale_converter.real_world_to_pixels(
            image_id, 15.0, "meters"
        )
        
        # 15 meters should be 300 pixels
        self.assertAlmostEqual(pixels, 300.0, places=2)

class TestReconstructionModule(unittest.TestCase):
    """Test cases for the 3D reconstruction module."""
    
    def setUp(self):
        """Set up test environment."""
        self.reconstructor = BuildingReconstructor()
        self.coordinator = ReconstructionCoordinator()
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'reconstruction')
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_reconstructor_initialization(self):
        """Test that the reconstructor initializes correctly."""
        self.assertIsNotNone(self.reconstructor)
        self.assertIsNotNone(self.coordinator)
    
    def test_building_outline_extraction(self):
        """Test building outline extraction."""
        # Create a simple floor plan with walls
        floor_plan = {
            'features': {
                'walls': [
                    {
                        'points': [(0, 0), (10, 0)],
                        'length': 10.0
                    },
                    {
                        'points': [(10, 0), (10, 8)],
                        'length': 8.0
                    },
                    {
                        'points': [(10, 8), (0, 8)],
                        'length': 10.0
                    },
                    {
                        'points': [(0, 8), (0, 0)],
                        'length': 8.0
                    }
                ]
            }
        }
        
        # Extract building outline
        outline = self.reconstructor._extract_building_outline([floor_plan])
        
        # Check that outline was extracted
        self.assertIsNotNone(outline)
        self.assertIn('exterior_walls', outline)
        
        # Check that the outline has at least one wall
        self.assertGreaterEqual(len(outline['exterior_walls']), 1)

class TestGbXMLModule(unittest.TestCase):
    """Test cases for the gbXML conversion module."""
    
    def setUp(self):
        """Set up test environment."""
        self.converter = GbXMLConverter()
        self.manager = GbXMLManager()
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'gbxml')
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_converter_initialization(self):
        """Test that the converter initializes correctly."""
        self.assertIsNotNone(self.converter)
        self.assertIsNotNone(self.manager)
    
    def test_sample_gbxml_generation(self):
        """Test generation of a sample gbXML file."""
        output_path = os.path.join(self.test_output_dir, 'sample.gbxml')
        
        # Generate sample gbXML
        result_path = self.manager.generate_sample_gbxml(output_path)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(result_path))
        
        # Check that the file has content
        with open(result_path, 'r') as f:
            content = f.read()
            self.assertGreater(len(content), 0)
            
            # Check for key gbXML elements
            self.assertIn('<gbXML', content)
            self.assertIn('<Campus', content)
            self.assertIn('<Building', content)
            self.assertIn('<Surface', content)

class TestIntegration(unittest.TestCase):
    """Integration tests for the entire application workflow."""
    
    def setUp(self):
        """Set up test environment."""
        self.image_processor = ImageProcessor()
        self.coordinator = ReconstructionCoordinator()
        self.gbxml_manager = GbXMLManager()
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'output', 'integration')
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_end_to_end_workflow(self):
        """Test the end-to-end workflow with mock data."""
        # Create mock floor plan data
        floor_plan_data = {
            'image_id': 'floor_plan_1',
            'file_path': 'mock_floor_plan.png',
            'features': {
                'walls': [
                    {
                        'type': 'wall',
                        'points': [(0, 0), (10, 0)],
                        'length': 10.0,
                        'thickness': 0.3
                    },
                    {
                        'type': 'wall',
                        'points': [(10, 0), (10, 8)],
                        'length': 8.0,
                        'thickness': 0.3
                    },
                    {
                        'type': 'wall',
                        'points': [(10, 8), (0, 8)],
                        'length': 10.0,
                        'thickness': 0.3
                    },
                    {
                        'type': 'wall',
                        'points': [(0, 8), (0, 0)],
                        'length': 8.0,
                        'thickness': 0.3
                    }
                ],
                'windows': [
                    {
                        'type': 'window',
                        'points': [(2, 0), (4, 0), (4, 1.5), (2, 1.5)],
                        'width': 2.0,
                        'height': 1.5
                    }
                ],
                'doors': [
                    {
                        'type': 'door',
                        'door_type': 'standard',
                        'points': [(7, 0), (8, 0)],
                        'length': 1.0
                    }
                ],
                'rooms': [
                    {
                        'type': 'room',
                        'points': [(0.3, 0.3), (9.7, 0.3), (9.7, 7.7), (0.3, 7.7)],
                        'area': 72.0,
                        'centroid': (5.0, 4.0)
                    }
                ]
            },
            'floor_plan_data': {
                'level': 0
            }
        }
        
        # Create mock elevation data
        elevation_data = {
            'image_id': 'elevation_1',
            'file_path': 'mock_elevation.png',
            'features': {
                'walls': [
                    {
                        'type': 'wall',
                        'points': [(0, 0), (10, 0)],
                        'length': 10.0,
                        'thickness': 0.3
                    }
                ]
            },
            'elevation_data': {
                'floor_levels': [
                    {
                        'type': 'floor_level',
                        'y_position': 0.0,
                        'points': [(0, 0), (10, 0)],
                        'length': 10.0
                    },
                    {
                        'type': 'floor_level',
                        'y_position': 3.0,
                        'points': [(0, 3), (10, 3)],
                        'length': 10.0
                    }
                ],
                'orientation': 'north'
            }
        }
        
        # Save mock data to files
        floor_plan_path = os.path.join(self.test_output_dir, 'floor_plan.json')
        with open(floor_plan_path, 'w') as f:
            json.dump(floor_plan_data, f)
            
        elevation_path = os.path.join(self.test_output_dir, 'elevation.json')
        with open(elevation_path, 'w') as f:
            json.dump(elevation_data, f)
        
        # Test reconstruction from mock data
        try:
            result = self.coordinator.process_building(
                [floor_plan_path], [elevation_path], output_dir=self.test_output_dir
            )
            
            # Check that reconstruction produced output
            self.assertIsNotNone(result)
            
            # Check for output files
            model_json_path = os.path.join(self.test_output_dir, 'building_model.json')
            self.assertTrue(os.path.exists(model_json_path))
            
            # Test gbXML conversion
            gbxml_path = os.path.join(self.test_output_dir, 'building_model.gbxml')
            self.gbxml_manager.convert_building_model(model_json_path, self.test_output_dir)
            
            # Check that gbXML file was created
            self.assertTrue(os.path.exists(gbxml_path))
            
        except Exception as e:
            self.fail(f"Integration test failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
