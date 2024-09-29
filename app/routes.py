from flask import Blueprint, render_template, request, jsonify
from app.utils.image_generation import ImageGenerator
from app.utils.text_generation import TextGenerator
from datetime import datetime
from uuid import uuid4
from app.utils.dash_top_trends import init_dash_top_trends, update_trending_searches
from app.utils.dash_analytics import init_dash_analytics
from app.utils.trending_topics import TrendingTopicsFetcher

main = Blueprint('main', __name__)

# Initialize the ImageGenerator
image_generator = ImageGenerator()

# Initialize the TextGenerator
text_generator = TextGenerator()

# Initialize the TrendingTopicsFetcher
trending_topics_fetcher = TrendingTopicsFetcher()

# Store posts in memory
posts = []

@main.route('/')
def home():
    # Render the home page with posts and model specifications
    return render_template('home.html', posts=posts, model_specs={
        'image_generation': 'DALL-E',
        'text_generation': 'GPT-3'
    })

@main.route('/generate_post', methods=['POST'])
def generate_post():
    # Generate a post with a given or random prompt
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
            print(f"Generated post: {new_post}")  # Debug print
            return jsonify(new_post), 200
        else:
            print("Failed to generate image")  # Debug print
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        print(f"Error generating post: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@main.route('/generate_random_comment/<int:post_id>', methods=['POST'])
def generate_random_comment(post_id):
    # Generate a random comment for a given post
    try:
        post = next((p for p in posts if p['id'] == post_id), None)
        if not post:
            print("Post not found")  # Debug print
            return jsonify({'error': 'Post not found'}), 404

        comment = text_generator.generate_comment(post['caption'], post.get('image_description', ''))
        post['comments'].append(comment)
        print(f"Generated comment: {comment}")  # Debug print
        return jsonify({'comments': post['comments']}), 200
    except Exception as e:
        print(f"Error generating comment: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@main.route('/top_trends')
def top_trends():
    # Fetch and display top trends from multiple search engines
    trends = trending_topics_fetcher.get_trending_topics()
    print(f"Fetched trends: {trends}")  # Debug print
    bing_api_call_count = trending_topics_fetcher.bing_api_call_count
    return render_template('top_trends.html', trends=trends, bing_api_call_count=bing_api_call_count)

@main.route('/update_trends', methods=['POST'])
def update_trends():
    # Manually update the trends
    try:
        update_trending_searches()
        print("Manually updated trends")  # Debug print
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error updating trends: {str(e)}")  # Debug print
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/analytics')
def analytics():
    # Render the analytics page
    return render_template('analytics.html')