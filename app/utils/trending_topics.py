import requests
from pytrends.request import TrendReq
import logging
from app.models import Config  # Import the Config class

class TrendingTopicsFetcher:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.bing_api_call_count = 0  # Initialize Bing API call count

    def get_trending_topics(self):
        logging.info("Fetching trending topics from various search engines.")
        # Define search engines and their regions
        search_engines = {
            'google': 'united_states',
            'bing': 'united_states',
            'duckduckgo': 'united_states',
            'baidu': 'china'
        }
        all_trends = {}

        # Fetch trending topics from each search engine
        for engine, region in search_engines.items():
            try:
                if engine == 'google':
                    # Fetch Google trends
                    trending_searches_df = self.pytrends.trending_searches(pn=region)
                    trending_searches_df = trending_searches_df.infer_objects(copy=False)  # Handle FutureWarning
                    all_trends[engine] = trending_searches_df[0].tolist()[:10]
                elif engine == 'bing':
                    # Fetch Bing trends
                    bing_trends = self.fetch_bing_trends()
                    all_trends[engine] = bing_trends
                elif engine == 'duckduckgo':
                    # Fetch DuckDuckGo trends
                    duckduckgo_trends = self.fetch_duckduckgo_trends()
                    all_trends[engine] = duckduckgo_trends
                else:
                    # Placeholder for other search engines
                    all_trends[engine] = [f"{engine} trend {i}" for i in range(1, 11)]
            except requests.exceptions.RequestException as e:
                # Log error and skip to the next search engine
                logging.error(f"Error fetching trending topics from {engine}: {str(e)}", exc_info=True)
                all_trends[engine] = []

        logging.info(f"Fetched trending topics: {all_trends}")
        return all_trends

    def fetch_bing_trends(self):
        # Get the Bing API key from the config
        api_key = Config.BING_API_KEY
        if not api_key:
            logging.error("Bing API key is not set.")
            return []

        headers = {'Ocp-Apim-Subscription-Key': api_key}
        url = 'https://api.bing.microsoft.com/v7.0/news/trendingtopics'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            trends = [topic['name'] for topic in data['value']]
            self.bing_api_call_count += 1  # Increment Bing API call count
            return trends[:10]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching Bing trends: {str(e)}", exc_info=True)
            return []

    def fetch_duckduckgo_trends(self):
        query = "trending topics"
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            trends = [item['Text'] for item in data['RelatedTopics']]
            return trends[:10]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching DuckDuckGo trends: {str(e)}", exc_info=True)
            return []
