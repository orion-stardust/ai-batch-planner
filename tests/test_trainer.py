import os
import sqlite3
import unittest
import database.db

# Patch the database name to a test database before importing app and services
TEST_DB_NAME = "database/test_batch_planner.db"
database.db.DATABASE_NAME = TEST_DB_NAME

from app import app
from services.trainer_service import (
    create_trainer,
    update_trainer,
    delete_trainer,
    get_all_trainers,
    get_trainer_by_id,
    update_trainer_availability,
    search_trainers,
    filter_trainers
)


class TrainerServiceTestCase(unittest.TestCase):
    """
    Unit tests for the Trainer service layer.
    """

    def setUp(self):
        # Recreate test table from schema.sql
        conn = sqlite3.connect(TEST_DB_NAME)
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "database", "schema.sql"
        )
        with open(schema_path, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(TEST_DB_NAME):
            try:
                os.remove(TEST_DB_NAME)
            except OSError:
                pass

    def test_create_trainer_valid(self):
        success, msg = create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            skills="Python, Flask",
            experience=4,
            status="Active",
            availability="Available"
        )
        self.assertTrue(success)
        self.assertEqual(msg, "Trainer saved successfully.")

        # Verify insertion
        trainers = get_all_trainers()
        self.assertEqual(len(trainers), 1)
        self.assertEqual(trainers[0]["full_name"], "Alice Smith")

    def test_create_trainer_invalid_name(self):
        success, msg = create_trainer(
            full_name="  ",
            email="alice@example.com",
            phone="1234567890",
            skills="Python",
            experience=4,
            status="Active",
            availability="Available"
        )
        self.assertFalse(success)
        self.assertEqual(msg, "Trainer name is required.")

    def test_create_trainer_invalid_phone(self):
        success, msg = create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="12345",  # Too short (must be 7-15 digits)
            skills="Python",
            experience=4,
            status="Active",
            availability="Available"
        )
        self.assertFalse(success)
        self.assertIn("Phone number must be a valid number with 7 to 15 digits", msg)

    def test_create_trainer_negative_experience(self):
        success, msg = create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            skills="Python",
            experience=-1,
            status="Active",
            availability="Available"
        )
        self.assertFalse(success)
        self.assertEqual(msg, "Experience cannot be negative.")

    def test_create_trainer_duplicate_email(self):
        # Insert first trainer
        create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            skills="Python",
            experience=4,
            status="Active",
            availability="Available"
        )
        # Attempt second with duplicate email
        success, msg = create_trainer(
            full_name="Bob Jones",
            email="alice@example.com",
            phone="0987654321",
            skills="Java",
            experience=5,
            status="Active",
            availability="Available"
        )
        self.assertFalse(success)
        self.assertEqual(msg, "Email already exists.")

    def test_update_trainer(self):
        create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            skills="Python",
            experience=4,
            status="Active",
            availability="Available"
        )
        trainer_id = get_all_trainers()[0]["trainer_id"]

        success, msg = update_trainer(
            trainer_id=trainer_id,
            full_name="Alice Updated",
            email="alice.updated@example.com",
            phone="1234567890",
            skills="Python, Flask, Docker",
            experience=5,
            status="Inactive",
            availability="Unavailable"
        )
        self.assertTrue(success)

        updated = get_trainer_by_id(trainer_id)
        self.assertEqual(updated["full_name"], "Alice Updated")
        self.assertEqual(updated["status"], "Inactive")
        self.assertEqual(updated["availability"], "Unavailable")

    def test_delete_trainer(self):
        create_trainer(
            full_name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            skills="Python",
            experience=4,
            status="Active",
            availability="Available"
        )
        trainer_id = get_all_trainers()[0]["trainer_id"]

        success, msg = delete_trainer(trainer_id)
        self.assertTrue(success)
        self.assertEqual(len(get_all_trainers()), 0)


class TrainerRoutesTestCase(unittest.TestCase):
    """
    Integration tests for the Trainer web controller routes.
    """

    def setUp(self):
        conn = sqlite3.connect(TEST_DB_NAME)
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "database", "schema.sql"
        )
        with open(schema_path, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(TEST_DB_NAME):
            try:
                os.remove(TEST_DB_NAME)
            except OSError:
                pass

    def test_route_view_trainers_empty(self):
        response = self.client.get("/trainers")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Trainer Management", response.data)

    def test_route_create_and_view_details(self):
        # Create trainer via POST
        data = {
            "full_name": "Bob Tester",
            "email": "bob@tester.com",
            "phone": "9876543210",
            "skills": "QA, Testing",
            "experience": "3",
            "status": "Active",
            "availability": "Available"
        }
        response = self.client.post("/trainers", data=data)
        # Should redirect to add trainer page with flash message
        self.assertEqual(response.status_code, 302)

        # Retrieve trainers to get ID
        trainers = get_all_trainers()
        self.assertEqual(len(trainers), 1)
        bob_id = trainers[0]["trainer_id"]

        # View Details Page
        response = self.client.get(f"/trainers/{bob_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bob Tester", response.data)
        self.assertIn(b"bob@tester.com", response.data)
        self.assertIn(b"QA, Testing", response.data)

    def test_route_filter_and_search(self):
        create_trainer(
            full_name="Bob Tester",
            email="bob@tester.com",
            phone="9876543210",
            skills="QA, Testing",
            experience=3,
            status="Active",
            availability="Available"
        )

        # Test Search Route
        response = self.client.get("/trainers/search?keyword=QA")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bob Tester", response.data)

        # Test Filter Route
        response = self.client.get("/trainers/filter?availability=Available&status=Active")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bob Tester", response.data)


if __name__ == "__main__":
    unittest.main()
