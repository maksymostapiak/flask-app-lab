from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response, current_app
import os
import secrets
from app.form import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from app.users.models import User
from app import db, bcrypt
from flask_bcrypt import check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from PIL import Image
from datetime import datetime, timezone


users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='templates', static_folder="static")

#VALID_USERNAME = "admin"
#VALID_PASSWORD = "12345"

@users_bp.before_app_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))

    return render_template("users/register.html", form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in successfully!', 'success')
            return redirect(url_for('users.account'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('users/login.html', form=form, title='Login')

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user = session.get("user")
    resp = make_response()
    if not user:
        flash("Будь ласка, увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    if request.method == 'POST' and 'add_cookie' in request.form:
        key = request.form['key']
        value = request.form['value']
        days = int(request.form['days'])
        resp.set_cookie(key, value, max_age=days*24*60*60)
        flash(f"Cookie '{key}' додано!", "success")

    if request.method == 'POST' and 'delete_cookie' in request.form:
        key = request.form['del_key']
        resp.delete_cookie(key)
        flash(f"Cookie '{key}' видалено!", "warning")

    if request.method == 'POST' and 'delete_all' in request.form:
        for key in request.cookies:
            resp.delete_cookie(key)
        flash("Всі cookies видалено!", "danger")

    resp.response = render_template("users/profile.html",username=user)
    return resp


@users_bp.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/theme", methods=["GET", "POST"])
def theme():
    if request.method == "POST":
        theme = request.form.get("theme", "light")
        resp = make_response(redirect(url_for("users.profile")))
        resp.set_cookie("theme", theme, max_age=60*60*24*30)
        return resp

    return render_template("users/theme.html")

@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file 
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Ваш акаунт було оновлено!', 'success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('users.static', filename=current_user.image if current_user.image else 'profile_default.jpg')
    
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)

@users_bp.route("/users")
@login_required
def users_list():
    users = User.query.all()
    total = len(users)
    return render_template("users/userslist.html", users=users, total=total)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(current_app.root_path, 'users/static', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    

    i.save(picture_path)

    return picture_fn

@users_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("users.change_password"))

        hashed = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        current_user.password = hashed
        db.session.commit()

        flash("Your password has been updated!", "success")
        return redirect(url_for("users.account"))

    return render_template("users/change_password.html", form=form)