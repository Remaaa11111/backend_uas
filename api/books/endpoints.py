from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection
import os

books_bp = Blueprint('books', __name__, url_prefix='/api/books')
UPLOAD_FOLDER = "img"

#GET semua buku
@books_bp.route('/', methods=['GET'])
def get_books():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
    conn.close()
    return jsonify(results)


# POST tambah buku
@books_bp.route('/create', methods=['POST'])
def create_book():
    data = request.form
    judul = data.get('judul')
    penulis = data.get('penulis')
    id_jenis = data.get('id_jenis')
    status = data.get('status')
    tanggal_pinjam = data.get('tanggal_pinjam')
    tanggal_kembali = data.get('tanggal_kembali')
    cover_image = data.get('cover_image')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO books (judul, penulis, id_jenis, status, tanggal_pinjam, tanggal_kembali, cover_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (judul, penulis, id_jenis, status, tanggal_pinjam, tanggal_kembali, cover_image)
        )
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Book created", "id_buku": new_id}), 201

# ✅ PUT update buku
@books_bp.route('/update/<int:id_buku>', methods=['PUT'])
def update_book(id_buku):
    data = request.form
    judul = data.get('judul')
    penulis = data.get('penulis')
    id_jenis = data.get('id_jenis')
    status = data.get('status')
    tanggal_pinjam = data.get('tanggal_pinjam')
    tanggal_kembali = data.get('tanggal_kembali')
    cover_image = data.get('cover_image')

    if not all([judul, penulis, id_jenis]):
        return jsonify({"error": "judul, penulis, dan id_jenis wajib diisi"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE books SET
                judul=%s, penulis=%s, id_jenis=%s, status=%s,
                tanggal_pinjam=%s, tanggal_kembali=%s, cover_image=%s
            WHERE id_buku=%s
        """, (judul, penulis, id_jenis, status, tanggal_pinjam, tanggal_kembali, cover_image, id_buku))
        conn.commit()
    conn.close()
    return jsonify({"message": "Book updated"})

# DELETE buku
@books_bp.route('/delete/<int:id_buku>', methods=['DELETE'])
def delete_book(id_buku):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE id_buku=%s", (id_buku,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Deleted", "id_buku": id_buku})

# Upload cover image
@books_bp.route("/upload", methods=["POST"])
def upload_cover():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({"message": "Uploaded", "file_path": file_path})
    return jsonify({"message": "Upload failed"}), 400