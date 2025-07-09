from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection

book_types_bp = Blueprint('book_types', __name__, url_prefix='/api/book-types')

# ✅ GET semua jenis buku
@book_types_bp.route('/', methods=['GET'])
def get_book_types():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM book_types")
        results = cursor.fetchall()
    conn.close()
    return jsonify(results)

# ✅ POST tambah jenis buku
@book_types_bp.route('/create', methods=['POST'])
def create_book_type():
    data = request.form
    nama_jenis = data.get('nama_jenis')

    if not nama_jenis:
        return jsonify({"error": "nama_jenis is required"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO book_types (nama_jenis) VALUES (%s)", (nama_jenis,))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Book type created", "id_jenis": new_id}), 201

# ✅ PUT update jenis buku
@book_types_bp.route('/update/<int:id_jenis>', methods=['PUT'])
def update_book_type(id_jenis):
    data = request.form
    nama_jenis = data.get('nama_jenis')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE book_types SET nama_jenis=%s WHERE id_jenis=%s", (nama_jenis, id_jenis))
        conn.commit()
    conn.close()
    return jsonify({"message": "Book type updated"})

# ✅ DELETE jenis buku
@book_types_bp.route('/delete/<int:id_jenis>', methods=['DELETE'])
def delete_book_type(id_jenis):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM book_types WHERE id_jenis=%s", (id_jenis,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Book type deleted"})
