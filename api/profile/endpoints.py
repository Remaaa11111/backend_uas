from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

@profile_bp.route('', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({"error": "Invalid user id in token"}), 400

    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Ambil data user
            cursor.execute("""
                SELECT id, email, role, nama, phone, alamat, avatar_url
                FROM users
                WHERE id = %s
            """, (user_id,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Hitung statistik peminjaman
            cursor.execute("SELECT COUNT(*) AS borrowed FROM loans WHERE user_id = %s", (user_id,))
            borrowed = cursor.fetchone()['borrowed']

            cursor.execute("SELECT COUNT(*) AS returned FROM loans WHERE user_id = %s AND status = 'returned'", (user_id,))
            returned = cursor.fetchone()['returned']

            cursor.execute("SELECT COUNT(*) AS overdue FROM loans WHERE user_id = %s AND status = 'overdue'", (user_id,))
            overdue = cursor.fetchone()['overdue']

            # Gabungkan hasil ke response
            user['borrowed'] = borrowed
            user['returned'] = returned
            user['overdue'] = overdue

            return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@profile_bp.route('/update', methods=['PATCH'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({"error": "Invalid user id in token"}), 400

    data = request.get_json()
    nama = data.get('nama')
    phone = data.get('phone')
    alamat = data.get('alamat')
    avatar_url = data.get('avatar_url')

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET nama = %s, phone = %s, alamat = %s, avatar_url = %s
                WHERE id = %s
            """, (nama, phone, alamat, avatar_url, user_id))
            conn.commit()
            return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
