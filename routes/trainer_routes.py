from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.trainer_service import (
    create_trainer,
    update_trainer,
    get_trainer_by_id,
    get_all_trainers,
    delete_trainer,
    search_trainers,
    filter_trainers,
    get_trainer_statistics
)
from services.course_service import CourseService

course_service = CourseService()

trainer_bp = Blueprint("trainer", __name__)


@trainer_bp.route("/trainers/new", methods=["GET"])
def add_trainer():
    """
    Display the Add Trainer form.
    """
    courses = course_service.get_all_courses()
    return render_template("trainer_form.html", courses=courses)


@trainer_bp.route("/trainers", methods=["POST"])
def save_trainer():
    """
    Save a new trainer.
    """
    created_by = "SystemAdmin"  # Placeholder for authenticated user

    selected_skills = request.form.getlist("skills")
    skills_str = ", ".join(selected_skills)

    success, message = create_trainer(
        full_name=request.form.get("full_name", ""),
        email=request.form.get("email", ""),
        phone=request.form.get("phone", ""),
        skills=skills_str,
        previous_experience=request.form.get("previous_experience", "0"),
        date_of_joining=request.form.get("date_of_joining", ""),
        status="Active",
        qualifications=request.form.get("qualifications", ""),
        created_by=created_by
    )

    if success:
        flash(message, "success")
        return redirect(url_for("trainer.view_trainers"))
    else:
        flash(message, "error")
        return redirect(url_for("trainer.add_trainer"))


@trainer_bp.route("/trainers", methods=["GET"])
def view_trainers():
    """
    Display all trainers, with support for search and filtering.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status", "").strip()

    if keyword or status:
        trainers = filter_trainers(status=status, keyword=keyword)
    else:
        trainers = get_all_trainers()

    stats = get_trainer_statistics()

    return render_template(
        "trainers.html",
        trainers=trainers,
        stats=stats
    )


@trainer_bp.route("/trainers/<int:trainer_id>", methods=["GET"])
def view_trainer_details(trainer_id):
    """
    Display details of a single trainer.
    """
    trainer = get_trainer_by_id(trainer_id)

    if not trainer:
        flash("Trainer not found.", "error")
        return redirect(url_for("trainer.view_trainers"))

    return render_template(
        "trainer_details.html",
        trainer=trainer
    )


@trainer_bp.route("/trainers/<int:trainer_id>/edit", methods=["GET"])
def edit_trainer_page(trainer_id):
    """
    Display the Edit Trainer form.
    """
    trainer = get_trainer_by_id(trainer_id)

    if not trainer:
        flash("Trainer not found.", "error")
        return redirect(url_for("trainer.view_trainers"))

    courses = course_service.get_all_courses()
    skills_str = trainer.get("skills", "")
    current_skills = [s.strip() for s in skills_str.split(",") if s.strip()]

    return render_template(
        "edit_trainer.html",
        trainer=trainer,
        courses=courses,
        current_skills=current_skills
    )


@trainer_bp.route("/trainers/<int:trainer_id>/edit", methods=["POST"])
def edit_trainer(trainer_id):
    """
    Update an existing trainer.
    """
    updated_by = "SystemAdmin"  # Placeholder for authenticated user

    selected_skills = request.form.getlist("skills")
    skills_str = ", ".join(selected_skills)

    success, message = update_trainer(
        trainer_id=trainer_id,
        full_name=request.form.get("full_name", ""),
        email=request.form.get("email", ""),
        phone=request.form.get("phone", ""),
        skills=skills_str,
        previous_experience=request.form.get("previous_experience", "0"),
        date_of_joining=request.form.get("date_of_joining", ""),
        status="Active",
        qualifications=request.form.get("qualifications", ""),
        updated_by=updated_by
    )

    if success:
        flash(message, "success")
        return redirect(url_for("trainer.view_trainer_details", trainer_id=trainer_id))
    else:
        flash(message, "error")
        return redirect(url_for("trainer.edit_trainer_page", trainer_id=trainer_id))


@trainer_bp.route("/trainers/<int:trainer_id>/delete", methods=["POST"])
def remove_trainer(trainer_id):
    """
    Delete a trainer.
    """
    success, message = delete_trainer(trainer_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("trainer.view_trainers"))


@trainer_bp.route("/trainers/search")
def search():
    keyword = request.args.get("keyword", "")
    trainers = search_trainers(keyword)
    stats = get_trainer_statistics()

    return render_template(
        "trainers.html",
        trainers=trainers,
        stats=stats
    )


@trainer_bp.route("/trainers/filter")
def filter():
    status = request.args.get("status", "")
    trainers = filter_trainers(status=status)
    stats = get_trainer_statistics()

    return render_template(
        "trainers.html",
        trainers=trainers,
        stats=stats
    )