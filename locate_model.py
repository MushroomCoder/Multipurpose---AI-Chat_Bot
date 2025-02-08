from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="meta-llama/Llama-3.2-1B", filename="config.json")
print(f"Model is cached at: {model_path}")
