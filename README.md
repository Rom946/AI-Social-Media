# Image Generation with Stable Diffusion and Text Generation

This project is a web application that generates images using the Stable Diffusion model and generates text (post names, usernames, and comments) using the GPT-Neo model from Hugging Face. The application is built with Flask and uses various libraries for image and text generation.

## Features

- Generate random images based on a prompt using the Stable Diffusion model.
- Generate creative and engaging post names, usernames, and comments using the GPT-Neo model.
- Display generated posts with images, captions, likes, dislikes, and comments.
- Add random comments to posts.

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

## Project Structure

```
image-generation-project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── analytics.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── scripts.js
│   │   └── images/
│   └── utils/
│       ├── __init__.py
│       ├── image_generation.py
│       └── text_generation.py
├── instance/
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_utils.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── .env
```

## Dependencies

- Flask
- transformers
- diffusers
- torch
- torchvision
- torchaudio
- Pillow
- requests
- huggingface_hub
- certifi
- pytest
- coverage

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Hugging Face](https://huggingface.co/) for providing the models and libraries.
- [PyTorch](https://pytorch.org/) for the deep learning framework.
- [Flask](https://flask.palletsprojects.com/) for the web framework.