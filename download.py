# from transformers import AutoTokenizer, AutoModelForCausalLM

# model_name = "meta-llama/Llama-3.2-1B"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

from transformers import AutoTokenizer, AutoModelForCausalLM

# Define the model name and custom save path
model_name = "meta-llama/Llama-3.2-1B"
custom_save_path = "/home/user/Desktop/meta-llama-Llama-3.2-1B/llm"

# Download and save the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(custom_save_path)

# Download and save the model
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(custom_save_path)

print(f"Model and tokenizer saved at {custom_save_path}")
