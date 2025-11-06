from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route('/')
def resume():
    return render_template(
        'resume.html',
        page_title='Резюме',
        header_title='Моє резюме'
    )

@app.route('/contacts')
def contacts():
    return render_template(
        'contacts.html',
        page_title='Контакти',
        header_title='Зв’язок зі мною'
    )
