from transformers import pipeline
import logging

class TextGenerator:
    def __init__(self):
        self.text_generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
        logging.info("TextGenerator initialized with Hugging Face Transformers.")

    def generate_text(self, prompt, max_length=50, num_return_sequences=1):
        response = self.text_generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)
        return response[0]['generated_text'].strip()

    def generate_comment(self, post_caption, post_image_description):
        prompt = f"Write a thoughtful and relevant comment about a post with the caption '{post_caption}' and an image described as '{post_image_description}'."
        return self.generate_text(prompt)

    def generate_random_post(self):
        prompt = "Generate a creative and engaging post name for a social media post based on the latest trends."
        return self.generate_text(prompt)