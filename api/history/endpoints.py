from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection

history_bp = Blueprint('history', __name__, url_prefix='/api/history')
ALLOWED_STATUS = ['dipinjam', 'returned', 'canceled']


# GET semua logs (admin)
@history_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_logs():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT h.id_log, h.id_peminjaman, b.judul AS judul_buku,
                   h.status, h.waktu, h.keterangan
            FROM history_log h
            JOIN loans l ON h.id_peminjaman = l.id_peminjaman
            JOIN books b ON l.book_id = b.id_buku
            ORDER BY h.waktu DESC
        """)
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200


# GET log berdasarkan loan id (misalnya detail 1 peminjaman)
@history_bp.route('/<int:id_peminjaman>', methods=['GET'])
@jwt_required()
def get_logs_by_peminjaman(id_peminjaman):
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT id_log, status, waktu, keterangan
            FROM history_log
            WHERE id_peminjaman = %s
            ORDER BY waktu DESC
        """, (id_peminjaman,))
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200


# GET log user yang sedang login (dinamis dari JWT)
@history_bp.route('/me', methods=['GET'])
@jwt_required()
def get_logs_for_current_user():
    user_id = get_jwt_identity()
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT h.id_log, h.id_peminjaman, b.judul AS judul_buku,
                   h.status, h.waktu, h.keterangan
            FROM history_log h
            JOIN loans l ON h.id_peminjaman = l.id_peminjaman
            JOIN books b ON l.book_id = b.id_buku
            WHERE l.user_id = %s
            ORDER BY h.waktu DESC
        """, (user_id,))
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200


#  POST tambah log baru
@history_bp.route('/create', methods=['POST'])
@jwt_required()
def create_log():
    data = request.form
    id_peminjaman = data.get('id_peminjaman')
    status = data.get('status')
    keterangan = data.get('keterangan', '')

    if not id_peminjaman or status not in ALLOWED_STATUS:
        return jsonify({"error": f"id_peminjaman dan status wajib. Status harus salah satu dari {ALLOWED_STATUS}"}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO history_log (id_peminjaman, status, keterangan)
                VALUES (%s, %s, %s)
            """, (id_peminjaman, status, keterangan))
            conn.commit()
            new_id = cursor.lastrowid
        return jsonify({"message": "Log created", "id_log": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
