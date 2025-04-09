# Building-to-3D Conversion Application

## Developer Documentation

This technical documentation is intended for developers who want to understand, modify, or extend the Building-to-3D Conversion Application.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Descriptions](#module-descriptions)
3. [Development Environment Setup](#development-environment-setup)
4. [Building and Testing](#building-and-testing)
5. [Extending the Application](#extending-the-application)
6. [API Documentation](#api-documentation)
7. [Data Structures](#data-structures)
8. [Algorithm Details](#algorithm-details)

## Architecture Overview

The Building-to-3D Conversion Application follows a modular architecture with clear separation of concerns:

### High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│    Frontend     │────▶│ Image Processing│────▶│3D Reconstruction│────▶│gbXML Conversion │
│    Interface    │     │     Module      │     │     Module      │     │     Module      │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Component Interaction

- **Frontend Interface**: Provides user interface for file uploads, scale setting, and result visualization
- **Image Processing Module**: Processes building plans to extract architectural features
- **3D Reconstruction Module**: Combines processed data to create 3D building models
- **gbXML Conversion Module**: Transforms 3D models into gbXML format for energy modeling

### Data Flow

1. User uploads building plans through the frontend
2. Frontend sends files to the backend API
3. Image processing module extracts features from the plans
4. 3D reconstruction module combines features into a 3D model
5. gbXML conversion module transforms the 3D model into gbXML format
6. Results are sent back to the frontend for visualization

## Module Descriptions

### Frontend Interface

The frontend is built with Next.js and React, providing a responsive and intuitive user interface.

#### Key Components

- **Page Components**: Main application pages (Home, Upload, Results)
- **UI Components**: Reusable interface elements (FileUploadDropzone, ScaleConfigurationTool, ThreeDViewer)
- **State Management**: Manages application state and user interactions
- **API Client**: Communicates with the backend API

#### File Structure

```
frontend/building-to-3d-app/
├── src/
│   ├── app/
│   │   ├── page.tsx                # Home page
│   │   ├── upload/
│   │   │   └── page.tsx            # Upload page
│   │   └── results/
│   │       └── page.tsx            # Results page
│   ├── components/
│   │   ├── FileUploadDropzone.tsx  # File upload component
│   │   ├── ScaleConfigurationTool.tsx # Scale setting component
│   │   ├── ThreeDViewer.tsx        # 3D model viewer
│   │   └── GbXMLViewer.tsx         # gbXML viewer
│   └── lib/
│       └── api.ts                  # API client functions
└── public/
    └── assets/                     # Static assets
```

### Image Processing Module

The image processing module uses OpenCV and other libraries to process building plans and extract architectural features.

#### Key Components

- **PDF to Vector Converter**: Converts PDF files to vector representations
- **Edge Detector**: Detects edges in building plans
- **Feature Extractor**: Identifies architectural elements (walls, windows, doors)
- **Scale Converter**: Converts pixel measurements to real-world units

#### File Structure

```
backend/image_processing/
├── pdf_to_vector.py       # PDF conversion utilities
├── edge_detector.py       # Edge detection algorithms
├── feature_extractor.py   # Feature extraction algorithms
├── scale_converter.py     # Scale conversion utilities
└── image_processor.py     # Main processing coordinator
```

### 3D Reconstruction Module

The 3D reconstruction module combines processed building plans to create 3D models.

#### Key Components

- **Building Reconstructor**: Creates 3D building models from processed plans
- **Reconstruction Coordinator**: Manages the reconstruction workflow
- **Model Visualizer**: Provides visualization capabilities for 3D models

#### File Structure

```
backend/reconstruction/
├── building_reconstructor.py    # 3D model creation
├── reconstruction_coordinator.py # Workflow coordination
└── model_visualizer.py          # 3D visualization utilities
```

### gbXML Conversion Module

The gbXML conversion module transforms 3D models into gbXML format for energy modeling.

#### Key Components

- **GbXML Converter**: Converts 3D models to gbXML format
- **GbXML Manager**: Manages gbXML file operations and validation

#### File Structure

```
backend/gbxml/
├── gbxml_converter.py     # gbXML conversion logic
└── gbxml_manager.py       # gbXML file management
```

## Development Environment Setup

### Prerequisites

- Python 3.8+ for backend development
- Node.js 14+ for frontend development
- Git for version control

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/example/building-to-3d.git
   cd building-to-3d
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install backend dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend/building-to-3d-app
   ```

2. Install frontend dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## Building and Testing

### Running Tests

The application includes comprehensive test suites for all modules.

1. Run all tests:
   ```
   ./run_tests.sh
   ```

2. Run specific test modules:
   ```
   python -m unittest tests/test_modules.py
   python -m unittest tests/test_deployment.py
   ```

### Building for Production

1. Build the frontend:
   ```
   cd frontend/building-to-3d-app
   npm run build
   ```

2. Create a deployment package:
   ```
   ./deploy.sh
   ```

3. The deployment package will be created as `building_to_3d_app.zip`

## Extending the Application

### Adding New Features

To add new features to the application:

1. Identify the appropriate module for your feature
2. Implement the feature following the existing patterns
3. Add tests for your feature
4. Update documentation to reflect the new feature

### Supporting New File Formats

To add support for new file formats:

1. Extend the `pdf_to_vector.py` module or create a new converter
2. Update the file upload component to accept the new format
3. Add appropriate validation and error handling

### Improving Algorithms

To improve the existing algorithms:

1. Identify the algorithm you want to improve
2. Implement your improvements in the appropriate module
3. Add tests to verify the improvements
4. Benchmark the performance against the original algorithm

## API Documentation

### Backend API Endpoints

#### Health Check
```
GET /api/health
```
Returns the status of the API server.

**Response**:
```json
{
  "status": "ok"
}
```

#### Upload File
```
POST /api/upload
```
Uploads and processes a building plan file.

**Request**:
- Content-Type: multipart/form-data
- Body:
  - `file`: The file to upload
  - `type`: File type (`floorPlan` or `elevation`)
  - `orientation`: Orientation for elevations (`north`, `east`, `south`, `west`)
  - `floorLevel`: Floor level for floor plans (integer, 0 for ground floor)

**Response**:
```json
{
  "success": true,
  "filename": "floor_plan_1.png",
  "result_file": "floor_plan_1_processed.json",
  "file_type": "floorPlan",
  "orientation": null,
  "floor_level": "0"
}
```

#### Set Scale
```
POST /api/set-scale
```
Sets the scale for an image.

**Request**:
- Content-Type: application/json
- Body:
```json
{
  "imageId": "floor_plan_1",
  "pixelLength": 100,
  "realLength": 5.0,
  "unit": "meters"
}
```

**Response**:
```json
{
  "success": true,
  "scale_factor": 0.05
}
```

#### Generate Model
```
POST /api/generate-model
```
Generates a 3D model from processed files.

**Request**:
- Content-Type: application/json
- Body:
```json
{
  "floorPlans": ["floor_plan_1_processed.json"],
  "elevations": [
    "elevation_north_processed.json",
    "elevation_east_processed.json",
    "elevation_south_processed.json",
    "elevation_west_processed.json"
  ]
}
```

**Response**:
```json
{
  "success": true,
  "model_file": "building_model.obj",
  "gbxml_file": "building_model.gbxml"
}
```

#### Get Result File
```
GET /api/results/{filename}
```
Retrieves a result file.

**Response**:
The requested file or an error message.

## Data Structures

### Processed Image Data

```json
{
  "image_id": "floor_plan_1",
  "file_path": "uploads/floor_plan_1.png",
  "features": {
    "walls": [
      {
        "type": "wall",
        "points": [[0, 0], [10, 0]],
        "length": 10.0,
        "thickness": 0.3
      }
    ],
    "windows": [
      {
        "type": "window",
        "points": [[2, 0], [4, 0], [4, 1.5], [2, 1.5]],
        "width": 2.0,
        "height": 1.5
      }
    ],
    "doors": [
      {
        "type": "door",
        "door_type": "standard",
        "points": [[7, 0], [8, 0]],
        "length": 1.0
      }
    ],
    "rooms": [
      {
        "type": "room",
        "points": [[0.3, 0.3], [9.7, 0.3], [9.7, 7.7], [0.3, 7.7]],
        "area": 72.0,
        "centroid": [5.0, 4.0]
      }
    ]
  },
  "floor_plan_data": {
    "level": 0
  }
}
```

### 3D Model Data

```json
{
  "building_model": {
    "floors": [0.0, 3.0, 6.0],
    "walls": [
      {
        "points": [[0, 0], [10, 0], [10, 8], [0, 8], [0, 0]],
        "height": 3.0,
        "base_height": 0.0,
        "thickness": 0.3
      }
    ],
    "openings": [
      {
        "type": "window",
        "position": [2, 0],
        "width": 1.5,
        "height": 1.2,
        "floor": 0
      },
      {
        "type": "door",
        "door_type": "standard",
        "position": [5, 0],
        "width": 1.0,
        "height": 2.1,
        "floor": 0
      }
    ],
    "roof": {
      "type": "flat",
      "outline": [
        {
          "points": [[0, 0], [10, 0], [10, 8], [0, 8], [0, 0]]
        }
      ],
      "height": 0.5
    }
  },
  "mesh_path": "results/building_model.obj"
}
```

## Algorithm Details

### Edge Detection

The application uses a combination of Canny edge detection and Hough line transformation to detect edges in building plans:

1. **Preprocessing**: Convert image to grayscale and apply Gaussian blur
2. **Edge Detection**: Apply Canny edge detection with adaptive thresholds
3. **Line Detection**: Use Hough line transformation to detect straight lines
4. **Line Filtering**: Filter lines based on length, orientation, and proximity
5. **Line Merging**: Merge collinear lines to form continuous walls

### Feature Extraction

Architectural features are extracted using these algorithms:

1. **Wall Detection**: Identify long, straight lines as potential walls
2. **Window Detection**: Identify rectangular shapes on walls with specific aspect ratios
3. **Door Detection**: Identify gaps in walls with specific widths
4. **Room Detection**: Use flood fill algorithm to identify enclosed spaces

### 3D Reconstruction

The 3D model is created using these steps:

1. **Floor Height Extraction**: Determine floor heights from elevation views
2. **Wall Extrusion**: Extrude walls from floor plans to create 3D walls
3. **Opening Placement**: Place windows and doors on walls based on coordinates
4. **Roof Creation**: Create roof based on top floor outline
5. **Mesh Generation**: Convert all elements to a unified 3D mesh
