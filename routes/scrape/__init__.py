from flask import Blueprint
from .start import start_scrape_bp

scrape_bp = Blueprint("scrape", __name__, url_prefix="/scrape")

scrape_bp.register_blueprint(start_scrape_bp)
