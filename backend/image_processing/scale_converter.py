class ScaleConverter:
    """
    Handles scale conversion between pixels and real-world measurements.
    """
    
    def __init__(self):
        """Initialize the scale converter."""
        self.scales = {}
    
    def set_scale(self, image_id, pixel_length, real_length, unit='meters'):
        """
        Set the scale for an image.
        
        Args:
            image_id (str): ID of the image
            pixel_length (float): Length in pixels
            real_length (float): Length in real-world units
            unit (str): Unit of measurement
            
        Returns:
            float: Scale factor (real-world units per pixel)
        """
        scale_factor = real_length / pixel_length
        
        self.scales[image_id] = {
            'scale_factor': scale_factor,
            'unit': unit
        }
        
        return scale_factor
    
    def get_scale(self, image_id):
        """
        Get the scale for an image.
        
        Args:
            image_id (str): ID of the image
            
        Returns:
            dict: Scale information
        """
        return self.scales.get(image_id, {'scale_factor': 1.0, 'unit': 'meters'})
    
    def pixels_to_real(self, image_id, pixels):
        """
        Convert pixels to real-world units.
        
        Args:
            image_id (str): ID of the image
            pixels (float): Length in pixels
            
        Returns:
            float: Length in real-world units
        """
        scale = self.get_scale(image_id)
        return pixels * scale['scale_factor']
    
    def real_to_pixels(self, image_id, real_length):
        """
        Convert real-world units to pixels.
        
        Args:
            image_id (str): ID of the image
            real_length (float): Length in real-world units
            
        Returns:
            float: Length in pixels
        """
        scale = self.get_scale(image_id)
        return real_length / scale['scale_factor']
