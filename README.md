# Building to 3D Models

A web application for converting building plans (floor plans and elevations) to 3D models.

## Features

- Upload and process floor plans and elevation drawings
- Set scale for accurate measurements
- Generate 3D models from processed plans
- Export to standard 3D formats and gbXML for energy analysis

## Prerequisites

- Python 3.8+
- Node.js 14+
- Git

## Setup and Installation

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anchapin/building_to_3d_models.git
   cd building_to_3d_models
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r deployment/api/requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   cd deployment/api
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend/building-to-3d-app
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload floor plans and elevation drawings
3. Set the scale for each drawing
4. Generate the 3D model
5. Download the resulting 3D model and gbXML files

## Running Tests

### Backend Tests

```bash
cd deployment/api
python run_tests.py
```

### Frontend Tests

```bash
cd frontend/building-to-3d-app
npm test
```

## Project Structure

- `deployment/api/` - Backend Flask API
  - `app.py` - Main API entry point
  - `image_processing/` - Image processing modules
  - `reconstruction/` - 3D reconstruction modules
  - `gbxml/` - gbXML conversion modules
  - `tests/` - Backend tests

- `frontend/building-to-3d-app/` - Next.js frontend application
  - `app/` - Next.js app directory
  - `components/` - React components
  - `services/` - API services
  - `__tests__/` - Frontend tests

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
