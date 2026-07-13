class Trainer:

    def __init__(
        self,
        trainer_id,
        full_name,
        email,
        phone,
        skills,
        experience,
        status,
        availability,
        created_at=None,
        updated_at=None,
    ):
        self.trainer_id = trainer_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.skills = skills
        self.experience = experience
        self.status = status
        self.availability = availability
        self.created_at = created_at
        self.updated_at = updated_at


from database.db import get_connection


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
                experience,
                status,
                availability,
                created_at,
                updated_at
            FROM trainer
            ORDER BY full_name ASC
        """

        cursor.execute(query)

        trainers = cursor.fetchall()

        return trainers

    finally:
        connection.close()


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
                experience = ?,
                status = ?,
                availability = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE trainer_id = ?
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                phone,
                skills,
                experience,
                status,
                availability,
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
    Search trainers by name, email, phone, or skills.
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
                experience,
                status,
                availability,
                created_at,
                updated_at
            FROM trainer
            WHERE
                full_name LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
                OR skills LIKE ?
            ORDER BY full_name
        """

        search_value = f"%{keyword}%"

        cursor.execute(
            query,
            (
                search_value,
                search_value,
                search_value,
                search_value
            )
        )

        return cursor.fetchall()

    finally:
        connection.close()


def filter_trainers(availability=None, status=None):
    """
    Filter trainers by availability and/or status.
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
                experience,
                status,
                availability,
                created_at,
                updated_at
            FROM trainer
        """

        conditions = []
        params = []

        if availability:
            conditions.append("availability = ?")
            params.append(availability)

        if status:
            conditions.append("status = ?")
            params.append(status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY full_name"

        cursor.execute(query, params)

        return cursor.fetchall()

    finally:
        connection.close()


def get_trainer_availability(trainer_id):
    """
    Retrieve a trainer's availability and status.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                trainer_id,
                full_name,
                availability,
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
                experience,
                status,
                availability,
                created_at,
                updated_at
            FROM trainer
            WHERE trainer_id = ?
        """

        cursor.execute(query, (trainer_id,))

        return cursor.fetchone()

    finally:
        connection.close()


def update_trainer_availability(trainer_id, availability):
    """
    Update a trainer's availability in the database.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            UPDATE trainer
            SET availability = ?, updated_at = CURRENT_TIMESTAMP
            WHERE trainer_id = ?
        """

        cursor.execute(query, (availability, trainer_id))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()
