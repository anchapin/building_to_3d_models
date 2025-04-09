# Building-to-3D Conversion Application Data Flow Diagram

```
+------------------+     +------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |     |                  |
|   User Input     |     |  Image           |     |  3D Model        |     |  gbXML           |
|   (PDF/Images)   | --> |  Processing      | --> |  Generation      | --> |  Export          |
|                  |     |                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+     +------------------+
        |                        |                        |                        |
        v                        v                        v                        v
+------------------+     +------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |     |                  |
|  Scale           |     |  Vector          |     |  Coordinate      |     |  Building        |
|  Information     |     |  Representation  |     |  System          |     |  Elements        |
|                  |     |                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+     +------------------+
                                |
                                v
                         +------------------+
                         |                  |
                         |  Feature         |
                         |  Extraction      |
                         |                  |
                         +------------------+
```

## Key Data Transformations

### 1. PDF/Images to Vector Representation
- Input: Building elevation PDFs/images and floor plan PDFs/images
- Process: PDF to vector conversion, edge detection
- Output: Vector representation of building elements (lines, curves, shapes)

### 2. Vector Representation to Feature Extraction
- Input: Vector representation of building elements
- Process: Feature detection algorithms to identify architectural elements
- Output: Classified building elements (walls, windows, doors, etc.)

### 3. Feature Extraction to 3D Model
- Input: Classified building elements with scale information
- Process: Combining floor plan (X-Y) data with elevation (Z) data
- Output: 3D geometric model with proper spatial relationships

### 4. 3D Model to gbXML
- Input: 3D geometric model
- Process: Mapping geometric elements to gbXML components, assigning properties
- Output: Valid gbXML file for energy modeling

## Data Storage Requirements

### Temporary Storage
- Original uploaded images/PDFs
- Intermediate vector representations
- Feature extraction results
- 3D model data before export

### User Configuration Data
- Scale information for each image
- Unit preferences (feet, meters, etc.)
- Export preferences

### Output Data
- 3D visualization data
- gbXML file
- Validation results

## Data Validation Points

1. **Input Validation**
   - Verify image/PDF format and quality
   - Ensure minimum required views are provided (4 elevations, 1+ floor plans)
   - Validate scale information

2. **Processing Validation**
   - Verify successful vector conversion
   - Ensure feature detection identifies expected elements
   - Validate scale conversion accuracy

3. **Reconstruction Validation**
   - Verify proper alignment between floor plans and elevations
   - Ensure 3D geometry is closed and valid
   - Check spatial relationships for consistency

4. **Output Validation**
   - Validate gbXML against schema
   - Ensure all required building elements are included
   - Verify thermal properties are assigned appropriately
