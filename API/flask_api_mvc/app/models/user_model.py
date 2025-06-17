from koneksi import get_db
import psycopg2
import psycopg2.extras
from psycopg2 import errors
from werkzeug.security import generate_password_hash

class User:
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = 'SELECT * FROM "user" order by id;'
        cursor.execute(query)
        
        users_data = cursor.fetchall()
        cursor.close()
        
        return [dict(row) for row in users_data]

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = 'SELECT * FROM "user" WHERE id = %s;'
        cursor.execute(query, (user_id,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data is None:
            return None
            
        return dict(user_data)

    @staticmethod
    def create(data):
        """Membuat user baru dan menyimpannya ke database."""
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        hashed_password = generate_password_hash(data['pass'])

        query = """
            INSERT INTO "user" (
                username, email, pass, nama, no_telp, alamat, ktp, selfie, 
                latitude, longitude, point, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'inactive')
            RETURNING *;
        """

        user_values = (
            data['username'],
            data['email'],
            hashed_password, 
            data['nama'],
            data.get('no_telp'),
            data.get('alamat'),
            data.get('ktp'),
            data.get('selfie'),
            data.get('latitude'),
            data.get('longitude'),
            data.get('point', 15), 
        )

        try:
            cursor.execute(query, user_values)
            new_user = cursor.fetchone()
            conn.commit()
            cursor.close()
            return dict(new_user)
        except Exception as e:
            conn.rollback()
            cursor.close()
            raise e
        
    @staticmethod
    def get_by_username(username):
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """SELECT * FROM "user" WHERE username = %s;"""
        cursor.execute(query, (username,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            return dict(user_data)
        
        return None