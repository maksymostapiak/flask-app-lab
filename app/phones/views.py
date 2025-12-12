from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from .models import Phone, Brand
from .forms import PhoneForm

phones_bp = Blueprint("phones", __name__, url_prefix="/phones", template_folder='templates')

@phones_bp.route("/", methods=["GET"])
def list_phones():

    search_query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'id_desc')

    phones_query = Phone.query

    if search_query:
        phones_query = phones_query.filter(Phone.model_name.contains(search_query))

    sort_options = {
        "name_asc": Phone.model_name.asc(),
        "name_desc": Phone.model_name.desc(),
        "price_asc": Phone.price.asc(),
        "price_desc": Phone.price.desc(),
        "brand_asc": Brand.name.asc(),
        "brand_desc": Brand.name.desc(),
        "id_asc": Phone.id.asc(),
        "id_desc": Phone.id.desc(),
    }

    if sort_by in sort_options:
        if "brand" in sort_by:
            phones_query = phones_query.join(Brand).order_by(sort_options[sort_by])
        else:
            phones_query = phones_query.order_by(sort_options[sort_by])

    phones = phones_query.all()

    return render_template(
        "phones/phones.html",
        phones=phones,
        search_query=search_query,
        sort_by=sort_by
    )

@phones_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_phone():
    form = PhoneForm()

    form.brand_id.choices = [(b.id, b.name) for b in Brand.query.all()]

    if form.validate_on_submit():
        phone = Phone(
            model_name=form.model_name.data,
            price=form.price.data,
            description=form.description.data,
            brand_id=form.brand_id.data,
            owner=current_user
        )
        db.session.add(phone)
        db.session.commit()
        flash("Телефон успішно додано!", "success")
        return redirect(url_for("phones.list_phones"))

    return render_template("phones/add_phone.html", form=form, title="Додати телефон")

@phones_bp.route("/<int:id>")
def detail_phone(id):
    phone = Phone.query.get_or_404(id)
    return render_template("phones/detail_phone.html", phone=phone)

@phones_bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_phone(id):
    phone = Phone.query.get_or_404(id)
    
    if phone.owner != current_user:
        flash("У вас немає прав для видалення цього запису.", "danger")
        return redirect(url_for('phones.list_phones'))

    form = PhoneForm()
    form.brand_id.choices = [(b.id, b.name) for b in Brand.query.all()]

    if form.validate_on_submit():
        phone.model_name = form.model_name.data
        phone.price = form.price.data
        phone.description = form.description.data
        phone.brand_id = form.brand_id.data
        
        db.session.commit()
        flash("Інформацію оновлено!", "success")
        return redirect(url_for("phones.detail_phone", id=phone.id))

    elif request.method == "GET":
        form.model_name.data = phone.model_name
        form.price.data = phone.price
        form.description.data = phone.description
        form.brand_id.data = phone.brand_id

    return render_template("phones/add_phone.html", form=form, title="Редагувати телефон")

@phones_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_phone(id):
    phone = Phone.query.get_or_404(id)
    
    if phone.owner != current_user:
        flash("У вас немає прав для видалення цього запису.", "danger")
        return redirect(url_for('phones.list_phones'))
        
    db.session.delete(phone)
    db.session.commit()
    flash("Запис видалено!", "info")
    return redirect(url_for("phones.list_phones"))