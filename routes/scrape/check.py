from dotenv import load_dotenv
from flask import Blueprint, request
from scrape import check_health
from utils.responses import error_response, success_response


load_dotenv()

check_scrape_bp = Blueprint("check_scrape", __name__)

@check_scrape_bp.route("/check", methods=['POST'])
def start_scrape():
    data = request.get_json(silent=True) or {}
    link = data.get("link")

    if not link:
        return error_response(
            message="Invalid link",
            error="Invalid link",
            status_code=422
        )

    try:
        result = check_health(
            link=link,
        )

        if not result['success']:
            return error_response(
                message="Health check failed",
                data={
                    "success": False,
                    "site": result["data"],
                },
                error=result['error'],
                status_code=200,
            )

        return success_response(
            message="Health check successful",
            data={
                "success": True,
                "site": result["data"],
            }
        )
    except Exception as e:
        return error_response(
            message="Health check failed",
            data={
                "success": False,
                "site": None,
            },
            error=f'{e}',
            status_code=200,
        )
