from src.flask_front import app

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"