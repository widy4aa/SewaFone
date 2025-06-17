from flask import Blueprint, request, jsonify
from app.models.user_model import User
from werkzeug.security import check_password_hash 
from flask_jwt_extended import create_access_token 


auth = Blueprint('auth_bp', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # ... (kode untuk ambil data dan validasi) ...
    data = request.get_json()
    if not data or not data.get('username') or not data.get('pass'):
        return jsonify({"msg": "Username dan password wajib diisi"}), 400

    username = data.get('username')
    password_candidate = data.get('pass')

    user = User.get_by_username(username)

    if user and check_password_hash(user['pass'], password_candidate):
        
        # --- PERBAIKAN DI SINI ---
        # Ubah user['id'] (integer) menjadi string sebelum dijadikan identity
        user_id_string = str(user['id'])
        access_token = create_access_token(identity=user_id_string)
        # -------------------------

        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Username atau password salah"}), 401