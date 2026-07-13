from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.trainer_service import (
    create_trainer,
    update_trainer,
    get_trainer_by_id,
    get_all_trainers,
    delete_trainer,
    search_trainers,
    filter_trainers,
    get_trainer_availability,
    update_trainer_availability
)

trainer_bp = Blueprint("trainer", __name__)


@trainer_bp.route("/trainers/new", methods=["GET"])
def add_trainer():
    """
    Display the Add Trainer form.
    """
    return render_template("trainer_form.html")


@trainer_bp.route("/trainers", methods=["POST"])
def save_trainer():
    """
    Save a new trainer.
    """

    success, message = create_trainer(
        request.form.get("full_name", ""),
        request.form.get("email", ""),
        request.form.get("phone", ""),
        request.form.get("skills", ""),
        request.form.get("experience", ""),
        request.form.get("status", ""),
        request.form.get("availability", "")
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("trainer.add_trainer"))


@trainer_bp.route("/trainers", methods=["GET"])
def view_trainers():
    """
    Display all trainers.
    """

    trainers = get_all_trainers()

    return render_template(
        "trainers.html",
        trainers=trainers
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

    return render_template(
        "edit_trainer.html",
        trainer=trainer
    )


@trainer_bp.route("/trainers/<int:trainer_id>/edit", methods=["POST"])
def edit_trainer(trainer_id):
    """
    Update an existing trainer.
    """

    success, message = update_trainer(
        trainer_id,
        request.form.get("full_name", ""),
        request.form.get("email", ""),
        request.form.get("phone", ""),
        request.form.get("skills", ""),
        request.form.get("experience", ""),
        request.form.get("status", ""),
        request.form.get("availability", "")
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("trainer.view_trainers"))


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

    return render_template(
        "trainers.html",
        trainers=trainers
    )


@trainer_bp.route("/trainers/filter")
def filter():

    availability = request.args.get("availability", "")
    status = request.args.get("status", "")

    trainers = filter_trainers(availability=availability, status=status)

    return render_template(
        "trainers.html",
        trainers=trainers
    )


@trainer_bp.route("/trainers/<int:trainer_id>/availability", methods=["GET"])
def trainer_availability(trainer_id):
    """
    Display trainer availability.
    """

    trainer = get_trainer_availability(trainer_id)

    return render_template(
        "trainer_availability.html",
        trainer=trainer
    )


@trainer_bp.route("/trainers/<int:trainer_id>/availability", methods=["POST"])
def update_availability(trainer_id):
    """
    Update trainer availability.
    """

    availability = request.form.get("availability", "")

    success, message = update_trainer_availability(trainer_id, availability)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("trainer.view_trainers"))