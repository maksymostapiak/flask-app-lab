from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response
from app.form import LoginForm, RegistrationForm
from app.users.models import User
from app import db, bcrypt
from flask_bcrypt import check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')

#VALID_USERNAME = "admin"
#VALID_PASSWORD = "12345"

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

@users_bp.route("/account")
@login_required
def account():
    user = current_user

    return render_template("users/account.html", user=user)

@users_bp.route("/users")
@login_required
def users_list():
    users = User.query.all()
    total = len(users)
    return render_template("users/userslist.html", users=users, total=total)
