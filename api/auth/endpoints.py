from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from helper.db_helper import get_connection
import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_endpoints = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_endpoints.route('/register', methods=['POST'])
def register():
    print("REGISTER CALLED")
    # Ambil data dari JSON atau form
    if request.is_json:
        data = request.get_json()
        nama = data.get('username')
        email = data.get('email')
        phone = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role = data.get('role', 'member')
    else:
        nama = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'member')
    status = 'active'

    # Validation
    if not nama or not email or not phone or not password or not confirm_password:
        return jsonify({"error": "Semua field wajib diisi"}), 400

    if password != confirm_password:
        return jsonify({"error": "Password dan konfirmasi password tidak sama"}), 400

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Check if the email is already in the database
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email sudah terdaftar"}), 409

            # Insert the new user (alamat, avatar_url diisi NULL)
            cursor.execute(
                "INSERT INTO users (nama, email, phone, alamat, avatar_url, password, role, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nama, email, phone, None, None, hashed_pw, role, status)
            )
            conn.commit()

        # Return success response
        return jsonify({"message": "User berhasil terdaftar"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@auth_endpoints.route('/login', methods=['POST'])
def login():
    # Get data from the request JSON body
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Validation
    if not email or not password or not role:
        return jsonify({"error": "Email, password, dan role wajib diisi"}), 400

    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Check if the user exists with provided email and role
            cursor.execute("SELECT * FROM users WHERE email = %s AND role = %s", (email, role))
            user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Create the JWT access token
            access_token = create_access_token(
                identity=str(user["id"]),
                additional_claims={
                    "email": user["email"],
                    "role": user["role"]
                }
            )
            return jsonify(
                access_token=access_token,
                role=user["role"],
                user_id=user["id"]
            ), 200

        return jsonify({"error": "Email atau password salah"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
