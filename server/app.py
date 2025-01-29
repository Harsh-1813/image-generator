from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import base64
import os
import io
import logging
from dotenv import load_dotenv

load_dotenv()
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
# 1) Import Pillow modules
from PIL import Image, ImageEnhance

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

logging.info("Flask app initialized.")


@app.route("/")
def hello():
    logging.info("Root endpoint accessed.")
    return "Hello, Image Generator!"


def fetch_prompt_from_lumo(user_input: str, model: str = "lumolabs/Lumo-70B-Instruct") -> str:
    """
    Sends the user_input to Lumo Labs to get back a refined or descriptive prompt
    for image generation.
    """
    logging.info("Fetching refined prompt from Lumo.")
    lumo_api_url = "https://sheer-walliw-lumolabs-6b447c84.koyeb.app/api/generate"
    
    prompt = (
        "Please take the following text or code, and generate a short, vivid prompt "
        "that can be used to create a descriptive image:\n\n"
        f"User Input:\n{user_input}"
    )

    payload = {
        "prompt": prompt,
        "model": model,
        "stream": False
    }

    try:
        response = requests.post(lumo_api_url, json=payload)
        data = response.json()
        refined_prompt = data.get("response", "")
        logging.info(f"Refined prompt: {refined_prompt}")
        return refined_prompt
    except Exception as e:
        logging.error(f"Error calling Lumo: {e}")
        return user_input


HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY", HUGGING_FACE_API_KEY)
STABLE_DIFFUSION_ENDPOINT = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large-turbo"

def generate_image(prompt: str) -> bytes:
    """
    Calls the Hugging Face Inference API for Stable Diffusion,
    returns raw image bytes.
    """
    logging.info("Generating image from Stable Diffusion.")
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }
    
    response = requests.post(STABLE_DIFFUSION_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code != 200:
        logging.error(f"Failed to generate image. Status: {response.status_code}, Message: {response.text}")
        return None
    
    logging.info("Image generated successfully.")
    return response.content  

def enhance_image(image_bytes: bytes) -> bytes:
    """
    Uses Pillow's ImageEnhance to tweak brightness, color, and sharpness.
    Returns new image bytes.
    """
    logging.info("Enhancing generated image.")
    
    image = Image.open(io.BytesIO(image_bytes))
    
    image = ImageEnhance.Brightness(image).enhance(1.1)
    image = ImageEnhance.Color(image).enhance(1.2)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="PNG")
    enhanced_bytes = output_buffer.getvalue()
    
    logging.info("Image enhancement completed.")
    return enhanced_bytes

@app.route("/generate-image", methods=["POST"])
def generate_image_endpoint():
    logging.info("Received request to generate an image.")
    data = request.json or {}
    user_input = data.get("prompt", "")
    
    if not user_input:
        logging.warning("No prompt provided in the request.")
        return jsonify({"error": "No prompt or input provided."}), 400
    
    refined_prompt = fetch_prompt_from_lumo(user_input, model="lumolabs/Lumo-8B-Instruct")
    image_bytes = generate_image(refined_prompt)
    
    if not image_bytes:
        logging.error("Image generation failed.")
        return jsonify({"error": "Image generation failed."}), 500
    
    enhanced_bytes = enhance_image(image_bytes)
    
    # try:
    #     with open("x.png", "wb") as f:
    #         f.write(enhanced_bytes)
    #     logging.info("Enhanced image saved as x.png.")
    # except Exception as e:
    #     logging.error(f"Error saving the image: {e}")
    #     return jsonify({"error": "Failed to save the enhanced image."}), 500
    
    image_base64 = base64.b64encode(enhanced_bytes).decode("utf-8")
    
    logging.info("Returning generated image to client.")
    return jsonify({
        "prompt_used": refined_prompt,
        "image_base64": image_base64,
        "saved_filename": "x.png"
    })

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=True)
