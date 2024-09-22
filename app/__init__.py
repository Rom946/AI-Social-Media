from flask import Flask
import os
import logging

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.abspath('../templates'),
                static_folder=os.path.abspath('../static'))
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        app.config.from_object('instance.config.Config')
    except ImportError:
        pass
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app