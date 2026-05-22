from flask import Flask

def create_app():
    """Factory function to create Flask app"""
    app = Flask(__name__, template_folder="templates")

    # Import and register home routing
    from . import routing
    app.register_blueprint(routing.home_bp)  # or whatever your routing blueprint is

    # Import and register blueprints
    from .recipes.routing import recipes_bp
    app.register_blueprint(recipes_bp)

    return app