import os
from app import create_app


DEBUG = os.getenv("DEBUG")

app, api = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4444", debug=DEBUG)

