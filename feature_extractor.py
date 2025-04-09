import numpy as np
import cv2
from skimage import measure, segmentation

class FeatureExtractor:
    """
    Class for extracting architectural features from building plans.
    """
    
    def __init__(self):
        """Initialize the feature extractor."""
        pass
    
    def extract_features(self, image, detected_elements=None):
        """
        Extract architectural features from an image.
        
        Args:
            image: Input image (numpy array)
            detected_elements: Optional dictionary of pre-detected elements
            
        Returns:
            dict: Extracted features
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # If no pre-detected elements, detect them now
        if detected_elements is None:
            from edge_detector import EdgeDetector
            edge_detector = EdgeDetector()
            detected_elements = edge_detector.detect_architectural_elements(gray)
        
        # Extract features for each element type
        features = {}
        
        # Process walls
        if 'walls' in detected_elements:
            features['walls'] = self._process_walls(detected_elements['walls'], gray)
            
        # Process windows
        if 'windows' in detected_elements:
            features['windows'] = self._process_windows(detected_elements['windows'], gray)
            
        # Process doors
        if 'doors' in detected_elements:
            features['doors'] = self._process_doors(detected_elements['doors'], gray)
            
        # Extract room boundaries
        features['rooms'] = self._extract_rooms(gray, detected_elements)
        
        return features
    
    def _process_walls(self, walls, image):
        """
        Process detected walls to extract additional features.
        
        Args:
            walls: List of detected wall lines
            image: Grayscale image
            
        Returns:
            list: Processed wall features
        """
        processed_walls = []
        
        for wall in walls:
            # Get wall points
            points = wall['points']
            p1, p2 = points
            
            # Calculate wall thickness by analyzing perpendicular profile
            thickness = self._estimate_wall_thickness(image, p1, p2)
            
            # Calculate wall orientation (angle in degrees)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            angle = np.degrees(np.arctan2(dy, dx)) % 180
            
            # Determine if wall is horizontal, vertical, or diagonal
            orientation = 'horizontal' if 0 <= angle < 45 or 135 <= angle < 180 else 'vertical'
            if 45 <= angle < 135:
                orientation = 'diagonal'
                
            # Create enhanced wall feature
            enhanced_wall = {
                'type': 'wall',
                'points': points,
                'length': wall['length'],
                'thickness': thickness,
                'angle': angle,
                'orientation': orientation
            }
            
            processed_walls.append(enhanced_wall)
            
        return processed_walls
    
    def _estimate_wall_thickness(self, image, p1, p2, sample_points=5):
        """
        Estimate wall thickness by analyzing perpendicular profiles.
        
        Args:
            image: Grayscale image
            p1, p2: Wall endpoints
            sample_points: Number of points to sample along the wall
            
        Returns:
            float: Estimated wall thickness in pixels
        """
        # Calculate wall direction vector
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = np.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return 1.0  # Default thickness for point
            
        # Normalize direction vector
        dx /= length
        dy /= length
        
        # Calculate perpendicular direction
        perp_dx = -dy
        perp_dy = dx
        
        thicknesses = []
        
        # Sample points along the wall
        for i in range(sample_points):
            # Calculate sample point
            t = i / (sample_points - 1) if sample_points > 1 else 0.5
            sample_x = int(p1[0] + t * (p2[0] - p1[0]))
            sample_y = int(p1[1] + t * (p2[1] - p1[1]))
            
            # Skip if out of bounds
            if (sample_x < 0 or sample_x >= image.shape[1] or 
                sample_y < 0 or sample_y >= image.shape[0]):
                continue
                
            # Sample perpendicular profile
            profile = []
            max_dist = 20  # Maximum distance to check
            
            for d in range(-max_dist, max_dist + 1):
                x = int(sample_x + d * perp_dx)
                y = int(sample_y + d * perp_dy)
                
                # Skip if out of bounds
                if (x < 0 or x >= image.shape[1] or 
                    y < 0 or y >= image.shape[0]):
                    continue
                    
                profile.append(image[y, x])
                
            # Estimate thickness from profile
            if profile:
                # Convert to numpy array
                profile = np.array(profile)
                
                # Threshold profile
                threshold = 128
                binary_profile = (profile < threshold).astype(np.uint8) * 255
                
                # Find transitions
                transitions = np.diff(binary_profile)
                transition_indices = np.where(transitions != 0)[0]
                
                if len(transition_indices) >= 2:
                    # Estimate thickness as distance between first and last transition
                    thickness = transition_indices[-1] - transition_indices[0]
                    thicknesses.append(thickness)
        
        # Return average thickness
        return np.mean(thicknesses) if thicknesses else 1.0
    
    def _process_windows(self, windows, image):
        """
        Process detected windows to extract additional features.
        
        Args:
            windows: List of detected window rectangles
            image: Grayscale image
            
        Returns:
            list: Processed window features
        """
        processed_windows = []
        
        for window in windows:
            # Get window points
            points = window['points']
            
            # Calculate window area
            width = window['width']
            height = window['height']
            area = width * height
            
            # Calculate aspect ratio
            aspect_ratio = width / height if height > 0 else 0
            
            # Determine window type based on aspect ratio and size
            window_type = 'standard'
            if aspect_ratio > 2:
                window_type = 'horizontal'
            elif aspect_ratio < 0.5:
                window_type = 'vertical'
            elif area > 10000:  # Large window
                window_type = 'picture'
                
            # Create enhanced window feature
            enhanced_window = {
                'type': 'window',
                'points': points,
                'width': width,
                'height': height,
                'area': area,
                'aspect_ratio': aspect_ratio,
                'window_type': window_type
            }
            
            processed_windows.append(enhanced_window)
            
        return processed_windows
    
    def _process_doors(self, doors, image):
        """
        Process detected doors to extract additional features.
        
        Args:
            doors: List of detected door elements
            image: Grayscale image
            
        Returns:
            list: Processed door features
        """
        processed_doors = []
        
        for door in doors:
            door_type = door['type']
            
            if door_type == 'door_arc':
                # Arc-type door (swing door)
                center = door['center']
                radius = door['radius']
                
                # Create enhanced door feature
                enhanced_door = {
                    'type': 'door',
                    'door_type': 'swing',
                    'center': center,
                    'radius': radius,
                    'swing_angle': 90  # Default swing angle
                }
                
                processed_doors.append(enhanced_door)
                
            elif door_type == 'door_line':
                # Line-type door
                points = door['points']
                length = door['length']
                angle = door['angle']
                
                # Determine door type based on angle and length
                door_subtype = 'standard'
                if length > 80:
                    door_subtype = 'double'
                    
                # Create enhanced door feature
                enhanced_door = {
                    'type': 'door',
                    'door_type': door_subtype,
                    'points': points,
                    'length': length,
                    'angle': angle
                }
                
                processed_doors.append(enhanced_door)
                
        return processed_doors
    
    def _extract_rooms(self, image, detected_elements):
        """
        Extract room boundaries from the image.
        
        Args:
            image: Grayscale image
            detected_elements: Dictionary of detected architectural elements
            
        Returns:
            list: Extracted room features
        """
        # Create a binary image highlighting walls
        binary = np.zeros_like(image)
        
        # Draw walls
        if 'walls' in detected_elements:
            for wall in detected_elements['walls']:
                p1, p2 = wall['points']
                cv2.line(binary, p1, p2, 255, 2)
        
        # Apply morphological operations to close gaps
        kernel = np.ones((5, 5), np.uint8)
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Invert the image (rooms are now black)
        inverted = cv2.bitwise_not(closed)
        
        # Apply watershed segmentation to find rooms
        distance = cv2.distanceTransform(inverted, cv2.DIST_L2, 5)
        _, markers = cv2.connectedComponents(np.uint8(distance > 0.5 * distance.max()))
        
        # Apply watershed
        markers = markers + 1
        markers[closed > 0] = 0
        segmented = segmentation.watershed(-distance, markers)
        
        # Extract room contours
        rooms = []
        
        for label in range(2, np.max(segmented) + 1):
            # Create mask for this room
            room_mask = np.zeros_like(image, dtype=np.uint8)
            room_mask[segmented == label] = 255
            
            # Find contours
            contours = measure.find_contours(room_mask, 0.5)
            
            if contours:
                # Get the largest contour
                largest_contour = max(contours, key=len)
                
                # Convert to the format we need
                points = [(int(x), int(y)) for y, x in largest_contour]
                
                # Calculate area
                area = cv2.contourArea(np.array(points).reshape(-1, 1, 2))
                
                # Skip very small areas (likely noise)
                if area < 1000:
                    continue
                    
                # Calculate centroid
                M = cv2.moments(np.array(points).reshape(-1, 1, 2))
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    centroid = (cx, cy)
                else:
                    centroid = (0, 0)
                
                # Create room feature
                room = {
                    'type': 'room',
                    'points': points,
                    'area': area,
                    'centroid': centroid,
                    'label': label
                }
                
                rooms.append(room)
        
        return rooms
