from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection

profileadmin_bp = Blueprint('profileadmin', __name__, url_prefix='/api/profile/admin')

@profileadmin_bp.route('', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({"error": "Invalid user ID"}), 400

    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT id, email, role, nama AS name, phone, alamat AS address, avatar_url
                FROM users
                WHERE id = %s
            """, (user_id,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found"}), 404

            if user['role'] != 'admin':
                return jsonify({"error": "Access denied"}), 403

            return jsonify(user), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()