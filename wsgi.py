import os
from dotenv import load_dotenv
from deploy import app

load_dotenv()

DEBUG = True if os.getenv("DEBUG") == "True" else False


if __name__ == '__main__':  
    if DEBUG:
        port = 4000
    else:
        port = 5000

    app.run(port=port, debug=DEBUG)
