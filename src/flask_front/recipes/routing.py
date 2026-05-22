from flask import Blueprint, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services.recipe_service import get_recipe_by_id,get_recipes_paginated
from src.alchemy_db.session.session import SessionLocal

recipes_bp = Blueprint(
        "recipes", 
    __name__, 
    url_prefix="/recipes",
    template_folder="templates"  # points to blueprints/recipes/templates
)

@recipes_bp.route('/')
def list_recipes():
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        recipes, total = get_recipes_paginated(session, page, per_page)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'list.html',
            recipes=recipes,
            page=page,
            total_pages=total_pages
        )

@recipes_bp.route("/<int:recipe_id>")
def recipe_details(recipe_id):
         with SessionLocal() as session:
            recipe=get_recipe_by_id(session,recipe_id)
            return render_template('details.html', recipe=recipe) 

@recipes_bp.route("/search")
def search_recipes():
    return redirect(url_for('home.home'))

@recipes_bp.route("/get/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return jsonify({"message": f"recipe {recipe_id}"})