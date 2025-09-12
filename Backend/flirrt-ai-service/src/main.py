import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.ai_analysis import ai_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'flirrt-ai-secret-key-2025'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Flirrt.ai API Service - Ready for AI-powered flirting suggestions! 💕", 200

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return {
        'service': 'Flirrt.ai API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'ai_analysis': '/api/ai/analyze-screenshot',
            'health_check': '/api/ai/health',
            'test_suggestions': '/api/ai/test-suggestions'
        }
    }

if __name__ == '__main__':
    print("🚀 Starting Flirrt.ai API Service...")
    print("💕 AI-powered flirting suggestions ready!")
    app.run(host='0.0.0.0', port=5000, debug=True)
