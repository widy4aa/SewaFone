#!/bin/bash

PROJECT_NAME="flask_api_mvc"

# Buat folder
mkdir -p $PROJECT_NAME/app/{models,controllers,routes,services}
mkdir -p $PROJECT_NAME/migrations

# File global
touch $PROJECT_NAME/.env
touch $PROJECT_NAME/requirements.txt

# run.py
cat > $PROJECT_NAME/run.py <<EOF
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
EOF

# app/__init__.py
cat > $PROJECT_NAME/app/__init__.py <<EOF
from flask import Flask
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    return app
EOF

# app/config.py
cat > $PROJECT_NAME/app/config.py <<EOF
# Kosongkan atau isi sesuai kebutuhan
EOF

# __init__.py di setiap folder
touch $PROJECT_NAME/app/models/__init__.py
touch $PROJECT_NAME/app/controllers/__init__.py
touch $PROJECT_NAME/app/routes/__init__.py
touch $PROJECT_NAME/app/services/__init__.py

# app/models/user_model.py (data dump di sini)
cat > $PROJECT_NAME/app/models/user_model.py <<EOF
dummy_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]
EOF

# app/controllers/user_controller.py
cat > $PROJECT_NAME/app/controllers/user_controller.py <<EOF
from flask import jsonify
from app.models.user_model import dummy_users

def get_users():
    return jsonify(dummy_users)
EOF

# app/routes/user_routes.py
cat > $PROJECT_NAME/app/routes/user_routes.py <<EOF
from flask import Blueprint
from app.controllers.user_controller import get_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users_route():
    return get_users()
EOF

# app/services/user_service.py
cat > $PROJECT_NAME/app/services/user_service.py <<EOF
# Kosongkan untuk sementara
EOF

echo "✅ Struktur Flask MVC dengan data dummy berhasil dibuat di '$PROJECT_NAME'"
