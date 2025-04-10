import os
import numpy as np
import json
import trimesh
import open3d as o3d

class ModelVisualizer:
    """
    Class for visualizing 3D building models.
    """
    
    def __init__(self):
        """Initialize the model visualizer."""
        pass
    
    def visualize_model(self, model_data, output_dir=None):
        """
        Visualize a 3D building model using Open3D.
        
        Args:
            model_data: Building model data or path to model file
            output_dir: Directory to save visualization files
            
        Returns:
            bool: Success status
        """
        try:
            # Load the model
            if isinstance(model_data, str):
                # Load from file
                if model_data.endswith('.obj'):
                    mesh = trimesh.load(model_data)
                    o3d_mesh = self._trimesh_to_open3d(mesh)
                elif model_data.endswith('.json'):
                    with open(model_data, 'r') as f:
                        model_data = json.load(f)
                    # Extract mesh path
                    mesh_path = model_data.get('mesh_path', '')
                    if mesh_path and os.path.exists(mesh_path):
                        mesh = trimesh.load(mesh_path)
                        o3d_mesh = self._trimesh_to_open3d(mesh)
                    else:
                        # Create mesh from model data
                        o3d_mesh = self._create_mesh_from_model(model_data)
                else:
                    # Try to load with Open3D
                    o3d_mesh = o3d.io.read_triangle_mesh(model_data)
            elif isinstance(model_data, dict) and 'mesh' in model_data:
                # Convert trimesh to Open3D mesh
                o3d_mesh = self._trimesh_to_open3d(model_data['mesh'])
            elif isinstance(model_data, dict):
                # Create mesh from model data
                o3d_mesh = self._create_mesh_from_model(model_data)
            else:
                raise ValueError("Unsupported model data format")
            
            # Ensure mesh has normals
            o3d_mesh.compute_vertex_normals()
            
            # Create a visualization window
            vis = o3d.visualization.Visualizer()
            vis.create_window(window_name="Building Model Visualization", width=1280, height=720)
            
            # Add the mesh to the visualization
            vis.add_geometry(o3d_mesh)
            
            # Set rendering options
            opt = vis.get_render_option()
            opt.background_color = np.array([0.8, 0.8, 0.8])  # Light gray background
            opt.point_size = 5.0
            opt.line_width = 2.0
            
            # Set camera position
            ctr = vis.get_view_control()
            ctr.set_zoom(0.8)
            ctr.set_front([0, -1, 0])
            ctr.set_lookat([0, 0, 0])
            ctr.set_up([0, 0, 1])
            
            # Save screenshot if output_dir is provided
            if output_dir:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Capture and save screenshot
                vis.poll_events()
                vis.update_renderer()
                screenshot_path = os.path.join(output_dir, "building_visualization.png")
                vis.capture_screen_image(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            
            # Run the visualization
            vis.run()
            vis.destroy_window()
            
            return True
        except Exception as e:
            print(f"Error visualizing model: {e}")
            return False
    
    def _trimesh_to_open3d(self, trimesh_mesh):
        """
        Convert a trimesh mesh to an Open3D mesh.
        
        Args:
            trimesh_mesh: Trimesh mesh
            
        Returns:
            open3d.geometry.TriangleMesh: Open3D mesh
        """
        # Create an Open3D mesh
        o3d_mesh = o3d.geometry.TriangleMesh()
        
        # Set vertices and faces
        o3d_mesh.vertices = o3d.utility.Vector3dVector(np.array(trimesh_mesh.vertices))
        o3d_mesh.triangles = o3d.utility.Vector3iVector(np.array(trimesh_mesh.faces))
        
        # Set vertex colors if available
        if hasattr(trimesh_mesh, 'visual') and hasattr(trimesh_mesh.visual, 'vertex_colors'):
            colors = np.array(trimesh_mesh.visual.vertex_colors[:, :3]) / 255.0
            o3d_mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
        
        # Compute normals
        o3d_mesh.compute_vertex_normals()
        
        return o3d_mesh
    
    def _create_mesh_from_model(self, model_data):
        """
        Create an Open3D mesh from model data.
        
        Args:
            model_data: Building model data
            
        Returns:
            open3d.geometry.TriangleMesh: Open3D mesh
        """
        # Create an empty Open3D mesh
        o3d_mesh = o3d.geometry.TriangleMesh()
        
        # Extract building model components
        building_model = model_data.get('building_model', model_data)
        
        # Process walls
        walls = building_model.get('walls', [])
        for wall in walls:
            wall_mesh = self._create_wall_mesh(wall)
            if wall_mesh:
                o3d_mesh += wall_mesh
        
        # Process openings
        openings = building_model.get('openings', [])
        for opening in openings:
            opening_mesh = self._create_opening_mesh(opening)
            if opening_mesh:
                o3d_mesh += opening_mesh
        
        # Process roof
        roof = building_model.get('roof', {})
        floors = building_model.get('floors', [])
        roof_mesh = self._create_roof_mesh(roof, floors)
        if roof_mesh:
            o3d_mesh += roof_mesh
        
        # Compute normals
        o3d_mesh.compute_vertex_normals()
        
        return o3d_mesh
    
    def _create_wall_mesh(self, wall):
        """
        Create an Open3D mesh for a wall.
        
        Args:
            wall: Wall data
            
        Returns:
            open3d.geometry.TriangleMesh: Wall mesh
        """
        # Similar implementation as in BuildingReconstructor._create_wall_mesh
        # but using Open3D instead of trimesh
        points = wall.get('points', [])
        if len(points) < 2:
            return None
            
        height = wall.get('height', 3.0)
        base_height = wall.get('base_height', 0.0)
        thickness = wall.get('thickness', 0.2)
        
        # Create a box for each wall segment
        meshes = []
        
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            
            # Calculate wall length and direction
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = np.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Create a box for this wall segment
                box = o3d.geometry.TriangleMesh.create_box(
                    width=length, height=thickness, depth=height
                )
                
                # Rotate to align with wall direction
                angle = np.arctan2(dy, dx)
                R = o3d.geometry.get_rotation_matrix_from_xyz([0, 0, angle])
                box.rotate(R, center=[0, 0, 0])
                
                # Translate to the correct position
                box.translate([p1[0], p1[1], base_height])
                
                meshes.append(box)
        
        if meshes:
            # Combine all wall segment meshes
            combined_mesh = meshes[0]
            for mesh in meshes[1:]:
                combined_mesh += mesh
            return combined_mesh
        
        return None
    
    def _create_opening_mesh(self, opening):
        """
        Create an Open3D mesh for an opening (window or door).
        
        Args:
            opening: Opening data
            
        Returns:
            open3d.geometry.TriangleMesh: Opening mesh
        """
        # Similar implementation as in BuildingReconstructor._create_opening_mesh
        # but using Open3D instead of trimesh
        opening_type = opening.get('type', '')
        
        if opening_type == 'window':
            # Create window mesh
            position = opening.get('position', (0, 0))
            width = opening.get('width', 1.0)
            height = opening.get('height', 1.0)
            floor = opening.get('floor', 0)
            
            # Create a box for the window
            window_mesh = o3d.geometry.TriangleMesh.create_box(
                width=width, height=0.1, depth=height
            )
            
            # Translate to the correct position
            window_height = floor * 3.0 + 1.0  # Simple height calculation
            window_mesh.translate([position[0], position[1], window_height])
            
            # Set color (blue for windows)
            window_mesh.paint_uniform_color([0.3, 0.5, 0.8])
            
            return window_mesh
            
        elif opening_type == 'door':
            # Create door mesh
            door_type = opening.get('door_type', 'standard')
            
            if door_type == 'swing':
                # Swing door
                position = opening.get('position', (0, 0))
                radius = opening.get('radius', 0.9)
                floor = opening.get('floor', 0)
                
                # Create a cylinder for the door
                door_mesh = o3d.geometry.TriangleMesh.create_cylinder(
                    radius=radius, height=2.0
                )
                
                # Translate to the correct position
                door_height = floor * 3.0  # Simple height calculation
                door_mesh.translate([position[0], position[1], door_height])
                
                # Set color (brown for doors)
                door_mesh.paint_uniform_color([0.6, 0.4, 0.2])
                
                return door_mesh
                
            else:
                # Standard door
                position = opening.get('position', (0, 0))
                width = opening.get('width', 0.9)
                height = opening.get('height', 2.0)
                floor = opening.get('floor', 0)
                
                # Create a box for the door
                door_mesh = o3d.geometry.TriangleMesh.create_box(
                    width=width, height=0.1, depth=height
                )
                
                # Translate to the correct position
                door_height = floor * 3.0  # Simple height calculation
                door_mesh.translate([position[0], position[1], door_height])
                
                # Set color (brown for doors)
                door_mesh.paint_uniform_color([0.6, 0.4, 0.2])
                
                return door_mesh
        
        return None
    
    def _create_roof_mesh(self, roof, floor_heights):
        """
        Create an Open3D mesh for the roof.
        
        Args:
            roof: Roof data
            floor_heights: List of floor heights
            
        Returns:
            open3d.geometry.TriangleMesh: Roof mesh
        """
        # Similar implementation as in BuildingReconstructor._create_roof_mesh
        # but using Open3D instead of trimesh
        roof_type = roof.get('type', 'flat')
        outline = roof.get('outline', [])
        
        if not outline:
            return None
            
        # Get the top floor height
        top_floor_height = floor_heights[0] if floor_heights else 3.0
        
        if roof_type == 'flat':
            # Create a flat roof
            roof_height = roof.get('height', 0.5)
            
            # Get the outline points
            for wall in outline:
                points = wall.get('points', [])
                if points:
                    # For simplicity, create a box based on the bounding box
                    min_x = min(p[0] for p in points)
                    min_y = min(p[1] for p in points)
                    max_x = max(p[0] for p in points)
                    max_y = max(p[1] for p in points)
                    
                    width = max_x - min_x
                    depth = max_y - min_y
                    
                    roof_mesh = o3d.geometry.TriangleMesh.create_box(
                        width=width, height=depth, depth=roof_height
                    )
                    
                    # Translate to the correct position
                    roof_mesh.translate([
                        min_x,
                        min_y,
                        top_floor_height
                    ])
                    
                    # Set color (gray for roof)
                    roof_mesh.paint_uniform_color([0.7, 0.7, 0.7])
                    
                    return roof_mesh
        
        # For other roof types, we would implement specific mesh creation
        # For now, we'll default to a flat roof
        return None
