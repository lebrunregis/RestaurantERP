import datetime

from flask import Blueprint, make_response, redirect, render_template, url_for, session

home_bp = Blueprint(
        "home", 
    __name__, 
    url_prefix="",
    template_folder="templates"  # points to blueprints/recipes/templates
)

@home_bp.route("/home")
def home():
    return render_template("home.html", current_year=datetime.datetime.now().year)

@home_bp.route("/")
@home_bp.route("/index")
def login():
    return redirect(url_for('home.home'))

@home_bp.errorhandler(404)
def not_found(error):
        """Page not found."""
        return make_response(
            render_template("404.html"),
            error
        )

@home_bp.errorhandler(400)
def bad_request(error):
        """Page not found."""
        return make_response(
            render_template("400.html"),
            error
        )

@home_bp.errorhandler(500)
def server_error(error):
        """Page not found."""
        return make_response(
            render_template("500.html"),
            error
        )