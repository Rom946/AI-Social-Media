from flask import Flask, render_template, request, jsonify
from ImageGeneration import ImageGenerator
import logging
from datetime import datetime

app = Flask(__name__)
image_generator = ImageGenerator()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

posts = []

@app.route('/')
def home():
    return render_template('home.html', posts=posts[::-1])  # Reverse the list to show newest posts first

@app.route('/generate_post', methods=['POST'])
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
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'username': image_generator.generate_text("Generate a realistic and unique username.")
            }
            if len(posts) >= 10:
                posts.pop(0)  # Remove the oldest post if there are already 10 posts
            posts.append(new_post)
            return jsonify(new_post), 200
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        app.logger.error(f"Error generating post: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_random_post', methods=['POST'])
def generate_random_post():
    try:
        post = image_generator.generate_random_post()
        new_post = {
            'id': len(posts),
            'image': post['url'],
            'caption': post['description'],
            'likes': 0,
            'dislikes': 0,
            'comments': [],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'username': image_generator.generate_text("Generate a realistic and unique username.")
        }
        if len(posts) >= 10:
            posts.pop(0)  # Remove the oldest post if there are already 10 posts
        posts.append(new_post)
        return jsonify(new_post), 200
    except Exception as e:
        app.logger.error(f"Error generating random post: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_random_comment/<int:post_id>', methods=['POST'])
def generate_random_comment(post_id):
    try:
        comment = image_generator.generate_text("Generate a thoughtful and relevant comment about the post.")
        for post in posts:
            if post['id'] == post_id:
                post['comments'].append(f"{image_generator.generate_text('Generate a realistic and unique username.')}: {comment}")
                return jsonify({'comments': post['comments']}), 200
        return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        app.logger.error(f"Error generating random comment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    for post in posts:
        if post['id'] == post_id:
            post['likes'] += 1
            return jsonify({'likes': post['likes']}), 200
    return jsonify({'error': 'Post not found'}), 404

@app.route('/dislike_post/<int:post_id>', methods=['POST'])
def dislike_post(post_id):
    for post in posts:
        if post['id'] == post_id:
            post['dislikes'] += 1
            return jsonify({'dislikes': post['dislikes']}), 200
    return jsonify({'error': 'Post not found'}), 404

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    comment = request.json.get('comment', '')
    username = image_generator.generate_text("Generate a realistic and unique username.")
    for post in posts:
        if post['id'] == post_id:
            post['comments'].append(f"{username}: {comment}")
            return jsonify({'comments': post['comments']}), 200
    return jsonify({'error': 'Post not found'}), 404

@app.route('/analytics')
def analytics():
    global_likes = sum(post['likes'] for post in posts)
    global_dislikes = sum(post['dislikes'] for post in posts)
    global_comments = sum(len(post['comments']) for post in posts)
    top_posts = sorted(posts, key=lambda x: x['likes'], reverse=True)[:3]
    return render_template('analytics.html', posts=posts, global_likes=global_likes, global_dislikes=global_dislikes, global_comments=global_comments, top_posts=top_posts)

if __name__ == '__main__':
    app.run(debug=True)