<<<<<<< HEAD
from flask import Flask, render_template

# This tells Flask where to find your files
app = Flask(__name__, 
            template_folder='app/templates', 
            static_folder='app/static')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/metrics')
def metrics():
    return render_template('body_metrics.html')

if __name__ == '__main__':
    # Running on 5001 so it doesn't clash with other stuff
    app.run(debug=True, port=5001)
=======
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> origin/develop
