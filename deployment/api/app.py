import os
import json
import flask
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import application modules
from image_processing.image_processor import ImageProcessor
from reconstruction.reconstruction_coordinator import ReconstructionCoordinator
from gbxml.gbxml_manager import GbXMLManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
RESULTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Initialize modules
image_processor = ImageProcessor()
reconstruction_coordinator = ReconstructionCoordinator()
gbxml_manager = GbXMLManager()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload building plan files."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Get file type from form data
    file_type = request.form.get('type', 'unknown')
    orientation = request.form.get('orientation', 'unknown')
    floor_level = request.form.get('floorLevel', '0')
    
    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Process file based on type
    try:
        if file_type == 'floorPlan':
            # Process floor plan
            result = image_processor.process_building_plan(
                file_path, 
                plan_type='floor_plan',
                output_dir=RESULTS_FOLDER
            )
            result['floor_level'] = int(floor_level)
            
        elif file_type == 'elevation':
            # Process elevation
            result = image_processor.process_building_plan(
                file_path, 
                plan_type='elevation',
                orientation=orientation,
                output_dir=RESULTS_FOLDER
            )
            
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
        # Save result to JSON file
        result_filename = f"{os.path.splitext(filename)[0]}_processed.json"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)
        
        with open(result_path, 'w') as f:
            json.dump(result, f)
            
        return jsonify({
            'success': True,
            'filename': filename,
            'result_file': result_filename,
            'file_type': file_type,
            'orientation': orientation if file_type == 'elevation' else None,
            'floor_level': floor_level if file_type == 'floorPlan' else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/set-scale', methods=['POST'])
def set_scale():
    """Set scale for an image."""
    data = request.json
    
    if not data or 'imageId' not in data or 'pixelLength' not in data or 'realLength' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
        
    try:
        # Set scale in the image processor
        scale_factor = image_processor.scale_converter.set_scale(
            data['imageId'],
            data['pixelLength'],
            data['realLength'],
            data.get('unit', 'meters')
        )
        
        return jsonify({
            'success': True,
            'scale_factor': scale_factor
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-model', methods=['POST'])
def generate_model():
    """Generate 3D model from processed files."""
    data = request.json
    
    if not data or 'floorPlans' not in data or 'elevations' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
        
    try:
        # Get file paths
        floor_plan_files = [os.path.join(RESULTS_FOLDER, fp) for fp in data['floorPlans']]
        elevation_files = [os.path.join(RESULTS_FOLDER, el) for el in data['elevations']]
        
        # Generate 3D model
        result = reconstruction_coordinator.process_building(
            floor_plan_files,
            elevation_files,
            output_dir=RESULTS_FOLDER
        )
        
        # Generate gbXML
        gbxml_path = gbxml_manager.convert_building_model(
            os.path.join(RESULTS_FOLDER, 'building_model.json'),
            output_dir=RESULTS_FOLDER
        )
        
        return jsonify({
            'success': True,
            'model_file': 'building_model.obj',
            'gbxml_file': 'building_model.gbxml'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results/<filename>', methods=['GET'])
def get_result_file(filename):
    """Get a result file."""
    file_path = os.path.join(RESULTS_FOLDER, secure_filename(filename))
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
        
    return send_file(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
