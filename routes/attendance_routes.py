import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.trainer_service import (
    get_all_trainers,
    get_trainer_by_id,
    determine_trainer_availability,
    get_trainer_availabilities,
    create_trainer_availability,
    delete_trainer_availability,
    get_all_calendar_events,
    create_calendar_event,
    delete_calendar_event,
    populate_calendar_holidays_if_needed
)

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/attendance", methods=["GET"])
def view_attendance():
    """
    Display attendance and availability dashboard for a given date.
    """
    date_param = request.args.get("date", "").strip()
    if not date_param:
        date_param = datetime.date.today().isoformat()

    try:
        dt = datetime.date.fromisoformat(date_param)
        selected_year = dt.year
    except ValueError:
        flash("Invalid date format. Defaulting to today.", "error")
        date_param = datetime.date.today().isoformat()
        selected_year = datetime.date.today().year

    # Automatically populate holidays for the chosen year
    populate_calendar_holidays_if_needed(selected_year)

    trainers = get_all_trainers()
    trainer_statuses = []

    for t in trainers:
        tid = t["trainer_id"]
        status_val, avail_type, desc, dur_type, slot, start, end = determine_trainer_availability(tid, date_param)
        trainer_statuses.append({
            "trainer_id": tid,
            "full_name": t["full_name"],
            "email": t["email"],
            "status": t["status"],
            "available": status_val,      # 1 = Available (Active), 0 = Unavailable (Inactive)
            "reason": avail_type,          # Available, Unavailable, Saturday, Public Holiday, etc.
            "description": desc,
            "duration_type": dur_type,
            "time_slot": slot,
            "start_time": start,
            "end_time": end
        })

    # Retrieve all availabilities and calendar events to display in management tabs
    all_availabilities = []
    for t in trainers:
        avails = get_trainer_availabilities(t["trainer_id"])
        for av in avails:
            all_availabilities.append({
                "availability_id": av["availability_id"],
                "trainer_id": av["trainer_id"],
                "full_name": t["full_name"],
                "date": av["date"],
                "status": av["status"],
                "availability_type": av["availability_type"],
                "duration_type": av["duration_type"],
                "time_slot": av["time_slot"],
                "start_time": av["start_time"],
                "end_time": av["end_time"],
                "description": av["description"]
            })

    # Sort availabilities by date descending
    all_availabilities.sort(key=lambda x: x["date"], reverse=True)

    events = get_all_calendar_events()

    return render_template(
        "attendance.html",
        date=date_param,
        year=selected_year,
        trainer_statuses=trainer_statuses,
        trainers=trainers,
        leaves=all_availabilities,  # Keep key 'leaves' for template context compatibility if needed, but rename variable
        events=events
    )


@attendance_bp.route("/attendance/availability/new", methods=["POST"])
def new_leave():
    """
    Record a trainer's availability override.
    """
    trainer_id = request.form.get("trainer_id", type=int)
    date_str = request.form.get("date", "").strip()
    availability_type = request.form.get("availability_type", "").strip()
    status = 1 if availability_type == "Available" else 0
    duration_type = request.form.get("duration_type", "").strip()
    time_slot = request.form.get("time_slot", "").strip() or None
    start_time = request.form.get("start_time", "").strip() or None
    end_time = request.form.get("end_time", "").strip() or None
    description = request.form.get("description", "").strip()

    if not trainer_id:
        flash("Trainer is required.", "error")
        return redirect(url_for("attendance.view_attendance", date=date_str))

    success, message = create_trainer_availability(
        trainer_id=trainer_id,
        date_str=date_str,
        status=status,
        availability_type=availability_type,
        duration_type=duration_type,
        time_slot=time_slot,
        start_time=start_time,
        end_time=end_time,
        description=description,
        created_by="SystemAdmin"
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("attendance.view_attendance", date=date_str))


@attendance_bp.route("/attendance/availability/<int:availability_id>/delete", methods=["POST"])
def remove_leave(availability_id):
    """
    Delete a trainer's availability/override record.
    """
    redirect_date = request.form.get("redirect_date", "").strip()
    success, message = delete_trainer_availability(availability_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("attendance.view_attendance", date=redirect_date))


@attendance_bp.route("/attendance/event/new", methods=["POST"])
def new_event():
    """
    Create a global calendar event (Public Holiday or Company Meeting).
    """
    date_str = request.form.get("date", "").strip()
    event_type = request.form.get("event_type", "").strip()
    description = request.form.get("description", "").strip()
    redirect_date = request.form.get("redirect_date", "").strip()

    success, message = create_calendar_event(
        date_str=date_str,
        event_type=event_type,
        description=description,
        created_by="SystemAdmin"
    )

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("attendance.view_attendance", date=redirect_date or date_str))


@attendance_bp.route("/attendance/event/import", methods=["POST"])
def import_holidays():
    """
    Import public holidays automatically for a given year.
    """
    year = request.form.get("year", type=int)
    redirect_date = request.form.get("redirect_date", "").strip()

    if not year:
        flash("Year is required.", "error")
        return redirect(url_for("attendance.view_attendance", date=redirect_date))

    success, message = populate_calendar_holidays_if_needed(year)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("attendance.view_attendance", date=redirect_date))


@attendance_bp.route("/attendance/event/<int:event_id>/delete", methods=["POST"])
def remove_event(event_id):
    """
    Delete a global calendar event.
    """
    redirect_date = request.form.get("redirect_date", "").strip()
    success, message = delete_calendar_event(event_id)

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("attendance.view_attendance", date=redirect_date))
