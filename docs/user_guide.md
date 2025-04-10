# Building-to-3D Conversion Application

## User Guide

This comprehensive guide will help you use the Building-to-3D Conversion Application to transform building elevations and floor plans into 3D models suitable for energy modeling software.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Uploading Building Plans](#uploading-building-plans)
5. [Setting Scale](#setting-scale)
6. [Generating 3D Models](#generating-3d-models)
7. [Viewing Results](#viewing-results)
8. [Exporting to gbXML](#exporting-to-gbxml)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)
11. [Technical Details](#technical-details)

## Introduction

The Building-to-3D Conversion Application allows you to convert 2D building plans (elevations and floor plans) into detailed 3D models that can be used with building energy modeling software. The application processes your uploaded images, detects architectural elements like walls, windows, and doors, and combines this information to create an accurate 3D representation of your building.

### Key Features

- Upload and process multiple building elevations (north, east, south, west)
- Upload and process multiple floor plans (one per building level)
- Set scale to convert from pixels to real-world measurements
- Automatic detection of walls, windows, doors, and other architectural elements
- 3D model generation with proper geometry and coordinates
- Export to gbXML format for use with energy modeling software
- Interactive 3D visualization

## Installation

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Internet connection

### Installation Options

#### Option 1: Access the Hosted Application

The application is available online at: `https://building-to-3d.example.com`

#### Option 2: Local Installation

1. Download the application package from the releases page
2. Extract the zip file to a location on your computer
3. Install the required dependencies:
   ```
   cd api
   pip install -r requirements.txt
   ```
4. Start the application server:
   ```
   python app.py
   ```
5. Open your web browser and navigate to `http://localhost:5000`

## Getting Started

### Application Workflow

The typical workflow for using the application is as follows:

1. Upload building plans (elevations and floor plans)
2. Set scale for each uploaded image
3. Process the images to detect architectural elements
4. Generate the 3D model
5. View and export the results

### Preparing Your Building Plans

For best results, prepare your building plans as follows:

- **File Formats**: Use PNG, JPG, or PDF formats
- **Image Quality**: Ensure clear, high-resolution images
- **Scale Indicators**: Include scale bars or known dimensions in your plans
- **Elevations**: Provide at least one elevation for each cardinal direction (north, east, south, west)
- **Floor Plans**: Provide one floor plan for each level of the building
- **Orientation**: Ensure consistent orientation between floor plans and elevations

## Uploading Building Plans

1. From the home page, click on "Start New Project" or navigate to the Upload page
2. For each building plan:
   - Click "Upload File" or drag and drop your file into the designated area
   - Select the file type (Floor Plan or Elevation)
   - If uploading a floor plan, specify the floor level (0 for ground floor, 1 for first floor, etc.)
   - If uploading an elevation, specify the orientation (North, East, South, or West)
   - Click "Upload" to process the file

### Supported File Types

- **Images**: PNG, JPG, JPEG, BMP
- **Documents**: PDF (will be converted to images)

### Tips for Successful Uploads

- Ensure files are less than 20MB in size
- For PDF files, ensure they contain vector graphics or high-resolution images
- If your plans have multiple pages, split them into individual files before uploading

## Setting Scale

After uploading your building plans, you need to set the scale for each image to ensure accurate measurements in the 3D model.

1. For each uploaded plan, click on "Set Scale"
2. In the scale configuration tool:
   - Click on two points on a known dimension in your plan (e.g., a scale bar or room dimension)
   - Enter the real-world length between these points
   - Select the unit of measurement (meters, feet, inches, etc.)
   - Click "Apply Scale"

### Tips for Accurate Scaling

- Use the longest available known dimension for better accuracy
- Ensure the points you select are precisely at the ends of the dimension
- If your plan includes a scale bar, use it for the most accurate results
- Verify the scale by checking if other known dimensions match their expected values

## Generating 3D Models

Once you have uploaded all building plans and set their scales, you can generate the 3D model.

1. Navigate to the "Generate Model" page
2. Review the list of uploaded plans to ensure all required plans are included
3. Click "Generate 3D Model" to start the process
4. The application will:
   - Process each image to detect architectural elements
   - Combine information from all plans to create a 3D model
   - Generate the gbXML output
   - Display the results when complete

### Processing Time

The processing time depends on the number and complexity of your building plans. Typically:
- Simple buildings (1-2 floors): 1-2 minutes
- Medium buildings (3-5 floors): 3-5 minutes
- Complex buildings (6+ floors): 5-10 minutes

## Viewing Results

After the 3D model is generated, you can view the results in the Results page.

### 3D Model Viewer

The 3D Model Viewer allows you to:
- Rotate, pan, and zoom the model using mouse controls
- Toggle visibility of different building elements (walls, windows, doors, etc.)
- Change the display mode (wireframe, solid, etc.)
- Take screenshots of the model

#### Controls
- **Rotate**: Click and drag
- **Pan**: Right-click and drag or Shift + click and drag
- **Zoom**: Scroll wheel or Ctrl + click and drag
- **Reset View**: Double-click

### Building Information

The Results page also displays information about your building:
- Total floor area
- Number of floors
- Number of rooms
- Window-to-wall ratio
- Other building metrics

## Exporting to gbXML

To use your 3D model with energy modeling software, you can export it to gbXML format.

1. In the Results page, click on the "gbXML" tab
2. Review the gbXML preview to ensure all elements are correctly represented
3. Click "Download gbXML" to save the file to your computer

### Compatible Energy Modeling Software

The generated gbXML files are compatible with many energy modeling applications, including:
- EnergyPlus
- OpenStudio
- eQUEST
- DesignBuilder
- IES Virtual Environment
- Trace 700
- HAP

## Troubleshooting

### Common Issues and Solutions

#### Upload Failures
- **Issue**: File upload fails or times out
- **Solution**: Ensure your file is less than 20MB and in a supported format. Try compressing or resizing large images.

#### Incorrect Element Detection
- **Issue**: Walls, windows, or doors are not correctly detected
- **Solution**: Ensure your plans have clear, high-contrast lines. Try adjusting the processing settings or manually editing the detected elements.

#### Scale Issues
- **Issue**: The 3D model dimensions don't match expected values
- **Solution**: Re-check your scale settings and ensure you've selected precise points on known dimensions.

#### Model Generation Failures
- **Issue**: The 3D model fails to generate
- **Solution**: Ensure all required plans are uploaded and properly scaled. Check that floor plans and elevations have consistent orientations.

### Getting Support

If you encounter issues not covered in this guide:
- Check the FAQ section on our website
- Contact support at support@building-to-3d.example.com
- Join our community forum at forum.building-to-3d.example.com

## API Reference

The application provides a RESTful API for integration with other software.

### Base URL

When running locally: `http://localhost:5000/api`
When using the hosted version: `https://building-to-3d.example.com/api`

### Endpoints

#### Health Check
```
GET /health
```
Returns the status of the API server.

#### Upload File
```
POST /upload
```
Uploads and processes a building plan file.

**Parameters**:
- `file`: The file to upload
- `type`: File type (`floorPlan` or `elevation`)
- `orientation`: Orientation for elevations (`north`, `east`, `south`, `west`)
- `floorLevel`: Floor level for floor plans (integer, 0 for ground floor)

#### Set Scale
```
POST /set-scale
```
Sets the scale for an image.

**Parameters**:
- `imageId`: ID of the image
- `pixelLength`: Length in pixels
- `realLength`: Length in real-world units
- `unit`: Unit of measurement (`meters`, `feet`, etc.)

#### Generate Model
```
POST /generate-model
```
Generates a 3D model from processed files.

**Parameters**:
- `floorPlans`: Array of floor plan file IDs
- `elevations`: Array of elevation file IDs

#### Get Result File
```
GET /results/{filename}
```
Retrieves a result file.

## Technical Details

### System Architecture

The Building-to-3D Conversion Application consists of four main modules:

1. **Frontend Interface**: React/Next.js web application
2. **Image Processing Module**: Processes building plans using OpenCV
3. **3D Reconstruction Module**: Combines processed data to create 3D models
4. **gbXML Conversion Module**: Converts 3D models to gbXML format

### Technologies Used

- **Frontend**: React, Next.js, Three.js, Tailwind CSS
- **Backend**: Python, Flask, OpenCV, NumPy
- **3D Processing**: Open3D, Trimesh
- **XML Processing**: lxml

### Data Flow

1. User uploads building plans
2. Image processing module detects architectural elements
3. Scale conversion transforms pixel coordinates to real-world measurements
4. 3D reconstruction module combines data to create a 3D model
5. gbXML conversion module transforms the 3D model into gbXML format
6. Results are displayed to the user

### Performance Considerations

- Processing large or complex building plans may require significant computational resources
- For best performance, use clear, high-resolution images with good contrast
- The application is optimized for buildings with up to 10 floors and 50 rooms
