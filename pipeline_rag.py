# import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Define the prompt for the chatbot
# prompt = "You are an AI Assistant representing a Data-Science company called Shyena Tech Yarns Pvt. Ltd."

# # Load the model and tokenizer
# model_path = "/home/user/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B/snapshots/4e20de362430cd3b72f300e6b0f18e50e7166e08"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Ensure proper padding token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Function to generate a response
# async def generate_response(query):
#     # Create the input prompt
#     input_text = f"{prompt}\nUser: {query}\nAI:"
    
#     # Tokenize the input
#     inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    
#     # Generate the response
#     with torch.no_grad():
#         outputs = model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    
#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response[len(input_text):]  # Strip the prompt from the response

# # Asynchronous function to handle user queries
# async def query_bot():
#     while True:
#         query = input("Enter your Query: ")
#         if query.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break
        
#         response = await generate_response(query)
#         print(f"AI: {response}")

# # Run the asynchronous chatbot
# asyncio.run(query_bot())

# import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Define the prompt template with instructions for the chatbot
# PROMPT_TEMPLATE = """
# 1]. You are an AI Assistant representing a data-science company, Shyena Tech Yarns Pvt. Ltd.
# 2]. You are supposed to provide responses to user queries based only on the PDF document.
# 3]. You are not supposed to provide responses to user queries that are unrelated to the company's data-science domain.
# 4]. If a query is unrelated to the company's domain, respond with "I'm sorry, I can't respond to that."
# 5]. You are supposed to provide responses to user queries which are related to greeting(hi,hello,hey,how are you,who are you?) 

# Question: {question}
# Context: {context}
# Answer:
# """

# # Load the model and tokenizer
# model_path = "/home/user/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B/snapshots/4e20de362430cd3b72f300e6b0f18e50e7166e08"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Ensure proper padding token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Function to generate a response using the new prompt template
# async def generate_response(query, context, prev_query=None):
#     # Check if the current query is too similar to the previous one
#     if prev_query and query.lower() == prev_query.lower():
#         return "You already asked this question. Please ask something different."

#     # Fill the template with the question and context
#     prompt = PROMPT_TEMPLATE.format(question=query, context=context)

#     # Tokenize the input with attention mask
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
    
#     # Explicitly create the attention mask if it's not already in the tokenized inputs
#     attention_mask = inputs['attention_mask'] if 'attention_mask' in inputs else None

#     # Generate the response with a longer max length
#     with torch.no_grad():
#         outputs = model.generate(
#             inputs["input_ids"], 
#             max_length=300,  # Increased max_length
#             num_return_sequences=1, 
#             pad_token_id=tokenizer.eos_token_id,
#             attention_mask=attention_mask
#         )

#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response[len(prompt):].strip()  # Strip the prompt and ensure clean output

# # Asynchronous function to handle user queries
# async def query_bot():
#     prev_query = None
#     context = "This is where the PDF context should go."  # Placeholder for PDF context
#     while True:
#         query = input("Enter your Query: ")
#         if query.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break
        
#         # Generate the response and print it
#         response = await generate_response(query, context, prev_query)
#         print(f"Assistant: {response}")
        
#         # Update the previous query
#         prev_query = query

# # Run the asynchronous chatbot
# asyncio.run(query_bot())


# import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Define the prompt template with instructions for the chatbot
# PROMPT_TEMPLATE = """
# You are an AI Assistant representing a data-science company, Shyena Tech Yarns Pvt. Ltd.
# - Only answer queries related to the company's domain or greetings.
# - For unrelated queries, respond with: "I'm sorry, I can't respond to that."
# - Provide concise and relevant responses for allowed queries.

# Question: {question}
# Answer:
# """

# # Load the model and tokenizer
# model_path = "/home/user/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B/snapshots/4e20de362430cd3b72f300e6b0f18e50e7166e08"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Ensure proper padding token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Define a function to check for greetings
# def is_greeting(query):
#     greetings = ['hi', 'hello', 'hey', 'how are you', 'who are you', 'good morning', 'good afternoon']
#     return any(greet in query.lower() for greet in greetings)

# # Generate a response using the prompt template
# async def generate_response(query, prev_query=None):
#     # Check if the current query is too similar to the previous one
#     if prev_query and query.lower() == prev_query.lower():
#         return "You already asked this question. Please ask something different."

#     # Check if the query is a greeting
#     if is_greeting(query):
#         return "Hello there! How can I assist you today?"

#     # Reject unrelated queries
#     allowed_topics = ["company", "services", "data science", "greetings"]
#     if not any(topic in query.lower() for topic in allowed_topics):
#         return "I'm sorry, I can't respond to that."

#     # Fill the template with the question
#     prompt = PROMPT_TEMPLATE.format(question=query)

#     # Tokenize the input
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)

#     # Generate the response
#     with torch.no_grad():
#         outputs = model.generate(
#             inputs["input_ids"],
#             max_length=150,  # Limit response length
#             num_return_sequences=1,
#             pad_token_id=tokenizer.eos_token_id,
#         )

#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Clean and return only the assistant's answer
#     return response.split("Answer:")[-1].strip()

# # Asynchronous function to handle user queries
# async def query_bot():
#     prev_query = None
#     while True:
#         query = input("Enter your Query: ")
#         if query.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break

#         # Generate the response
#         response = await generate_response(query, prev_query)
#         print(f"Assistant: {response}")

#         # Update the previous query
#         prev_query = query

# # Run the chatbot
# asyncio.run(query_bot())

# import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Define the prompt template with instructions for the chatbot
# PROMPT_TEMPLATE = """
# You are an AI Assistant representing a data-science company, Shyena Tech Yarns Pvt. Ltd.
# - Only answer queries related to the company's domain or greetings.
# - For unrelated queries, respond with: "I'm sorry, I can't respond to that."
# - Provide concise and relevant responses for allowed queries.

# Question: {question}
# Answer:
# """

# # Load the model and tokenizer
# model_path = "/home/user/.cache/huggingface/hub/models--meta-llama--Llama-3.2-1B/snapshots/4e20de362430cd3b72f300e6b0f18e50e7166e08"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Ensure proper padding token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Define direct responses for predefined queries
# PREDEFINED_RESPONSES = {
#     "greetings": ["hi", "hello", "hey"],
#     "investigate": ["how are you?", "how are things", "how’s it going"],
#     "time_of_day": ["good morning", "good afternoon"],
#     "gesture": ["who are you?", "tell me about yourself?", "what are you?"]
# }

# def get_predefined_response(query):
#     query_lower = query.lower().strip()
#     if query_lower in PREDEFINED_RESPONSES["greetings"]:
#         return "Hey there! How can I assist you today?"
#     elif query_lower in PREDEFINED_RESPONSES["investigate"]:
#         return "I'm doing great, thank you! How about you?"
#     elif query_lower in PREDEFINED_RESPONSES["time_of_day"]:
#         if "morning" in query_lower:
#             return "Good Morning! How's everything going?"
#         elif "afternoon" in query_lower:
#             return "Good Afternoon! How's everything going?"
#     elif query_lower in PREDEFINED_RESPONSES["gesture"]:
#         return "I'm an AI Assistant created by Shyena Tech Yarns Pvt. Ltd. I'm here to assist you with questions you have regarding our company. How can I help you today?"
#     return None

# # Generate a response using the prompt template
# async def generate_response(query, prev_query=None):
#     # Check if the current query is too similar to the previous one
#     if prev_query and query.lower() == prev_query.lower():
#         return "You already asked this question. Please ask something different."

#     # Check for predefined responses
#     predefined_response = get_predefined_response(query)
#     if predefined_response:
#         return predefined_response

#     # Reject unrelated queries
#     allowed_topics = ["company", "services", "data science"]
#     if not any(topic in query.lower() for topic in allowed_topics):
#         return "I'm sorry, I can't respond to that."

#     # Fill the template with the question
#     prompt = PROMPT_TEMPLATE.format(question=query)

#     # Tokenize the input with attention mask to avoid EOS token issues
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
#     inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()

#     # Generate the response
#     with torch.no_grad():
#         outputs = model.generate(
#             inputs["input_ids"],
#             attention_mask=inputs["attention_mask"],
#             max_length=300,  # Increased token limit for more comprehensive responses
#             num_return_sequences=1,
#             pad_token_id=tokenizer.pad_token_id,
#             temperature=0.7,  # Adjusted for more natural responses
#             top_p=0.9,
#             top_k=50
#         )

#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Clean and return only the assistant's answer
#     return response.split("Answer:")[-1].strip()

# # Asynchronous function to handle user queries
# async def query_bot():
#     prev_query = None
#     while True:
#         query = input("Enter your Query: ")
#         if query.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break

#         # Generate the response
#         response = await generate_response(query, prev_query)
#         print(f"Assistant: {response}")

#         # Update the previous query
#         prev_query = query

# # Run the chatbot
# asyncio.run(query_bot())


# import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Define the prompt template with instructions for the chatbot
# PROMPT_TEMPLATE = """
# You are an AI Assistant representing a data-science company, Shyena Tech Yarns Pvt. Ltd.
# - Only answer queries related to the company's domain or greetings based only on the vector database.
# - For unrelated queries, respond with: "I'm sorry, I can't respond to that."
# - Provide concise and relevant responses for allowed queries.

# Question: {question}
# Answer:
# """

# # Load the model and tokenizer
# model_path = "/home/user/Desktop/meta-llama-Llama-3.2-1B/llm"
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)

# # Ensure proper padding token
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token

# # Define direct responses for predefined queries
# PREDEFINED_RESPONSES = {
#     "greetings": ["hi", "hello", "hey"],
#     "investigate": ["how are you?", "how are things", "how’s it going"],
#     "time_of_day": ["good morning", "good afternoon"],
#     "gesture": ["who are you?", "tell me about yourself?", "what are you?"]
# }

# def get_predefined_response(query):
#     query_lower = query.lower().strip()
#     if query_lower in PREDEFINED_RESPONSES["greetings"]:
#         return "Hey there! How can I assist you today?"
#     elif query_lower in PREDEFINED_RESPONSES["investigate"]:
#         return "I'm doing great, thank you! How about you?"
#     elif query_lower in PREDEFINED_RESPONSES["time_of_day"]:
#         if "morning" in query_lower:
#             return "Good Morning! How's everything going?"
#         elif "afternoon" in query_lower:
#             return "Good Afternoon! How's everything going?"
#     elif query_lower in PREDEFINED_RESPONSES["gesture"]:
#         return "I'm an AI Assistant created by Shyena Tech Yarns Pvt. Ltd. I'm here to assist you with questions you have regarding our company. How can I help you today?"
#     return None

# # Generate a response using the prompt template
# async def generate_response(query, prev_query=None):
#     # Check if the current query is too similar to the previous one
#     if prev_query and query.lower() == prev_query.lower():
#         return "You already asked this question. Please ask something different."

#     # Check for predefined responses
#     predefined_response = get_predefined_response(query)
#     if predefined_response:
#         return predefined_response

#     # Reject unrelated queries
#     allowed_topics = ["company", "services", "data science"]
#     if not any(topic in query.lower() for topic in allowed_topics):
#         return "I'm sorry, I can't respond to that."

#     # Fill the template with the question
#     prompt = PROMPT_TEMPLATE.format(question=query)

#     # Tokenize the input with attention mask to avoid EOS token issues
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
#     inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()

#     # Generate the response
#     with torch.no_grad():
#         outputs = model.generate(
#             inputs["input_ids"],
#             attention_mask=inputs["attention_mask"],
#             max_length=500,  # Increased to 500 tokens for longer responses
#             num_return_sequences=1,
#             pad_token_id=tokenizer.pad_token_id,
#             temperature=0.7,  # Adjusted for more natural responses
#             top_p=0.9,
#             top_k=50,
#             no_repeat_ngram_size=3  # Prevent repetitive phrases
#         )

#     # Decode the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Clean and return only the assistant's answer
#     return response.split("Answer:")[-1].strip()

# # Asynchronous function to handle user queries
# async def query_bot():
#     prev_query = None
#     while True:
#         query = input("Enter your Query: ")
#         if query.lower() in ['exit', 'quit']:
#             print("Goodbye!")
#             break

#         # Generate the response
#         response = await generate_response(query, prev_query)
#         print(f"Assistant: {response}")

#         # Update the previous query
#         prev_query = query

# # Run the chatbot
# asyncio.run(query_bot())

import asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Define the prompt template with strict instructions for single responses
PROMPT_TEMPLATE = """
You are an AI Assistant representing a data-science company called Shyena Tech Yarns Pvt. Ltd. 
Only answer queries related to the company's domain, services, or greetings. 
If a query is irrelevant or out-of-context, respond with: "I'm sorry, I can't respond to that."
Provide relevant response for allowed queries.

Question: {question}
Answer:
"""

# Load the model and tokenizer
model_path = "/home/user/Desktop/meta-llama-Llama-3.2-1B/llm"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Ensure proper padding token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Define direct responses for predefined queries
PREDEFINED_RESPONSES = {
    "greetings": ["hi", "hello", "hey"],
    "investigate": ["how are you?", "how are things", "how’s it going"],
    "time_of_day": ["good morning", "good afternoon"],
    "gesture": ["who are you?", "tell me about yourself?", "what are you?"]
}

def get_predefined_response(query):
    query_lower = query.lower().strip()
    if query_lower in PREDEFINED_RESPONSES["greetings"]:
        return "Hey there! How can I assist you today?"
    elif query_lower in PREDEFINED_RESPONSES["investigate"]:
        return "I'm doing great, thank you! How about you?"
    elif query_lower in PREDEFINED_RESPONSES["time_of_day"]:
        if "morning" in query_lower:
            return "Good Morning! How's everything going?"
        elif "afternoon" in query_lower:
            return "Good Afternoon! How's everything going?"
    elif query_lower in PREDEFINED_RESPONSES["gesture"]:
        return "I'm an AI Assistant crafted at Shyena Tech Yarns Pvt. Ltd. I'm here to assist you with questions you have regarding our company. How can I help you today?"
    return None

# Generate a response using the prompt template
async def generate_response(query, prev_query=None):
    # Check if the current query is too similar to the previous one
    if prev_query and query.lower() == prev_query.lower():
        return "You already asked this question. Please ask something different."

    # Check for predefined responses
    predefined_response = get_predefined_response(query)
    if predefined_response:
        return predefined_response

    # Reject unrelated queries
    allowed_topics = ["company", "services", "data science"]
    if not any(topic in query.lower() for topic in allowed_topics):
        return "I'm sorry, I can't respond to that."

    # Fill the template with the question
    prompt = PROMPT_TEMPLATE.format(question=query)

    # Tokenize the input with attention mask to avoid EOS token issues
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
    inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()

    # Generate the response
    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=500,  # Increased to 500 tokens for longer responses
            num_return_sequences=1,
            pad_token_id=tokenizer.pad_token_id,
            temperature=0.7,  # Adjusted for more natural responses
            top_p=0.9,
            top_k=50,
            no_repeat_ngram_size=3  # Prevent repetitive phrases
        )

    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean and return only the assistant's answer
    return response.split("Answer:")[-1].strip()

# Asynchronous function to handle user queries
async def query_bot():
    prev_query = None
    while True:
        query = input("Enter your Query: ")
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Generate the response
        response = await generate_response(query, prev_query)
        print(f"Assistant: {response}")

        # Update the previous query
        prev_query = query

# Run the chatbot
asyncio.run(query_bot())
