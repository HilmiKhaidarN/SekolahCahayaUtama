from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.app import db
from app.models import User, Lesson, LessonProgress
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Akses ditolak. Halaman ini khusus admin.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_students = User.query.filter_by(role="student").count()
    total_lessons = Lesson.query.count()
    total_completions = LessonProgress.query.filter_by(is_completed=True).count()
    recent_users = (
        User.query.filter_by(role="student")
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template(
        "admin/dashboard.html",
        school_name=school_name,
        total_students=total_students,
        total_lessons=total_lessons,
        total_completions=total_completions,
        recent_users=recent_users,
    )


@admin_bp.route("/users")
@login_required
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template("admin/manage_users.html", users=users, school_name=school_name)


@admin_bp.route("/users/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    school_name = current_app.config.get("SCHOOL_NAME")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")

        if not all([username, email, full_name, password]):
            flash("Semua field wajib diisi.", "danger")
            return render_template("admin/add_user.html", school_name=school_name)

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return render_template("admin/add_user.html", school_name=school_name)

        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan.", "danger")
            return render_template("admin/add_user.html", school_name=school_name)

        user = User(username=username, email=email, full_name=full_name, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f"Pengguna {full_name} berhasil ditambahkan.", "success")
        return redirect(url_for("admin.manage_users"))

    return render_template("admin/add_user.html", school_name=school_name)


@admin_bp.route("/users/toggle/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Tidak bisa menonaktifkan akun sendiri.", "warning")
        return redirect(url_for("admin.manage_users"))
    user.is_active = not user.is_active
    db.session.commit()
    status = "diaktifkan" if user.is_active else "dinonaktifkan"
    flash(f"Akun {user.full_name} berhasil {status}.", "success")
    return redirect(url_for("admin.manage_users"))


@admin_bp.route("/lessons")
@login_required
@admin_required
def manage_lessons():
    lessons = Lesson.query.order_by(Lesson.created_at.desc()).all()
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template("admin/manage_lessons.html", lessons=lessons, school_name=school_name)


@admin_bp.route("/lessons/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_lesson():
    school_name = current_app.config.get("SCHOOL_NAME")
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()
        content = request.form.get("content", "").strip()
        level = request.form.get("level", "Dasar")

        if not all([title, subject, description, content]):
            flash("Semua field wajib diisi.", "danger")
            return render_template("admin/add_lesson.html", school_name=school_name)

        lesson = Lesson(
            title=title, subject=subject,
            description=description, content=content, level=level
        )
        db.session.add(lesson)
        db.session.commit()
        flash(f"Materi '{title}' berhasil ditambahkan.", "success")
        return redirect(url_for("admin.manage_lessons"))

    return render_template("admin/add_lesson.html", school_name=school_name)


@admin_bp.route("/lessons/delete/<int:lesson_id>", methods=["POST"])
@login_required
@admin_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    LessonProgress.query.filter_by(lesson_id=lesson_id).delete()
    db.session.delete(lesson)
    db.session.commit()
    flash(f"Materi '{lesson.title}' berhasil dihapus.", "success")
    return redirect(url_for("admin.manage_lessons"))
