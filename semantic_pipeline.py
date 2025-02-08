from llama_index.llms.ollama import Ollama
from sentence_transformers import SentenceTransformer, util
import json

# Define paths
QNA_DOCUMENT_PATH = "/home/user/Desktop/copy/meta-llama-Llama-3.2-1B/Q&A.json"

# Load Q&A document
def load_qna_document(path):
    with open(path, "r") as file:
        return json.load(file)

# Initialize models
llm = Ollama(model="llama3.2:1b")
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")  # For Q&A semantic search

# Define the prompt template
PROMPT_TEMPLATE = """
You are an AI Assistant representing Shyena Tech Yarns Pvt. Ltd., a data-science company.
Your role is to provide concise and accurate responses strictly based on company data stored in the Q&A document.
Provide a clear, plain response and do not mention the reference of the Q&A document.

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
def synthesize_response_with_prompt(query, chat_history):
    # Format the prompt using the chat history and query
    response_input = PROMPT_TEMPLATE.format(chat_history=chat_history, question=query)

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
def query_chatbot(qna_data):
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
            # Generate the response
            response = synthesize_response_with_prompt(query, "\n".join(chat_history))
            chat_history.append(f"User: {query}\nAssistant: {response}")
            print(f"Assistant: {response}")
        except Exception as e:
            error_response = "I'm sorry, I encountered an issue generating the response."
            chat_history.append(f"User: {query}\nAssistant: {error_response}")
            print(f"Error during query execution: {e}")

# Load Q&A data and start the chatbot
if __name__ == "__main__":
    try:
        qna_data = load_qna_document(QNA_DOCUMENT_PATH)
        query_chatbot(qna_data)
    except Exception as e:
        print(f"Failed to start chatbot: {e}")
