from flask import Blueprint, Response, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services import client_service

from src.alchemy_db.session.session import SessionLocal

clients_bp = Blueprint(
        "clients", 
    __name__, 
    url_prefix="/clients",
    template_folder="templates"  # points to blueprints/clients/templates
)

@clients_bp.route('/')
def list_clients()->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        clients, total = client_service.get_clients_paginated(session, page, per_page)
        total = client_service.
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'clients/list.html',
            clients=clients,
            page=page,
            total_pages=total_pages
        )

@clients_bp.route("/<int:client_id>")
def client_details(client_id)->str:
    with SessionLocal() as session:
        client=client_service.get_client_by_id(session,client_id)
        return render_template('clients/details.html', client=client) 
         
@clients_bp.route("/search")
def search_clients()->str:
    query = request.args.get("q","").strip()
    if not query:
        return render_template("clients/list.html", clients=[])
    else:
       return  search_clients_by_name(query)

def search_clients_by_name(client_name: str)->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        clients = client_service.get_clients_containing_in_name_paginated(session,client_name, page, per_page)
        total = len(clients)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'clients/list.html',
            clients=clients,
            page=page,
            total_pages=total_pages
        )
    
@clients_bp.route("/get/<int:client_id>", methods=["GET"])
def get_client(client_id)->Response:
    return jsonify({"message": f"client {client_id}"})