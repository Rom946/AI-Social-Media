import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import random
import base64
from io import BytesIO
from PIL import Image
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class ImageGenerator:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        logging.info("ImageGenerator initialized with web scraping capabilities.")

    def get_trending_topics(self):
        trending_searches_df = self.pytrends.trending_searches(pn='united_states')
        return trending_searches_df[0].tolist()

    def search_images(self, query):
        url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2&first=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [img['src'] for img in soup.find_all('img') if img.get('src') and img['src'].startswith('http')]

    def generate_random_images(self, num_images=1, size=(512, 512), prompt=None):
        logging.info(f"Attempting to generate {num_images} images with prompt: {prompt}")
        
        generated_images = []
        
        trending_topics = self.get_trending_topics()
        
        for _ in range(num_images):
            try:
                if not prompt:
                    prompt = random.choice(trending_topics)
                
                image_urls = self.search_images(prompt)
                if not image_urls:
                    raise Exception("No images found for the given prompt")
                
                image_url = random.choice(image_urls)
                response = requests.get(image_url, verify=False)
                img = Image.open(BytesIO(response.content))
                img = img.resize(size)
                
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                generated_images.append({
                    'url': f"data:image/png;base64,{img_str}",
                    'description': prompt
                })
            except Exception as e:
                logging.error(f"Error generating image: {str(e)}", exc_info=True)
                generated_images.append({
                    'url': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
                    'description': f"Error generating image: {prompt or 'No prompt provided'}"
                })
        
        return generated_images

    def generate_text(self, prompt):
        # For simplicity, we'll just return a random trending topic as the generated text
        return random.choice(self.get_trending_topics())