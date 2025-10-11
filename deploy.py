#import os
from flask import Flask
#from middlewares.auth import AuthMiddleware
from dotenv import load_dotenv
from routes.scrape import scrape_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(scrape_bp)


# Add the AuthMiddleware to the app
#app.wsgi_app = AuthMiddleware(app, os.getenv('API_KEY'))
