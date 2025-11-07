import logging
from flask import request, redirect, url_for, render_template, abort, flash
from . import app
from app.form import ContactForm


logging.basicConfig(
    filename="contact_form.log",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

@app.route('/')
def resume():
    return render_template(
        'resume.html',
        page_title='Резюме',
        header_title='Моє резюме'
    )

@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():

        logging.info(
            f"User: {form.name.data}, Email: {form.email.data}, Phone: {form.phone.data}, Subject: {form.subject.data}"
        )

        flash(f"Повідомлення надіслано! Дякуємо, {form.name.data}. Ваша пошта - {form.email.data}", "success")

        return redirect(url_for("contacts"))

    return render_template("contacts.html", form=form)
