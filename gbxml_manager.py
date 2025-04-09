import os
import json
from gbxml_converter import GbXMLConverter

class GbXMLManager:
    """
    Class for managing the gbXML conversion process.
    """
    
    def __init__(self):
        """Initialize the gbXML manager."""
        self.converter = GbXMLConverter()
        
    def convert_building_model(self, model_data, output_dir=None, building_info=None):
        """
        Convert a building model to gbXML format.
        
        Args:
            model_data: Building model data or path to model file
            output_dir: Directory to save output files
            building_info: Additional building information
            
        Returns:
            str: Path to the generated gbXML file
        """
        # Create output directory if needed
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Load model data if a file path is provided
        if isinstance(model_data, str):
            if model_data.endswith('.json'):
                with open(model_data, 'r') as f:
                    model_data = json.load(f)
        
        # Set default building info if not provided
        if building_info is None:
            building_info = {
                'name': 'Building Model',
                'location_name': 'Unknown Location',
                'latitude': 0.0,
                'longitude': 0.0,
                'elevation': 0.0,
                'time_zone': 0
            }
        
        # Set output path
        if output_dir:
            output_path = os.path.join(output_dir, "building_model.gbxml")
        else:
            output_path = "building_model.gbxml"
        
        # Convert to gbXML
        gbxml_content = self.converter.convert_to_gbxml(model_data, output_path, building_info)
        
        return output_path
    
    def validate_gbxml(self, gbxml_path, schema_path=None):
        """
        Validate a gbXML file against the schema.
        
        Args:
            gbxml_path: Path to the gbXML file
            schema_path: Path to the gbXML schema file
            
        Returns:
            bool: True if valid, False otherwise
        """
        return self.converter.validate_gbxml(gbxml_path, schema_path)
    
    def extract_building_info(self, model_data):
        """
        Extract building information from model data.
        
        Args:
            model_data: Building model data
            
        Returns:
            dict: Building information
        """
        building_info = {
            'name': 'Building Model',
            'location_name': 'Unknown Location',
            'latitude': 0.0,
            'longitude': 0.0,
            'elevation': 0.0,
            'time_zone': 0
        }
        
        # Extract building name if available
        if 'building_name' in model_data:
            building_info['name'] = model_data['building_name']
        
        # Extract location information if available
        if 'location' in model_data:
            location = model_data['location']
            if 'name' in location:
                building_info['location_name'] = location['name']
            if 'latitude' in location:
                building_info['latitude'] = location['latitude']
            if 'longitude' in location:
                building_info['longitude'] = location['longitude']
            if 'elevation' in location:
                building_info['elevation'] = location['elevation']
            if 'time_zone' in location:
                building_info['time_zone'] = location['time_zone']
        
        return building_info
    
    def generate_sample_gbxml(self, output_path):
        """
        Generate a sample gbXML file for testing.
        
        Args:
            output_path: Path to save the sample gbXML file
            
        Returns:
            str: Path to the generated gbXML file
        """
        # Create a simple building model
        building_model = {
            'floors': [0.0, 3.0, 6.0],  # Ground floor, first floor, second floor
            'walls': [
                {
                    'points': [(0, 0), (10, 0), (10, 8), (0, 8), (0, 0)],
                    'height': 3.0,
                    'base_height': 0.0,
                    'thickness': 0.3
                },
                {
                    'points': [(0, 0), (10, 0), (10, 8), (0, 8), (0, 0)],
                    'height': 3.0,
                    'base_height': 3.0,
                    'thickness': 0.3
                }
            ],
            'openings': [
                {
                    'type': 'window',
                    'position': (2, 0),
                    'width': 1.5,
                    'height': 1.2,
                    'floor': 0
                },
                {
                    'type': 'door',
                    'door_type': 'standard',
                    'position': (5, 0),
                    'width': 1.0,
                    'height': 2.1,
                    'floor': 0
                }
            ],
            'roof': {
                'type': 'flat',
                'outline': [
                    {
                        'points': [(0, 0), (10, 0), (10, 8), (0, 8), (0, 0)]
                    }
                ],
                'height': 0.5
            }
        }
        
        # Set building information
        building_info = {
            'name': 'Sample Building',
            'location_name': 'Sample Location',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'elevation': 10.0,
            'time_zone': -8
        }
        
        # Convert to gbXML
        gbxml_content = self.converter.convert_to_gbxml(building_model, output_path, building_info)
        
        return output_path
