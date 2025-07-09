from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# GET all users
@users_bp.route('/', methods=['GET'])
@jwt_required()  # Optional, only accessible by admin or authorized users
def get_users():
    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, email, role, status FROM users")
            users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# DELETE user
@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Optional, requires authentication
def delete_user(id):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (id,))
            conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
