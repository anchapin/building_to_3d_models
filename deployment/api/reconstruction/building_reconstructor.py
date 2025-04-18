import os
import numpy as np
import trimesh

# Try to import open3d, but continue if not available
try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False
    print("Warning: open3d not available, some 3D functionality may be limited")

class BuildingReconstructor:
    """
    Class for reconstructing 3D building models from processed floor plans and elevations.
    """
    
    def __init__(self):
        """Initialize the building reconstructor."""
        pass
    
    def reconstruct_building(self, floor_plans, elevations, output_dir=None):
        """
        Reconstruct a 3D building model from floor plans and elevations.
        
        Args:
            floor_plans: List of processed floor plan data (dict per floor)
            elevations: List of processed elevation data (dict per elevation)
            output_dir: Directory to save output files
            
        Returns:
            dict: 3D building model data
        """
        # Create output directory if needed
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Validate input data
        if not floor_plans:
            raise ValueError("At least one floor plan is required")
        if not elevations:
            raise ValueError("At least one elevation is required")
            
        # Extract building outline from floor plans
        building_outline = self._extract_building_outline(floor_plans)
        
        # Extract floor heights from elevations
        floor_heights = self._extract_floor_heights(elevations)
        
        # Create walls from floor plans and heights
        walls = self._create_walls(floor_plans, floor_heights)
        
        # Create openings (windows and doors) from floor plans and elevations
        openings = self._create_openings(floor_plans, elevations)
        
        # Create roof from top floor plan and elevations
        roof = self._create_roof(floor_plans[-1], elevations)
        
        # Combine all elements into a single 3D model
        building_model = {
            'outline': building_outline,
            'floors': floor_heights,
            'walls': walls,
            'openings': openings,
            'roof': roof
        }
        
        # Generate 3D mesh
        mesh = self._generate_mesh(building_model)
        
        # Save mesh if output_dir is provided
        if output_dir:
            mesh_path = os.path.join(output_dir, "building_model.obj")
            mesh.export(mesh_path)
            
        return {
            'building_model': building_model,
            'mesh': mesh
        }
    
    def _extract_building_outline(self, floor_plans):
        """
        Extract the building outline from floor plans.
        
        Args:
            floor_plans: List of processed floor plan data
            
        Returns:
            dict: Building outline data
        """
        # For simplicity, we'll use the outline of the first floor
        # In a real implementation, this would handle multiple floors with different outlines
        first_floor = floor_plans[0]
        
        # Extract walls from the floor plan
        walls = first_floor['features'].get('walls', [])
        
        # Find exterior walls (simplified approach)
        # In a real implementation, this would use more sophisticated algorithms
        # to determine which walls are exterior
        exterior_walls = []
        
        # For now, we'll assume walls that form a closed loop are exterior walls
        # This is a simplification; real implementation would be more complex
        if walls:
            # Sort walls by length (longest first)
            sorted_walls = sorted(walls, key=lambda w: w.get('length', 0), reverse=True)
            
            # Take the top N walls that likely form the building perimeter
            # This is a heuristic approach
            top_walls = sorted_walls[:min(20, len(sorted_walls))]
            
            # Try to form a closed loop
            exterior_walls = self._find_closed_loop(top_walls)
        
        # If no exterior walls found, try using room boundaries
        if not exterior_walls:
            rooms = first_floor['features'].get('rooms', [])
            if rooms:
                # Find the largest room (likely the building outline)
                largest_room = max(rooms, key=lambda r: r.get('area', 0))
                exterior_walls = [{
                    'type': 'exterior_wall',
                    'points': largest_room.get('points', []),
                    'closed': True
                }]
        
        return {
            'exterior_walls': exterior_walls,
            'level': 0
        }
    
    def _find_closed_loop(self, walls):
        """
        Find a closed loop of walls.
        
        Args:
            walls: List of wall features
            
        Returns:
            list: Walls forming a closed loop
        """
        # This is a simplified implementation
        # In a real implementation, this would use graph algorithms
        # to find cycles in the wall graph
        
        # For now, we'll just check if the walls form a single closed polygon
        all_points = []
        for wall in walls:
            points = wall.get('points', [])
            if len(points) >= 2:
                all_points.append(points[0])
                all_points.append(points[1])
        
        # Check if we have enough points
        if len(all_points) < 6:  # Need at least 3 walls (6 points)
            return []
        
        # Try to order the points to form a closed loop
        ordered_points = self._order_points_to_form_polygon(all_points)
        
        if ordered_points:
            return [{
                'type': 'exterior_wall',
                'points': ordered_points,
                'closed': True
            }]
        
        return []
    
    def _order_points_to_form_polygon(self, points):
        """
        Try to order points to form a closed polygon.
        
        Args:
            points: List of points (x, y)
            
        Returns:
            list: Ordered points forming a closed polygon
        """
        # This is a simplified implementation
        # In a real implementation, this would use more sophisticated algorithms
        
        # For now, we'll use a convex hull as a simple approximation
        try:
            # Convert to numpy array
            points_array = np.array(points)
            
            # Use trimesh to compute convex hull
            hull = trimesh.convex.convex_hull(points_array)
            
            # Extract vertices of the hull
            hull_vertices = hull.vertices.tolist()
            
            return hull_vertices
        except Exception:
            # Fallback: return empty list if convex hull fails
            return []
    
    def _extract_floor_heights(self, elevations):
        """
        Extract floor heights from elevations.
        
        Args:
            elevations: List of processed elevation data
            
        Returns:
            list: Floor heights
        """
        floor_heights = []
        
        # Collect floor levels from all elevations
        all_levels = []
        for elevation in elevations:
            elevation_data = elevation.get('elevation_data', {})
            levels = elevation_data.get('floor_levels', [])
            
            for level in levels:
                y_position = level.get('y_position', 0)
                all_levels.append(y_position)
        
        # Sort and remove duplicates
        if all_levels:
            # Sort in descending order (top to bottom)
            all_levels.sort(reverse=True)
            
            # Remove duplicates (with tolerance)
            unique_levels = [all_levels[0]]
            for level in all_levels[1:]:
                # Check if this level is significantly different from the last one
                if abs(level - unique_levels[-1]) > 0.5:  # 0.5 unit tolerance
                    unique_levels.append(level)
            
            # Convert to heights (distance from ground)
            ground_level = unique_levels[-1]
            floor_heights = [level - ground_level for level in unique_levels]
            
            # Ensure ground floor is at height 0
            floor_heights[-1] = 0
        else:
            # Fallback: create default floor heights
            # Assume 3 meters per floor
            num_floors = max(1, len(elevations))
            floor_heights = [i * 3.0 for i in range(num_floors)]
        
        return floor_heights
    
    def _create_walls(self, floor_plans, floor_heights):
        """
        Create 3D walls from floor plans and heights.
        
        Args:
            floor_plans: List of processed floor plan data
            floor_heights: List of floor heights
            
        Returns:
            list: 3D wall data
        """
        walls_3d = []
        
        # Process each floor
        for i, floor_plan in enumerate(floor_plans):
            # Get the height of this floor
            floor_height = floor_heights[i] if i < len(floor_heights) else 0
            
            # Get the height of the next floor (or roof)
            next_height = floor_heights[i-1] if i > 0 else (floor_height + 3.0)  # Default to 3m height
            
            # Calculate wall height
            wall_height = next_height - floor_height
            
            # Get walls from the floor plan
            walls = floor_plan['features'].get('walls', [])
            
            # Create 3D walls
            for wall in walls:
                points = wall.get('points', [])
                if len(points) >= 2:
                    # Create 3D wall
                    wall_3d = {
                        'type': 'wall',
                        'points': points,
                        'height': wall_height,
                        'base_height': floor_height,
                        'thickness': wall.get('thickness', 0.2)  # Default thickness
                    }
                    walls_3d.append(wall_3d)
        
        return walls_3d
    
    def _create_openings(self, floor_plans, elevations):
        """
        Create 3D openings (windows and doors) from floor plans and elevations.
        
        Args:
            floor_plans: List of processed floor plan data
            elevations: List of processed elevation data
            
        Returns:
            list: 3D opening data
        """
        openings_3d = []
        
        # Process windows and doors from floor plans
        for i, floor_plan in enumerate(floor_plans):
            # Get windows from the floor plan
            windows = floor_plan['features'].get('windows', [])
            
            # Create 3D windows
            for window in windows:
                points = window.get('points', [])
                if len(points) >= 4:  # Need at least 4 points for a rectangle
                    # Calculate window position and dimensions
                    min_x = min(p[0] for p in points)
                    min_y = min(p[1] for p in points)
                    max_x = max(p[0] for p in points)
                    max_y = max(p[1] for p in points)
                    
                    width = max_x - min_x
                    height = max_y - min_y
                    
                    # Create 3D window
                    window_3d = {
                        'type': 'window',
                        'position': (min_x, min_y),
                        'width': width,
                        'height': height,
                        'floor': i
                    }
                    openings_3d.append(window_3d)
            
            # Get doors from the floor plan
            doors = floor_plan['features'].get('doors', [])
            
            # Create 3D doors
            for door in doors:
                if door.get('door_type') == 'swing':
                    # Swing door
                    center = door.get('center', (0, 0))
                    radius = door.get('radius', 0)
                    
                    # Create 3D door
                    door_3d = {
                        'type': 'door',
                        'door_type': 'swing',
                        'position': center,
                        'radius': radius,
                        'floor': i
                    }
                    openings_3d.append(door_3d)
                else:
                    # Standard door
                    points = door.get('points', [])
                    if len(points) >= 2:
                        # Calculate door position and dimensions
                        p1, p2 = points[:2]
                        
                        # Create 3D door
                        door_3d = {
                            'type': 'door',
                            'door_type': 'standard',
                            'position': p1,
                            'width': np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2),
                            'height': 2.0,  # Default door height
                            'floor': i
                        }
                        openings_3d.append(door_3d)
        
        # Process windows from elevations
        for elevation in elevations:
            # This would extract windows from elevation views
            # For simplicity, we'll skip this in this implementation
            pass
        
        return openings_3d
    
    def _create_roof(self, top_floor_plan, elevations):
        """
        Create 3D roof from top floor plan and elevations.
        
        Args:
            top_floor_plan: Processed top floor plan data
            elevations: List of processed elevation data
            
        Returns:
            dict: 3D roof data
        """
        # Extract building outline from top floor
        outline = self._extract_building_outline([top_floor_plan])
        exterior_walls = outline.get('exterior_walls', [])
        
        # Default roof type is flat
        roof_type = 'flat'
        roof_height = 0.5  # Default height for flat roof
        
        # Try to determine roof type from elevations
        for elevation in elevations:
            # This would analyze elevation views to determine roof type
            # For simplicity, we'll use a flat roof in this implementation
            pass
        
        # Create roof based on type
        if roof_type == 'flat':
            roof = {
                'type': 'flat',
                'outline': exterior_walls,
                'height': roof_height
            }
        elif roof_type == 'gabled':
            # For a gabled roof, we would need to determine the ridge line
            # For simplicity, we'll use a flat roof
            roof = {
                'type': 'flat',
                'outline': exterior_walls,
                'height': roof_height
            }
        else:
            # Default to flat roof
            roof = {
                'type': 'flat',
                'outline': exterior_walls,
                'height': roof_height
            }
        
        return roof
    
    def _generate_mesh(self, building_model):
        """
        Generate a 3D mesh from the building model.
        
        Args:
            building_model: Building model data
            
        Returns:
            trimesh.Trimesh: 3D mesh
        """
        # Create an empty scene
        scene = trimesh.Scene()
        
        # Add walls
        for wall in building_model['walls']:
            wall_mesh = self._create_wall_mesh(wall)
            if wall_mesh:
                scene.add_geometry(wall_mesh)
        
        # Add openings (windows and doors)
        for opening in building_model['openings']:
            opening_mesh = self._create_opening_mesh(opening)
            if opening_mesh:
                scene.add_geometry(opening_mesh)
        
        # Add roof
        roof_mesh = self._create_roof_mesh(building_model['roof'], building_model['floors'])
        if roof_mesh:
            scene.add_geometry(roof_mesh)
        
        # Export as a single mesh
        mesh = scene.dump(concatenate=True)
        
        return mesh
    
    def _create_wall_mesh(self, wall):
        """
        Create a mesh for a wall.
        
        Args:
            wall: Wall data
            
        Returns:
            trimesh.Trimesh: Wall mesh
        """
        points = wall.get('points', [])
        if len(points) < 2:
            return None
            
        height = wall.get('height', 3.0)
        base_height = wall.get('base_height', 0.0)
        thickness = wall.get('thickness', 0.2)
        
        # Create a path for the wall
        path = np.array(points)
        
        # Create a rectangular cross-section
        # The cross-section is perpendicular to the path
        cross_section = np.array([
            [-thickness/2, 0],
            [thickness/2, 0],
            [thickness/2, height],
            [-thickness/2, height]
        ])
        
        try:
            # Create the wall mesh by extruding the cross-section along the path
            wall_mesh = trimesh.creation.extrude_polygon(
                cross_section=cross_section,
                polygon=path
            )
            
            # Translate to the correct base height
            wall_mesh.apply_translation([0, 0, base_height])
            
            return wall_mesh
        except Exception:
            # Fallback: create a box for each wall segment
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
                    box = trimesh.creation.box(
                        extents=[length, thickness, height]
                    )
                    
                    # Rotate to align with wall direction
                    angle = np.arctan2(dy, dx)
                    rotation = trimesh.transformations.rotation_matrix(
                        angle, [0, 0, 1]
                    )
                    box.apply_transform(rotation)
                    
                    # Translate to the correct position
                    translation = [p1[0], p1[1], base_height]
                    box.apply_translation(translation)
                    
                    meshes.append(box)
            
            if meshes:
                # Combine all wall segment meshes
                wall_mesh = trimesh.util.concatenate(meshes)
                return wall_mesh
            
            return None
    
    def _create_opening_mesh(self, opening):
        """
        Create a mesh for an opening (window or door).
        
        Args:
            opening: Opening data
            
        Returns:
            trimesh.Trimesh: Opening mesh
        """
        opening_type = opening.get('type', '')
        
        if opening_type == 'window':
            # Create window mesh
            position = opening.get('position', (0, 0))
            width = opening.get('width', 1.0)
            height = opening.get('height', 1.0)
            floor = opening.get('floor', 0)
            
            # Create a simple box for the window
            window_mesh = trimesh.creation.box(
                extents=[width, 0.1, height]  # Thin box
            )
            
            # Translate to the correct position
            # Assume windows are 1m above floor level
            window_height = floor * 3.0 + 1.0  # Simple height calculation
            translation = [position[0], position[1], window_height]
            window_mesh.apply_translation(translation)
            
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
                door_mesh = trimesh.creation.cylinder(
                    radius=radius,
                    height=2.0  # Standard door height
                )
                
                # Translate to the correct position
                door_height = floor * 3.0  # Simple height calculation
                translation = [position[0], position[1], door_height]
                door_mesh.apply_translation(translation)
                
                return door_mesh
                
            else:
                # Standard door
                position = opening.get('position', (0, 0))
                width = opening.get('width', 0.9)
                height = opening.get('height', 2.0)
                floor = opening.get('floor', 0)
                
                # Create a simple box for the door
                door_mesh = trimesh.creation.box(
                    extents=[width, 0.1, height]  # Thin box
                )
                
                # Translate to the correct position
                door_height = floor * 3.0  # Simple height calculation
                translation = [position[0], position[1], door_height]
                door_mesh.apply_translation(translation)
                
                return door_mesh
        
        return None
    
    def _create_roof_mesh(self, roof, floor_heights):
        """
        Create a mesh for the roof.
        
        Args:
            roof: Roof data
            floor_heights: List of floor heights
            
        Returns:
            trimesh.Trimesh: Roof mesh
        """
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
                    # Create a 2D polygon for the roof
                    polygon = np.array(points)
                    
                    try:
                        # Create the roof mesh by extruding a flat polygon
                        roof_mesh = trimesh.creation.extrude_polygon(
                            polygon=polygon,
                            height=roof_height
                        )
                        
                        # Translate to the top floor height
                        roof_mesh.apply_translation([0, 0, top_floor_height])
                        
                        return roof_mesh
                    except Exception:
                        # Fallback: create a simple box
                        min_x = min(p[0] for p in points)
                        min_y = min(p[1] for p in points)
                        max_x = max(p[0] for p in points)
                        max_y = max(p[1] for p in points)
                        
                        width = max_x - min_x
                        depth = max_y - min_y
                        
                        roof_mesh = trimesh.creation.box(
                            extents=[width, depth, roof_height]
                        )
                        
                        # Translate to the correct position
                        translation = [
                            min_x + width/2,
                            min_y + depth/2,
                            top_floor_height
                        ]
                        roof_mesh.apply_translation(translation)
                        
                        return roof_mesh
        
        # For other roof types, we would implement specific mesh creation
        # For now, we'll default to a flat roof
        return None
