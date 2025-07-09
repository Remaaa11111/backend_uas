from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection

members_bp = Blueprint('members', __name__, url_prefix='/api/members')

# ✅ GET semua anggota
@members_bp.route('/', methods=['GET'])
def get_members():
    conn = get_connection()
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM members")
        results = cursor.fetchall()
    conn.close()
    return jsonify(results)

# ✅ POST tambah anggota
@members_bp.route('/create', methods=['POST'])
def create_member():
    data = request.form
    nama = data.get('nama')
    telepon = data.get('telepon')
    email = data.get('email')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO members (nama, telepon, email) VALUES (%s, %s, %s)", (nama, telepon, email))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Member created", "id_anggota": new_id}), 201

# ✅ PUT update anggota
@members_bp.route('/update/<int:id_anggota>', methods=['PUT'])
def update_member(id_anggota):
    data = request.form
    nama = data.get('nama')
    telepon = data.get('telepon')
    email = data.get('email')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE members SET nama=%s, telepon=%s, email=%s WHERE id_anggota=%s", (nama, telepon, email, id_anggota))
        conn.commit()
    conn.close()
    return jsonify({"message": "Member updated"})

# ✅ DELETE anggota
@members_bp.route('/delete/<int:id_anggota>', methods=['DELETE'])
def delete_member(id_anggota):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM members WHERE id_anggota=%s", (id_anggota,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Member deleted"})
