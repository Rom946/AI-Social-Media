from flask import Blueprint, render_template, request, jsonify
from app.utils.image_generation import ImageGenerator
from app.utils.text_generation import TextGenerator
from datetime import datetime
from uuid import uuid4

main = Blueprint('main', __name__)

image_generator = ImageGenerator()
text_generator = TextGenerator()

posts = []

@main.route('/')
def home():
    model_specs = {
        'image_generation': 'Web Scraping',
        'text_generation': 'EleutherAI/gpt-neo-2.7B'
    }
    return render_template('home.html', posts=posts[::-1], model_specs=model_specs)

@main.route('/generate_random_post', methods=['POST'])
def generate_random_post():
    try:
        # Your logic to generate a random post
        new_post = {
            'id': len(posts),
            'image': image_generator.generate_random_images(1, (512, 512))[0]['url'],
            'caption': image_generator.generate_text("Generate a creative and engaging post name for a social media post."),
            'likes': 0,
            'dislikes': 0,
            'comments': [],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'username': image_generator.generate_text("Generate a realistic and unique username.")
        }
        posts.append(new_post)
        return jsonify(new_post), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/generate_post', methods=['POST'])
def generate_post():
    prompt = request.json.get('prompt', image_generator.generate_text("Generate a creative and engaging post name for a social media post."))
    try:
        images = image_generator.generate_random_images(1, (512, 512), prompt)
        if images:
            new_post = {
                'id': len(posts),
                'image': images[0]['url'],
                'caption': prompt,
                'likes': 0,
                'dislikes': 0,
                'comments': [],
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'username': image_generator.generate_text("Generate a realistic and unique username.")
            }
            if len(posts) >= 10:
                posts.pop(0)
            posts.append(new_post)
            return jsonify(new_post), 200
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/generate_random_comment/<int:post_id>', methods=['POST'])
def generate_random_comment(post_id):
    print(f"Generating comment for post {post_id}")  # Debug print
    try:
        post = next((p for p in posts if p['id'] == post_id), None)
        if not post:
            print(f"Post {post_id} not found")  # Debug print
            return jsonify({'error': 'Post not found'}), 404

        comment = text_generator.generate_comment(post['caption'], post.get('image_description', ''))
        post['comments'].append(comment)
        print(f"Generated comment: {comment}")  # Debug print
        return jsonify({'comments': post['comments']}), 200
    except Exception as e:
        print(f"Error generating comment: {str(e)}")
        return jsonify({'error': str(e)}), 500