from flask import Blueprint, render_template, request, jsonify
from app.utils.image_generation import ImageGenerator
from datetime import datetime

main = Blueprint('main', __name__)

image_generator = ImageGenerator()

posts = []

@main.route('/')
def home():
    return render_template('home.html', posts=posts[::-1])

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
    try:
        post = next((post for post in posts if post['id'] == post_id), None)
        if not post:
            return jsonify({'error': 'Post not found'}), 404

        comment = image_generator.generate_comment(post['caption'], post['image'])
        post['comments'].append(f"{image_generator.generate_text('Generate a realistic and unique username.')}: {comment}")
        return jsonify({'comments': post['comments']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500