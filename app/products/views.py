from flask import Blueprint, request, redirect, url_for, render_template

products_bp = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')

@products_bp.route("/list")
def product_list():
    products = [
        {"name": "Laptop", "price": 1200},
        {"name": "Phone", "price": 800},
        {"name": "Tablet", "price": 500}
    ]
    return render_template('products/list.html', products=products)