import os
import numpy as np
import cv2
from pdf_to_vector import PDFToVectorConverter
from edge_detector import EdgeDetector
from feature_extractor import FeatureExtractor
from scale_converter import ScaleConverter

class ImageProcessor:
    """
    Main class for the image processing module that coordinates the entire workflow.
    """
    
    def __init__(self):
        """Initialize the image processor with its component modules."""
        self.pdf_converter = PDFToVectorConverter()
        self.edge_detector = EdgeDetector()
        self.feature_extractor = FeatureExtractor()
        self.scale_converter = ScaleConverter()
        
    def process_building_plan(self, file_path, scale_info=None, output_dir=None, output_unit='meters'):
        """
        Process a building plan image or PDF.
        
        Args:
            file_path: Path to the image or PDF file
            scale_info: Dictionary with scale information (points and real-world length)
            output_dir: Directory to save output files
            output_unit: Desired output unit for measurements
            
        Returns:
            dict: Processed building plan data with extracted features
        """
        # Create output directory if needed
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Generate a unique ID for this image
        image_id = os.path.basename(file_path)
        
        # Step 1: Convert PDF to vector or load image
        if file_path.lower().endswith('.pdf'):
            vector_data = self.pdf_converter.convert_pdf_to_vector(file_path, output_dir)
            # For simplicity, we'll use the first page
            page_key = list(vector_data.keys())[0]
            vector_data = vector_data[page_key]
            
            # Create an image from vector data for further processing
            width, height = int(vector_data['width']), int(vector_data['height'])
            image = np.ones((height, width), dtype=np.uint8) * 255
            
            # Draw paths on the image
            for path in vector_data['paths']:
                if 'points' in path:
                    points = np.array(path['points'], dtype=np.int32).reshape((-1, 1, 2))
                    cv2.polylines(image, [points], path.get('closed', False), 0, 1)
        else:
            # Load image directly
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Failed to load image: {file_path}")
                
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
                
            # Create basic vector data
            vector_data = {
                'width': image.shape[1],
                'height': image.shape[0],
                'paths': []
            }
            
            # Find contours for basic vector representation
            edges = self.edge_detector.detect_edges(gray)
            contours = measure.find_contours(edges, 0.5)
            
            for contour in contours:
                points = [(float(x), float(y)) for y, x in contour]
                if len(points) >= 5:
                    path = {
                        'type': 'contour',
                        'points': points,
                        'closed': np.allclose(points[0], points[-1])
                    }
                    vector_data['paths'].append(path)
        
        # Step 2: Set scale if provided
        if scale_info:
            if 'points' in scale_info:
                point1, point2 = scale_info['points']
                real_length = scale_info['real_length']
                unit = scale_info.get('unit', 'meters')
                self.scale_converter.set_scale_from_points(image_id, point1, point2, real_length, unit)
            elif 'pixel_length' in scale_info:
                pixel_length = scale_info['pixel_length']
                real_length = scale_info['real_length']
                unit = scale_info.get('unit', 'meters')
                self.scale_converter.set_scale(image_id, pixel_length, real_length, unit)
        
        # Step 3: Detect edges and architectural elements
        detected_elements = self.edge_detector.detect_architectural_elements(image)
        
        # Step 4: Extract features
        features = self.feature_extractor.extract_features(image, detected_elements)
        
        # Step 5: Apply scale conversion if scale is set
        if image_id in self.scale_converter.scale_factors:
            scaled_features = self.scale_converter.apply_scale_to_features(
                image_id, features, output_unit
            )
        else:
            scaled_features = features
            
        # Prepare result
        result = {
            'image_id': image_id,
            'file_path': file_path,
            'vector_data': vector_data,
            'features': scaled_features
        }
        
        # Add scale information if available
        if image_id in self.scale_converter.scale_factors:
            result['scale_info'] = self.scale_converter.get_scale_info(image_id)
            
        # Save result to file if output_dir is provided
        if output_dir:
            import json
            
            # Helper function to make JSON serializable
            def convert_for_json(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_for_json(i) for i in obj]
                else:
                    return obj
            
            output_path = os.path.join(output_dir, f"{os.path.basename(file_path)}_processed.json")
            with open(output_path, 'w') as f:
                json.dump(convert_for_json(result), f, indent=2)
                
        return result
    
    def process_elevation_view(self, file_path, scale_info=None, output_dir=None, output_unit='meters'):
        """
        Process an elevation view image or PDF.
        
        Args:
            file_path: Path to the image or PDF file
            scale_info: Dictionary with scale information
            output_dir: Directory to save output files
            output_unit: Desired output unit for measurements
            
        Returns:
            dict: Processed elevation data with extracted features
        """
        # Process using the general method first
        result = self.process_building_plan(file_path, scale_info, output_dir, output_unit)
        
        # Add elevation-specific processing
        # For elevation views, we're particularly interested in:
        # 1. Detecting the building outline
        # 2. Identifying floors/levels
        # 3. Detecting windows and doors on the facade
        
        # Load or reuse the image
        if 'image' in locals():
            pass  # Use the image already loaded
        else:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Failed to load image: {file_path}")
                
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
        
        # Detect horizontal lines (potential floor levels)
        _, lines = self.edge_detector._hough_line_detection(
            gray, threshold=50, min_line_length=100, max_line_gap=10
        )
        
        floor_levels = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Calculate line angle
                angle = np.degrees(np.arctan2(y2 - y1, x2 - x1)) % 180
                
                # Consider horizontal lines (with some tolerance)
                if abs(angle) < 10 or abs(angle - 180) < 10:
                    # Calculate average y-coordinate
                    y_avg = (y1 + y2) / 2
                    
                    floor_levels.append({
                        'type': 'floor_level',
                        'y_position': y_avg,
                        'points': [(x1, y1), (x2, y2)],
                        'length': np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    })
        
        # Sort floor levels by y-position (top to bottom)
        floor_levels.sort(key=lambda x: x['y_position'])
        
        # Apply scale conversion if scale is set
        image_id = os.path.basename(file_path)
        if image_id in self.scale_converter.scale_factors:
            for level in floor_levels:
                level['points'] = [
                    self.scale_converter.pixels_to_real_world(image_id, point, output_unit)
                    for point in level['points']
                ]
                level['length'] = self.scale_converter.pixels_to_real_world(
                    image_id, level['length'], output_unit
                )
                level['y_position'] = self.scale_converter.pixels_to_real_world(
                    image_id, level['y_position'], output_unit
                )
                level['unit'] = output_unit
        
        # Add to result
        result['elevation_data'] = {
            'floor_levels': floor_levels,
            'orientation': 'unknown'  # This would be set based on user input or filename
        }
        
        # Update the output file if needed
        if output_dir:
            import json
            
            # Helper function to make JSON serializable
            def convert_for_json(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_for_json(i) for i in obj]
                else:
                    return obj
            
            output_path = os.path.join(output_dir, f"{os.path.basename(file_path)}_processed.json")
            with open(output_path, 'w') as f:
                json.dump(convert_for_json(result), f, indent=2)
        
        return result
    
    def process_floor_plan(self, file_path, scale_info=None, output_dir=None, output_unit='meters'):
        """
        Process a floor plan image or PDF.
        
        Args:
            file_path: Path to the image or PDF file
            scale_info: Dictionary with scale information
            output_dir: Directory to save output files
            output_unit: Desired output unit for measurements
            
        Returns:
            dict: Processed floor plan data with extracted features
        """
        # Process using the general method first
        result = self.process_building_plan(file_path, scale_info, output_dir, output_unit)
        
        # Add floor plan-specific processing
        # For floor plans, we're particularly interested in:
        # 1. Room boundaries
        # 2. Wall connections
        # 3. Spatial relationships between rooms
        
        # The room information is already extracted by the feature extractor
        rooms = result['features'].get('rooms', [])
        
        # Analyze spatial relationships between rooms
        room_connections = []
        
        for i, room1 in enumerate(rooms):
            for j, room2 in enumerate(rooms):
                if i >= j:  # Skip self-connections and duplicates
                    continue
                
                # Check if rooms share a wall (simplified approach)
                # In a real implementation, this would be more sophisticated
                connected = False
                shared_wall = None
                
                # For demonstration, we'll use a simple distance-based approach
                centroid1 = room1.get('centroid', (0, 0))
                centroid2 = room2.get('centroid', (0, 0))
                
                # Calculate distance between centroids
                distance = np.sqrt(
                    (centroid2[0] - centroid1[0])**2 + 
                    (centroid2[1] - centroid1[1])**2
                )
                
                # If centroids are close enough, consider rooms connected
                # This is a simplification; real implementation would check for shared walls
                if distance < 200:  # Threshold in pixels
                    connected = True
                    
                    # Create a simple representation of the shared wall
                    # In reality, this would be determined by analyzing the actual walls
                    midpoint = (
                        (centroid1[0] + centroid2[0]) / 2,
                        (centroid1[1] + centroid2[1]) / 2
                    )
                    
                    # Apply scale conversion if scale is set
                    image_id = os.path.basename(file_path)
                    if image_id in self.scale_converter.scale_factors:
                        distance = self.scale_converter.pixels_to_real_world(
                            image_id, distance, output_unit
                        )
                        midpoint = self.scale_converter.pixels_to_real_world(
                            image_id, midpoint, output_unit
                        )
                    
                    room_connections.append({
                        'room1_id': room1.get('label', i),
                        'room2_id': room2.get('label', j),
                        'connected': connected,
                        'distance': distance,
                        'midpoint': midpoint,
                        'unit': output_unit if image_id in self.scale_converter.scale_factors else 'pixels'
                    })
        
        # Add to result
        result['floor_plan_data'] = {
            'room_connections': room_connections,
            'level': 0  # This would be set based on user input or filename
        }
        
        # Update the output file if needed
        if output_dir:
            import json
            
            # Helper function to make JSON serializable
            def convert_for_json(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_for_json(i) for i in obj]
                else:
                    return obj
            
            output_path = os.path.join(output_dir, f"{os.path.basename(file_path)}_processed.json")
            with open(output_path, 'w') as f:
                json.dump(convert_for_json(result), f, indent=2)
        
        return result
