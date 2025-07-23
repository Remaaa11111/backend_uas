from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection
from datetime import datetime, timedelta

loans_bp = Blueprint('loans', __name__, url_prefix='/api/loans')

ALLOWED_STATUS = ['scheduled', 'borrowed', 'returned', 'overdue', 'cancelled']

def translate_status(status):
    return status

@loans_bp.route('/', methods=['GET'])
@jwt_required()
def get_loans():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                l.id_peminjaman, 
                l.user_id,
                u.email AS email_user, 
                b.judul AS judul_buku,
                l.tanggal_pinjam, 
                l.tanggal_kembali, 
                l.status
            FROM loans l
            JOIN users u ON l.user_id = u.id
            JOIN books b ON l.book_id = b.id_buku
            ORDER BY l.id_peminjaman DESC
        """)
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

@loans_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_loans_by_user(user_id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                l.id_peminjaman, 
                l.user_id,
                u.email AS email_user, 
                b.judul AS judul_buku,
                l.tanggal_pinjam, 
                l.tanggal_kembali, 
                l.status
            FROM loans l
            JOIN users u ON l.user_id = u.id
            JOIN books b ON l.book_id = b.id_buku
            WHERE l.user_id = %s
            ORDER BY l.id_peminjaman DESC
        """, (user_id,))
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

@loans_bp.route('/<int:id_peminjaman>', methods=['GET'])
@jwt_required()
def get_loan_by_id(id_peminjaman):
    try:
        conn = get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT 
                    l.id_peminjaman, l.user_id, l.book_id,
                    u.email AS email_user, 
                    b.judul AS judul_buku,
                    l.tanggal_pinjam, l.tanggal_kembali, l.status
                FROM loans l
                JOIN users u ON l.user_id = u.id
                JOIN books b ON l.book_id = b.id_buku
                WHERE l.id_peminjaman = %s
            """, (id_peminjaman,))
            loan = cursor.fetchone()

        if not loan:
            return jsonify({"error": "Data peminjaman tidak ditemukan"}), 404

        return jsonify(loan), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@loans_bp.route('/create', methods=['POST'])
@jwt_required()
def create_loan():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    tanggal_pinjam = data.get('tanggal_pinjam')
    tanggal_kembali = data.get('tanggal_kembali')
    status = data.get('status', 'borrowed')

    if not all([user_id, book_id, tanggal_pinjam, tanggal_kembali]):
        return jsonify({"error": "Semua field wajib diisi"}), 400

    if status not in ALLOWED_STATUS:
        return jsonify({"error": f"Status harus salah satu dari {ALLOWED_STATUS}"}), 400

    translated_status = translate_status(status)

    try:
        conn = get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT stok_buku, status FROM books WHERE id_buku = %s", (book_id,))
            book = cursor.fetchone()

            if not book:
                return jsonify({"error": "Buku tidak ditemukan"}), 404
            if book['stok_buku'] <= 0 or book['status'] == 'not available':
                return jsonify({"error": "Buku tidak tersedia untuk dipinjam"}), 400

            new_stok = book['stok_buku'] - 1
            new_status = 'not available' if new_stok == 0 else 'available'
            cursor.execute("""
                UPDATE books SET stok_buku = %s, status = %s WHERE id_buku = %s
            """, (new_stok, new_status, book_id))

            cursor.execute("""
                INSERT INTO loans (user_id, book_id, tanggal_pinjam, tanggal_kembali, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, book_id, tanggal_pinjam, tanggal_kembali, status))
            new_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO history_log (id_peminjaman, status, keterangan)
                VALUES (%s, %s, %s)
            """, (new_id, translated_status, f"Peminjaman dibuat dengan status {translated_status}"))

            conn.commit()
        return jsonify({"message": "Loan created, stock updated, and history logged", "id_peminjaman": new_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@loans_bp.route('/update/<int:id_peminjaman>', methods=['PUT'])
@jwt_required()
def update_loan(id_peminjaman):
    data = request.json
    status = data.get('status')
    tanggal_kembali_input = data.get('tanggal_kembali')

    if status not in ALLOWED_STATUS:
        return jsonify({"error": "Status tidak valid"}), 400

    translated_status = translate_status(status)

    try:
        conn = get_connection()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT l.tanggal_pinjam, l.book_id, l.status AS current_status, b.stok_buku 
                FROM loans l 
                JOIN books b ON l.book_id = b.id_buku 
                WHERE l.id_peminjaman = %s
            """, (id_peminjaman,))
            loan = cursor.fetchone()

            if not loan:
                return jsonify({"error": "Data peminjaman tidak ditemukan"}), 404

            tanggal_pinjam = loan['tanggal_pinjam']
            book_id = loan['book_id']
            current_status = loan['current_status']
            current_stok = loan['stok_buku']

            if status == 'borrowed':
                tanggal_kembali = (tanggal_pinjam + timedelta(days=7)).strftime('%Y-%m-%d')
            elif tanggal_kembali_input:
                tanggal_kembali = tanggal_kembali_input
            else:
                return jsonify({"error": "Tanggal kembali wajib diisi"}), 400

            cursor.execute("""
                UPDATE loans 
                SET tanggal_kembali = %s, status = %s 
                WHERE id_peminjaman = %s
            """, (tanggal_kembali, status, id_peminjaman))

            if status in ['returned', 'cancelled', 'canceled'] and current_status not in ['cancelled', 'canceled']:
                new_stok = current_stok + 1
                cursor.execute("""
                    UPDATE books SET stok_buku = %s, status = 'available' WHERE id_buku = %s
                """, (new_stok, book_id))

            cursor.execute("""
                INSERT INTO history_log (id_peminjaman, status, keterangan)
                VALUES (%s, %s, %s)
            """, (id_peminjaman, translated_status, f"Status diubah ke {translated_status}"))

            conn.commit()

        return jsonify({"message": "Loan updated & history logged", "id_peminjaman": id_peminjaman}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@loans_bp.route('/delete/<int:id_peminjaman>', methods=['DELETE'])
@jwt_required()
def delete_loan(id_peminjaman):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM loans WHERE id_peminjaman=%s", (id_peminjaman,))
            conn.commit()
        return jsonify({"message": "Loan deleted", "id_peminjaman": id_peminjaman}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()