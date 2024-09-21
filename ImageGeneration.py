import os
import logging
from io import BytesIO
import base64
from PIL import Image
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
import requests
from huggingface_hub import configure_http_backend

# Configure HTTP backend to disable SSL verification
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)

class ImageGenerator:
    def __init__(self):
        self.text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
        device = "cpu"  # Force using CPU
        self.image_generator = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32).to(device)
        logging.info(f"ImageGenerator initialized with Hugging Face Transformers and Stable Diffusion on {device}.")
        
    def generate_random_images(self, num_images=1, size=(512, 512), prompt=None):
        logging.info(f"Attempting to generate {num_images} images with prompt: {prompt}")
        
        generated_images = []
        
        for _ in range(num_images):
            try:
                # Generate image using Stable Diffusion
                image = self.image_generator(prompt).images[0]
                
                # Resize image to the desired size
                image = image.resize(size)
                
                # Convert image to base64 string
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                generated_images.append({
                    'url': f"data:image/png;base64,{img_str}",
                    'description': prompt or "Generated Image Description"
                })
            except Exception as e:
                logging.error(f"Error generating image: {str(e)}", exc_info=True)
                # If image generation fails, add a placeholder
                generated_images.append({
                    'url': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
                    'description': f"Error generating image: {prompt or 'No prompt provided'}"
                })
        
        return generated_images

    def generate_random_post(self):
        prompt = self.generate_text("Generate a creative and engaging post name for a social media post.")
        return self.generate_random_images(1, (512, 512), prompt)[0]

    def generate_text(self, prompt):
        response = self.text_generator(prompt, max_length=50, num_return_sequences=1)
        return response[0]['generated_text'].strip()
