from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import requests

# Initialize the model and tokenizer
model_name = "distilgpt2"  # A smaller, manageable model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_text(prompt, temperature=0.7, max_length=100, top_k=50):
    try:
        # Generate text
        generated = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=1,
            temperature=temperature,
            top_k=top_k,
            do_sample=True
        )

        # Extract the generated text
        generated_text = generated[0]['generated_text']

        # Truncate to max_length if necessary
        if len(generated_text) > max_length:
            generated_text = generated_text[:max_length]

        return generated_text
    except Exception as e:
        print(f"Error in text generation: {str(e)}")
        raise

def get_tgi_status():
    try:
        tgi_url = "https://api-inference.huggingface.co"
        api_url = "https://api-inference.huggingface.co/models/mlabonne/Hermes-3-Llama-3.1-70B-lorablated"
        
        response = requests.get(f"{tgi_url}/status")
        if response.status_code == 200:
            return {"status": "OK", "tgi_url": tgi_url, "api_url": api_url}
        else:
            return {"status": "Error", "tgi_url": tgi_url, "api_url": api_url}
    except Exception as e:
        print(f"Error checking TGI status: {str(e)}")
        return {"status": "Error", "tgi_url": "N/A", "api_url": "N/A"}
