from transformers import pipeline  # Import pipeline from transformers for text generation
import logging  # Import logging for logging information
import requests  # Import requests for HTTP requests
from huggingface_hub import configure_http_backend, hf_hub_download  # Import Hugging Face Hub utilities
from urllib3.exceptions import InsecureRequestWarning  # Import InsecureRequestWarning from urllib3
import urllib3  # Import urllib3 for HTTP requests
from app.utils.download_utils import download_with_progress  # Import the new utility function

# Suppress InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# Define a factory function for creating a requests session
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False  # Disable SSL verification
    return session

# Configure the HTTP backend for Hugging Face Hub
configure_http_backend(backend_factory=backend_factory)

class TextGenerator:
    def __init__(self):
        logging.info("Initializing TextGenerator with Hugging Face Transformers.")
        # Initialize the text generation pipeline with the GPT-Neo model
        self.text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
        logging.info("TextGenerator initialized with GPT-Neo model.")

    def generate_text(self, prompt, max_length=100, num_return_sequences=1):
        logging.info(f"Generating text for prompt: {prompt}")
        # Generate text based on the given prompt
        response = self.text_generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
        generated_text = response[0]['generated_text'].strip()
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        logging.info(f"Generated text: {generated_text}")
        return generated_text

    def generate_comment(self, post_caption, post_image_description):
        logging.info(f"Generating comment for post with caption: '{post_caption}' and image description: '{post_image_description}'")
        # Generate a comment based on the post caption and image description
        prompt = f"Write a thoughtful and relevant comment about a post with the caption '{post_caption}' and an image described as '{post_image_description}'.\nComment:"
        comment = self.generate_text(prompt, max_length=150)
        # If the comment still starts with the prompt, remove it
        if comment.startswith("Write a thoughtful"):
            comment = comment.split("\n")[-1].strip()
        logging.info(f"Generated comment: {comment}")
        return comment

    def generate_random_post(self):
        logging.info("Generating a random post name based on the latest trends.")
        # Generate a random post name based on the latest trends
        prompt = "Generate a creative and engaging post name for a social media post based on the latest trends.\nPost:"
        post = self.generate_text(prompt, max_length=50)
        # If the post still starts with the prompt, remove it
        if post.startswith("Generate a creative"):
            post = post.split("\n")[-1].strip()
        logging.info(f"Generated random post: {post}")
        return post