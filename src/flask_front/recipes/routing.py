from flask import Blueprint,  jsonify, render_template, request

from src.flask_front import app
from src.alchemy_db.accessors.recipes_repository import get_all_recipes,get_recipe_by_id
from src.alchemy_db.session.session import SessionLocal


recipes_bp = Blueprint(
        "recipes", 
    __name__, 
    url_prefix="/recipes",
    template_folder="templates"  # points to blueprints/recipes/templates
)
@recipes_bp.route('/')
def list_recipes():
         with SessionLocal() as session:
            recipeList=get_all_recipes(session)
            return render_template('home.html', recipeList=recipeList)

@recipes_bp.route("/<int:recipe_id>")
def recipe_details(recipe_id):
         with SessionLocal() as session:
            recipe=get_recipe_by_id(session,recipe_id)
            return render_template('home.html', recipe=recipe) 

@recipes_bp.route("/get", methods=["GET"])
def get_recipes():
    with SessionLocal() as session:
        recipeList=get_all_recipes(session)
        return jsonify(recipeList)

@recipes_bp.route("/get/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return jsonify({"message": f"recipe {recipe_id}"})


app.register_blueprint(recipes_bp)

