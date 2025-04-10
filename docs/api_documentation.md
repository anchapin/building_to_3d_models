# Building-to-3D Conversion Application

## API Documentation

This document provides detailed information about the Building-to-3D Conversion Application's API endpoints, request/response formats, and usage examples.

## Base URL

When running locally: `http://localhost:5000/api`
When using the hosted version: `https://building-to-3d.example.com/api`

## Authentication

The API currently does not require authentication. All endpoints are publicly accessible.

## Endpoints

### Health Check

Check if the API server is running.

```
GET /health
```

#### Response

```json
{
  "status": "ok"
}
```

### Upload File

Upload and process a building plan file.

```
POST /upload
```

#### Request

- Content-Type: `multipart/form-data`
- Body Parameters:
  - `file`: (Required) The file to upload (PNG, JPG, PDF)
  - `type`: (Required) File type (`floorPlan` or `elevation`)
  - `orientation`: (Required for elevations) Orientation (`north`, `east`, `south`, `west`)
  - `floorLevel`: (Required for floor plans) Floor level (integer, 0 for ground floor)

#### Response

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

#### Error Response

```json
{
  "error": "No file part"
}
```

#### cURL Example

```bash
curl -X POST \
  http://localhost:5000/api/upload \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/floor_plan.png' \
  -F 'type=floorPlan' \
  -F 'floorLevel=0'
```

### Set Scale

Set the scale for an image to convert from pixels to real-world measurements.

```
POST /set-scale
```

#### Request

- Content-Type: `application/json`
- Body:
```json
{
  "imageId": "floor_plan_1",
  "pixelLength": 100,
  "realLength": 5.0,
  "unit": "meters"
}
```

#### Parameters

- `imageId`: (Required) ID of the image
- `pixelLength`: (Required) Length in pixels
- `realLength`: (Required) Length in real-world units
- `unit`: (Optional) Unit of measurement (`meters`, `feet`, `inches`, `cm`). Defaults to `meters`

#### Response

```json
{
  "success": true,
  "scale_factor": 0.05
}
```

#### Error Response

```json
{
  "error": "Missing required parameters"
}
```

#### cURL Example

```bash
curl -X POST \
  http://localhost:5000/api/set-scale \
  -H 'Content-Type: application/json' \
  -d '{
    "imageId": "floor_plan_1",
    "pixelLength": 100,
    "realLength": 5.0,
    "unit": "meters"
  }'
```

### Generate Model

Generate a 3D model from processed files.

```
POST /generate-model
```

#### Request

- Content-Type: `application/json`
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

#### Parameters

- `floorPlans`: (Required) Array of floor plan file IDs
- `elevations`: (Required) Array of elevation file IDs

#### Response

```json
{
  "success": true,
  "model_file": "building_model.obj",
  "gbxml_file": "building_model.gbxml"
}
```

#### Error Response

```json
{
  "error": "Missing required parameters"
}
```

#### cURL Example

```bash
curl -X POST \
  http://localhost:5000/api/generate-model \
  -H 'Content-Type: application/json' \
  -d '{
    "floorPlans": ["floor_plan_1_processed.json"],
    "elevations": [
      "elevation_north_processed.json",
      "elevation_east_processed.json",
      "elevation_south_processed.json",
      "elevation_west_processed.json"
    ]
  }'
```

### Get Result File

Retrieve a result file.

```
GET /results/{filename}
```

#### Parameters

- `filename`: (Required) Name of the file to retrieve

#### Response

The requested file or an error message.

#### Error Response

```json
{
  "error": "File not found"
}
```

#### cURL Example

```bash
curl -X GET \
  http://localhost:5000/api/results/building_model.gbxml \
  -o building_model.gbxml
```

## Response Codes

- `200 OK`: The request was successful
- `400 Bad Request`: The request was invalid or missing required parameters
- `404 Not Found`: The requested resource was not found
- `500 Internal Server Error`: An error occurred on the server

## Rate Limiting

The API currently does not implement rate limiting, but excessive requests may be throttled in the future.

## Versioning

The current API version is v1. The version is not included in the URL path but may be in future releases.

## Examples

### Complete Workflow Example

1. Upload a floor plan:

```bash
curl -X POST \
  http://localhost:5000/api/upload \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/floor_plan.png' \
  -F 'type=floorPlan' \
  -F 'floorLevel=0'
```

2. Upload elevations:

```bash
curl -X POST \
  http://localhost:5000/api/upload \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/north_elevation.png' \
  -F 'type=elevation' \
  -F 'orientation=north'
```

3. Set scale for floor plan:

```bash
curl -X POST \
  http://localhost:5000/api/set-scale \
  -H 'Content-Type: application/json' \
  -d '{
    "imageId": "floor_plan_1",
    "pixelLength": 100,
    "realLength": 5.0,
    "unit": "meters"
  }'
```

4. Generate 3D model:

```bash
curl -X POST \
  http://localhost:5000/api/generate-model \
  -H 'Content-Type: application/json' \
  -d '{
    "floorPlans": ["floor_plan_1_processed.json"],
    "elevations": ["north_elevation_processed.json"]
  }'
```

5. Download gbXML file:

```bash
curl -X GET \
  http://localhost:5000/api/results/building_model.gbxml \
  -o building_model.gbxml
```

## Error Handling

The API returns error messages in JSON format with an `error` field containing a description of the error.

Example:

```json
{
  "error": "File not found"
}
```

## Support

For API support, please contact api-support@building-to-3d.example.com.
