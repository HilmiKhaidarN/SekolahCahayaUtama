from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.app import db
from app.models import Lesson, LessonProgress
from datetime import datetime

student_bp = Blueprint("student", __name__)


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash("Akses ditolak.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@student_bp.route("/dashboard")
@login_required
@student_required
def dashboard():
    lessons = Lesson.query.filter_by(is_published=True).all()
    completed_ids = {
        p.lesson_id
        for p in LessonProgress.query.filter_by(
            user_id=current_user.id, is_completed=True
        ).all()
    }
    total = len(lessons)
    completed = len(completed_ids)
    percent = int((completed / total * 100)) if total > 0 else 0
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template(
        "student/dashboard.html",
        school_name=school_name,
        lessons=lessons,
        completed_ids=completed_ids,
        total=total,
        completed=completed,
        percent=percent,
    )


@student_bp.route("/lessons")
@login_required
@student_required
def lessons():
    all_lessons = Lesson.query.filter_by(is_published=True).order_by(Lesson.subject).all()
    completed_ids = {
        p.lesson_id
        for p in LessonProgress.query.filter_by(
            user_id=current_user.id, is_completed=True
        ).all()
    }
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template(
        "student/lessons.html",
        school_name=school_name,
        lessons=all_lessons,
        completed_ids=completed_ids,
    )


@student_bp.route("/lessons/<int:lesson_id>")
@login_required
@student_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson_id
    ).first()
    school_name = current_app.config.get("SCHOOL_NAME")
    return render_template(
        "student/lesson_detail.html",
        school_name=school_name,
        lesson=lesson,
        progress=progress,
    )


@student_bp.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
@login_required
@student_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson_id
    ).first()

    if not progress:
        progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id)
        db.session.add(progress)

    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = datetime.utcnow()
        db.session.commit()
        flash(f"Selamat! Kamu telah menyelesaikan materi '{lesson.title}'.", "success")
    else:
        flash("Materi ini sudah kamu selesaikan sebelumnya.", "info")

    return redirect(url_for("student.lessons"))
