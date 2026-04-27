import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode is OFF by default to prevent sensitive data exposure in tracebacks.
    # Set FLASK_DEBUG=1 in your local .env file during development only.
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, port=5001)