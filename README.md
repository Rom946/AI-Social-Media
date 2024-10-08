# Image Generation with Web Scraping and Text Generation

This project is a web application that generates images by scraping the web based on trending topics and generates text (post names, usernames, and comments) using the GPT-Neo model from Hugging Face. The application is built with Flask and uses various libraries for image scraping and text generation.

## Features

- Generate random images based on trending topics using web scraping.
- Generate creative and engaging post names, usernames, and comments using the GPT-Neo model.
- Display generated posts with images, captions, likes, dislikes, and comments.
- Add random comments to posts.
- View analytics of posts using Dash.
- View top trending topics using Dash.

## Installation

### Prerequisites

- Python 3.7 or higher
- Git
- Virtual environment (optional but recommended)

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create and activate a virtual environment (optional):**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add any necessary environment variables (e.g., API keys).

5. **Run the application:**

   ```sh
   python run.py
   ```

6. **Open your web browser and navigate to:**

   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Generating a Post

1. Open the web application in your browser.
2. Click on the "Generate Post" button to create a new post with a generated image and caption.

### Adding a Comment

1. Click on a post to view its details.
2. Click on the "Generate Comment" button to add a random comment to the post.

### Viewing Analytics

1. Navigate to `/analytics` to view the analytics dashboard.

### Viewing Top Trends

1. Navigate to `/top_trends` to view the top trending topics.

## Project Structure

```
image-generation-project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── utils/
│   │   ├── image_generation.py
│   │   ├── text_generation.py
│   │   ├── dash_top_trends.py
│   │   ├── dash_analytics.py
│   │   ├── download_utils.py
│   │   └── trending_topics.py
│   │   └── tracker.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── analytics.html
│   └── top_trends.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── scripts.js
│   │   ├── home.js
│   │   ├── analytics.js
│   │   └── top_trends.js
│   └── images/
├── instance/
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_utils.py
│   └── run_profiled.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── .env
```

## Dependencies

- Flask
- Dash
- transformers
- diffusers
- torch
- torchvision
- torchaudio
- Pillow
- requests
- beautifulsoup4
- pytrends
- huggingface_hub
- certifi
- pytest
- coverage
- schedule
- plotly

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Hugging Face](https://huggingface.co/) for providing the models and libraries.
- [PyTrends](https://github.com/GeneralMills/pytrends) for Google Trends API.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Dash](https://dash.plotly.com/) for the analytics dashboard.