from flask import Blueprint, Response, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services import menu_service

from src.alchemy_db.session.session import SessionLocal

menu_bp = Blueprint(
        "menu", 
    __name__, 
    url_prefix="/menu",
    template_folder="templates"  # points to blueprints/menu/templates
)

@menu_bp.route('/')
def list_menu()->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        menu, total = menu_service.get_menu_paginated(session, page, per_page)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'menu/list.html',
            menu=menu,
            page=page,
            total_pages=total_pages
        )

@menu_bp.route("/<int:menu_id>")
def menu_details(menu_id)->str:
    with SessionLocal() as session:
        menu=menu_service.get_menu_by_id(session,menu_id)
        return render_template('menu/details.html', menu=menu) 
         
@menu_bp.route("/search")
def search_menu()->str:
    query = request.args.get("q","").strip()
    if not query:
        return render_template("menu/list.html", menu=[])
    else:
       return  search_menu_by_name(query)

def search_menu_by_name(menu_name: str)->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        menu = menu_service.get_menu_containing_in_name_paginated(session,menu_name, page, per_page)
        total = len(menu)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'menu/list.html',
            menu=menu,
            page=page,
            total_pages=total_pages
        )
    
@menu_bp.route("/get/<int:menu_id>", methods=["GET"])
def get_menu(menu_id)->Response:
    return jsonify({"message": f"menu {menu_id}"})