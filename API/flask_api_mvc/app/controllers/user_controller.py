from flask import jsonify
from app.models.user_model import dummy_users

def get_users():
    return jsonify(dummy_users)
