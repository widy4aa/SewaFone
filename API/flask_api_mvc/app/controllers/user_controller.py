from flask import jsonify
from app.models.user_model import User
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
from psycopg2 import errors

def read_all_user():
    try:
        users = User.get_all()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def read_user(id):
    try:
        users = User.get_by_id(id)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def create_user(data):
    try:
        new_user = User.create(data)
        
        if 'pass' in new_user:
            del new_user['pass']

        return jsonify(new_user), 201

    except errors.UniqueViolation as e:
        return jsonify({"error": "Username atau email sudah terdaftar."}), 409 # 

    except Exception as e:
        return jsonify({"error": "Terjadi kesalahan pada server", "details": str(e)}), 500
    
