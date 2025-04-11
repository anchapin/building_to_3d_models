import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class GbXMLManager:
    """
    Manages gbXML file operations.
    """
    
    def __init__(self):
        """Initialize the gbXML manager."""
        pass
    
    def convert_building_model(self, model_file, output_dir=None):
        """
        Convert a building model to gbXML format.
        
        Args:
            model_file (str): Path to the building model file
            output_dir (str, optional): Directory to save output files
            
        Returns:
            str: Path to the generated gbXML file
        """
        # Load the building model
        with open(model_file, 'r') as f:
            model_data = json.load(f)
        
        # Create a simple gbXML document
        gbxml = ET.Element('gbXML')
        gbxml.set('xmlns', 'http://www.gbxml.org/schema')
        gbxml.set('version', '6.01')
        
        # Add campus element
        campus = ET.SubElement(gbxml, 'Campus')
        campus.set('id', 'campus-1')
        
        # Add building element
        building = ET.SubElement(campus, 'Building')
        building.set('id', 'building-1')
        
        # Add space element
        space = ET.SubElement(building, 'Space')
        space.set('id', 'space-1')
        
        # Add surface elements
        for i, face in enumerate(model_data['faces']):
            surface = ET.SubElement(space, 'Surface')
            surface.set('id', f'surface-{i+1}')
            surface.set('surfaceType', 'ExteriorWall')
            
            # Add polyloop
            planar_geometry = ET.SubElement(surface, 'PlanarGeometry')
            polyloop = ET.SubElement(planar_geometry, 'PolyLoop')
            
            # Add points
            for vertex_idx in face:
                vertex = model_data['vertices'][vertex_idx]
                point = ET.SubElement(polyloop, 'CartesianPoint')
                
                # Add coordinates
                for j, coord in enumerate(['X', 'Y', 'Z']):
                    coordinate = ET.SubElement(point, 'Coordinate')
                    coordinate.text = str(vertex[j])
        
        # Save the gbXML file
        if output_dir:
            gbxml_path = os.path.join(output_dir, 'building_model.gbxml')
            
            # Convert to string and pretty-print
            rough_string = ET.tostring(gbxml, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")
            
            with open(gbxml_path, 'w') as f:
                f.write(pretty_xml)
            
            return gbxml_path
        
        return None
