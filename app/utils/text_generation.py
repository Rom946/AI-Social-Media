from transformers import pipeline
import logging
import requests
from huggingface_hub import configure_http_backend

def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)

class TextGenerator:
    def __init__(self):
        self.text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
        logging.info("TextGenerator initialized with Hugging Face Transformers.")

    def generate_text(self, prompt, max_length=100, num_return_sequences=1):
        response = self.text_generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
        generated_text = response[0]['generated_text'].strip()
        # Remove the original prompt from the generated text
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        return generated_text

    def generate_comment(self, post_caption, post_image_description):
        prompt = f"Write a thoughtful and relevant comment about a post with the caption '{post_caption}' and an image described as '{post_image_description}'.\nComment:"
        comment = self.generate_text(prompt, max_length=150)
        # If the comment still starts with the prompt, remove it
        if comment.startswith("Write a thoughtful"):
            comment = comment.split("\n")[-1].strip()
        return comment

    def generate_random_post(self):
        prompt = "Generate a creative and engaging post name for a social media post based on the latest trends.\nPost:"
        post = self.generate_text(prompt, max_length=50)
        # If the post still starts with the prompt, remove it
        if post.startswith("Generate a creative"):
            post = post.split("\n")[-1].strip()
        return post