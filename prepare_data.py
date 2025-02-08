# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from chromadb import PersistentClient

# # Load the model and tokenizer
# model_path = "/home/user/Desktop/meta-llama-Llama-3.2-1B/llm"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Function to perform chunking and embedding
# def chunk_and_embed_docs(documents, model):
#     inputs = tokenizer(documents, truncation=True, padding=True, return_tensors="pt")
#     with torch.no_grad():
#         embeddings = model.base_model(inputs["input_ids"]).last_hidden_state.mean(dim=1)
#     return embeddings

# # Initialize ChromaPersistentClient
# persist_directory = '/home/user/Desktop/meta-llama-Llama-3.2-1B/vector_db0'  # Path for persistent storage
# chroma_client = PersistentClient(path=persist_directory)

# # Function to process and store documents in Chroma
# def process_documents(directory_path):
#     documents = SimpleDirectoryReader(directory_path).load_data()
#     doc_texts = [doc.text for doc in documents]
#     embeddings = chunk_and_embed_docs(doc_texts, model)

#     # Create Chroma collection
#     collection = chroma_client.get_or_create_collection(name="knowledge_base")

#     # Separate documents and embeddings
#     documents_list = [doc.text for doc in documents]
#     embeddings_list = embeddings.tolist()

#     # Add documents and embeddings to Chroma collection
#     for i, (doc, emb) in enumerate(zip(documents_list, embeddings_list)):
#         collection.add(
#             embeddings=[emb],  # embeddings as list
#             documents=[doc],  # documents as list
#             metadatas=[{"source": "file"}],  # Example metadata, customize as needed
#             ids=[str(i)]  # Unique ID for each document
#         )

#     return collection

# def store_embeddings_in_chroma(directory_path, index_save_path):
#     collection = process_documents(directory_path)
#     # Optionally, save the vector store if necessary (not required for Chroma PersistentClient)
#     return collection

# # Load the model
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Specify document directory path
# documents_path = "/home/user/Desktop/meta-llama-Llama-3.2-1B/data"

# # Generate and store the embeddings, then save the index
# collection = store_embeddings_in_chroma(documents_path, persist_directory)

# # Optionally, print confirmation
# print(f"Index saved in Chroma at {persist_directory}")

# import os
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from chromadb import PersistentClient
# from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.core import SimpleDirectoryReader

# # Initialize the HuggingFace embedding model
# embedding_model_name = "BAAI/bge-small-en-v1.5"
# embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)

# # Initialize Chroma PersistentClient
# persist_directory = '/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/final_vectordb'
# chroma_client = PersistentClient(path=persist_directory)

# # Function to process and store documents in Chroma
# def process_documents(directory_path):
#     # Load documents from the specified directory
#     documents = SimpleDirectoryReader(directory_path).load_data()
#     doc_texts = [doc.text for doc in documents]
    
#     # Generate embeddings for the documents
#     embeddings = [embed_model.get_text_embedding(doc) for doc in doc_texts]

#     # Create or get an existing Chroma collection
#     collection = chroma_client.get_or_create_collection(name="knowledge_base")

#     # Add documents and embeddings to Chroma collection
#     for i, (doc, emb) in enumerate(zip(doc_texts, embeddings)):
#         collection.add(
#             embeddings=[emb],  # embeddings as a list
#             documents=[doc],  # documents as a list
#             metadatas=[{"source": "file"}],  # Example metadata, can be customized
#             ids=[str(i)]  # Unique ID for each document
#         )

#     return collection

# # Function to store embeddings in Chroma
# def store_embeddings_in_chroma(directory_path):
#     collection = process_documents(directory_path)
#     return collection




import os
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from chromadb import PersistentClient
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import SimpleDirectoryReader

# Load environment variables
load_dotenv()

# Fetch credentials and paths from .env file
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
CHROMA_STORAGE_PATH = os.getenv("CHROMA_STORAGE_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Initialize the HuggingFace embedding model
embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

# Initialize Chroma PersistentClient
chroma_client = PersistentClient(path=CHROMA_STORAGE_PATH)

# Function to process and store documents in Chroma
def process_documents(directory_path):
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(directory_path).load_data()
    doc_texts = [doc.text for doc in documents]
    
    # Generate embeddings for the documents
    embeddings = [embed_model.get_text_embedding(doc) for doc in doc_texts]

    # Create or get an existing Chroma collection
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    # Add documents and embeddings to Chroma collection
    for i, (doc, emb) in enumerate(zip(doc_texts, embeddings)):
        collection.add(
            embeddings=[emb],  # embeddings as a list
            documents=[doc],  # documents as a list
            metadatas=[{"source": "file"}],  # Example metadata, can be customized
            ids=[str(i)]  # Unique ID for each document
        )

    return collection

# Function to store embeddings in Chroma
def store_embeddings_in_chroma(directory_path):
    collection = process_documents(directory_path)
    return collection

if __name__ == "__main__":
    DOCUMENT_DIRECTORY = os.getenv("DOCUMENT_DIRECTORY")
    if not DOCUMENT_DIRECTORY:
        print("Error: DOCUMENT_DIRECTORY not set in .env file.")
    else:
        try:
            store_embeddings_in_chroma(DOCUMENT_DIRECTORY)
            print(f"Documents processed and stored in Chroma collection '{COLLECTION_NAME}'.")
        except Exception as e:
            print(f"Failed to process documents: {e}")
