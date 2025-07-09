# File: api/data_protected/endpoints.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

protected_endpoints = Blueprint('protected', __name__, url_prefix='/api/protected')

@protected_endpoints.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Halo, {current_user}! Ini adalah endpoint yang dilindungi."})
