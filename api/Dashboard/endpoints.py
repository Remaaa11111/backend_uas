from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper.db_helper import get_connection
from datetime import datetime

member_bp = Blueprint('member', __name__, url_prefix='/api/dashboard')

@member_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def member_dashboard():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except Exception:
        return jsonify({"error": "Invalid user ID in token"}), 400

    conn = get_connection()
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Buku sedang dipinjam user
            cursor.execute("""
                SELECT COUNT(*) AS borrowed
                FROM loans
                WHERE user_id = %s AND status = 'borrowed'
            """, (user_id,))
            borrowed = cursor.fetchone()['borrowed']

            # Buku sudah dikembalikan user
            cursor.execute("""
                SELECT COUNT(*) AS returned
                FROM loans
                WHERE user_id = %s AND status = 'returned'
            """, (user_id,))
            returned = cursor.fetchone()['returned']

            # Aktivitas terakhir
            cursor.execute("""
                SELECT b.judul, l.status, l.tanggal_pinjam, l.tanggal_kembali
                FROM loans l
                JOIN books b ON l.book_id = b.id_buku
                WHERE l.user_id = %s
                ORDER BY l.created_at DESC
                LIMIT 5
            """, (user_id,))
            activity = cursor.fetchall()
            for row in activity:
                row['tanggal_pinjam'] = row['tanggal_pinjam'].strftime('%Y-%m-%d') if row['tanggal_pinjam'] else None
                row['tanggal_kembali'] = row['tanggal_kembali'].strftime('%Y-%m-%d') if row['tanggal_kembali'] else None

            # Total buku
            cursor.execute("SELECT COUNT(*) AS total_books FROM books")
            total_books = cursor.fetchone()['total_books']

            # Buku tersedia
            cursor.execute("SELECT COUNT(*) AS books_available FROM books WHERE status = 'available'")
            books_available = cursor.fetchone()['books_available']

            # Statistik peminjaman bulanan oleh user
            cursor.execute("""
                SELECT DATE_FORMAT(tanggal_pinjam, '%%Y-%%m') AS bulan, COUNT(*) AS jumlah
                FROM loans
                WHERE user_id = %s
                GROUP BY bulan
                ORDER BY bulan DESC
                LIMIT 6
            """, (user_id,))
            borrow_chart = cursor.fetchall()
            borrow_chart.reverse()  # supaya urut dari lama ke terbaru

        return jsonify({
            "borrowed": borrowed,
            "returned": returned,
            "recent_activity": activity,
            "total_books": total_books,
            "books_available": books_available,
            "borrow_chart": borrow_chart
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()