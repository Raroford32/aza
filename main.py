from flask import Flask, render_template, request, jsonify
from utils.text_generation import generate_text, get_tgi_status
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    temperature = float(data.get("temperature", 0.7))
    max_length = int(data.get("max_length", 100))
    top_k = int(data.get("top_k", 50))

    if not prompt or len(prompt) > 500:  # Character limit for input prompt
        return jsonify({"error": "Invalid prompt. Must be between 1 and 500 characters."}), 400

    try:
        generated_text = generate_text(prompt, temperature, max_length, top_k)
        return jsonify({"generated_text": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tgi_status")
def tgi_status():
    status = get_tgi_status()
    return jsonify(status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
