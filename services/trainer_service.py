import logging
import os
import datetime
import holidays
from database.db import get_connection

# Configure Audit Logger
logger = logging.getLogger("trainer_audit")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Set log path to the project root directory
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "trainer_audit.log")
    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

from models.trainer import (
    get_all_trainers as fetch_trainers,
    update_trainer as update_trainer_model,
    delete_trainer as delete_trainer_model,
    search_trainers as search_trainers_model,
    filter_trainers as filter_trainers_model,
    get_trainer_availability as get_availability_model,
    get_trainer_by_id as get_trainer_by_id_model,
    update_trainer_availability as update_availability_model_db,
    get_trainer_statistics as fetch_trainer_stats,
    
    # Child Availabilities tables
    get_trainer_availabilities as db_get_trainer_availabilities,
    get_trainer_availability_by_date as db_get_trainer_availability_by_date,
    create_trainer_availability as db_create_trainer_availability,
    update_trainer_availability_record as db_update_trainer_availability_record,
    delete_trainer_availability as db_delete_trainer_availability,
    
    # Calendar Events tables
    get_all_calendar_events as db_get_all_calendar_events,
    get_calendar_event_by_date as db_get_calendar_event_by_date,
    create_calendar_event as db_create_calendar_event,
    delete_calendar_event as db_delete_calendar_event
)


def _validate_trainer(
    full_name,
    email,
    phone,
    skills,
    qualifications,
    previous_experience,
    date_of_joining,
    status
):
    if not full_name or not full_name.strip():
        return False, "Trainer name is required."

    if not email or not email.strip():
        return False, "Email is required."

    import re
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.strip()):
        return False, "Email address must be a valid format."

    if not phone or not phone.strip():
        return False, "Phone number is required."

    # Validate phone format: must contain exactly 10 digits
    cleaned_phone = "".join([c for c in phone if c.isdigit()])
    if len(cleaned_phone) != 10:
        return False, "Phone number must contain exactly 10 digits."

    if not skills or not skills.strip():
        return False, "Skills is required."

    # Qualifications is optional, but if present must be text
    if qualifications is not None and not isinstance(qualifications, str):
        return False, "Qualifications must be text."

    try:
        exp_val = float(previous_experience)
        if exp_val < 0:
            return False, "Previous Experience cannot be negative."
    except (ValueError, TypeError):
        return False, "Previous Experience must be a valid number."

    if date_of_joining:
        try:
            datetime.date.fromisoformat(date_of_joining)
        except ValueError:
            return False, "Date of Joining must be in YYYY-MM-DD format."
    else:
        return False, "Date of Joining is required."

    if status not in ("Active", "Inactive"):
        return False, "Status must be Active or Inactive."

    return True, ""


def create_trainer(
    full_name,
    email,
    phone,
    skills,
    previous_experience,
    date_of_joining,
    status="Active",
    qualifications="",
    created_by="SystemAdmin"
):
    """
    Insert a new trainer into the database.
    """
    is_valid, msg = _validate_trainer(
        full_name,
        email,
        phone,
        skills,
        qualifications,
        previous_experience,
        date_of_joining,
        status
    )

    if not is_valid:
        logger.warning(f"Failed to create trainer. Validation error: {msg}")
        return False, msg

    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO trainer
            (
                full_name,
                email,
                phone,
                skills,
                qualifications,
                experience,
                date_of_joining,
                previous_experience,
                status,
                created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            query,
            (
                full_name,
                email,
                phone,
                skills,
                qualifications,
                int(float(previous_experience)),
                date_of_joining,
                float(previous_experience),
                status,
                created_by
            )
        )
        connection.commit()
        logger.info(f"Successfully created trainer: name='{full_name}', email='{email}'")
        return True, "Trainer saved successfully."
    except Exception as error:
        logger.error(f"Failed to create trainer: name='{full_name}', email='{email}'. DB Error: {error}")
        print(f"Database Error: {error}")
        err_msg = str(error).lower()
        if "unique constraint failed" in err_msg:
            if "email" in err_msg:
                return False, "Email already exists."
            elif "phone" in err_msg:
                return False, "Phone number already exists."
            return False, "Email or Phone already exists."
        return False, "Failed to save trainer."
    finally:
        connection.close()


def get_all_trainers():
    """
    Return all trainers with calculated experience metrics.
    """
    trainers = fetch_trainers()
    today = datetime.date.today()
    trainer_list = []
    for t in trainers:
        t_dict = dict(t)
        doj_str = t_dict.get('date_of_joining')
        prev_exp = t_dict.get('previous_experience') or 0.0
        this_org_exp = 0.0
        if doj_str:
            try:
                doj = datetime.date.fromisoformat(doj_str)
                this_org_exp = max(0.0, (today - doj).days / 365.25)
            except Exception:
                pass
        t_dict['this_org_experience'] = round(this_org_exp, 1)
        t_dict['total_experience'] = round(prev_exp + this_org_exp, 1)
        trainer_list.append(t_dict)
    return trainer_list


def update_trainer(
    trainer_id,
    full_name,
    email,
    phone,
    skills,
    previous_experience,
    date_of_joining,
    status="Active",
    qualifications="",
    updated_by="SystemAdmin"
):
    """
    Validate and update trainer.
    """
    is_valid, msg = _validate_trainer(
        full_name,
        email,
        phone,
        skills,
        qualifications,
        previous_experience,
        date_of_joining,
        status
    )

    if not is_valid:
        logger.warning(f"Failed to update trainer ID {trainer_id}. Validation error: {msg}")
        return False, msg

    updated = update_trainer_model(
        trainer_id,
        full_name,
        email,
        phone,
        skills,
        qualifications,
        int(float(previous_experience)),
        date_of_joining,
        float(previous_experience),
        status,
        updated_by
    )

    if updated:
        logger.info(f"Successfully updated trainer ID {trainer_id}: name='{full_name}'")
        return True, "Trainer updated successfully."

    logger.warning(f"Failed to update trainer ID {trainer_id}: Trainer not found.")
    return False, "Trainer not found."


def delete_trainer(trainer_id):
    """
    Delete trainer after validation.
    """
    deleted = delete_trainer_model(trainer_id)
    if deleted:
        logger.info(f"Successfully deleted trainer ID {trainer_id}")
        return True, "Trainer deleted successfully."
    logger.warning(f"Failed to delete trainer ID {trainer_id}: Trainer not found.")
    return False, "Trainer not found."


def search_trainers(keyword):
    """
    Search trainers.
    """
    if not keyword.strip():
        return []
    trainers = search_trainers_model(keyword)
    today = datetime.date.today()
    trainer_list = []
    for t in trainers:
        t_dict = dict(t)
        doj_str = t_dict.get('date_of_joining')
        prev_exp = t_dict.get('previous_experience') or 0.0
        this_org_exp = 0.0
        if doj_str:
            try:
                doj = datetime.date.fromisoformat(doj_str)
                this_org_exp = max(0.0, (today - doj).days / 365.25)
            except Exception:
                pass
        t_dict['this_org_experience'] = round(this_org_exp, 1)
        t_dict['total_experience'] = round(prev_exp + this_org_exp, 1)
        trainer_list.append(t_dict)
    return trainer_list


def filter_trainers(status=None, keyword=None):
    """
    Filter trainers by status and search keyword.
    """
    trainers = filter_trainers_model(status, keyword)
    today = datetime.date.today()
    trainer_list = []
    for t in trainers:
        t_dict = dict(t)
        doj_str = t_dict.get('date_of_joining')
        prev_exp = t_dict.get('previous_experience') or 0.0
        this_org_exp = 0.0
        if doj_str:
            try:
                doj = datetime.date.fromisoformat(doj_str)
                this_org_exp = max(0.0, (today - doj).days / 365.25)
            except Exception:
                pass
        t_dict['this_org_experience'] = round(this_org_exp, 1)
        t_dict['total_experience'] = round(prev_exp + this_org_exp, 1)
        trainer_list.append(t_dict)
    return trainer_list


def get_trainer_availability(trainer_id):
    """
    Get trainer availability (kept for compatibility, returns active/inactive status).
    """
    trainer = get_availability_model(trainer_id)
    if trainer:
        return trainer
    return None


def get_trainer_by_id(trainer_id):
    """
    Get trainer by ID.
    """
    trainer = get_trainer_by_id_model(trainer_id)
    if trainer:
        trainer_dict = dict(trainer)
        
        # Calculate dynamic experience metrics
        doj_str = trainer_dict.get('date_of_joining')
        prev_exp = trainer_dict.get('previous_experience') or 0.0
        
        this_org_exp = 0.0
        if doj_str:
            try:
                doj = datetime.date.fromisoformat(doj_str)
                today = datetime.date.today()
                this_org_exp = max(0.0, (today - doj).days / 365.25)
            except Exception:
                pass
        trainer_dict['this_org_experience'] = round(this_org_exp, 1)
        trainer_dict['total_experience'] = round(prev_exp + this_org_exp, 1)
        
        today_str = datetime.date.today().isoformat()
        status_val, _, _, _, _, _, _ = determine_trainer_availability(trainer_id, today_str)
        trainer_dict['availability'] = "Available" if status_val == 1 else "Unavailable"
        return trainer_dict
    return None


def update_trainer_availability(trainer_id, availability, updated_by="SystemAdmin"):
    """
    Update today's availability override for compatibility.
    """
    if availability not in ("Available", "Unavailable"):
        logger.warning(f"Failed to update availability for trainer ID {trainer_id}. Invalid availability: {availability}")
        return False, "Invalid availability status."

    updated = update_availability_model_db(trainer_id, availability, updated_by)
    if updated:
        logger.info(f"Successfully updated availability for trainer ID {trainer_id} to '{availability}'")
        return True, "Availability updated successfully."

    logger.warning(f"Failed to update availability for trainer ID {trainer_id}: Trainer not found.")
    return False, "Trainer not found."


def get_trainer_statistics():
    """
    Get trainer statistics.
    """
    return fetch_trainer_stats()


# --- Trainer Leaves Services ---

def determine_trainer_availability(trainer_id, date_str):
    """
    Determine a trainer's availability for a given date in format YYYY-MM-DD.
    Lookup hierarchy:
    1. trainer_availablity child table (override).
    2. Trainer Status (if Inactive, default to Unavailable).
    3. calendar_event (Public Holiday / Company Meeting).
    4. Saturday / Sunday (Weekend).
    5. Default: Available.
    """
    # 1. Check trainer availability table (override)
    override = db_get_trainer_availability_by_date(trainer_id, date_str)
    if override is not None:
        status_val = override['status']
        avail_type = override['availability_type']
        desc = override['description']
        dur_type = override['duration_type']
        slot = override['time_slot']
        start = override['start_time']
        end = override['end_time']
        return status_val, avail_type, desc, dur_type, slot, start, end

    # 2. Check trainer profile status
    trainer = get_trainer_by_id_model(trainer_id)
    if trainer and trainer['status'] == 'Inactive':
         return 0, "Inactive", "Trainer is Inactive", "Full Day", None, None, None

    # 3. Check calendar events
    cal_event = db_get_calendar_event_by_date(date_str)
    if cal_event is not None:
        return 0, cal_event['event_type'], cal_event['description'], "Full Day", None, None, None

    # 4. Check weekend (Saturday or Sunday)
    try:
        dt = datetime.date.fromisoformat(date_str)
        if dt.weekday() == 5: # Saturday
            return 0, "Weekend", "Weekend (Saturday)", "Full Day", None, None, None
        elif dt.weekday() == 6: # Sunday
            return 0, "Weekend", "Weekend (Sunday)", "Full Day", None, None, None
    except ValueError:
        return 0, "Error", "Invalid Date Format", "Full Day", None, None, None

    # 5. Default: Available
    return 1, "Available", "Available", "Full Day", None, None, None


def get_trainer_availabilities(trainer_id):
    """Get all availabilities/overrides for a trainer."""
    return db_get_trainer_availabilities(trainer_id)


def create_trainer_availability(trainer_id, date_str, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by="SystemAdmin"):
    """
    Create an availability record (status = 0 for Unavailable, 1 for Available).
    """
    if status not in (0, 1):
        return False, "Status must be 0 (Unavailable) or 1 (Available)."
    if availability_type not in ("Available", "Unavailable"):
        return False, "Availability Type must be Available or Unavailable."
    if not date_str:
        return False, "Date is required."

    try:
        datetime.date.fromisoformat(date_str)
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."

    # Prevent duplicate date for the same trainer
    existing = db_get_trainer_availability_by_date(trainer_id, date_str)
    if existing:
        return False, f"Trainer already has an availability record set on {date_str}."

    success = db_create_trainer_availability(trainer_id, date_str, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by)
    if success:
        logger.info(f"Recorded availability for trainer {trainer_id} on {date_str}: status={status}")
        return True, "Availability record created successfully."
    return False, "Failed to create availability record."


def update_trainer_availability(availability_id, status, availability_type, duration_type, time_slot, start_time, end_time, description, updated_by="SystemAdmin"):
    """Update an availability record."""
    if status not in (0, 1):
        return False, "Status must be 0 (Unavailable) or 1 (Available)."
    if availability_type not in ("Available", "Unavailable"):
        return False, "Availability Type must be Available or Unavailable."

    success = db_update_trainer_availability_record(availability_id, status, availability_type, duration_type, time_slot, start_time, end_time, description, updated_by)
    if success:
        logger.info(f"Updated availability record ID {availability_id}")
        return True, "Availability record updated successfully."
    return False, "Failed to update availability record."


def delete_trainer_availability(availability_id):
    """Delete an availability record."""
    success = db_delete_trainer_availability(availability_id)
    if success:
        logger.info(f"Deleted availability record ID {availability_id}")
        return True, "Availability record deleted successfully."
    return False, "Failed to delete availability record."


# --- Global Calendar Event Services ---

def get_all_calendar_events():
    """Retrieve all calendar events (Holidays/Meetings)."""
    return db_get_all_calendar_events()


def populate_calendar_holidays_if_needed(year):
    """
    Automatically populates the calendar_event table with public holidays
    for the given year if they are not already populated.
    """
    try:
        # Use region 'IN' matching UTC+5:30
        in_holidays = holidays.country_holidays('IN', years=int(year))
        
        inserted_count = 0
        for date_obj, name in sorted(in_holidays.items()):
            date_str = date_obj.isoformat()
            existing = db_get_calendar_event_by_date(date_str)
            if not existing:
                db_create_calendar_event(
                    date_str=date_str,
                    event_type="Public Holiday",
                    description=name,
                    created_by="SystemAdmin"
                )
                inserted_count += 1
        if inserted_count > 0:
            logger.info(f"Automatically populated {inserted_count} public holidays for year {year}")
        return True, f"Imported {inserted_count} public holidays for year {year}."
    except Exception as e:
        logger.error(f"Failed to populate holidays for year {year}: {e}")
        return False, f"Failed to populate holidays: {e}"


def create_calendar_event(date_str, event_type, description, created_by="SystemAdmin"):
    """Create a new calendar event manually."""
    if event_type not in ("Public Holiday", "Company Meeting"):
        return False, "Event Type must be Public Holiday or Company Meeting."
    if not date_str:
        return False, "Date is required."

    try:
        datetime.date.fromisoformat(date_str)
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."

    existing = db_get_calendar_event_by_date(date_str)
    if existing:
        return False, f"A calendar event already exists on {date_str}."

    success = db_create_calendar_event(date_str, event_type, description, created_by)
    if success:
        logger.info(f"Created calendar event on {date_str}: {event_type}")
        return True, "Calendar event created successfully."
    return False, "Failed to create calendar event."


def delete_calendar_event(event_id):
    """Delete a calendar event."""
    success = db_delete_calendar_event(event_id)
    if success:
        logger.info(f"Deleted calendar event ID {event_id}")
        return True, "Calendar event deleted successfully."
    return False, "Failed to delete calendar event."