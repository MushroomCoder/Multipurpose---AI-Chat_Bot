# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# import mysql.connector
# from mysql.connector import pooling
# from datetime import datetime
# import prepare_data
# import a

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# # MySQL Connection Pool
# db_config = {
#     'host': '164.52.195.88',
#     'user': 'root',
#     'password': 'Unknown!345',
#     'database': 'chatbot_db',
#     'port': 3312
# }

# connection_pool = mysql.connector.pooling.MySQLConnectionPool(
#     pool_name="mypool",
#     pool_size=5,
#     **db_config
# )

# def get_connection():
#     return connection_pool.get_connection()

# # Import necessary functions from prepare_data.py and a.py
# from prepare_data import store_embeddings_in_chroma
# from a import load_index_from_chroma_vectorstore, find_similar_qna, synthesize_response_with_prompt, is_valid_query

# # Load Q&A document and index
# QNA_DOCUMENT_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/Q&A.json"
# CHROMA_STORAGE_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/final_vectordb"
# qna_data = a.load_qna_document(QNA_DOCUMENT_PATH)
# index = a.load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)

# # API Endpoints
# @app.route('/pdf_upload', methods=['POST'])
# def vector_store():
#     try:
#         data = request.json
#         pdf_path = data.get("pdf_path")

#         if not pdf_path:
#             return jsonify({"error": "PDF path is required"}), 400

#         status = store_embeddings_in_chroma(pdf_path)
#         return jsonify({'status': status}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route("/pdf_query", methods=["POST"])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# def pdf_query():
#     connection = None
#     cursor = None
#     try:
#         data = request.json
#         question = data.get("question")
#         print(">>>>", data)
#         if not question:
#             raise ValueError("Question not provided")

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

#         return jsonify({"answer": str(ans)})

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': str(e)}), 500

# @app.route("/submit", methods=["POST"])
# def submit():
#     connection = None
#     cursor = None
#     try:
#         session_ip = request.json
#         connection = get_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT user_email_id FROM user_info")
#         existing_emails = [row[0] for row in cursor.fetchall()]

#         today = datetime.today().strftime('%Y-%m-%d')

#         if session_ip["email"] not in existing_emails:
#             query = """INSERT INTO user_info (user_email_id, mobile_number)
#                        VALUES (%s, %s);"""
#             cursor.execute(query, (session_ip["email"], session_ip["phone"]))
#             connection.commit()

#             cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
#             result = cursor.fetchone()

#             ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
#                            VALUES (%s, %s, %s, %s, %s);"""
#             cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
#             connection.commit()

#             return jsonify(message="New user added"), 201
#         else:
#             cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
#             result = cursor.fetchone()

#             ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
#                            VALUES (%s, %s, %s, %s, %s);"""
#             cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
#             connection.commit()

#             return jsonify(message="Session created for existing user"), 200

#     except mysql.connector.Error as err:
#         print("MySQL error:", err)
#         return jsonify(error="Database error"), 500

#     except Exception as e:
#         print("Error:", e)
#         return jsonify(error="Internal server error"), 500

#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# if __name__ == '__main__':
#     app.run(debug=True, port=7072, host="0.0.0.0")


# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# import mysql.connector
# from mysql.connector import pooling
# from datetime import datetime
# import os
# from dotenv import load_dotenv

# # Load environment variables from the .env1 file
# load_dotenv(".env1")

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# # MySQL Connection Pool
# db_config = {
#     'host': os.getenv('DB_HOST'),
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'database': os.getenv('DB_NAME'),
#     'port': int(os.getenv('DB_PORT'))
# }

# connection_pool = mysql.connector.pooling.MySQLConnectionPool(
#     pool_name="mypool",
#     pool_size=5,
#     **db_config
# )

# def get_connection():
#     return connection_pool.get_connection()

# # Import necessary functions from prepare_data.py and a.py
# from prepare_data import store_embeddings_in_chroma
# import a

# # Load Q&A document and index
# QNA_DOCUMENT_PATH = os.getenv('QNA_DOCUMENT_PATH')
# CHROMA_STORAGE_PATH = os.getenv('CHROMA_STORAGE_PATH')
# qna_data = a.load_qna_document(QNA_DOCUMENT_PATH)
# index = a.load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)

# # API Endpoints
# @app.route('/pdf_upload', methods=['POST'])
# def vector_store():
#     try:
#         data = request.json
#         pdf_path = data.get("pdf_path")

#         if not pdf_path:
#             return jsonify({"error": "PDF path is required"}), 400

#         status = store_embeddings_in_chroma(pdf_path)
#         return jsonify({'status': status}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route("/pdf_query", methods=["POST"])
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# def pdf_query():
#     connection = None
#     cursor = None
#     try:
#         data = request.json
#         question = data.get("question")
#         print(">>>>", data)
#         if not question:
#             raise ValueError("Question not provided")

#         # Query the chatbot
#         qna_response = a.find_similar_qna(question, qna_data)
#         if qna_response:
#             ans = qna_response
#         else:
#             if not a.is_valid_query(question):
#                 ans = "I'm sorry, I can't respond to that."
#             else:
#                 query_engine = index.as_query_engine()
#                 response_chunks = query_engine.retrieve(question)
#                 ans = a.synthesize_response_with_prompt(question, response_chunks, "")

#         print(">>>>>>>>>>>>>>>>>>5", ans)

#         return jsonify({"answer": str(ans)})

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': str(e)}), 500

# @app.route("/submit", methods=["POST"])
# def submit():
#     connection = None
#     cursor = None
#     try:
#         session_ip = request.json
#         connection = get_connection()
#         cursor = connection.cursor()

#         cursor.execute("SELECT user_email_id FROM user_info")
#         existing_emails = [row[0] for row in cursor.fetchall()]

#         today = datetime.today().strftime('%Y-%m-%d')

#         if session_ip["email"] not in existing_emails:
#             query = """INSERT INTO user_info (user_email_id, mobile_number)
#                        VALUES (%s, %s);"""
#             cursor.execute(query, (session_ip["email"], session_ip["phone"]))
#             connection.commit()

#             cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
#             result = cursor.fetchone()

#             ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
#                            VALUES (%s, %s, %s, %s, %s);"""
#             cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
#             connection.commit()

#             return jsonify(message="New user added"), 201
#         else:
#             cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
#             result = cursor.fetchone()

#             ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
#                            VALUES (%s, %s, %s, %s, %s);"""
#             cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
#             connection.commit()

#             return jsonify(message="Session created for existing user"), 200

#     except mysql.connector.Error as err:
#         print("MySQL error:", err)
#         return jsonify(error="Database error"), 500

#     except Exception as e:
#         print("Error:", e)
#         return jsonify(error="Internal server error"), 500

#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# if __name__ == '__main__':
#     app.run(debug=True, port=7072, host="0.0.0.0")

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
from mysql.connector import pooling, Error
from datetime import datetime
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from chromadb import PersistentClient
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from sentence_transformers import SentenceTransformer, util
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

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
    try:
        return connection_pool.get_connection()
    except Error as err:
        print(f"Error: {err}")
        raise

# Initialize the HuggingFace embedding model
embedding_model_name = "BAAI/bge-small-en-v1.5"
embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)

# Initialize Chroma PersistentClient
persist_directory = '/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/final_vectordb'
chroma_client = PersistentClient(path=persist_directory)

# Function to process and store documents in Chroma
def process_documents(directory_path):
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(directory_path).load_data()
    doc_texts = [doc.text for doc in documents]

    # Generate embeddings for the documents
    embeddings = [embed_model.get_text_embedding(doc) for doc in doc_texts]

    # Create or get an existing Chroma collection
    collection_name = "knowledge_base"
    chroma_collection = chroma_client.get_or_create_collection(name=collection_name)

    # Add documents and embeddings to Chroma collection
    for i, (doc, emb) in enumerate(zip(doc_texts, embeddings)):
        chroma_collection.add(
            embeddings=[emb],  # embeddings as a list
            documents=[doc],  # documents as a list
            metadatas=[{"source": "file"}],  # Example metadata, can be customized
            ids=[str(i)]  # Unique ID for each document
        )

    return chroma_collection

# Function to store embeddings in Chroma
def store_embeddings_in_chroma(directory_path):
    collection = process_documents(directory_path)
    return collection

# Load Q&A document
def load_qna_document(path):
    with open(path, "r") as file:
        return json.load(file)

# Initialize models
llm = Ollama(model="llama3.2:1b")
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")  # For Q&A semantic search

Settings.llm = llm
Settings.embed_model = embed_model

# Load index from Chroma VectorStore
def load_index_from_chroma_vectorstore(storage_path):
    try:
        db = PersistentClient(path=storage_path)
        collection_name = "knowledge_base"
        chroma_collection = db.get_or_create_collection(collection_name)
        chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store=chroma_vector_store)
        return index
    except Exception as e:
        raise RuntimeError(f"Failed to load Chroma VectorStore: {e}")

# Define the prompt template
PROMPT_TEMPLATE = """
You are an AI Assistant representing Shyena Tech Yarns Pvt. Ltd., a data-science company.
Your role is to provide concise and accurate responses strictly based on company data stored in the vector database and Q&A document.
Provide a clear, plain response and do not mention the reference of vector database and Q&A document.

Previous Conversations:
{chat_history}

Question: {question}
Answer:
"""

# Q&A semantic search
def find_similar_qna(query, qna_data, threshold=0.7):
    questions = [item["question"] for item in qna_data]
    query_embedding = semantic_model.encode(query, convert_to_tensor=True)
    question_embeddings = semantic_model.encode(questions, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, question_embeddings).squeeze()
    best_match_idx = scores.argmax()
    if scores[best_match_idx] >= threshold:
        return qna_data[best_match_idx]["answer"]
    return None

# Synthesize response using prompt template
def synthesize_response_with_prompt(query, chunks, chat_history):
    if not chunks:
        return "I'm sorry, I couldn't find relevant information in the database."

    # Combine all retrieved chunks into one coherent text
    retrieved_text = " ".join([chunk.text.strip() for chunk in chunks if chunk.text])

    # Format the prompt using the retrieved text and chat history
    response_input = PROMPT_TEMPLATE.format(chat_history=chat_history, question=query) + retrieved_text

    try:
        # Generate response using the LLM
        response = llm.complete(prompt=response_input)

        # Extract the response content
        if hasattr(response, "content"):
            return response.content.strip()
        return str(response).strip()
    except Exception as e:
        return "I'm sorry, I encountered an issue generating the response."

# Check if the query is domain-related
def is_valid_query(query):
    valid_keywords = ["company", "services", "products", "Shyena Tech Yarns", "data science"]
    return any(keyword in query.lower() for keyword in valid_keywords)

# Chatbot interaction loop
def query_chatbot(index, qna_data):
    chat_history = []  # Initialize chat history

    while True:
        query = input("Enter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("Exiting chatbot. Goodbye!")
            break
        if not query:
            print("Empty query. Please try again.")
            continue

        # Search the Q&A document
        qna_response = find_similar_qna(query, qna_data)
        if qna_response:
            chat_history.append(f"User: {query}\nAssistant: {qna_response}")
            print(f"Assistant: {qna_response}")
            continue

        # Check if the query is domain-related
        if not is_valid_query(query):
            generic_response = "I'm sorry, I can't respond to that."
            chat_history.append(f"User: {query}\nAssistant: {generic_response}")
            print(f"Assistant: {generic_response}")
            continue

        try:
            # Retrieve chunks and generate the response
            query_engine = index.as_query_engine()
            response_chunks = query_engine.retrieve(query)
            response = synthesize_response_with_prompt(query, response_chunks, "\n".join(chat_history))
            chat_history.append(f"User: {query}\nAssistant: {response}")
            print(f"Assistant: {response}")
        except Exception as e:
            error_response = "I'm sorry, I encountered an issue generating the response."
            chat_history.append(f"User: {query}\nAssistant: {error_response}")
            print(f"Error during query execution: {e}")

# Load Q&A document and index
QNA_DOCUMENT_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/Q&A.json"
CHROMA_STORAGE_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/final_vectordb"
qna_data = load_qna_document(QNA_DOCUMENT_PATH)
index = load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)

# API Endpoints
@app.route('/pdf_upload', methods=['POST'])
def pdf_upload():
    try:
        data = request.json
        pdf_path = data.get("pdf_path")

        if not pdf_path:
            return jsonify({"error": "PDF path is required"}), 400

        status = store_embeddings_in_chroma(pdf_path)
        return jsonify({'status': status}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/pdf_query", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>5", ans)

        # Insert conversation data into qa_pairs table
        connection = get_connection()
        cursor = connection.cursor()
        ins_query = """INSERT INTO qa_pairs (session_no, question, answer)
                       VALUES ((SELECT session_no FROM session_data WHERE sessionID = %s), %s, %s);"""
        cursor.execute(ins_query, (data["sessionID"], question, ans))
        connection.commit()
        print("Conversation data inserted")

        return jsonify({"answer": str(ans)})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route("/submit", methods=["POST"])
def submit():
    connection = None
    cursor = None
    try:
        session_ip = request.json
        print("Received data:", session_ip)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT user_email_id FROM user_info")
        existing_emails = [row[0] for row in cursor.fetchall()]
        print("Existing emails:", existing_emails)

        today = datetime.today().strftime('%Y-%m-%d')
        print("Today's date:", today)

        if session_ip["email"] not in existing_emails:
            query = """INSERT INTO user_info (user_email_id, mobile_number)
                       VALUES (%s, %s);"""
            cursor.execute(query, (session_ip["email"], session_ip["phone"]))
            connection.commit()
            print("New user inserted")

            cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
            result = cursor.fetchone()
            print("User ID:", result[0])

            ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
                           VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
            connection.commit()
            print("New session data inserted")

            return jsonify(message="New user added"), 201
        else:
            cursor.execute("SELECT user_id FROM user_info WHERE user_email_id = %s;", (session_ip["email"],))
            result = cursor.fetchone()
            print("User ID:", result[0])

            ins_query = """INSERT INTO session_data (user_id, start_time, session_date, query_type, sessionID)
                           VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(ins_query, (result[0], session_ip["sessionINTime"], today, session_ip["optionName"], session_ip["sessionID"]))
            connection.commit()
            print("Session data inserted for existing user")

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
