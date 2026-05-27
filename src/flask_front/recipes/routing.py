from flask import Blueprint, Response, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services.recipe_service import (
    get_recipe_by_id,get_recipes_paginated,
    get_top_matching_recipes_by_ingredients_paginated,
    get_recipes_containing_in_name_paginated
    )
from src.alchemy_db.session.session import SessionLocal

recipes_bp = Blueprint(
        "recipes", 
    __name__, 
    url_prefix="/recipes",
    template_folder="templates"  # points to blueprints/recipes/templates
)

@recipes_bp.route('/')
def list_recipes()->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        recipes, total = get_recipes_paginated(session, page, per_page)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'recipes/list.html',
            recipes=recipes,
            page=page,
            total_pages=total_pages
        )

@recipes_bp.route("/<int:recipe_id>")
def recipe_details(recipe_id)->str:
    with SessionLocal() as session:
        recipe=get_recipe_by_id(session,recipe_id)
        return render_template('recipes/details.html', recipe=recipe) 
         
@recipes_bp.route("/search")
def search_recipes()->str:
    query = request.args.get("q","").strip()
    search_type = request.args.get("search_type", "name")
    if not query:
        return render_template("recipes/list.html", recipes=[])

    if search_type == "ingredient":
      return  search_recipes_by_ingredients(query)
    else:
       return  search_recipes_by_name(query)

def search_recipes_by_name(recipe_name: str)->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        recipes = get_recipes_containing_in_name_paginated(session,recipe_name, page, per_page)
        total = len(recipes)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'recipes/list.html',
            recipes=recipes,
            page=page,
            total_pages=total_pages
        )
    
def search_recipes_by_ingredients(ingredients : str) ->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed
    ingredient_list = ingredients.split()
    with SessionLocal() as session:
        results = get_top_matching_recipes_by_ingredients_paginated(session,ingredient_list, page, per_page)
        recipes_score = results[0]
        total = results[1]
        total_pages = (total + per_page - 1) // per_page  # ceil division
        
    return render_template(
        "recipes/scored_list.html",
        recipe_score_data=recipes_score,
        page=page,
        total_pages=total_pages
    )

@recipes_bp.route("/get/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id)->Response:
    return jsonify({"message": f"recipe {recipe_id}"})