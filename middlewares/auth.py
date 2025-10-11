from flask import Flask
from werkzeug import Request

class AuthMiddleware:
    def __init__(self, app: Flask, api_key: str):
        self.app = app.wsgi_app
        self.api_key = api_key

    def __call__(self, environ, start_response):
        request = Request(environ)
        headers = request.headers

        # Check if the api key in the headers matches the api key in the environment
        if headers.get('x-api-key') != self.api_key:
            start_response('401 Unauthorized', [('Content-Type', 'text/plain')])
            return [b'Unauthorized']

        return self.app(environ, start_response)
