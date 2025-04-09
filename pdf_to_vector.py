import os
import fitz  # PyMuPDF
import numpy as np
import cv2
from skimage import measure

class PDFToVectorConverter:
    """
    Class for converting PDF drawings to vector format.
    Extracts vector graphics when available or processes raster images.
    """
    
    def __init__(self):
        """Initialize the converter."""
        pass
    
    def convert_pdf_to_vector(self, pdf_path, output_dir=None):
        """
        Convert a PDF file to vector format.
        
        Args:
            pdf_path (str): Path to the PDF file
            output_dir (str, optional): Directory to save output files
            
        Returns:
            dict: Dictionary containing vector data for each page
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        result = {}
        
        # Process each page
        for page_num, page in enumerate(doc):
            page_vectors = self._process_page(page, page_num)
            result[f"page_{page_num}"] = page_vectors
            
            # Save to file if output_dir is provided
            if output_dir:
                output_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_page_{page_num}.json")
                self._save_vectors_to_file(page_vectors, output_path)
                
        return result
    
    def _process_page(self, page, page_num):
        """
        Process a single PDF page to extract vector data.
        
        Args:
            page: PyMuPDF page object
            page_num (int): Page number
            
        Returns:
            dict: Vector data for the page
        """
        # Try to extract vector graphics directly
        paths = self._extract_vector_paths(page)
        
        # If no vector paths found, process as raster image
        if not paths:
            paths = self._process_raster_page(page)
            
        return {
            "page_number": page_num,
            "width": page.rect.width,
            "height": page.rect.height,
            "paths": paths
        }
    
    def _extract_vector_paths(self, page):
        """
        Extract vector paths directly from PDF page.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            list: List of path dictionaries
        """
        paths = []
        
        # Get the page's display list
        dl = page.get_displaylist()
        
        # Convert display list to a list of paths
        for item in dl:
            if item[0] == "f" or item[0] == "s":  # fill or stroke path
                path_data = item[1]
                if isinstance(path_data, list) and len(path_data) > 0:
                    path = {
                        "type": "vector",
                        "stroke": item[0] == "s",
                        "fill": item[0] == "f",
                        "points": path_data,
                        "color": item[2] if len(item) > 2 else None
                    }
                    paths.append(path)
        
        return paths
    
    def _process_raster_page(self, page):
        """
        Process page as raster image when vector data is not available.
        
        Args:
            page: PyMuPDF page object
            
        Returns:
            list: List of detected contours as paths
        """
        # Render page to an image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        
        # Convert to grayscale if needed
        if pix.n == 4:  # RGBA
            gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        elif pix.n == 3:  # RGB
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img
            
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours = measure.find_contours(edges, 0.5)
        
        paths = []
        for contour in contours:
            # Convert to the format we need
            points = [(float(x), float(y)) for y, x in contour]
            
            # Skip very small contours (likely noise)
            if len(points) < 5:
                continue
                
            path = {
                "type": "contour",
                "points": points,
                "closed": np.allclose(points[0], points[-1])
            }
            paths.append(path)
            
        return paths
    
    def _save_vectors_to_file(self, vectors, output_path):
        """
        Save vector data to a JSON file.
        
        Args:
            vectors (dict): Vector data
            output_path (str): Path to save the JSON file
        """
        import json
        
        # Convert numpy arrays to lists for JSON serialization
        def convert_for_json(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_for_json(i) for i in obj]
            else:
                return obj
        
        json_data = convert_for_json(vectors)
        
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)
            
    def convert_image_to_vector(self, image_path, output_dir=None):
        """
        Convert an image file to vector format.
        
        Args:
            image_path (str): Path to the image file
            output_dir (str, optional): Directory to save output files
            
        Returns:
            dict: Dictionary containing vector data
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to read image: {image_path}")
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours = measure.find_contours(edges, 0.5)
        
        paths = []
        for contour in contours:
            # Convert to the format we need
            points = [(float(x), float(y)) for y, x in contour]
            
            # Skip very small contours (likely noise)
            if len(points) < 5:
                continue
                
            path = {
                "type": "contour",
                "points": points,
                "closed": np.allclose(points[0], points[-1])
            }
            paths.append(path)
            
        result = {
            "width": img.shape[1],
            "height": img.shape[0],
            "paths": paths
        }
        
        # Save to file if output_dir is provided
        if output_dir:
            output_path = os.path.join(output_dir, f"{os.path.basename(image_path)}.json")
            self._save_vectors_to_file(result, output_path)
            
        return result
