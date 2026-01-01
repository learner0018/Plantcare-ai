# app.py
# This is the main Flask application - the server that handles all requests
# Think of it as the "control center" that connects everything together

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import traceback
from flask import Flask, request, jsonify, render_template
# Import our custom modules
from model_handler import PlantDiseaseModel
from disease_database import get_disease_info, is_healthy , get_confidence_message
from ai_chat_handler_free import PlantCareAI



# Initialize Flask app
# __name__ tells Flask where to look for templates and static files
app = Flask(__name__)
ai_assistant = PlantCareAI()

# Enable CORS (Cross-Origin Resource Sharing)
# This allows our frontend (React/HTML) to communicate with backend
CORS(app)

# Configuration
# This section contains settings for our application
UPLOAD_FOLDER = 'uploads'  # Where we temporarily store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}  # Allowed image types
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize our AI model
# This loads the model when the server starts
print("🚀 Initializing Plant Disease Detection System...")
model = PlantDiseaseModel()
print("✓ System ready!")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """
    Checks if uploaded file has an allowed extension
    
    Parameters:
        filename: Name of the uploaded file
    
    Returns:
        True if file type is allowed, False otherwise
    
    Example:
        allowed_file('plant.jpg') -> True
        allowed_file('document.pdf') -> False
    """
    # Check if filename has a dot and the extension is in ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_response(success, message, data=None):
    """
    Creates a standardized API response
    All our API endpoints return responses in this format for consistency
    
    Parameters:
        success: Boolean indicating if request was successful
        message: Human-readable message about the result
        data: Any additional data to include in response
    
    Returns:
        Dictionary in standard format
    """
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.now().isoformat()  # When response was created
    }
    
    if data:
        response['data'] = data
    
    return response


# ============================================================================
# API ROUTES (ENDPOINTS)
# ============================================================================



@app.route('/')
def home():
    """Serve the frontend HTML page"""
    return render_template('index.html')



@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Used to verify the API is running properly
    """
    return jsonify(generate_response(
        success=True,
        message='API is healthy and running',
        data={
            'model_status': 'loaded',
            'uptime': 'active'
        }
    ))


@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    """
    Lists all diseases the model can detect
    Useful for frontend to know what's possible
    """
    from disease_database import get_all_diseases
    
    diseases = get_all_diseases()
    
    return jsonify(generate_response(
        success=True,
        message=f'Found {len(diseases)} detectable conditions',
        data={'diseases': diseases}
    ))


@app.route('/api/analyze', methods=['POST'])
def analyze_plant():
    """
    Main endpoint for plant disease detection
    This is where the magic happens!
    
    Expects:
        - POST request with image file
        - File should be in 'image' field of form-data
    
    Returns:
        - Disease detection results
        - Detailed information about the disease
        - Treatment recommendations
    """
    
    try:
        # Step 1: Validate that an image was sent
        if 'image' not in request.files:
            return jsonify(generate_response(
                success=False,
                message='No image file provided. Please upload an image.'
            )), 400
        
        file = request.files['image']
        
        # Step 2: Check if a file was actually selected
        if file.filename == '':
            return jsonify(generate_response(
                success=False,
                message='No file selected'
            )), 400
        
        # Step 3: Validate file type
        if not allowed_file(file.filename):
            return jsonify(generate_response(
                success=False,
                message=f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            )), 400
        
        print(f"📸 Received image: {file.filename}")
        
        # Step 4: Read image data
        # We read it into memory instead of saving to disk (faster)
        image_data = file.read()
        
        # Optional: Check file size
        if len(image_data) > MAX_FILE_SIZE:
            return jsonify(generate_response(
                success=False,
                message='File too large. Maximum size is 10MB'
            )), 400
        
        print("🔍 Analyzing image with AI model...")
        
        # Step 5: Make prediction using our AI model
        prediction = model.predict(image_data)
        
        disease_key = prediction['disease_key']
        confidence = prediction['confidence']
        
        print(f"✓ Prediction complete: {disease_key} ({confidence}%)")
        # Get confidence message
        confidence_info = get_confidence_message(confidence, disease_key)
        
        # Step 6: Get detailed information from our database
        disease_info = get_disease_info(disease_key)
        
        if not disease_info:
            return jsonify(generate_response(
                success=False,
                message='Disease information not found in database'
            )), 500
        
        # Step 7: Determine if plant is healthy or diseased
        plant_is_healthy = is_healthy(disease_key)
        
        # Step 8: Build comprehensive response
        result = {
            # Basic prediction info
            'diseaseDetected': not plant_is_healthy,
            'confidence': confidence,
            'confidenceLevel': confidence_info['level'],
            'confidenceWarning': confidence_info['message'],
            'confidenceColor': confidence_info['color'],
            
            # Plant information
            'plantName': disease_info['plantName'],
            'diseaseName': disease_info.get('diseaseName'),
            'scientificName': disease_info.get('scientificName'),
            
            # Health status
            'healthStatus': 'Healthy' if plant_is_healthy else 'Diseased',
            'severity': disease_info.get('severity', 'Unknown'),
            
            # Detailed information
            'description': disease_info.get('description', ''),
            'symptoms': disease_info.get('symptoms', []),
            'causes': disease_info.get('causes', []),
            'solutions': disease_info.get('solutions', []),
            'preventiveCare': disease_info.get('preventiveCare', []),
            
            # Environmental factors
            'environmentalFactors': disease_info.get('environmentalFactors', {}),
            
            # Metadata
            'analysisDate': datetime.now().isoformat(),
            'modelVersion': '1.0-demo'
        }
        
        print("✓ Analysis complete! Sending response...")
        
        return jsonify(generate_response(
            success=True,
            message='Analysis completed successfully',
            data=result
        ))
    
    except Exception as e:
        # If anything goes wrong, log the error and return error response
        print(f"❌ Error during analysis: {str(e)}")
        print(traceback.format_exc())  # Print full error trace for debugging
        
        return jsonify(generate_response(
            success=False,
            message=f'Error analyzing image: {str(e)}'
        )), 500


@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """
    AI chat endpoint for personalized plant advice
    Users can ask any plant-related questions
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify(generate_response(
                success=False,
                message='No message provided'
            )), 400
        
        user_message = data['message']
        context = data.get('context')  # Optional context from recent analysis
        
        print(f"💬 Chat request: {user_message}")
        
        # Get AI response
        ai_response = ai_assistant.get_response(user_message, context)
        
        return jsonify(generate_response(
            success=True,
            message='Response generated',
            data={
                'response': ai_response,
                'timestamp': datetime.now().isoformat()
            }
        ))
    
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify(generate_response(
            success=False,
            message=f'Error: {str(e)}'
        )), 500
# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors (page not found)"""
    return jsonify(generate_response(
        success=False,
        message='Endpoint not found'
    )), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors (server errors)"""
    return jsonify(generate_response(
        success=False,
        message='Internal server error'
    )), 500


# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌱 PlantCare AI Server Starting...")
    print("="*60)
    print("\n📡 Server will be available at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    # Start Flask development server
    # debug=True enables auto-reload when code changes
    # host='0.0.0.0' makes it accessible from other devices on network
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )