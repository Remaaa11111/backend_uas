from flask import Blueprint, request, jsonify, current_app
from helper.db_helper import get_connection
import os

books_bp = Blueprint('books', __name__, url_prefix='/api/books')
ALLOWED_STATUS = ['available', 'not available']

#  GET all books
@books_bp.route('/', methods=['GET'])
def get_books():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

#  GET book details by ID
@books_bp.route('/<int:id_buku>', methods=['GET'])
def get_book_detail(id_buku):
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM books WHERE id_buku = %s", (id_buku,))
        book = cursor.fetchone()
    conn.close()

    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

#  POST create book (upload file or URL)
@books_bp.route('/create', methods=['POST'])
def create_book():
    data = request.form
    judul = data.get('judul')
    penulis = data.get('penulis')
    genre = data.get('genre')
    deskripsi = data.get('deskripsi')
    stok_buku = data.get('stok_buku')
    harga = data.get('harga')
    status = data.get('status', 'available')

    cover_image = None
    uploaded_file = request.files.get('cover_image')

    if uploaded_file and uploaded_file.filename != '':
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "img")
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(filepath)
        cover_image = uploaded_file.filename
    elif data.get('cover_image'):
        cover_image = data.get('cover_image')

    if not all([judul, penulis, deskripsi, stok_buku, harga]):
        return jsonify({"error": "Field judul, penulis, deskripsi, stok_buku, harga wajib diisi"}), 400
    if status not in ALLOWED_STATUS:
        return jsonify({"error": f"Status harus salah satu dari {ALLOWED_STATUS}"}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO books (judul, penulis, genre, cover_image, deskripsi, stok_buku, status, harga)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (judul, penulis, genre, cover_image, deskripsi, stok_buku, status, harga))
            conn.commit()
            new_id = cursor.lastrowid
        return jsonify({"message": "Book created", "id_buku": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

#  PUT update book
@books_bp.route('/update/<int:id_buku>', methods=['PUT'])
def update_book(id_buku):
    data = request.form
    judul = data.get('judul')
    penulis = data.get('penulis')
    genre = data.get('genre')
    deskripsi = data.get('deskripsi')
    stok_buku = data.get('stok_buku')
    harga = data.get('harga')
    status = data.get('status')

    uploaded_file = request.files.get('cover_image')
    cover_image = None

    if uploaded_file and uploaded_file.filename != '':
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "img")
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(filepath)
        cover_image = uploaded_file.filename
    elif data.get('cover_image'):
        cover_image = data.get('cover_image')

    if not all([judul, penulis, deskripsi, stok_buku, status, harga]):
        return jsonify({"error": "Semua field wajib diisi"}), 400
    if status not in ALLOWED_STATUS:
        return jsonify({"error": f"Status harus salah satu dari {ALLOWED_STATUS}"}), 400

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            if cover_image:
                cursor.execute("""
                    UPDATE books SET
                        judul=%s, penulis=%s, genre=%s, cover_image=%s,
                        deskripsi=%s, stok_buku=%s, status=%s, harga=%s
                    WHERE id_buku=%s
                """, (judul, penulis, genre, cover_image, deskripsi, stok_buku, status, harga, id_buku))
            else:
                cursor.execute("""
                    UPDATE books SET
                        judul=%s, penulis=%s, genre=%s,
                        deskripsi=%s, stok_buku=%s, status=%s, harga=%s
                    WHERE id_buku=%s
                """, (judul, penulis, genre, deskripsi, stok_buku, status, harga, id_buku))
            conn.commit()
        return jsonify({"message": "Book updated", "id_buku": id_buku}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

#  DELETE book
@books_bp.route('/delete/<int:id_buku>', methods=['DELETE'])
def delete_book(id_buku):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE id_buku=%s", (id_buku,))
            conn.commit()
        return jsonify({"message": "Deleted", "id_buku": id_buku}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

#  UPLOAD cover image separately if desired (optional)
@books_bp.route('/upload', methods=['POST'])
def upload_cover():
    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename != '':
        try:
            upload_folder = current_app.config.get("UPLOAD_FOLDER", "img")
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, uploaded_file.filename)
            uploaded_file.save(file_path)
            return jsonify({
                "message": "Uploaded successfully",
                "file_path": file_path.replace("\\", "/")
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Upload failed, file not found"}), 400
