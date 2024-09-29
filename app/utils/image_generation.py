import requests
from bs4 import BeautifulSoup
import random
import base64
from io import BytesIO
from PIL import Image
import logging
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import pandas as pd
import time
from app.utils.download_utils import download_with_progress  # Import the new utility function
from app.utils.trending_topics import TrendingTopicsFetcher  # Import the TrendingTopicsFetcher class

# Suppress InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# Set pandas option to opt-in to the future behavior
pd.set_option('mode.chained_assignment', None)
pd.set_option('future.no_silent_downcasting', True)

class ImageGenerator:
    def __init__(self):
        self.trending_topics_fetcher = TrendingTopicsFetcher()
        logging.info("ImageGenerator initialized with web scraping capabilities.")

    def get_trending_topics(self):
        return self.trending_topics_fetcher.get_trending_topics()

    def search_images(self, query):
        logging.info(f"Searching images for query: {query}")
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        time.sleep(2)  # Add a delay to avoid being blocked
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = [img['src'] for img in soup.find_all('img') if img.get('src') and img['src'].startswith('http')]
        logging.info(f"Found {len(image_urls)} images for query: {query}")
        return image_urls

    def generate_random_images(self, num_images=1, size=(512, 512), prompt=None):
        logging.info(f"Attempting to generate {num_images} images with prompt: {prompt}")
        
        generated_images = []
        
        # Get trending topics
        trending_topics = self.get_trending_topics()
        
        for _ in range(num_images):
            try:
                if not prompt:
                    # Randomly select a search engine and a trending topic
                    engine = random.choice(list(trending_topics.keys()))
                    prompt = random.choice(trending_topics[engine]) if trending_topics[engine] else "default prompt"
                
                # Search for images based on the prompt
                image_urls = self.search_images(prompt)
                if not image_urls:
                    raise Exception("No images found for the given prompt")
                
                # Download and process the image
                image_url = random.choice(image_urls)
                logging.info(f"Downloading image from URL: {image_url}")
                download_with_progress(image_url, 'temp_image.jpg')
                img = Image.open('temp_image.jpg')
                img = img.resize(size)
                
                # Encode the image as base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                generated_images.append({
                    'url': f"data:image/png;base64,{img_str}",
                    'description': prompt
                })
                logging.info(f"Generated image for prompt: {prompt}")
            except Exception as e:
                logging.error(f"Error generating image: {str(e)}", exc_info=True)
                generated_images.append({
                    'url': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
                    'description': f"Error generating image: {prompt or 'No prompt provided'}"
                })
        
        return generated_images

    def generate_text(self, prompt):
        logging.info(f"Generating text for prompt: {prompt}")
        # For simplicity, return a random trending topic as the generated text
        generated_text = random.choice(self.get_trending_topics()['google'])
        logging.info(f"Generated text: {generated_text}")
        return generated_text