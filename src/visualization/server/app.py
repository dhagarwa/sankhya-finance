from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.visualization.visualization_agent import VisualizationAgent

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# @app.route('/generate-visualization', methods=['OPTIONS'])
# def options():
#     print("Options request received")
#     response = app.response_class(status=200)
#     response.headers["Access-Control-Allow-Origin"] = "http://localhost:4321"
#     response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response



@app.route('/generate-visualization', methods=['POST'])
def generate_visualization():
    try:
        data = request.json
        prompt = data.get('prompt')
        visualization_data = {
            'company': ['Apple', 'Microsoft', 'Amazon'],
            '2022': [280, 250, 260],
            '2023': [300, 280, 280]
        }
        
        visualization_code = agent.generate_visualization_code(
            prompt=prompt,
            data=visualization_data
        )
        
        return jsonify({
            'visualizationCode': visualization_code,
            'data': visualization_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()
    
    # Initialize the visualization agent
    agent = VisualizationAgent(api_key=os.getenv('GOOGLE_API_KEY'))
    
    # Run with debug mode and allow all origins in development
    app.run(debug=True) 