import os
import json
import numpy as np
import cv2
from .scale_converter import ScaleConverter

class ImageProcessor:
    """
    Processes building plans to extract architectural features.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        self.scale_converter = ScaleConverter()
    
    def process_building_plan(self, file_path, plan_type='floor_plan', orientation=None, output_dir=None):
        """
        Process a building plan image.
        
        Args:
            file_path (str): Path to the image file
            plan_type (str): Type of plan ('floor_plan' or 'elevation')
            orientation (str, optional): Orientation for elevations ('north', 'east', 'south', 'west')
            output_dir (str, optional): Directory to save output files
            
        Returns:
            dict: Processed data
        """
        # Create a simple mock result for testing
        filename = os.path.basename(file_path)
        image_id = os.path.splitext(filename)[0]
        
        # Mock result data
        result = {
            'image_id': image_id,
            'plan_type': plan_type,
            'orientation': orientation,
            'dimensions': {
                'width': 800,
                'height': 600
            },
            'elements': {
                'walls': [],
                'windows': [],
                'doors': []
            }
        }
        
        # Add mock elements based on plan type
        if plan_type == 'floor_plan':
            # Add mock walls for floor plan
            result['elements']['walls'] = [
                {'id': 'wall1', 'start': [100, 100], 'end': [700, 100], 'thickness': 10},
                {'id': 'wall2', 'start': [700, 100], 'end': [700, 500], 'thickness': 10},
                {'id': 'wall3', 'start': [700, 500], 'end': [100, 500], 'thickness': 10},
                {'id': 'wall4', 'start': [100, 500], 'end': [100, 100], 'thickness': 10}
            ]
            # Add mock windows and doors
            result['elements']['windows'] = [
                {'id': 'window1', 'wall_id': 'wall1', 'position': 300, 'width': 100, 'height': 80}
            ]
            result['elements']['doors'] = [
                {'id': 'door1', 'wall_id': 'wall3', 'position': 400, 'width': 90, 'height': 210}
            ]
        elif plan_type == 'elevation':
            # Add mock elements for elevation
            result['elements']['walls'] = [
                {'id': 'wall1', 'start': [100, 300], 'end': [700, 300], 'height': 300}
            ]
            result['elements']['windows'] = [
                {'id': 'window1', 'position': 300, 'width': 100, 'height': 80, 'sill_height': 100}
            ]
            result['elements']['doors'] = [
                {'id': 'door1', 'position': 500, 'width': 90, 'height': 210}
            ]
        
        return result
