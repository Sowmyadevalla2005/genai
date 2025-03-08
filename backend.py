from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import speech_recognition as sr
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO
import webbrowser
import threading
import os

app = Flask(_name_, static_folder="static", template_folder="templates")
CORS(app)

# Load Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4").to(device)

@app.route("/")
def home():
    return render_template("index.html")  # Serve the frontend

@app.route("/generate_text", methods=["POST"])
def generate_text():
    data = request.json
    text_prompt = data.get("text_prompt")

    if not text_prompt:
        return jsonify({"error": "Text prompt is required"}), 400

    # Generate Image
    image = pipe(text_prompt).images[0]

    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"image": f"data:image/png;base64,{img_str}"})

@app.route("/record_audio", methods=["POST"])
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text_prompt = recognizer.recognize_google(audio)
        print(f"Transcribed Text: {text_prompt}")

        # Generate Image
        image = pipe(text_prompt).images[0]

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({"image": f"data:image/png;base64,{img_str}"})

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError:
        return jsonify({"error": "Speech recognition service error"}), 500

# Function to open the website automatically
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()  # Open browser after 1.25 sec delay
    app.run(debug=True, port=5000)