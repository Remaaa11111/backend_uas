# File: api/loans/endpoints.py

from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection

loans_bp = Blueprint('loans', __name__, url_prefix='/api/loans')

# ✅ GET semua peminjaman
@loans_bp.route('/', methods=['GET'])
def get_loans():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM loans")
        results = cursor.fetchall()
    conn.close()
    return jsonify(results)

# ✅ POST tambah peminjaman
@loans_bp.route('/create', methods=['POST'])
def create_loan():
    data = request.form
    id_buku = data.get('id_buku')
    id_anggota = data.get('id_anggota')
    tanggal_pinjam = data.get('tanggal_pinjam')
    tanggal_kembali = data.get('tanggal_kembali')
    denda = data.get('denda', 0)

    if not all([id_buku, id_anggota, tanggal_pinjam, tanggal_kembali]):
        return jsonify({"error": "Semua field wajib diisi"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO loans (id_buku, id_anggota, tanggal_pinjam, tanggal_kembali, denda) VALUES (%s, %s, %s, %s, %s)",
            (id_buku, id_anggota, tanggal_pinjam, tanggal_kembali, denda)
        )
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Loan created", "id": new_id}), 201

# ✅ PUT update peminjaman
@loans_bp.route('/update/<int:id>', methods=['PUT'])
def update_loan(id):
    data = request.form
    tanggal_kembali = data.get('tanggal_kembali')
    denda = data.get('denda')

    if not tanggal_kembali or denda is None:
        return jsonify({"error": "Field tanggal_kembali dan denda wajib diisi"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE loans SET tanggal_kembali=%s, denda=%s WHERE id=%s", (tanggal_kembali, denda, id))
        conn.commit()
    conn.close()
    return jsonify({"message": "Loan updated"})

# ✅ DELETE peminjaman
@loans_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_loan(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM loans WHERE id=%s", (id,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Loan deleted"})
