from flask import Flask
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from extensions import jwt
from config import Config
from flasgger import Swagger
from flask import Blueprint
import os

# Import all endpoint blueprints
from api.books.endpoints import books_bp
from api.loans.endpoints import loans_bp
from api.history.endpoints import history_bp
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints
from static.static_file_server import static_file_server
from api.Dashboard.endpoints import member_bp
from api.profile.endpoints import profile_bp
from api.profileadmin.endpoints import profileadmin_bp 
from api.users.endpoints import users_bp

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

#  Add this so file uploads can be stored
app.config['UPLOAD_FOLDER'] = 'img'

# Check if the upload folder exists, if not, create it
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allow CORS & JWT
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])  # Adjust the origin if needed
jwt.init_app(app)

# Enable Swagger UI for API documentation
Swagger(app)

# Register blueprints for the different endpoints
app.register_blueprint(books_bp)
app.register_blueprint(loans_bp)
app.register_blueprint(auth_endpoints)
app.register_blueprint(protected_endpoints)
app.register_blueprint(history_bp)
app.register_blueprint(member_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(profileadmin_bp)
app.register_blueprint(users_bp)

# (Optional) Static file server for handling file uploads
app.register_blueprint(static_file_server)

# Sample route to test CORS for specific route
@app.route('/api/data')
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def data():
    return "CORS is enabled for this route."

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Print the URL map for debugging purposes
print(app.url_map)
