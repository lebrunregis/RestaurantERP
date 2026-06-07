from flask import Blueprint, Response, app,  jsonify, redirect, render_template, request, url_for
from pytest import Cache


from src.adapters_logic.services import client_order_service

from src.alchemy_db.session.session import SessionLocal

client_orders_bp = Blueprint(
        "client_orders", 
    __name__, 
    url_prefix="/client_orders",
    template_folder="templates"  # points to blueprints/client_orders/templates
)

@client_orders_bp.route('/')
def list_client_orders()->str:
    page = request.args.get('page', default=1, type=int)
    per_page = 50  # adjust as needed

    with SessionLocal() as session:
        client_orders, total = client_order_service.get_all_client_orders_paginated(session, page, per_page)
        total_pages = (total + per_page - 1) // per_page  # ceil division

        return render_template(
            'client_orders/list.html',
            client_orders=client_orders,
            page=page,
            total_pages=total_pages
        )


@client_orders_bp.route("/<int:client_order_id>")
def client_order_details(client_order_id)->str:
    with SessionLocal() as session:
        client_order=client_order_service.get_client_order_by_id(session,client_order_id)
        return render_template('client_orders/details.html', client_order=client_order) 

@client_orders_bp.route("/client/<int:client_id>")
def client_orders(client_id)->str:
    with SessionLocal() as session:
        client_orders=client_order_service.get_orders_by_client(session, client_id) 
        return render_template('client_orders/list.html', client_orders=client_orders) 

@client_orders_bp.route("/get/<int:client_order_id>", methods=["GET"])
def get_client_order(client_order_id)->Response:
    return jsonify({"message": f"client_order {client_order_id}"})