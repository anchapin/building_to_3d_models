import numpy as np
import cv2

class ScaleConverter:
    """
    Class for converting between pixel coordinates and real-world measurements.
    """
    
    def __init__(self):
        """Initialize the scale converter."""
        self.scale_factors = {}  # Dictionary to store scale factors for different images
    
    def set_scale(self, image_id, pixel_length, real_length, unit='meters'):
        """
        Set the scale for an image based on a known dimension.
        
        Args:
            image_id: Identifier for the image
            pixel_length: Length in pixels
            real_length: Length in real-world units
            unit: Unit of measurement ('meters', 'feet', 'inches', 'cm')
            
        Returns:
            float: Scale factor (units per pixel)
        """
        # Convert all measurements to meters internally
        real_length_meters = self._convert_to_meters(real_length, unit)
        
        # Calculate scale factor (meters per pixel)
        scale_factor = real_length_meters / pixel_length
        
        # Store the scale factor
        self.scale_factors[image_id] = {
            'scale_factor': scale_factor,
            'original_unit': unit,
            'pixel_length': pixel_length,
            'real_length': real_length
        }
        
        return scale_factor
    
    def set_scale_from_points(self, image_id, point1, point2, real_length, unit='meters'):
        """
        Set the scale for an image based on two points and a known dimension.
        
        Args:
            image_id: Identifier for the image
            point1: First point (x, y) in pixels
            point2: Second point (x, y) in pixels
            real_length: Length in real-world units
            unit: Unit of measurement ('meters', 'feet', 'inches', 'cm')
            
        Returns:
            float: Scale factor (units per pixel)
        """
        # Calculate pixel distance between points
        pixel_length = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        
        # Set scale using the calculated pixel length
        return self.set_scale(image_id, pixel_length, real_length, unit)
    
    def pixels_to_real_world(self, image_id, pixels, output_unit='meters'):
        """
        Convert pixel measurements to real-world units.
        
        Args:
            image_id: Identifier for the image
            pixels: Length in pixels or coordinates (x, y) in pixels
            output_unit: Desired output unit
            
        Returns:
            float or tuple: Length or coordinates in real-world units
        """
        if image_id not in self.scale_factors:
            raise ValueError(f"No scale factor set for image {image_id}")
            
        scale_factor = self.scale_factors[image_id]['scale_factor']
        
        # Handle different input types
        if isinstance(pixels, (int, float)):
            # Convert single length
            real_world_meters = pixels * scale_factor
            return self._convert_from_meters(real_world_meters, output_unit)
            
        elif isinstance(pixels, (list, tuple)) and len(pixels) == 2:
            # Convert coordinates
            x, y = pixels
            real_x = x * scale_factor
            real_y = y * scale_factor
            
            # Convert to desired output unit
            real_x = self._convert_from_meters(real_x, output_unit)
            real_y = self._convert_from_meters(real_y, output_unit)
            
            return (real_x, real_y)
            
        elif isinstance(pixels, np.ndarray) and pixels.shape[-1] == 2:
            # Convert array of coordinates
            real_world = pixels * scale_factor
            
            # Convert to desired output unit
            conversion_factor = self._get_conversion_factor('meters', output_unit)
            real_world = real_world * conversion_factor
            
            return real_world
            
        else:
            raise ValueError("Unsupported input format for pixels")
    
    def real_world_to_pixels(self, image_id, real_world, input_unit='meters'):
        """
        Convert real-world measurements to pixels.
        
        Args:
            image_id: Identifier for the image
            real_world: Length or coordinates in real-world units
            input_unit: Unit of the input measurement
            
        Returns:
            float or tuple: Length or coordinates in pixels
        """
        if image_id not in self.scale_factors:
            raise ValueError(f"No scale factor set for image {image_id}")
            
        scale_factor = self.scale_factors[image_id]['scale_factor']
        
        # Handle different input types
        if isinstance(real_world, (int, float)):
            # Convert single length
            real_world_meters = self._convert_to_meters(real_world, input_unit)
            return real_world_meters / scale_factor
            
        elif isinstance(real_world, (list, tuple)) and len(real_world) == 2:
            # Convert coordinates
            x, y = real_world
            x_meters = self._convert_to_meters(x, input_unit)
            y_meters = self._convert_to_meters(y, input_unit)
            
            pixel_x = x_meters / scale_factor
            pixel_y = y_meters / scale_factor
            
            return (pixel_x, pixel_y)
            
        elif isinstance(real_world, np.ndarray) and real_world.shape[-1] == 2:
            # Convert array of coordinates
            conversion_factor = self._get_conversion_factor(input_unit, 'meters')
            real_world_meters = real_world * conversion_factor
            
            pixels = real_world_meters / scale_factor
            
            return pixels
            
        else:
            raise ValueError("Unsupported input format for real_world")
    
    def _convert_to_meters(self, length, unit):
        """
        Convert a length from the specified unit to meters.
        
        Args:
            length: Length in the specified unit
            unit: Unit of measurement
            
        Returns:
            float: Length in meters
        """
        if unit == 'meters':
            return length
        elif unit == 'feet':
            return length * 0.3048
        elif unit == 'inches':
            return length * 0.0254
        elif unit == 'cm':
            return length * 0.01
        else:
            raise ValueError(f"Unsupported unit: {unit}")
    
    def _convert_from_meters(self, length_meters, unit):
        """
        Convert a length from meters to the specified unit.
        
        Args:
            length_meters: Length in meters
            unit: Target unit of measurement
            
        Returns:
            float: Length in the specified unit
        """
        if unit == 'meters':
            return length_meters
        elif unit == 'feet':
            return length_meters / 0.3048
        elif unit == 'inches':
            return length_meters / 0.0254
        elif unit == 'cm':
            return length_meters / 0.01
        else:
            raise ValueError(f"Unsupported unit: {unit}")
    
    def _get_conversion_factor(self, from_unit, to_unit):
        """
        Get the conversion factor between two units.
        
        Args:
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            float: Conversion factor
        """
        # Convert to meters first
        meters = self._convert_to_meters(1.0, from_unit)
        
        # Then convert from meters to target unit
        return self._convert_from_meters(meters, to_unit)
    
    def get_scale_info(self, image_id):
        """
        Get scale information for an image.
        
        Args:
            image_id: Identifier for the image
            
        Returns:
            dict: Scale information
        """
        if image_id not in self.scale_factors:
            raise ValueError(f"No scale factor set for image {image_id}")
            
        return self.scale_factors[image_id]
    
    def apply_scale_to_features(self, image_id, features, output_unit='meters'):
        """
        Apply scale conversion to extracted features.
        
        Args:
            image_id: Identifier for the image
            features: Dictionary of extracted features
            output_unit: Desired output unit
            
        Returns:
            dict: Features with real-world measurements
        """
        scaled_features = {}
        
        for feature_type, feature_list in features.items():
            scaled_features[feature_type] = []
            
            for feature in feature_list:
                # Create a copy of the feature
                scaled_feature = feature.copy()
                
                # Convert coordinates
                if 'points' in feature:
                    scaled_feature['points'] = [
                        self.pixels_to_real_world(image_id, point, output_unit)
                        for point in feature['points']
                    ]
                
                # Convert lengths
                for key in ['length', 'width', 'height', 'thickness', 'radius']:
                    if key in feature:
                        scaled_feature[key] = self.pixels_to_real_world(
                            image_id, feature[key], output_unit
                        )
                
                # Convert areas
                if 'area' in feature:
                    # Area conversion requires squaring the scale factor
                    area_pixels = feature['area']
                    scale_factor = self.scale_factors[image_id]['scale_factor']
                    area_meters = area_pixels * (scale_factor ** 2)
                    
                    # Convert to desired output unit
                    if output_unit == 'meters':
                        scaled_feature['area'] = area_meters
                    elif output_unit == 'feet':
                        scaled_feature['area'] = area_meters * 10.7639  # sq meters to sq feet
                    elif output_unit == 'inches':
                        scaled_feature['area'] = area_meters * 1550.0  # sq meters to sq inches
                    elif output_unit == 'cm':
                        scaled_feature['area'] = area_meters * 10000.0  # sq meters to sq cm
                
                # Add unit information
                scaled_feature['unit'] = output_unit
                
                scaled_features[feature_type].append(scaled_feature)
        
        return scaled_features
