# from llama_index.llms.ollama import Ollama
# from llama_index.core import VectorStoreIndex, Settings
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from sentence_transformers import SentenceTransformer, util
# import chromadb
# import json
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Fetch credentials and paths from .env file
# CHROMA_STORAGE_PATH = os.getenv("CHROMA_STORAGE_PATH")
# QNA_DOCUMENT_PATH = os.getenv("QNA_DOCUMENT_PATH")
# LLAMA_MODEL = os.getenv("LLAMA_MODEL")
# EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
# SEMANTIC_MODEL = os.getenv("SEMANTIC_MODEL")
# COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# # Load Q&A document
# def load_qna_document(path):
#     with open(path, "r") as file:
#         return json.load(file)

# # Initialize models
# llm = Ollama(model=LLAMA_MODEL)
# embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
# semantic_model = SentenceTransformer(SEMANTIC_MODEL)  # For Q&A semantic search

# Settings.llm = llm
# Settings.embed_model = embed_model

# # Load index from Chroma VectorStore
# def load_index_from_chroma_vectorstore(storage_path):
#     try:
#         db = chromadb.PersistentClient(path=storage_path)
#         chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
#         chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
#         index = VectorStoreIndex.from_vector_store(vector_store=chroma_vector_store)
#         return index
#     except Exception as e:
#         raise RuntimeError(f"Failed to load Chroma VectorStore: {e}")

# # Define the prompt template
# PROMPT_TEMPLATE = """
# You are an AI Assistant representing Shyena Tech Yarns Pvt. Ltd., a data-science company. 
# Your role is to provide concise and accurate responses strictly based on company data stored in the vector database and Q&A document. 
# Provide a clear, plain response and do not mention the reference of vector database and Q&A document.

# Previous Conversations:
# {chat_history}

# Question: {question}
# Answer:
# """

# # Q&A semantic search
# def find_similar_qna(query, qna_data, threshold=0.7):
#     questions = [item["question"] for item in qna_data]
#     query_embedding = semantic_model.encode(query, convert_to_tensor=True)
#     question_embeddings = semantic_model.encode(questions, convert_to_tensor=True)
#     scores = util.pytorch_cos_sim(query_embedding, question_embeddings).squeeze()
#     best_match_idx = scores.argmax()
#     if scores[best_match_idx] >= threshold:
#         return qna_data[best_match_idx]["answer"]
#     return None

# # Synthesize response using prompt-template
# def synthesize_response_with_prompt(query, chunks, chat_history):
#     if not chunks:
#         return "I'm sorry, I couldn't find relevant information in the database."

#     # Combine all retrieved chunks into one coherent text
#     retrieved_text = " ".join([chunk.text.strip() for chunk in chunks if chunk.text])

#     # Format the prompt using the retrieved text and chat history
#     response_input = PROMPT_TEMPLATE.format(chat_history=chat_history, question=query) + retrieved_text

#     try:
#         # Generate response using the LLM
#         response = llm.complete(prompt=response_input)

#         # Extract the response content
#         if hasattr(response, "content"):
#             return response.content.strip()
#         return str(response).strip()
#     except Exception as e:
#         return "I'm sorry, I encountered an issue generating the response."

# # Check if the query is domain-related
# def is_valid_query(query):
#     valid_keywords = ["company", "services", "products", "Shyena Tech Yarns", "data science"]
#     return any(keyword in query.lower() for keyword in valid_keywords)

# # Chatbot interaction loop
# def query_chatbot(index, qna_data):
#     chat_history = []  # Initialize chat history

#     while True:
#         query = input("Enter your query (or type 'exit' to quit): ").strip()
#         if query.lower() == "exit":
#             print("Exiting chatbot. Goodbye!")
#             break
#         if not query:
#             print("Empty query. Please try again.")
#             continue

#         # Search the Q&A document
#         qna_response = find_similar_qna(query, qna_data)
#         if qna_response:
#             chat_history.append(f"User: {query}\nAssistant: {qna_response}")
#             print(f"Assistant: {qna_response}")
#             continue

#         # Check if the query is domain-related
#         if not is_valid_query(query):
#             generic_response = "I'm sorry, I can't respond to that."
#             chat_history.append(f"User: {query}\nAssistant: {generic_response}")
#             print(f"Assistant: {generic_response}")
#             continue

#         try:
#             # Retrieve chunks and generate the response
#             query_engine = index.as_query_engine()
#             response_chunks = query_engine.retrieve(query)
#             response = synthesize_response_with_prompt(query, response_chunks, "\n".join(chat_history))
#             chat_history.append(f"User: {query}\nAssistant: {response}")
#             print(f"Assistant: {response}")
#         except Exception as e:
#             error_response = "I'm sorry, I encountered an issue generating the response."
#             chat_history.append(f"User: {query}\nAssistant: {error_response}")
#             print(f"Error during query execution: {e}")

# # Load model, index, and Q&A data, then start the chatbot
# if __name__ == "__main__":
#     try:
#         qna_data = load_qna_document(QNA_DOCUMENT_PATH)
#         index = load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)
#         query_chatbot(index, qna_data)
#     except Exception as e:
#         print(f"Failed to start chatbot: {e}")

from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sentence_transformers import SentenceTransformer, util
import chromadb
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch credentials and paths from .env file
CHROMA_STORAGE_PATH = os.getenv("CHROMA_STORAGE_PATH")
QNA_DOCUMENT_PATH = os.getenv("QNA_DOCUMENT_PATH")
LLAMA_MODEL = os.getenv("LLAMA_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
SEMANTIC_MODEL = os.getenv("SEMANTIC_MODEL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Load Q&A document
def load_qna_document(path):
    with open(path, "r") as file:
        return json.load(file)

# Initialize models
llm = Ollama(model=LLAMA_MODEL)
embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
semantic_model = SentenceTransformer(SEMANTIC_MODEL)  # For Q&A semantic search

Settings.llm = llm
Settings.embed_model = embed_model

# Load index from Chroma VectorStore
def load_index_from_chroma_vectorstore(storage_path):
    try:
        db = chromadb.PersistentClient(path=storage_path)
        chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
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

# Synthesize response using prompt-template
def synthesize_response_with_prompt(query, chunks, chat_history):
    if not chunks:
        return "I'm sorry, I couldn't find relevant information in the database."

    # Combine all retrieved chunks into one coherent text
    retrieved_text = " ".join([chunk.text.strip() for chunk in chunks if chunk.text])

    # Format the prompt using the retrieved text and chat history
    formatted_chat_history = "\n".join(chat_history)
    response_input = PROMPT_TEMPLATE.format(chat_history=formatted_chat_history, question=query) + retrieved_text

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
            response = synthesize_response_with_prompt(query, response_chunks, chat_history)
            chat_history.append(f"User: {query}\nAssistant: {response}")
            print(f"Assistant: {response}")
        except Exception as e:
            error_response = "I'm sorry, I encountered an issue generating the response."
            chat_history.append(f"User: {query}\nAssistant: {error_response}")
            print(f"Error during query execution: {e}")

# Load model, index, and Q&A data, then start the chatbot
if __name__ == "__main__":
    try:
        qna_data = load_qna_document(QNA_DOCUMENT_PATH)
        index = load_index_from_chroma_vectorstore(CHROMA_STORAGE_PATH)
        query_chatbot(index, qna_data)
    except Exception as e:
        print(f"Failed to start chatbot: {e}")
