from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    app=Flask(__name__)

    CORS(app)
    
    if test_config is None:
        app.config.from_pyfile("config.py")

    else:
        app.config.update(test_config)
    
    
