import requests
import os

TGI_SERVER_URL = os.environ.get("TGI_SERVER_URL", "http://130.61.18.101:8080")
API_URL = f"{TGI_SERVER_URL}/generate"

def generate_text(prompt, temperature=0.7, max_length=100, top_k=50):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_length,
                "temperature": temperature,
                "top_k": top_k,
                "do_sample": True,
                "best_of": 1,
                "use_cache": False,
                "return_full_text": False,
                "truncate": None,
                "typical_p": 0.95,
                "watermark": False,
                "seed": None
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        print(f"Error in text generation: {str(e)}")
        raise

def get_tgi_status():
    try:
        health_response = requests.get(f"{TGI_SERVER_URL}/health", timeout=10)
        health_response.raise_for_status()
        info_response = requests.get(f"{TGI_SERVER_URL}/info", timeout=10)
        info_response.raise_for_status()
        info = info_response.json()
        return {
            "status": "OK",
            "tgi_url": TGI_SERVER_URL,
            "api_url": API_URL,
            "model_id": info.get("model_id", "Not available"),
            "docker_image": info.get("docker_image", "Not available"),
            "num_gpus": info.get("num_gpus", "Not available")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error checking TGI status: {str(e)}")
        return {
            "status": "Error",
            "tgi_url": TGI_SERVER_URL,
            "api_url": API_URL,
            "error_message": str(e)
        }
