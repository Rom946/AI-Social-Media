import logging
from io import BytesIO
import base64
from PIL import Image
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
from app.utils.text_generation import TextGenerator

class ImageGenerator:
    def __init__(self):
        self.text_generator = TextGenerator()
        device = "cpu"
        self.image_generator = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32).to(device)
        logging.info(f"ImageGenerator initialized with Hugging Face Transformers and Stable Diffusion on {device}.")

    def generate_random_images(self, num_images=1, size=(512, 512), prompt=None):
        logging.info(f"Attempting to generate {num_images} images with prompt: {prompt}")
        
        generated_images = []
        
        for _ in range(num_images):
            try:
                image = self.image_generator(prompt).images[0]
                image = image.resize(size)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                generated_images.append({
                    'url': f"data:image/png;base64,{img_str}",
                    'description': prompt or "Generated Image Description"
                })
            except Exception as e:
                logging.error(f"Error generating image: {str(e)}", exc_info=True)
                generated_images.append({
                    'url': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
                    'description': f"Error generating image: {prompt or 'No prompt provided'}"
                })
        
        return generated_images

    def generate_random_post(self):
        prompt = self.text_generator.generate_random_post()
        return self.generate_random_images(1, (512, 512), prompt)[0]

    def generate_text(self, prompt):
        return self.text_generator.generate_text(prompt)

    def generate_comment(self, post_caption, post_image_description):
        return self.text_generator.generate_comment(post_caption, post_image_description)