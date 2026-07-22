from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.batch_service import BatchService
from services.course_service import CourseService
from services.trainer_service import get_all_trainers
from services.student_service import StudentService

batch_bp = Blueprint("batch_bp", __name__)
batch_service = BatchService()
course_service = CourseService()
student_service = StudentService()


@batch_bp.route("/batches")
def list_batches():
    """
    Displays the batch management dashboard and filtered list of batches.
    """
    status = request.args.get("status")
    course_id = request.args.get("course_id")
    trainer_id = request.args.get("trainer_id")
    mode = request.args.get("mode")
    search = request.args.get("search")

    batches = batch_service.get_all_batches(
        status=status,
        course_id=course_id,
        trainer_id=trainer_id,
        mode=mode,
        search=search
    )
    stats = batch_service.get_statistics()
    courses = course_service.get_active_courses()
    trainers = [t for t in get_all_trainers() if t.get('status') == 'Active']

    return render_template(
        "batches.html",
        batches=batches,
        stats=stats,
        courses=courses,
        trainers=trainers,
        selected_status=status or "",
        selected_course=course_id or "",
        selected_trainer=trainer_id or "",
        selected_mode=mode or "",
        search_query=search or ""
    )


@batch_bp.route("/batches/create", methods=["GET", "POST"])
def create_batch():
    """
    Renders creation form and processes new batch registration.
    """
    if request.method == "POST":
        batch_code = request.form.get("batch_code", "").strip()
        batch_name = request.form.get("batch_name", "").strip()
        course_id = request.form.get("course_id")
        trainer_id = request.form.get("trainer_id")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        slot_type = request.form.get("slot_type")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        mode = request.form.get("mode", "Offline")
        location = request.form.get("location")
        max_capacity = request.form.get("max_capacity", 30)
        enrolled_count = request.form.get("enrolled_count", 1)
        status = request.form.get("status", "Upcoming")
        description = request.form.get("description")

        try:
            res = batch_service.create_batch(
                batch_code=batch_code,
                batch_name=batch_name,
                course_id=course_id,
                trainer_id=trainer_id,
                start_date=start_date,
                end_date=end_date,
                slot_type=slot_type,
                start_time=start_time,
                end_time=end_time,
                mode=mode,
                location=location,
                max_capacity=max_capacity,
                enrolled_count=enrolled_count,
                status=status,
                description=description,
                created_by="Admin"
            )
            flash(res["message"], "success")
            return redirect(url_for("batch_bp.list_batches"))
        except ValueError as e:
            flash(str(e), "error")
            courses = course_service.get_active_courses()
            trainers = [t for t in get_all_trainers() if t.get('status') == 'Active']
            return render_template(
                "batch_form.html",
                action="Create",
                batch=request.form,
                courses=courses,
                trainers=trainers
            )

    # GET Request
    auto_code = batch_service.generate_batch_code()
    courses = course_service.get_active_courses()
    trainers = [t for t in get_all_trainers() if t.get('status') == 'Active']

    return render_template(
        "batch_form.html",
        action="Create",
        batch={"batch_code": auto_code, "max_capacity": 30, "enrolled_count": 1, "status": "Upcoming", "mode": "Offline"},
        courses=courses,
        trainers=trainers
    )


@batch_bp.route("/batches/<int:batch_id>")
def view_batch_details(batch_id):
    """
    Renders details page for a specific batch.
    """
    try:
        batch = batch_service.get_batch_by_id(batch_id)
        students = student_service.get_students_by_batch(batch_id)
        return render_template("batch_details.html", batch=batch, students=students)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("batch_bp.list_batches"))


@batch_bp.route("/batches/<int:batch_id>/edit", methods=["GET", "POST"])
def edit_batch(batch_id):
    """
    Renders edit form and updates existing batch details.
    """
    if request.method == "POST":
        batch_name = request.form.get("batch_name", "").strip()
        course_id = request.form.get("course_id")
        trainer_id = request.form.get("trainer_id")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        slot_type = request.form.get("slot_type")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        mode = request.form.get("mode", "Offline")
        location = request.form.get("location")
        max_capacity = request.form.get("max_capacity", 30)
        status = request.form.get("status", "Upcoming")
        description = request.form.get("description")

        try:
            res = batch_service.update_batch(
                batch_id=batch_id,
                batch_name=batch_name,
                course_id=course_id,
                trainer_id=trainer_id,
                start_date=start_date,
                end_date=end_date,
                slot_type=slot_type,
                start_time=start_time,
                end_time=end_time,
                mode=mode,
                location=location,
                max_capacity=max_capacity,
                status=status,
                description=description,
                updated_by="Admin"
            )
            flash(res["message"], "success")
            return redirect(url_for("batch_bp.view_batch_details", batch_id=batch_id))
        except ValueError as e:
            flash(str(e), "error")
            courses = course_service.get_active_courses()
            trainers = [t for t in get_all_trainers() if t.get('status') == 'Active']
            existing_batch = batch_service.get_batch_by_id(batch_id)
            form_data = dict(existing_batch) if existing_batch else {}
            form_data.update(request.form)
            return render_template(
                "batch_form.html",
                action="Edit",
                batch=form_data,
                courses=courses,
                trainers=trainers
            )

    # GET Request
    try:
        batch = batch_service.get_batch_by_id(batch_id)
        courses = course_service.get_active_courses()
        trainers = [t for t in get_all_trainers() if t.get('status') == 'Active']
        return render_template(
            "batch_form.html",
            action="Edit",
            batch=batch,
            courses=courses,
            trainers=trainers
        )
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("batch_bp.list_batches"))


@batch_bp.route("/batches/<int:batch_id>/status", methods=["POST"])
def update_batch_status(batch_id):
    """
    Updates status of a batch directly (e.g. from dropdown or quick button).
    """
    status = request.form.get("status")
    try:
        res = batch_service.update_status(batch_id, status, updated_by="Admin")
        flash(res["message"], "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(request.referrer or url_for("batch_bp.list_batches"))


@batch_bp.route("/batches/<int:batch_id>/delete", methods=["POST"])
def delete_batch(batch_id):
    """
    Deletes a batch record if validation permits.
    """
    try:
        res = batch_service.delete_batch(batch_id)
        flash(res["message"], "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("batch_bp.list_batches"))


@batch_bp.route("/api/calculate-end-date")
def api_calculate_end_date():
    """
    AJAX endpoint for automatic end date and project submission date estimation.
    """
    course_id = request.args.get("course_id")
    start_date = request.args.get("start_date")
    slot_type = request.args.get("slot_type")

    if not course_id or not start_date or not slot_type:
        return jsonify({"success": False, "error": "Missing parameters"}), 400

    try:
        res = batch_service.calculate_end_date(course_id, start_date, slot_type)
        if isinstance(res, dict):
            return jsonify({"success": True, "end_date": res.get("end_date"), "project_date": res.get("project_date")})
        return jsonify({"success": True, "end_date": res})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

