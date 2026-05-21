from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role(current_user)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not username or not password:
            flash("Username dan password wajib diisi.", "danger")
            return render_template("login.html")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            flash(f"Selamat datang, {user.full_name}!", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return _redirect_by_role(user)

        flash("Username atau password salah.", "danger")

    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template("login.html", school_name=school_name)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Kamu berhasil logout.", "info")
    return redirect(url_for("auth.login"))


def _redirect_by_role(user):
    if user.is_admin():
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("student.dashboard"))
