# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector
# from mysql.connector import Error

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# # Establish MySQL connection
# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="164.52.195.88",
#             user='root',
#             passwd='Unknown!345',
#             database="chatbot_db",
#             port=3312
#         )
#         return connection
#     except Error as e:
#         print("Error connecting to MySQL", e)
#         return None

# @app.route('/update_bookmark', methods=['POST'])
# def update_bookmark():
#     connection = get_db_connection()
#     if not connection:
#         return jsonify({"message": "Failed to connect to the database."}), 500

#     cursor = connection.cursor()

#     # Fetch JSON data from the request
#     data = request.get_json()
#     session_no = data.get("session_no")
#     bookmark_status = data.get("bookmark")

#     # Validate session_no
#     if not session_no:
#         return jsonify({"message": "Missing or invalid session_no."}), 400

#     # Handle the case where bookmark_status is an empty string
#     if bookmark_status == "":
#         bookmark_status = "unmarked"  # Default value

#     # Validate bookmark_status
#     elif bookmark_status not in ["marked", "unmarked"]:
#         return jsonify({"message": "Invalid bookmark status. Must be 'marked' or 'unmarked'."}), 400

#     # Update the bookmark status in the database
#     update_query = """
#         UPDATE session_data
#         SET bookmark = %s
#         WHERE session_no = %s
#     """
#     try:
#         cursor.execute(update_query, (bookmark_status, session_no))
#         connection.commit()
#         if cursor.rowcount > 0:
#             return jsonify({"message": "Bookmark updated successfully."})
#         else:
#             return jsonify({"message": "Session not found."}), 404
#     except Error as e:
#         print(f"Error: {e}")
#         return jsonify({"message": "An error occurred while updating the bookmark."}), 500
#     finally:
#         cursor.close()  # Ensure the cursor is closed after the operation
#         connection.close()  # Ensure the connection is closed after the operation

# if __name__ == '__main__':
#     app.run(debug=True, port=7078, host="0.0.0.0")

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# Establish MySQL connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),  # Get the host from .env
            user=os.getenv("DB_USER"),  # Get the user from .env
            passwd=os.getenv("DB_PASSWORD"),  # Get the password from .env
            database=os.getenv("DB_NAME"),  # Get the database from .env
            port=int(os.getenv("DB_PORT"))  # Get the port from .env
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL", e)
        return None

@app.route('/update_bookmark', methods=['POST'])
def update_bookmark():
    connection = get_db_connection()
    if not connection:
        return jsonify({"message": "Failed to connect to the database."}), 500

    cursor = connection.cursor()

    # Fetch JSON data from the request
    data = request.get_json()
    session_no = data.get("session_no")
    bookmark_status = data.get("bookmark")

    # Validate session_no
    if not session_no:
        return jsonify({"message": "Missing or invalid session_no."}), 400

    # Handle the case where bookmark_status is an empty string
    if bookmark_status == "":
        bookmark_status = "unmarked"  # Default value

    # Validate bookmark_status
    elif bookmark_status not in ["marked", "unmarked"]:
        return jsonify({"message": "Invalid bookmark status. Must be 'marked' or 'unmarked'."}), 400

    # Update the bookmark status in the database
    update_query = """
        UPDATE session_data
        SET bookmark = %s
        WHERE session_no = %s
    """
    try:
        cursor.execute(update_query, (bookmark_status, session_no))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "Bookmark updated successfully."})
        else:
            return jsonify({"message": "Session not found."}), 404
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while updating the bookmark."}), 500
    finally:
        cursor.close()  # Ensure the cursor is closed after the operation
        connection.close()  # Ensure the connection is closed after the operation

if __name__ == '__main__':
    app.run(debug=True, port=7078, host="0.0.0.0")
