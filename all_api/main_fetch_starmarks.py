# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector
# from mysql.connector import Error
# from datetime import datetime
# import re

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

# # Function to classify the search input
# def classify_search_input(input_value):
#     # Email detection based on presence of '@' and 'com'
#     if '@' in input_value and 'com' in input_value:
#         return "email", input_value

#     # Phone regex pattern (assuming phone numbers are digits only)
#     phone_pattern = re.compile(r"^\d+$")

#     if phone_pattern.match(input_value):
#         return "phone", input_value

#     # Query types
#     return "query_type", input_value

# @app.route('/fetch_star_marked', methods=['GET'])
# def fetch_star_marked():
#     connection = get_db_connection()
#     if not connection:
#         return jsonify({"message": "Failed to connect to the database."}), 500

#     try:
#         cursor = connection.cursor()

#         # Fetch query parameters
#         start_date = request.args.get("start_date")
#         end_date = request.args.get("end_date")
#         query_type = request.args.get("query_type")
#         search_input = request.args.get("search")

#         # Define the base query to fetch data with 'bookmark' value 'marked'
#         query = """
#         WITH ranked_sessions AS (
#             SELECT sd.session_no, sd.user_id,
#                    RANK() OVER (PARTITION BY sd.user_id ORDER BY sd.session_no) AS visit_rank
#             FROM session_data sd
#             WHERE sd.bookmark = 'marked'
#         )
#         SELECT sd.*, ui.user_email_id, ui.mobile_number, qa.question, qa.answer, qa.record_id,
#                rs.visit_rank
#         FROM session_data sd
#         LEFT JOIN ranked_sessions rs ON sd.session_no = rs.session_no AND sd.user_id = rs.user_id
#         LEFT JOIN user_info ui ON sd.user_id = ui.user_id
#         LEFT JOIN qa_pairs qa ON sd.session_no = qa.session_no
#         WHERE sd.bookmark = 'marked'
#         """

#         conditions = []
#         params = []

#         # Add date conditions if start_date and end_date are provided
#         if start_date and end_date:
#             conditions.append("DATE(sd.session_date) BETWEEN %s AND %s")
#             params.extend([start_date, end_date])

#         # Add query_type condition if provided
#         if query_type:
#             conditions.append("sd.query_type = %s")
#             params.append(query_type)

#         # Add search input condition if provided
#         if search_input:
#             key, value = classify_search_input(search_input)
#             if key == "email":
#                 conditions.append("ui.user_email_id = %s")
#                 params.append(value)
#             elif key == "phone":
#                 conditions.append("ui.mobile_number LIKE %s")
#                 params.append(f"%{value}%")
#             elif key == "query_type":
#                 conditions.append("sd.query_type LIKE %s")
#                 params.append(f"%{value}%")

#         # Append conditions to the query
#         if conditions:
#             query += " AND " + " AND ".join(conditions)

#         query += " ORDER BY sd.session_no DESC, qa.record_id;"

#         print("Query:", query)  # Debug: Print the query for verification

#         cursor.execute(query, tuple(params))
#         result = cursor.fetchall()
#         columns = [col[0] for col in cursor.description]

#         data = {}
#         for row in result:
#             session_no = row[columns.index('session_no')]
#             if session_no not in data:
#                 data[session_no] = {
#                     "user_id": row[columns.index('user_id')],
#                     "session_no": session_no,
#                     "record_id": row[columns.index('record_id')],
#                     "visit_rank": row[columns.index('visit_rank')],
#                     "start_time": row[columns.index('start_time')].isoformat() if isinstance(row[columns.index('start_time')], datetime) else row[columns.index('start_time')],
#                     "end_time": row[columns.index('end_time')].isoformat() if isinstance(row[columns.index('end_time')], datetime) else row[columns.index('end_time')],
#                     "session_date": row[columns.index('session_date')].isoformat() if isinstance(row[columns.index('session_date')], datetime) else row[columns.index('session_date')],
#                     "query_type": row[columns.index('query_type')],
#                     "sessionID": row[columns.index('sessionID')],
#                     "user_email_id": row[columns.index('user_email_id')],
#                     "mobile_number": row[columns.index('mobile_number')],
#                     "bookmark": row[columns.index('bookmark')],
#                     "conversation": []
#                 }

#             # Append question-answer pairs if available
#             if row[columns.index('question')] and row[columns.index('answer')]:
#                 data[session_no]["conversation"].append({
#                     "question": row[columns.index('question')],
#                     "answer": row[columns.index('answer')]
#                 })

#         final_data = list(data.values())
#         record_count = len(final_data)
#         connection.commit()

#         print("Fetched data:", final_data)  # Debug: Print the fetched data for verification

#         if record_count == 0:
#             return jsonify({"message": "No records found with 'marked' bookmark.", "data": [], "record_count": record_count})

#         return jsonify({"message": "successful", "data": final_data, "record_count": record_count})

#     except Error as e:
#         print("Error executing query:", e)
#         return jsonify({"message": "An error occurred while fetching data."}), 500
#     finally:
#         cursor.close()
#         connection.close()

# if __name__ == '__main__':
#     app.run(debug=True, port=7080, host="0.0.0.0")

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# Establish MySQL connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL", e)
        return None

# Function to classify the search input
def classify_search_input(input_value):
    # Email detection based on presence of '@' and 'com'
    if '@' in input_value and 'com' in input_value:
        return "email", input_value

    # Phone regex pattern (assuming phone numbers are digits only)
    phone_pattern = re.compile(r"^\d+$")

    if phone_pattern.match(input_value):
        return "phone", input_value

    # Query types
    return "query_type", input_value

@app.route('/fetch_star_marked', methods=['GET'])
def fetch_star_marked():
    connection = get_db_connection()
    if not connection:
        return jsonify({"message": "Failed to connect to the database."}), 500

    try:
        cursor = connection.cursor()

        # Fetch query parameters
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        query_type = request.args.get("query_type")
        search_input = request.args.get("search")

        # Define the base query to fetch data with 'bookmark' value 'marked'
        query = """
        WITH ranked_sessions AS (
            SELECT sd.session_no, sd.user_id,
                   RANK() OVER (PARTITION BY sd.user_id ORDER BY sd.session_no) AS visit_rank
            FROM session_data sd
            WHERE sd.bookmark = 'marked'
        )
        SELECT sd.*, ui.user_email_id, ui.mobile_number, qa.question, qa.answer, qa.record_id,
               rs.visit_rank
        FROM session_data sd
        LEFT JOIN ranked_sessions rs ON sd.session_no = rs.session_no AND sd.user_id = rs.user_id
        LEFT JOIN user_info ui ON sd.user_id = ui.user_id
        LEFT JOIN qa_pairs qa ON sd.session_no = qa.session_no
        WHERE sd.bookmark = 'marked'
        """

        conditions = []
        params = []

        # Add date conditions if start_date and end_date are provided
        if start_date and end_date:
            conditions.append("DATE(sd.session_date) BETWEEN %s AND %s")
            params.extend([start_date, end_date])

        # Add query_type condition if provided
        if query_type:
            conditions.append("sd.query_type = %s")
            params.append(query_type)

        # Add search input condition if provided
        if search_input:
            key, value = classify_search_input(search_input)
            if key == "email":
                conditions.append("ui.user_email_id = %s")
                params.append(value)
            elif key == "phone":
                conditions.append("ui.mobile_number LIKE %s")
                params.append(f"%{value}%")
            elif key == "query_type":
                conditions.append("sd.query_type LIKE %s")
                params.append(f"%{value}%")

        # Append conditions to the query
        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " ORDER BY sd.session_no DESC, qa.record_id;"

        print("Query:", query)  # Debug: Print the query for verification

        cursor.execute(query, tuple(params))
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        data = {}
        for row in result:
            session_no = row[columns.index('session_no')]
            if session_no not in data:
                data[session_no] = {
                    "user_id": row[columns.index('user_id')],
                    "session_no": session_no,
                    "record_id": row[columns.index('record_id')],
                    "visit_rank": row[columns.index('visit_rank')],
                    "start_time": row[columns.index('start_time')].isoformat() if isinstance(row[columns.index('start_time')], datetime) else row[columns.index('start_time')],
                    "end_time": row[columns.index('end_time')].isoformat() if isinstance(row[columns.index('end_time')], datetime) else row[columns.index('end_time')],
                    "session_date": row[columns.index('session_date')].isoformat() if isinstance(row[columns.index('session_date')], datetime) else row[columns.index('session_date')],
                    "query_type": row[columns.index('query_type')],
                    "sessionID": row[columns.index('sessionID')],
                    "user_email_id": row[columns.index('user_email_id')],
                    "mobile_number": row[columns.index('mobile_number')],
                    "bookmark": row[columns.index('bookmark')],
                    "conversation": []
                }

            # Append question-answer pairs if available
            if row[columns.index('question')] and row[columns.index('answer')]:
                data[session_no]["conversation"].append({
                    "question": row[columns.index('question')],
                    "answer": row[columns.index('answer')]
                })

        final_data = list(data.values())
        record_count = len(final_data)
        connection.commit()

        print("Fetched data:", final_data)  # Debug: Print the fetched data for verification

        if record_count == 0:
            return jsonify({"message": "No records found with 'marked' bookmark.", "data": [], "record_count": record_count})

        return jsonify({"message": "successful", "data": final_data, "record_count": record_count})

    except Error as e:
        print("Error executing query:", e)
        return jsonify({"message": "An error occurred while fetching data."}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=7080, host="0.0.0.0")
