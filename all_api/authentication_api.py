import os
from dotenv import load_dotenv
import sys
sys.path.append('/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/all_api')

from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

# Load environment variables
load_dotenv()

# Fetch credentials from .env
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS"))

# Initialize database connection
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)

app = Flask(__name__)
CORS(app)

# Configuring the JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=JWT_EXPIRATION_HOURS)

jwtm = JWTManager(app)

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    cursor = connection.cursor()
    try:
        if password != confirm_password:
            return jsonify(message="Password and confirm password do not match"), 400

        hashed_password = generate_password_hash(password)

        # Check if the email is already registered
        cursor.execute("SELECT * FROM t_app_user WHERE email = %s", [email])
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify(message="Email already registered"), 409

        # Insert new user
        cursor.execute("INSERT INTO t_app_user (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        connection.commit()
        cursor.close()

        return jsonify(message="User registered successfully"), 201

    except Exception as e:
        print("Exception at register: ", str(e))
        return jsonify(message="Something Went Wrong"), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM t_app_user WHERE email = %s", [email])
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            access_token = create_access_token(identity={'id': user[0], 'name': user[1], 'email': user[2]})
            return jsonify(access_token=access_token), 200

        return jsonify(message="Invalid credentials"), 401

    except Exception as e:
        print("Exception at login: ", str(e))
        return jsonify(message="Something Went Wrong"), 500


@app.route('/verify_user', methods=['POST'])
def check_user():
    data = request.get_json()
    email = data['email']

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_app_user WHERE email = %s", [email])
    existing_user = cursor.fetchone()
    cursor.close()

    if existing_user:
        reset_token = jwt.encode(
            {'email': email, 'exp': datetime.utcnow() + timedelta(hours=1)},
            app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify(exists=True, reset_token=reset_token), 200
    else:
        return jsonify(exists=False), 404


@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data['token']
    new_password = data['new_password']
    confirm_password = data['confirm_password']

    if new_password != confirm_password:
        return jsonify(message="Password and confirm password do not match"), 400

    try:
        decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        email = decoded_token['email']
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token has expired"), 400
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token"), 400

    hashed_password = generate_password_hash(new_password)

    cursor = connection.cursor()
    cursor.execute("UPDATE t_app_user SET password = %s WHERE email = %s", (hashed_password, email))
    connection.commit()
    cursor.close()

    return jsonify(message="Password reset successfully"), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=False, port=7071, host="0.0.0.0")
