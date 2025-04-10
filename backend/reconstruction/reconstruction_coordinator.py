import os
import numpy as np
import json
import trimesh
from building_reconstructor import BuildingReconstructor

class ReconstructionCoordinator:
    """
    Main class for coordinating the 3D reconstruction process.
    """
    
    def __init__(self):
        """Initialize the reconstruction coordinator."""
        self.reconstructor = BuildingReconstructor()
        
    def process_building(self, floor_plan_files, elevation_files, scale_info=None, output_dir=None):
        """
        Process building plans and create a 3D model.
        
        Args:
            floor_plan_files: List of processed floor plan JSON files
            elevation_files: List of processed elevation JSON files
            scale_info: Dictionary with scale information
            output_dir: Directory to save output files
            
        Returns:
            dict: 3D building model data
        """
        # Create output directory if needed
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Load floor plan data
        floor_plans = []
        for file_path in floor_plan_files:
            try:
                with open(file_path, 'r') as f:
                    floor_plan = json.load(f)
                floor_plans.append(floor_plan)
            except Exception as e:
                print(f"Error loading floor plan {file_path}: {e}")
        
        # Sort floor plans by level (if available)
        floor_plans.sort(key=lambda fp: fp.get('floor_plan_data', {}).get('level', 0), reverse=True)
        
        # Load elevation data
        elevations = []
        for file_path in elevation_files:
            try:
                with open(file_path, 'r') as f:
                    elevation = json.load(f)
                elevations.append(elevation)
            except Exception as e:
                print(f"Error loading elevation {file_path}: {e}")
        
        # Reconstruct the building
        result = self.reconstructor.reconstruct_building(floor_plans, elevations, output_dir)
        
        # Save result to file if output_dir is provided
        if output_dir:
            # Helper function to make JSON serializable
            def convert_for_json(obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items() if k != 'mesh'}
                elif isinstance(obj, list):
                    return [convert_for_json(i) for i in obj]
                else:
                    return obj
            
            output_path = os.path.join(output_dir, "building_model.json")
            with open(output_path, 'w') as f:
                json.dump(convert_for_json(result), f, indent=2)
        
        return result
    
    def visualize_model(self, model_path, output_dir=None):
        """
        Visualize a 3D building model.
        
        Args:
            model_path: Path to the 3D model file (OBJ, STL, etc.)
            output_dir: Directory to save visualization files
            
        Returns:
            bool: Success status
        """
        try:
            # Load the mesh
            mesh = trimesh.load(model_path)
            
            # Create a scene
            scene = trimesh.Scene(mesh)
            
            # Save visualization if output_dir is provided
            if output_dir:
                # Save as PNG
                png_path = os.path.join(output_dir, "building_visualization.png")
                try:
                    # Get a rendering of the scene
                    png = scene.save_image(resolution=[1920, 1080], visible=True)
                    with open(png_path, 'wb') as f:
                        f.write(png)
                    print(f"Visualization saved to {png_path}")
                except Exception as e:
                    print(f"Error saving visualization: {e}")
                
                # Save as HTML (for interactive viewing)
                html_path = os.path.join(output_dir, "building_visualization.html")
                try:
                    # Export as HTML
                    html = trimesh.exchange.html.scene_to_html(scene)
                    with open(html_path, 'w') as f:
                        f.write(html)
                    print(f"Interactive visualization saved to {html_path}")
                except Exception as e:
                    print(f"Error saving HTML visualization: {e}")
            
            return True
        except Exception as e:
            print(f"Error visualizing model: {e}")
            return False
    
    def export_model(self, model_path, output_format, output_dir=None):
        """
        Export a 3D building model to different formats.
        
        Args:
            model_path: Path to the 3D model file
            output_format: Output format ('obj', 'stl', 'glb', etc.)
            output_dir: Directory to save output files
            
        Returns:
            str: Path to the exported file
        """
        try:
            # Load the mesh
            mesh = trimesh.load(model_path)
            
            # Create output directory if needed
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Set output path
            output_path = os.path.join(output_dir or os.path.dirname(model_path),
                                      f"building_model.{output_format}")
            
            # Export to the specified format
            mesh.export(output_path)
            
            print(f"Model exported to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error exporting model: {e}")
            return None
