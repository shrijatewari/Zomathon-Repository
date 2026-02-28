"""
Flask API Service for Kitchen Prep Time (KPT) Prediction

This API provides a REST endpoint to predict kitchen prep time based on
restaurant load indicators.

Endpoint: /predict
Method: POST
Input: JSON with queue_length and orders_last_10min
Output: JSON with predicted_prep_time
"""

from flask import Flask, request, jsonify
import pickle
import os
import numpy as np
import pandas as pd

app = Flask(__name__)

# Global variable to store the loaded model
model = None

# Default handover delay estimation parameters
# These are estimated from the training data distribution
# handover_delay typically ranges from 1-5 minutes with correlation to queue_length
DEFAULT_HANDOVER_DELAY_BASE = 2.5  # Base delay in minutes
HANDOVER_DELAY_QUEUE_FACTOR = 0.1  # Additional delay per queue item


def load_model():
    """
    Load the trained XGBoost model from disk.
    
    Returns:
    --------
    model: Trained XGBoost model
    """
    global model
    if model is None:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'kpt_model.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                "Please train the model first using the notebook."
            )
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        print(f"Model loaded successfully from {model_path}")
    
    return model


def estimate_handover_delay(queue_length):
    """
    Estimate handover delay based on queue length.
    
    In production, this would be calculated from real-time restaurant load data.
    For now, we estimate it based on the correlation observed in training data.
    
    Parameters:
    -----------
    queue_length : int
        Number of orders in the queue
    
    Returns:
    --------
    float
        Estimated handover delay in minutes
    """
    # Estimate delay: base + queue impact + small random variation
    estimated_delay = (
        DEFAULT_HANDOVER_DELAY_BASE + 
        queue_length * HANDOVER_DELAY_QUEUE_FACTOR +
        np.random.normal(0, 0.3)  # Small random variation
    )
    
    # Ensure delay is within realistic bounds (0.5 to 6 minutes)
    estimated_delay = max(0.5, min(estimated_delay, 6.0))
    
    return estimated_delay


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
    --------
    JSON response with status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'KPT Prediction API is running'
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict kitchen prep time based on restaurant load indicators.
    
    Expected JSON input:
    {
        "queue_length": int (0-20),
        "orders_last_10min": int (0-50)
    }
    
    Returns:
    --------
    JSON response with predicted prep time:
    {
        "predicted_prep_time": float (minutes),
        "queue_length": int,
        "orders_last_10min": int,
        "estimated_handover_delay": float
    }
    """
    try:
        # Load model if not already loaded
        model = load_model()
        
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input data
        if data is None:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
        
        # Extract and validate queue_length
        if 'queue_length' not in data:
            return jsonify({
                'error': 'Missing required field: queue_length'
            }), 400
        
        queue_length = data['queue_length']
        if not isinstance(queue_length, (int, float)) or queue_length < 0:
            return jsonify({
                'error': 'queue_length must be a non-negative number'
            }), 400
        
        queue_length = int(queue_length)
        
        # Extract and validate orders_last_10min
        if 'orders_last_10min' not in data:
            return jsonify({
                'error': 'Missing required field: orders_last_10min'
            }), 400
        
        orders_last_10min = data['orders_last_10min']
        if not isinstance(orders_last_10min, (int, float)) or orders_last_10min < 0:
            return jsonify({
                'error': 'orders_last_10min must be a non-negative number'
            }), 400
        
        orders_last_10min = int(orders_last_10min)
        
        # Estimate handover_delay based on queue_length
        estimated_handover_delay = estimate_handover_delay(queue_length)
        
        # Prepare features for prediction
        # Model expects: queue_length, orders_last_10min, handover_delay
        features = pd.DataFrame({
            'queue_length': [queue_length],
            'orders_last_10min': [orders_last_10min],
            'handover_delay': [estimated_handover_delay]
        })
        
        # Make prediction
        predicted_prep_time = model.predict(features)[0]
        
        # Ensure prediction is positive (realistic constraint)
        predicted_prep_time = max(0.0, float(predicted_prep_time))
        
        # Return prediction
        return jsonify({
            'predicted_prep_time': round(predicted_prep_time, 4),
            'queue_length': queue_length,
            'orders_last_10min': orders_last_10min,
            'estimated_handover_delay': round(estimated_handover_delay, 4)
        }), 200
    
    except FileNotFoundError as e:
        return jsonify({
            'error': str(e)
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500


@app.route('/', methods=['GET'])
def index():
    """
    API documentation endpoint.
    
    Returns:
    --------
    JSON response with API information
    """
    return jsonify({
        'name': 'Kitchen Prep Time (KPT) Prediction API',
        'version': '1.0.0',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            },
            '/predict': {
                'method': 'POST',
                'description': 'Predict kitchen prep time',
                'input': {
                    'queue_length': 'int (0-20) - Number of orders in queue',
                    'orders_last_10min': 'int (0-50) - Orders in last 10 minutes'
                },
                'output': {
                    'predicted_prep_time': 'float - Predicted prep time in minutes',
                    'queue_length': 'int - Input queue length',
                    'orders_last_10min': 'int - Input orders count',
                    'estimated_handover_delay': 'float - Estimated handover delay'
                }
            }
        },
        'example_request': {
            'url': '/predict',
            'method': 'POST',
            'body': {
                'queue_length': 10,
                'orders_last_10min': 25
            }
        }
    }), 200


if __name__ == '__main__':
    # Load model on startup
    try:
        load_model()
        print("="*60)
        print("KPT Prediction API Server")
        print("="*60)
        print("Model loaded successfully!")
        print("\nAvailable endpoints:")
        print("  GET  /              - API documentation")
        print("  GET  /health        - Health check")
        print("  POST /predict       - Predict prep time")
        print("\nStarting Flask server...")
        print("="*60)
        
        # Run Flask app
        # In production, use a proper WSGI server like gunicorn
        app.run(host='0.0.0.0', port=5000, debug=True)
    
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Please train the model first using the notebook:")
        print("  notebooks/kpt_prediction.ipynb")
