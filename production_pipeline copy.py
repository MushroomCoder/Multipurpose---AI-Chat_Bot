

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from datetime import datetime
import prepare_data
import a

app = Flask(__name__)
CORS(app)

# MySQL Connection Pool
db_config = {
    'host': '164.52.195.88',
    'user': 'root',
    'password': 'Unknown!345',
    'database': 'chatbot_db',
    'port': 3312
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_connection():
    return connection_pool.get_connection()

# Import necessary functions from prepare_data.py and a.py
from prepare_data import store_embeddings_in_chroma
from a import load_index_from_chroma_vectorstore, find_similar_qna, synthesize_response_with_prompt, is_valid_query

# Load Q&A document and index
QNA_DOCUMENT_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/Q&A.json"
CHROMA_STORAGE_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/final_vectordb"
qna_data = a.load_qna_document(QNA_DOCUMENT_PATH)
index = a.load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)

# API Endpoints
@app.route('/pdf_upload', methods=['POST'])
def vector_store():
    try:
        data = request.json
        pdf_path = data.get("pdf_path")
        

        if not pdf_path:
            return jsonify({"error": "PDF path is required"}), 400

        status = store_embeddings_in_chroma(pdf_path)
        return jsonify({'status': status}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route("/pdf_query", methods=["POST"])
# def pdf_query():
#     connection = None
#     cursor = None
#     try:
#         data = request.json
#         question = data.get("question")
#         print(">>>>", data)
#         if not question:
#             raise ValueError("Question not provided")

#         connection = get_connection()
#         cursor = connection.cursor(buffered=True)

#         query = """SELECT session_no FROM session_data WHERE sessionID=%s;"""
#         cursor.execute(query, (data["sessionID"],))
#         result = cursor.fetchone()
#         print(">>>>>>>>>>>>>>>>>>4", result)

#         if result is None:
#             raise ValueError("Invalid session ID")

#         # Query the chatbot
#         qna_response = find_similar_qna(question, qna_data)
#         if qna_response:
#             ans = qna_response
#         else:
#             if not is_valid_query(question):
#                 ans = "I'm sorry, I can't respond to that."
#             else:
#                 query_engine = index.as_query_engine()
#                 response_chunks = query_engine.retrieve(question)
#                 ans = synthesize_response_with_prompt(question, response_chunks, "")

#         print(">>>>>>>>>>>>>>>>>>5", ans)

#         ins_query = """INSERT INTO qa_pairs (session_no, question, answer)
#                        VALUES (%s, %s, %s);"""
#         cursor.execute(ins_query, (result[0], question, ans))
#         connection.commit()
#         print(">>>>>>>>>>>>>>>>>>6")

#         return jsonify({"answer": str(ans)})

#     except mysql.connector.Error as err:
#         print("MySQL error:", err)
#         return jsonify({'error': "Database error"}), 500
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': str(e)}), 500
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()


@app.route("/pdf_query", methods=["POST"])
def pdf_query():
    connection = None
    cursor = None
    try:
        data = request.json
        question = data.get("question")
        print(">>>>", data)
        if not question:
            raise ValueError("Question not provided")

 

        # Query the chatbot
        qna_response = find_similar_qna(question, qna_data)
        if qna_response:
            ans = qna_response
        else:
            if not is_valid_query(question):
                ans = "I'm sorry, I can't respond to that."
            else:
                query_engine = index.as_query_engine()
                response_chunks = query_engine.retrieve(question)
                ans = synthesize_response_with_prompt(question, response_chunks, "")

        print(">>>>>>>>>>>>>>>>>>5", ans)



        return jsonify({"answer": str(ans)})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500




@app.route("/submit", methods=["POST"])
def submit():
    connection = None
    cursor = None
    try:
        session_ip = request.json
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT user_email_id FROM user_info")
        existing_emails = [row[0] for row in cursor.fetchall()]

        today = datetime.today().strftime('%Y-%m-%d')

        if session_ip["email"] not in existing_emails:
            query = """INSERT INTO user_info (user_email_id, mobile_number)
                       VALUES (%s, %s);"""
            cursor.execute(query, (session_ip["email"], session_ip["phone"]))
            connection.commit()

            cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
            result = cursor.fetchone()

            ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
                           VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
            connection.commit()

            return jsonify(message="New user added"), 201
        else:
            cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
            result = cursor.fetchone()

            ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
                           VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
            connection.commit()

            return jsonify(message="Session created for existing user"), 200
    except mysql.connector.Error as err:
        print("MySQL error:", err)
        return jsonify(error="Database error"), 500
    except Exception as e:
        print("Error:", e)
        return jsonify(error="Internal server error"), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=7072, host="0.0.0.0")
