# Building-to-3D Conversion Application

## Quick Start Guide

This quick start guide will help you get up and running with the Building-to-3D Conversion Application in just a few minutes.

## Installation

### Option 1: Use the Hosted Application

Visit `https://building-to-3d.example.com` to use the application without installation.

### Option 2: Local Installation

1. Download the application package: `building_to_3d_app.zip`
2. Extract the zip file to a location on your computer
3. Install dependencies and start the server:
   ```
   cd api
   pip install -r requirements.txt
   python app.py
   ```
4. Open your web browser and navigate to `http://localhost:5000`

## Basic Workflow

### 1. Upload Building Plans

1. Click "Start New Project" on the home page
2. Upload your floor plans and elevations:
   - For floor plans, specify the floor level (0 for ground floor)
   - For elevations, specify the orientation (North, East, South, West)

### 2. Set Scale

1. For each uploaded plan, click "Set Scale"
2. Click on two points on a known dimension in your plan
3. Enter the real-world length between these points
4. Select the unit of measurement (meters, feet, etc.)
5. Click "Apply Scale"

### 3. Generate 3D Model

1. Click "Generate 3D Model"
2. Wait for the processing to complete
3. View the resulting 3D model in the viewer

### 4. Export Results

1. To export the gbXML file, click on the "gbXML" tab
2. Click "Download gbXML" to save the file
3. Use the downloaded file with your energy modeling software

## Tips for Best Results

- Provide clear, high-resolution images of your building plans
- Include at least one floor plan for each level of the building
- Include elevations for all four cardinal directions if possible
- Ensure your plans include scale indicators or known dimensions
- Verify the scale settings before generating the 3D model

## Need Help?

- Refer to the full [User Guide](user_guide.md) for detailed instructions
- Check the [Troubleshooting](user_guide.md#troubleshooting) section for common issues
- Contact support at support@building-to-3d.example.com
