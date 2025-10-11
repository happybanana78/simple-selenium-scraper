import os, docker, random
from dotenv import load_dotenv
from flask import Blueprint, request
from docker_utils.selenium_container import SeleniumContainer
from scrape import handle_scraping
from utils.normalize import normalize
from utils.responses import error_response, success_response


load_dotenv()

start_scrape_bp = Blueprint("start_scrape", __name__)

DEBUG = True if os.getenv("DEBUG") == "True" else False

@start_scrape_bp.route("/start", methods=['POST'])
def start_scrape():
    try:
        data = request.get_json(silent=True) or {}
        link = data.get("link")

        if not link:
            return error_response(
                message="Invalid link",
                error="Invalid link",
                status_code=422
            )

        docker_client = docker.from_env()

        port = str(random.randint(4000, 7000))

        selenium_container = SeleniumContainer(
            client=docker_client,
            port=port,
        )

        selenium_container.start()
    except Exception as error:
        return error_response(
            message="Failed to start scrape selenium container",
            error=f"{error}",
        )

    try:
        if DEBUG:
            selenium_url = f"http://127.0.0.1:{port}"
        else:
            selenium_url = f"http://{selenium_container.name}:4444"

        result = handle_scraping(
            url=selenium_url,
            link=link,
        )

        stop_container(selenium_container)

        if not result['success']:
            return error_response(
                message="Scrape failed",
                error=result['error'],
            )

        normalized_data = normalize(result['data'])

        return success_response(
            message="Scrape successful",
            data=normalized_data,
        )
    except Exception as e:
        stop_container(selenium_container)

        return error_response(
            message="Scrape failed",
            error=f'{e}',
        )


def stop_container(container:SeleniumContainer):
    container.container.stop()
    container.container.remove()
