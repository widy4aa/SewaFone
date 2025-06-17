from flask import Blueprint, jsonify, request
from app.controllers.user_controller import read_all_user,read_user,create_user
from flask_jwt_extended import jwt_required, get_jwt_identity 


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users_route():
    return read_all_user()

@user_bp.route('/<int:id>', methods=['GET'])
def get_users_by_id(id):
    return read_user(id)

@user_bp.route('/add', methods=['POST'])
def post_user():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Data tidak boleh kosong"}), 400

    required_fields = ['username', 'email', 'pass', 'nama']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Field '{field}' wajib diisi"}), 400
        
    return create_user(data)