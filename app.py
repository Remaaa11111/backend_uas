# app.py

"""Library Management App - Basic Flask CRUD"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from config import Config
from flasgger import Swagger

# Import all endpoint blueprints
from api.books.endpoints import books_bp
from api.members.endpoints import members_bp
from api.loans.endpoints import loans_bp
from api.book_types.endpoints import book_types_bp

# (Opsional) auth & protected endpoint
from api.auth.endpoints import auth_endpoints
from api.data_protected.endpoints import protected_endpoints

# (Opsional) static file handler
from static.static_file_server import static_file_server

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Allow CORS & JWT
CORS(app)
jwt.init_app(app)

# Enable Swagger UI
Swagger(app)

# Register blueprints
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(loans_bp)
app.register_blueprint(book_types_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

print(app.url_map)
