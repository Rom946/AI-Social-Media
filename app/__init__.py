import warnings

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

import ssl  # Import ssl module

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask
import os
import logging
from app.utils.tracker import Tracker  # Import the Tracker from the utils folder
from app.utils.dash_top_trends import init_dash_top_trends  # Import the init_dash_top_trends function for top trends
from app.utils.dash_analytics import init_dash_analytics  # Import the init_dash_analytics function

# Create an instance of the Tracker
tracker = Tracker()

def create_app():
    tracker.start('create_app')  # Start tracking the create_app function
    
    # Initialize the Flask app
    app = Flask(__name__, 
                template_folder=os.path.abspath('../templates'),
                static_folder=os.path.abspath('../static'))
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Load configuration
    tracker.start('load_config')  # Start tracking the load_config step
    try:
        app.config.from_object('instance.config.Config')
    except ImportError:
        pass
    tracker.stop('load_config')  # Stop tracking the load_config step
    
    # Register blueprints
    tracker.start('register_blueprints')  # Start tracking the register_blueprints step
    from app.routes import main, posts  # Import posts to pass to init_dash_analytics
    app.register_blueprint(main)
    tracker.stop('register_blueprints')  # Stop tracking the register_blueprints step
    
    # Initialize Dash apps
    tracker.start('init_dash_apps')  # Start tracking the init_dash_apps step
    init_dash_top_trends(app)  # Initialize the Dash app for top trends
    init_dash_analytics(app, posts)  # Initialize the Dash app for analytics with real post data
    tracker.stop('init_dash_apps')  # Stop tracking the init_dash_apps step
    
    tracker.stop('create_app')  # Stop tracking the create_app function
    tracker.report()  # Report the tracked times
    
    return app