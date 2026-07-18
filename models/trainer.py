import datetime
from database.db import get_connection

class Trainer:

    def __init__(
        self,
        trainer_id,
        full_name,
        email,
        phone,
        skills,
        qualifications,
        experience,
        date_of_joining=None,
        previous_experience=0.0,
        status='Active',
        created_at=None,
        updated_at=None,
        created_by=None,
        updated_by=None,
    ):
        self.trainer_id = trainer_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.qualifications = qualifications
        self.experience = experience
        self.date_of_joining = date_of_joining
        self.previous_experience = previous_experience
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by


def get_all_trainers():
    """
    Retrieve all trainers from the database.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                trainer_id,
                full_name,
                email,
                phone,
                skills,
                qualifications,
                experience,
                date_of_joining,
                previous_experience,
                status,
                created_at,
                updated_at,
                created_by,
                updated_by
            FROM trainer
            ORDER BY full_name ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def update_trainer(
    trainer_id,
    full_name,
    email,
    phone,
    skills,
    qualifications,
    experience,
    date_of_joining,
    previous_experience,
    status,
    updated_by=None
):
    """
    Update trainer information.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            UPDATE trainer
            SET
                full_name = ?,
                email = ?,
                phone = ?,
                skills = ?,
                qualifications = ?,
                experience = ?,
                date_of_joining = ?,
                previous_experience = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = ?
            WHERE trainer_id = ?
        """
        cursor.execute(
            query,
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
                updated_by,
                trainer_id
            )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_trainer(trainer_id):
    """
    Delete a trainer from the database.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            DELETE FROM trainer
            WHERE trainer_id = ?
        """
        cursor.execute(query, (trainer_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def search_trainers(keyword):
    """
    Search trainers by name, email, phone, skills, or qualifications.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                trainer_id,
                full_name,
                email,
                phone,
                skills,
                qualifications,
                experience,
                date_of_joining,
                previous_experience,
                status,
                created_at,
                updated_at,
                created_by,
                updated_by
            FROM trainer
            WHERE
                full_name LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
                OR skills LIKE ?
                OR qualifications LIKE ?
            ORDER BY full_name
        """
        search_value = f"%{keyword}%"
        cursor.execute(
            query,
            (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            )
        )
        return cursor.fetchall()
    finally:
        connection.close()


def filter_trainers(status=None, keyword=None):
    """
    Filter trainers by status and search keyword.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                trainer_id,
                full_name,
                email,
                phone,
                skills,
                qualifications,
                experience,
                date_of_joining,
                previous_experience,
                status,
                created_at,
                updated_at,
                created_by,
                updated_by
            FROM trainer
        """
        conditions = []
        params = []

        if status:
            conditions.append("status = ?")
            params.append(status)

        if keyword:
            conditions.append("(full_name LIKE ? OR email LIKE ? OR phone LIKE ? OR skills LIKE ? OR qualifications LIKE ?)")
            like = f"%{keyword}%"
            params.extend([like, like, like, like, like])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY full_name"
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        connection.close()


def get_trainer_availability(trainer_id):
    """
    Retrieve a trainer's basic info and status (kept for compatibility).
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                trainer_id,
                full_name,
                status
            FROM trainer
            WHERE trainer_id = ?
        """
        cursor.execute(query, (trainer_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def get_trainer_by_id(trainer_id):
    """
    Retrieve a single trainer by ID.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                trainer_id,
                full_name,
                email,
                phone,
                skills,
                qualifications,
                experience,
                date_of_joining,
                previous_experience,
                status,
                created_at,
                updated_at,
                created_by,
                updated_by
            FROM trainer
            WHERE trainer_id = ?
        """
        cursor.execute(query, (trainer_id,))
        return cursor.fetchone()
    finally:
        connection.close()


def update_trainer_availability(trainer_id, availability, updated_by=None):
    """
    Dummy/compatibility method: updates/inserts a leave/override record for today.
    """
    today_str = datetime.date.today().isoformat()
    status_val = 1 if availability == "Available" else 0
    availability_type = "Available" if status_val == 1 else "Unavailable"
    
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO trainer_availablity (trainer_id, date, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(trainer_id, date) DO UPDATE SET
                status = excluded.status,
                availability_type = excluded.availability_type,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = excluded.updated_by
        """
        cursor.execute(query, (trainer_id, today_str, status_val, availability_type, 'Full Day', None, None, None, "Global toggle override", updated_by, updated_by))
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        connection.close()


def get_trainer_statistics():
    """
    Retrieve trainer statistics: total and average experience.
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM trainer").fetchone()[0]
        
        # Calculate dynamic average experience
        trainers = cursor.execute("SELECT date_of_joining, previous_experience FROM trainer").fetchall()
        total_exp = 0.0
        count = len(trainers)
        today = datetime.date.today()
        
        for t in trainers:
            prev = t['previous_experience'] or 0.0
            doj_str = t['date_of_joining']
            this_org = 0.0
            if doj_str:
                try:
                    doj = datetime.date.fromisoformat(doj_str)
                    this_org = max(0.0, (today - doj).days / 365.25)
                except Exception:
                    pass
            total_exp += (prev + this_org)
            
        avg_exp = (total_exp / count) if count > 0 else 0.0
        
        return {
            "total_trainers": total or 0,
            "average_experience": round(avg_exp, 1)
        }
    finally:
        connection.close()


# --- Trainer Availability Helpers ---

def get_trainer_availabilities(trainer_id):
    """Retrieve all availability/override records for a trainer."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT availability_id, trainer_id, date, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_at, updated_at, created_by, updated_by
            FROM trainer_availablity
            WHERE trainer_id = ?
            ORDER BY date DESC
        """
        cursor.execute(query, (trainer_id,))
        return cursor.fetchall()
    finally:
        connection.close()


def get_trainer_availability_by_date(trainer_id, date_str):
    """Retrieve availability/override record for a trainer on a specific date."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT availability_id, trainer_id, date, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_at, updated_at, created_by, updated_by
            FROM trainer_availablity
            WHERE trainer_id = ? AND date = ?
        """
        cursor.execute(query, (trainer_id, date_str))
        return cursor.fetchone()
    finally:
        connection.close()


def create_trainer_availability(trainer_id, date_str, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by=None):
    """Create a new availability/override record for a trainer."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO trainer_availablity (trainer_id, date, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (trainer_id, date_str, status, availability_type, duration_type, time_slot, start_time, end_time, description, created_by, created_by))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def update_trainer_availability_record(availability_id, status, availability_type, duration_type, time_slot, start_time, end_time, description, updated_by=None):
    """Update an existing availability record."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            UPDATE trainer_availablity
            SET status = ?, availability_type = ?, duration_type = ?, time_slot = ?, start_time = ?, end_time = ?, description = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?
            WHERE availability_id = ?
        """
        cursor.execute(query, (status, availability_type, duration_type, time_slot, start_time, end_time, description, updated_by, availability_id))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_trainer_availability(availability_id):
    """Delete an availability record."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = "DELETE FROM trainer_availablity WHERE availability_id = ?"
        cursor.execute(query, (availability_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


# --- Global Calendar Event Helpers ---

def get_all_calendar_events():
    """Retrieve all calendar events (Holidays/Meetings)."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT event_id, date, event_type, description, created_at, updated_at, created_by, updated_by
            FROM calendar_event
            ORDER BY date DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def get_calendar_event_by_date(date_str):
    """Retrieve calendar event for a specific date."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT event_id, date, event_type, description, created_at, updated_at, created_by, updated_by
            FROM calendar_event
            WHERE date = ?
        """
        cursor.execute(query, (date_str,))
        return cursor.fetchone()
    finally:
        connection.close()


def create_calendar_event(date_str, event_type, description, created_by=None):
    """Create a new calendar event."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO calendar_event (date, event_type, description, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (date_str, event_type, description, created_by, created_by))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_calendar_event(event_id):
    """Delete a calendar event."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = "DELETE FROM calendar_event WHERE event_id = ?"
        cursor.execute(query, (event_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()
