from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response
from app.form import LoginForm, RegistrationForm
from app.users.models import User
from app import db, bcrypt
from flask_bcrypt import check_password_hash


users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')

#VALID_USERNAME = "admin"
#VALID_PASSWORD = "12345"

@users_bp.route("/register", methods=["GET", "POST"])
def register():
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

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        entered = form.username.data.strip()

        user = User.query.filter(
            (User.username == entered) | (User.email == entered)
        ).first()

        if user and check_password_hash(user.password, form.password.data):
            session["user"] = user.id

            if form.remember.data:
                flash(f"Вітаємо, {user.username}! (Запам'ятати увімкнено)", "success")
            else:
                flash(f"Вітаємо, {user.username}!", "success")

            return redirect(url_for("users.profile"))

        flash("Невірний username або пароль!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", form=form)

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
    session.pop("user", None)
    flash("Ви вийшли із системи!", "info")
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
def account():
    user_id = session.get("user")

    if not user_id:
        flash("Спочатку увійдіть у свій акаунт!", "warning")
        return redirect(url_for("users.login"))

    user = User.query.get(user_id)

    return render_template("users/account.html", user=user)

@users_bp.route("/users")
def users_list():
    users = User.query.all()
    total = len(users)
    return render_template("users/userslist.html", users=users, total=total)
