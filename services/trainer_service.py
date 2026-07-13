import logging
import os
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


def _validate_trainer(
    full_name,
    email,
    phone,
    skills,
    experience,
    status,
    availability
):
    if not full_name or not full_name.strip():
        return False, "Trainer name is required."

    if not email or not email.strip():
        return False, "Email is required."

    if not phone or not phone.strip():
        return False, "Phone number is required."

    # Validate phone format: must contain 7 to 15 digits
    cleaned_phone = "".join([c for c in phone if c.isdigit()])
    if len(cleaned_phone) < 7 or len(cleaned_phone) > 15:
        return False, "Phone number must be a valid number with 7 to 15 digits."

    if not skills or not skills.strip():
        return False, "Skills is required."

    try:
        exp_val = int(experience)
        if exp_val < 0:
            return False, "Experience cannot be negative."
    except (ValueError, TypeError):
        return False, "Experience must be a valid number."

    if status not in ("Active", "Inactive"):
        return False, "Status must be Active or Inactive."

    if availability not in ("Available", "Unavailable"):
        return False, "Availability must be Available or Unavailable."

    return True, ""


def create_trainer(
    full_name,
    email,
    phone,
    skills,
    experience,
    status,
    availability
):
    """
    Insert a new trainer into the database.
    """

    is_valid, msg = _validate_trainer(
        full_name,
        email,
        phone,
        skills,
        experience,
        status,
        availability
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
                experience,
                status,
                availability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                phone,
                skills,
                int(experience),
                status,
                availability
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


from models.trainer import get_all_trainers as fetch_trainers


def get_all_trainers():
    """
    Return all trainers.
    """

    return fetch_trainers()


from models.trainer import update_trainer as update_trainer_model


def update_trainer(
    trainer_id,
    full_name,
    email,
    phone,
    skills,
    experience,
    status,
    availability
):
    """
    Validate and update trainer.
    """

    is_valid, msg = _validate_trainer(
        full_name,
        email,
        phone,
        skills,
        experience,
        status,
        availability
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
        int(experience),
        status,
        availability
    )

    if updated:
        logger.info(f"Successfully updated trainer ID {trainer_id}: name='{full_name}'")
        return True, "Trainer updated successfully."

    logger.warning(f"Failed to update trainer ID {trainer_id}: Trainer not found.")
    return False, "Trainer not found."


from models.trainer import delete_trainer as delete_trainer_model


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


from models.trainer import search_trainers as search_trainers_model


def search_trainers(keyword):
    """
    Search trainers.
    """

    if not keyword.strip():
        return []

    return search_trainers_model(keyword)


from models.trainer import filter_trainers as filter_trainers_model


def filter_trainers(availability=None, status=None):
    """
    Filter trainers by availability and/or status.
    """

    return filter_trainers_model(availability, status)


from models.trainer import get_trainer_availability as get_availability_model


def get_trainer_availability(trainer_id):
    """
    Get trainer availability.
    """

    trainer = get_availability_model(trainer_id)

    if trainer:
        return trainer

    return None


from models.trainer import get_trainer_by_id as get_trainer_by_id_model


def get_trainer_by_id(trainer_id):
    """
    Get trainer by ID.
    """

    trainer = get_trainer_by_id_model(trainer_id)

    if trainer:
        return trainer

    return None


from models.trainer import update_trainer_availability as update_availability_model_db


def update_trainer_availability(trainer_id, availability):
    """
    Update a trainer's availability.
    """

    if availability not in ("Available", "Unavailable"):
        logger.warning(f"Failed to update availability for trainer ID {trainer_id}. Invalid availability: {availability}")
        return False, "Invalid availability status."

    updated = update_availability_model_db(trainer_id, availability)

    if updated:
        logger.info(f"Successfully updated availability for trainer ID {trainer_id} to '{availability}'")
        return True, "Availability updated successfully."

    logger.warning(f"Failed to update availability for trainer ID {trainer_id}: Trainer not found.")
    return False, "Trainer not found."