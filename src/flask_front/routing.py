import datetime

from flask import make_response, redirect, render_template, url_for, session
from src.flask_front import app

@app.route("/home")
def home():
    return render_template("home.html", current_year=datetime.datetime.now().year)

@app.route("/")
@app.route("/index")
def login():
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(error):
    if app.debug:
        """Page not found."""
        return make_response(
            render_template("404.html"),
            error
        )
    else:
        return redirect(url_for('home'))


@app.errorhandler(400)
def bad_request(error):
    if app.debug:
        """Page not found."""
        return make_response(
            render_template("400.html"),
            error
        )
    else:
        return redirect(url_for('home'))

@app.errorhandler(500)
def server_error(error):
    if app.debug:
        """Page not found."""
        return make_response(
            render_template("500.html"),
            error
        )
    else:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)  