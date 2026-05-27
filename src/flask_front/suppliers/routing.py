from flask import Blueprint, Response, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services import supplier_service

from src.alchemy_db.session.session import SessionLocal

suppliers_bp = Blueprint(
        "suppliers", 
    __name__, 
    url_prefix="/suppliers",
    template_folder="templates"  # points to blueprints/suppliers/templates
)

@suppliers_bp.route('/')
def list_suppliers()->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        suppliers, total = supplier_service.get_suppliers_paginated(session, page, per_page)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'suppliers/list.html',
            suppliers=suppliers,
            page=page,
            total_pages=total_pages
        )

@suppliers_bp.route("/<int:supplier_id>")
def supplier_details(supplier_id)->str:
    with SessionLocal() as session:
        supplier=supplier_service.get_supplier_by_id(session,supplier_id)
        return render_template('suppliers/details.html', supplier=supplier) 
         
@suppliers_bp.route("/search")
def search_suppliers()->str:
    query = request.args.get("q","").strip()
    if not query:
        return render_template("suppliers/list.html", suppliers=[])
    else:
       return  search_suppliers_by_name(query)

def search_suppliers_by_name(supplier_name: str)->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        suppliers = supplier_service.get_suppliers_containing_in_name_paginated(session,supplier_name, page, per_page)
        total = len(suppliers)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'suppliers/list.html',
            suppliers=suppliers,
            page=page,
            total_pages=total_pages
        )
    
@suppliers_bp.route("/get/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id)->Response:
    return jsonify({"message": f"supplier {supplier_id}"})