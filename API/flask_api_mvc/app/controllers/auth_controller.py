from flask import Blueprint, request, jsonify
from app.models.user_model import User
from werkzeug.security import check_password_hash # Penting untuk membandingkan password
from flask_jwt_extended import create_access_token # Penting untuk membuat token

# Membuat Blueprint untuk auth. URL prefix /api akan menangani /api/login
bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint untuk login user.
    Menerima username & password, mengembalikan token JWT jika valid.
    """
    # 1. Ambil data JSON dari body request
    data = request.get_json()

    # 2. Lakukan validasi input dasar
    if not data or not data.get('username') or not data.get('pass'):
        return jsonify({"msg": "Username dan password wajib diisi"}), 400

    username = data.get('username')
    password_candidate = data.get('pass')

    # 3. Cari user di database menggunakan model
    user = User.get_by_username(username)

    # 4. Verifikasi: Cek apakah user ada DAN passwordnya cocok
    #    check_password_hash akan membandingkan password dari user dengan hash di DB
    if user and check_password_hash(user['pass'], password_candidate):
        
        # 5. Jika berhasil, buat token JWT.
        #    'identity' adalah penanda unik untuk user ini di dalam token (biasanya user ID)
        access_token = create_access_token(identity=user['id'])
        
        # 6. Kirim token sebagai response
        return jsonify(access_token=access_token), 200
    
    # 7. Jika user tidak ada atau password salah, kirim pesan error
    return jsonify({"msg": "Username atau password salah"}), 401 # 401 Unauthorized