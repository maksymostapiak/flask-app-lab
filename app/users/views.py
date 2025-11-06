from flask import Blueprint, request, redirect, url_for, render_template, flash, session, make_response

users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='templates')

VALID_USERNAME = "admin"
VALID_PASSWORD = "12345"

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["user"] = username  
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірне ім’я користувача або пароль!", "danger")
            return redirect(url_for("users.login"))

    return render_template("users/login.html")

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