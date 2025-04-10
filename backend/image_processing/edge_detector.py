import cv2
import numpy as np
from skimage import feature, measure, morphology

class EdgeDetector:
    """
    Class for detecting edges and architectural elements in building plans.
    """
    
    def __init__(self):
        """Initialize the edge detector."""
        pass
    
    def detect_edges(self, image, method='canny', **kwargs):
        """
        Detect edges in an image using various methods.
        
        Args:
            image: Input image (numpy array)
            method (str): Edge detection method ('canny', 'sobel', or 'hough')
            **kwargs: Additional parameters for the specific method
            
        Returns:
            numpy array: Edge image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Apply preprocessing
        gray = self._preprocess_image(gray)
        
        # Apply the selected edge detection method
        if method == 'canny':
            return self._canny_edge_detection(gray, **kwargs)
        elif method == 'sobel':
            return self._sobel_edge_detection(gray, **kwargs)
        elif method == 'hough':
            return self._hough_line_detection(gray, **kwargs)
        else:
            raise ValueError(f"Unsupported edge detection method: {method}")
    
    def _preprocess_image(self, image):
        """
        Preprocess the image for better edge detection.
        
        Args:
            image: Grayscale image
            
        Returns:
            numpy array: Preprocessed image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Apply adaptive thresholding to handle varying lighting
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Remove small noise with morphological operations
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        
        return opening
    
    def _canny_edge_detection(self, image, low_threshold=50, high_threshold=150):
        """
        Apply Canny edge detection.
        
        Args:
            image: Preprocessed grayscale image
            low_threshold: Lower threshold for the hysteresis procedure
            high_threshold: Higher threshold for the hysteresis procedure
            
        Returns:
            numpy array: Edge image
        """
        return cv2.Canny(image, low_threshold, high_threshold)
    
    def _sobel_edge_detection(self, image, ksize=3):
        """
        Apply Sobel edge detection.
        
        Args:
            image: Preprocessed grayscale image
            ksize: Size of the Sobel kernel
            
        Returns:
            numpy array: Edge image
        """
        # Compute gradients in x and y directions
        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
        
        # Compute gradient magnitude
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize and convert to uint8
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Apply threshold to get binary edge image
        _, edges = cv2.threshold(magnitude, 50, 255, cv2.THRESH_BINARY)
        
        return edges
    
    def _hough_line_detection(self, image, rho=1, theta=np.pi/180, threshold=100, 
                             min_line_length=100, max_line_gap=10):
        """
        Apply Hough line detection.
        
        Args:
            image: Preprocessed grayscale image
            rho: Distance resolution in pixels
            theta: Angle resolution in radians
            threshold: Minimum number of votes
            min_line_length: Minimum line length
            max_line_gap: Maximum allowed gap between line segments
            
        Returns:
            tuple: (edge image, detected lines)
        """
        # Apply Canny edge detection first
        edges = cv2.Canny(image, 50, 150)
        
        # Apply Hough Line Transform
        lines = cv2.HoughLinesP(
            edges, rho, theta, threshold, 
            minLineLength=min_line_length, 
            maxLineGap=max_line_gap
        )
        
        # Create an image with the detected lines
        line_image = np.zeros_like(image)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), 255, 2)
        
        return edges, lines
    
    def detect_architectural_elements(self, image, element_type='all'):
        """
        Detect specific architectural elements in building plans.
        
        Args:
            image: Input image (numpy array)
            element_type (str): Type of element to detect ('walls', 'windows', 'doors', or 'all')
            
        Returns:
            dict: Detected elements
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Preprocess the image
        preprocessed = self._preprocess_image(gray)
        
        # Detect edges
        edges = self._canny_edge_detection(preprocessed)
        
        result = {}
        
        # Detect walls (thick lines)
        if element_type in ['walls', 'all']:
            walls = self._detect_walls(edges, preprocessed)
            result['walls'] = walls
            
        # Detect windows (usually double lines or dashed lines)
        if element_type in ['windows', 'all']:
            windows = self._detect_windows(edges, preprocessed)
            result['windows'] = windows
            
        # Detect doors (usually arcs or lines with specific patterns)
        if element_type in ['doors', 'all']:
            doors = self._detect_doors(edges, preprocessed)
            result['doors'] = doors
            
        return result
    
    def _detect_walls(self, edges, original):
        """
        Detect walls in building plans.
        
        Args:
            edges: Edge image
            original: Original preprocessed image
            
        Returns:
            list: Detected wall lines
        """
        # Apply morphological operations to enhance wall lines
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Apply Hough Line Transform to detect straight lines
        _, lines = self._hough_line_detection(
            dilated, threshold=50, min_line_length=50, max_line_gap=10
        )
        
        walls = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Calculate line length
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Filter out short lines
                if length > 50:
                    walls.append({
                        'type': 'wall',
                        'points': [(x1, y1), (x2, y2)],
                        'length': length
                    })
        
        return walls
    
    def _detect_windows(self, edges, original):
        """
        Detect windows in building plans.
        
        Args:
            edges: Edge image
            original: Original preprocessed image
            
        Returns:
            list: Detected window rectangles
        """
        # Windows are often represented as rectangles with thin lines
        # Apply morphological operations to isolate potential window patterns
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(edges, kernel, iterations=1)
        
        # Find contours
        contours = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        windows = []
        for contour in contours:
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Windows are typically rectangular with 4 vertices
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                
                # Filter based on aspect ratio and size
                aspect_ratio = float(w) / h
                if 0.5 < aspect_ratio < 4 and 20 < w < 200 and 20 < h < 200:
                    windows.append({
                        'type': 'window',
                        'points': [(x, y), (x+w, y), (x+w, y+h), (x, y+h)],
                        'width': w,
                        'height': h
                    })
        
        return windows
    
    def _detect_doors(self, edges, original):
        """
        Detect doors in building plans.
        
        Args:
            edges: Edge image
            original: Original preprocessed image
            
        Returns:
            list: Detected door arcs and lines
        """
        # Doors often have distinctive arc patterns
        # Apply Hough Circle Transform to detect arcs
        circles = cv2.HoughCircles(
            original, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
            param1=50, param2=30, minRadius=10, maxRadius=30
        )
        
        doors = []
        
        # Process detected circles (door arcs)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                center_x, center_y, radius = circle
                doors.append({
                    'type': 'door_arc',
                    'center': (int(center_x), int(center_y)),
                    'radius': int(radius)
                })
        
        # Also look for specific line patterns that might represent doors
        _, lines = self._hough_line_detection(
            edges, threshold=30, min_line_length=30, max_line_gap=5
        )
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Calculate line length
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Filter for potential door lines (typically shorter than walls)
                if 30 < length < 100:
                    # Check if there's a perpendicular line nearby (door frame)
                    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                    
                    # Add as potential door
                    doors.append({
                        'type': 'door_line',
                        'points': [(x1, y1), (x2, y2)],
                        'length': length,
                        'angle': angle
                    })
        
        return doors
