# Building-to-3D Conversion Application Technology Stack

## Frontend Technologies

### Framework
- **Next.js**: For building the web application interface
- **React**: For creating interactive UI components
- **Tailwind CSS**: For styling the application

### 3D Visualization
- **Three.js**: For rendering and displaying 3D models in the browser
- **react-three-fiber**: React bindings for Three.js

### File Handling
- **react-dropzone**: For handling file uploads
- **file-saver**: For downloading generated gbXML files

## Backend Technologies

### Core Language
- **Python 3.10+**: Primary programming language for backend processing

### Image Processing
- **OpenCV**: For edge detection, feature extraction, and image processing
- **PyMuPDF**: For PDF to vector conversion
- **NumPy**: For numerical operations and array manipulation
- **scikit-image**: For additional image processing capabilities

### 3D Reconstruction
- **Open3D**: For 3D geometry creation and manipulation
- **Trimesh**: For mesh operations and analysis
- **SciPy**: For spatial algorithms and mathematical operations

### gbXML Generation
- **lxml**: For XML creation and manipulation
- **ElementTree**: Alternative XML library for Python

## Development Tools

### Version Control
- **Git**: For source code management
- **GitHub**: For repository hosting and collaboration

### Development Environment
- **Visual Studio Code**: Recommended IDE with Python and JavaScript extensions
- **Jupyter Notebook**: For prototyping and testing algorithms

### Testing
- **pytest**: For Python unit and integration testing
- **Jest**: For JavaScript/React component testing

### Deployment
- **Docker**: For containerization
- **Cloudflare Pages**: For frontend deployment
- **Python API**: Backend processing as serverless functions

## Third-Party Services

### Storage
- **Browser LocalStorage**: For temporary client-side storage
- **Server-side file storage**: For processing uploaded files

### Validation
- **gbXML Validator**: For validating generated gbXML files against schema

## System Requirements

### Client-Side
- Modern web browser with WebGL support (Chrome, Firefox, Safari, Edge)
- Minimum 8GB RAM recommended for handling complex models
- Sufficient disk space for temporary file storage

### Server-Side
- Python 3.10+ runtime environment
- Sufficient CPU resources for image processing and 3D reconstruction
- Adequate memory for handling large building models
- Temporary storage for processing files
