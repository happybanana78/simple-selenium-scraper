from flask import jsonify


def error_response(message:str, error:str=None, status_code:int=500):
    return (
        jsonify({
            "message": message,
            "data": None,
            "error": error or message,
        }),
        status_code
    )


def success_response(message:str, data=None, status_code:int=200):
    return (
        jsonify({
            "message": message,
            "data": data,
            "error": None,
        }),
        status_code
    )
