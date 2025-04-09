import os
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from lxml import etree
import uuid
import datetime

class GbXMLConverter:
    """
    Class for converting 3D building models to gbXML format.
    """
    
    def __init__(self):
        """Initialize the gbXML converter."""
        # Define gbXML namespace
        self.ns = "http://www.gbxml.org/schema"
        # Define schema version
        self.schema_version = "6.01"
        
    def convert_to_gbxml(self, building_model, output_path=None, building_info=None):
        """
        Convert a 3D building model to gbXML format.
        
        Args:
            building_model: 3D building model data
            output_path: Path to save the gbXML file
            building_info: Additional building information
            
        Returns:
            str: gbXML content
        """
        # Create the root element
        root = ET.Element("gbXML")
        root.set("xmlns", self.ns)
        root.set("version", self.schema_version)
        
        # Add header information
        self._add_header(root, building_info)
        
        # Add campus element (required by gbXML)
        campus = ET.SubElement(root, "Campus")
        campus.set("id", "campus-1")
        
        # Add location information
        self._add_location(campus, building_info)
        
        # Add building element
        building = ET.SubElement(campus, "Building")
        building.set("id", "building-1")
        building.set("buildingType", "Unknown")
        
        # Add building name if available
        if building_info and 'name' in building_info:
            building_name = ET.SubElement(building, "Name")
            building_name.text = building_info['name']
        
        # Add building storeys
        self._add_building_storeys(building, building_model)
        
        # Add spaces (rooms)
        spaces = self._add_spaces(building, building_model)
        
        # Add surfaces (walls, floors, roofs)
        surfaces = self._add_surfaces(campus, building_model, spaces)
        
        # Add openings (windows, doors)
        self._add_openings(surfaces, building_model)
        
        # Convert to string with pretty formatting
        xml_string = self._prettify_xml(root)
        
        # Save to file if output_path is provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(xml_string)
            print(f"gbXML file saved to {output_path}")
        
        return xml_string
    
    def _add_header(self, root, building_info):
        """
        Add header information to the gbXML document.
        
        Args:
            root: Root XML element
            building_info: Building information dictionary
        """
        # Add file header
        header = ET.SubElement(root, "Header")
        
        # Add file description
        description = ET.SubElement(header, "Description")
        description.text = "Building model converted to gbXML"
        
        # Add author information
        author = ET.SubElement(header, "Author")
        
        # Add creation date and time
        created = ET.SubElement(header, "Created")
        created.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # Add software information
        software = ET.SubElement(header, "DocumentHistory")
        software.text = "Building-to-3D Conversion Application"
        
        # Add time zone if available
        if building_info and 'time_zone' in building_info:
            time_zone = ET.SubElement(header, "TimeZone")
            time_zone.text = str(building_info['time_zone'])
        
        # Add units
        units = ET.SubElement(header, "Unit")
        units.set("lengthUnit", "Meters")
        units.set("areaUnit", "SquareMeters")
        units.set("volumeUnit", "CubicMeters")
        units.set("temperatureUnit", "C")
    
    def _add_location(self, campus, building_info):
        """
        Add location information to the campus element.
        
        Args:
            campus: Campus XML element
            building_info: Building information dictionary
        """
        # Add location element
        location = ET.SubElement(campus, "Location")
        
        # Add location name if available
        if building_info and 'location_name' in building_info:
            name = ET.SubElement(location, "Name")
            name.text = building_info['location_name']
        
        # Add latitude and longitude if available
        if building_info:
            if 'latitude' in building_info and 'longitude' in building_info:
                latitude = ET.SubElement(location, "Latitude")
                latitude.text = str(building_info['latitude'])
                
                longitude = ET.SubElement(location, "Longitude")
                longitude.text = str(building_info['longitude'])
        
        # Add elevation if available
        if building_info and 'elevation' in building_info:
            elevation = ET.SubElement(location, "Elevation")
            elevation.text = str(building_info['elevation'])
    
    def _add_building_storeys(self, building, building_model):
        """
        Add building storeys to the building element.
        
        Args:
            building: Building XML element
            building_model: Building model data
            
        Returns:
            dict: Dictionary mapping storey IDs to storey elements
        """
        # Get floor heights from the building model
        floor_heights = building_model.get('floors', [])
        
        # Create a dictionary to store storey elements
        storeys = {}
        
        # Add building storey for each floor
        for i, height in enumerate(floor_heights):
            storey_id = f"storey-{i+1}"
            
            # Create building storey element
            storey = ET.SubElement(building, "BuildingStorey")
            storey.set("id", storey_id)
            
            # Add storey name
            name = ET.SubElement(storey, "Name")
            if i == 0:
                name.text = "Ground Floor"
            else:
                name.text = f"Floor {i}"
            
            # Add storey level
            level = ET.SubElement(storey, "Level")
            level.text = str(height)
            
            # Store storey element
            storeys[storey_id] = storey
        
        return storeys
    
    def _add_spaces(self, building, building_model):
        """
        Add spaces (rooms) to the building element.
        
        Args:
            building: Building XML element
            building_model: Building model data
            
        Returns:
            dict: Dictionary mapping space IDs to space elements
        """
        # Create a dictionary to store space elements
        spaces = {}
        
        # Get floor plans from the building model
        floor_plans = building_model.get('floor_plans', [])
        
        # Add space for each room in each floor plan
        for i, floor_plan in enumerate(floor_plans):
            # Get rooms from the floor plan
            rooms = floor_plan.get('features', {}).get('rooms', [])
            
            for j, room in enumerate(rooms):
                space_id = f"space-{i+1}-{j+1}"
                
                # Create space element
                space = ET.SubElement(building, "Space")
                space.set("id", space_id)
                space.set("buildingStoreyIdRef", f"storey-{i+1}")
                
                # Add space name
                name = ET.SubElement(space, "Name")
                name.text = f"Room {j+1} on Floor {i+1}"
                
                # Add space area if available
                if 'area' in room:
                    area = ET.SubElement(space, "Area")
                    area.text = str(room['area'])
                
                # Add space volume (estimated)
                if 'area' in room:
                    # Assume standard ceiling height of 3 meters
                    volume = ET.SubElement(space, "Volume")
                    volume.text = str(room['area'] * 3.0)
                
                # Store space element
                spaces[space_id] = space
        
        return spaces
    
    def _add_surfaces(self, campus, building_model, spaces):
        """
        Add surfaces (walls, floors, roofs) to the campus element.
        
        Args:
            campus: Campus XML element
            building_model: Building model data
            spaces: Dictionary of space elements
            
        Returns:
            dict: Dictionary mapping surface IDs to surface elements
        """
        # Create a dictionary to store surface elements
        surfaces = {}
        
        # Get walls from the building model
        walls = building_model.get('walls', [])
        
        # Add surface for each wall
        for i, wall in enumerate(walls):
            surface_id = f"surface-wall-{i+1}"
            
            # Create surface element
            surface = ET.SubElement(campus, "Surface")
            surface.set("id", surface_id)
            surface.set("surfaceType", "ExteriorWall")  # Default to exterior wall
            
            # Add surface name
            name = ET.SubElement(surface, "Name")
            name.text = f"Wall {i+1}"
            
            # Add adjacent space references
            # For simplicity, we'll assume each wall is adjacent to one space
            # In a real implementation, this would be determined by spatial analysis
            if spaces and i < len(spaces):
                space_id = list(spaces.keys())[i % len(spaces)]
                adjacent_space = ET.SubElement(surface, "AdjacentSpaceId")
                adjacent_space.set("spaceIdRef", space_id)
            
            # Add rectangular geometry
            self._add_rectangular_geometry(surface, wall)
            
            # Store surface element
            surfaces[surface_id] = surface
        
        # Add roof surfaces
        roof = building_model.get('roof', {})
        if roof:
            surface_id = "surface-roof-1"
            
            # Create surface element
            surface = ET.SubElement(campus, "Surface")
            surface.set("id", surface_id)
            surface.set("surfaceType", "Roof")
            
            # Add surface name
            name = ET.SubElement(surface, "Name")
            name.text = "Roof"
            
            # Add rectangular geometry
            self._add_rectangular_geometry(surface, roof)
            
            # Store surface element
            surfaces[surface_id] = surface
        
        # Add floor surfaces
        # For simplicity, we'll create one floor surface per storey
        floor_heights = building_model.get('floors', [])
        for i, height in enumerate(floor_heights):
            surface_id = f"surface-floor-{i+1}"
            
            # Create surface element
            surface = ET.SubElement(campus, "Surface")
            surface.set("id", surface_id)
            surface.set("surfaceType", "SlabOnGrade" if i == 0 else "InteriorFloor")
            
            # Add surface name
            name = ET.SubElement(surface, "Name")
            name.text = f"Floor {i+1}"
            
            # Add adjacent space references
            if spaces:
                # Find spaces on this floor
                floor_spaces = [space_id for space_id in spaces.keys() if f"-{i+1}-" in space_id]
                for space_id in floor_spaces:
                    adjacent_space = ET.SubElement(surface, "AdjacentSpaceId")
                    adjacent_space.set("spaceIdRef", space_id)
            
            # Add rectangular geometry
            # For simplicity, we'll use the building outline
            outline = building_model.get('outline', {})
            self._add_rectangular_geometry(surface, outline)
            
            # Store surface element
            surfaces[surface_id] = surface
        
        return surfaces
    
    def _add_openings(self, surfaces, building_model):
        """
        Add openings (windows, doors) to the surface elements.
        
        Args:
            surfaces: Dictionary of surface elements
            building_model: Building model data
        """
        # Get openings from the building model
        openings = building_model.get('openings', [])
        
        # Add opening for each window and door
        for i, opening in enumerate(openings):
            opening_type = opening.get('type', '')
            
            if opening_type == 'window':
                # Find a suitable wall surface
                # For simplicity, we'll use the first wall surface
                surface_id = next((sid for sid in surfaces.keys() if 'wall' in sid), None)
                if not surface_id:
                    continue
                
                surface = surfaces[surface_id]
                
                # Create opening element
                opening_element = ET.SubElement(surface, "Opening")
                opening_element.set("id", f"opening-window-{i+1}")
                opening_element.set("openingType", "FixedWindow")
                
                # Add opening name
                name = ET.SubElement(opening_element, "Name")
                name.text = f"Window {i+1}"
                
                # Add rectangular geometry
                self._add_rectangular_geometry(opening_element, opening)
                
            elif opening_type == 'door':
                # Find a suitable wall surface
                # For simplicity, we'll use the second wall surface if available
                surface_ids = [sid for sid in surfaces.keys() if 'wall' in sid]
                surface_id = surface_ids[1] if len(surface_ids) > 1 else surface_ids[0] if surface_ids else None
                if not surface_id:
                    continue
                
                surface = surfaces[surface_id]
                
                # Create opening element
                opening_element = ET.SubElement(surface, "Opening")
                opening_element.set("id", f"opening-door-{i+1}")
                opening_element.set("openingType", "NonSlidingDoor")
                
                # Add opening name
                name = ET.SubElement(opening_element, "Name")
                name.text = f"Door {i+1}"
                
                # Add rectangular geometry
                self._add_rectangular_geometry(opening_element, opening)
    
    def _add_rectangular_geometry(self, parent, element):
        """
        Add rectangular geometry to an element.
        
        Args:
            parent: Parent XML element
            element: Element data with geometry information
        """
        # Create rectangular geometry element
        geom = ET.SubElement(parent, "RectangularGeometry")
        
        # Add height and width if available
        if 'height' in element:
            height = ET.SubElement(geom, "Height")
            height.text = str(element['height'])
        
        if 'width' in element:
            width = ET.SubElement(geom, "Width")
            width.text = str(element['width'])
        
        # Add azimuth if available
        if 'angle' in element:
            azimuth = ET.SubElement(geom, "Azimuth")
            azimuth.text = str(element['angle'])
        
        # Add cartesian points
        points = element.get('points', [])
        if points:
            # Create planar geometry element
            planar_geom = ET.SubElement(parent, "PlanarGeometry")
            
            # Create polyloop element
            polyloop = ET.SubElement(planar_geom, "PolyLoop")
            
            # Add cartesian points
            for point in points:
                cartesian_point = ET.SubElem
(Content truncated due to size limit. Use line ranges to read in chunks)