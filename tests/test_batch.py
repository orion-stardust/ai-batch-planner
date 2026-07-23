import unittest
import datetime
import sqlite3
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database.db import initialize_database
from models.batch import BatchModel
from models.course import CourseModel
from models.trainer import create_calendar_event
from services.trainer_service import create_trainer, get_all_trainers
from services.batch_service import BatchService


class TestBatchManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()
        cls.batch_model = BatchModel()
        cls.course_model = CourseModel()
        cls.batch_service = BatchService()
        cls.app = app
        cls.client = cls.app.test_client()

    def setUp(self):
        # Clear database tables before each test
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "batch_planner.db"))
        conn.execute("DELETE FROM batch")
        conn.execute("DELETE FROM trainer_availablity")
        conn.execute("DELETE FROM calendar_event")
        conn.execute("DELETE FROM trainer")
        conn.execute("DELETE FROM student")
        conn.commit()
        conn.close()

    def test_01_model_crud_and_uniqueness(self):
        """Test Model CRUD operations and batch_code uniqueness."""
        # Create dummy course
        course_id = self._get_or_create_active_course("Test Python Course", "Python")

        batch_id = self.batch_model.create_batch(
            batch_code="BTH-TEST-001",
            batch_name="Python Morning Batch 1",
            course_id=course_id,
            trainer_id=None,
            start_date="2026-08-01",
            end_date="2026-08-30",
            slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
            mode="Offline",
            max_capacity=25,
            status="Upcoming"
        )
        self.assertIsNotNone(batch_id)
        self.assertTrue(self.batch_model.batch_code_exists("BTH-TEST-001"))

        # Verify retrieval
        batch = self.batch_model.get_batch_by_id(batch_id)
        self.assertEqual(batch['batch_name'], "Python Morning Batch 1")
        self.assertEqual(batch['max_capacity'], 25)

        # Update batch
        updated = self.batch_model.update_batch(
            batch_id=batch_id,
            batch_name="Python Morning Batch 1 Updated",
            course_id=course_id,
            trainer_id=None,
            start_date="2026-08-01",
            end_date="2026-08-31",
            slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
            start_time="09:30",
            end_time="11:30",
            mode="Online",
            location="Zoom",
            max_capacity=30,
            status="Upcoming",
            description="Updated description",
            updated_by="Tester"
        )
        self.assertTrue(updated)

        fetched = self.batch_model.get_batch_by_id(batch_id)
        self.assertEqual(fetched['batch_name'], "Python Morning Batch 1 Updated")
        self.assertEqual(fetched['mode'], "Online")

        # Delete batch
        deleted = self.batch_model.delete_batch(batch_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.batch_model.get_batch_by_id(batch_id))

    def test_02_service_end_date_and_holiday_calculation(self):
        """Test calculation of end_date and project_date with weekend and holiday skips."""
        course_id = self._get_or_create_active_course("Fast Java Course", "Java", duration_hours=20)

        # Create a public holiday on 2026-08-05
        create_calendar_event("2026-08-05", "Public Holiday", "Test Holiday", created_by="Tester")

        # 20 hours duration with Weekday slot (2 hrs/day) = 10 sessions.
        # Start date: 2026-08-03 (Monday)
        # Sessions:
        # Mon Aug 3 (1)
        # Tue Aug 4 (2)
        # Wed Aug 5 (HOLIDAY - SKIP)
        # Thu Aug 6 (3)
        # Fri Aug 7 (4)
        # Sat Aug 8 / Sun Aug 9 (WEEKEND - SKIP)
        # Mon Aug 10 (5)
        # Tue Aug 11 (6)
        # Wed Aug 12 (7)
        # Thu Aug 13 (8)
        # Fri Aug 14 (9)
        # Sat Aug 15 / Sun Aug 16 (WEEKEND - SKIP)
        # Mon Aug 17 (10) -> End Date: 2026-08-17
        res = self.batch_service.calculate_end_date(course_id, "2026-08-03", "Weekday Morning (9:30 AM - 11:30 AM)")
        self.assertEqual(res["end_date"], "2026-08-17")

        # Project Date: 5 working days after 2026-08-17
        # Tue Aug 18 (1), Wed Aug 19 (2), Thu Aug 20 (3), Fri Aug 21 (4), Mon Aug 24 (5) -> Project Date: 2026-08-24
        self.assertEqual(res["project_date"], "2026-08-24")

    def test_03_trainer_conflict_and_skill_validation(self):
        """Test trainer scheduling conflict and skill alignment validation."""
        course_id = self._get_or_create_active_course("Python Web Development", "Python", duration_hours=40)
        trainer_id = self._create_test_trainer("Python Expert", "pyexpert@example.com", "9998887771", "Python, Django, Flask")

        # Create first batch
        res1 = self.batch_service.create_batch(
            batch_code="BTH-PY-001",
            batch_name="Python Batch 1",
            course_id=course_id,
            trainer_id=trainer_id,
            start_date="2026-09-01",
            end_date="2026-09-30",
            slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
            mode="Offline",
            max_capacity=20,
            status="Upcoming"
        )
        self.assertTrue(res1["success"])

        # Attempt to create second overlapping batch with same trainer in same slot
        with self.assertRaises(ValueError) as ctx:
            self.batch_service.create_batch(
                batch_code="BTH-PY-002",
                batch_name="Python Batch 2",
                course_id=course_id,
                trainer_id=trainer_id,
                start_date="2026-09-15",
                end_date="2026-10-15",
                slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
                mode="Offline",
                max_capacity=20,
                status="Upcoming"
            )
        self.assertIn("Trainer scheduling conflict", str(ctx.exception))

        # Skill mismatch check
        c_java_id = self._get_or_create_active_course("Java Core", "Java", duration_hours=30)
        with self.assertRaises(ValueError) as ctx2:
            self.batch_service.create_batch(
                batch_code="BTH-JV-001",
                batch_name="Java Batch",
                course_id=c_java_id,
                trainer_id=trainer_id,  # Python trainer
                start_date="2026-11-01",
                end_date="2026-11-30",
                slot_type="Weekday Afternoon (2:45 PM - 4:45 PM)",
                mode="Offline",
                max_capacity=20,
                status="Upcoming"
            )
        self.assertIn("Trainer skills", str(ctx2.exception))

    def test_04_status_transition_and_capacity_rules(self):
        """Test In Progress state transition rules and capacity enforcement."""
        course_id = self._get_or_create_active_course("Data Science Basics", "Python", duration_hours=40)

        # Batch without trainer cannot transition to In Progress
        res = self.batch_service.create_batch(
            batch_code="BTH-DS-001",
            batch_name="Data Science Unassigned",
            course_id=course_id,
            trainer_id=None,
            start_date="2026-11-01",
            end_date="2026-11-30",
            slot_type="Weekday Evening (5:00 PM - 7:00 PM)",
            mode="Online",
            max_capacity=10,
            status="Upcoming"
        )
        batch_id = res["batch_id"]

        with self.assertRaises(ValueError) as ctx:
            self.batch_service.update_status(batch_id, "In Progress")
        self.assertIn("Trainer assignment is mandatory", str(ctx.exception))

        # Enrolled count restriction on deletion
        self.batch_model.increment_enrolled_count(batch_id)
        with self.assertRaises(ValueError) as ctx2:
            self.batch_service.delete_batch(batch_id)
        self.assertIn("Cannot delete a batch with enrolled students", str(ctx2.exception))

    def test_05_route_integration(self):
        """Test Flask HTTP route endpoints."""
        course_id = self._get_or_create_active_course("Web App Security", "Security", duration_hours=30)

        # GET /batches
        response = self.client.get("/batches")
        self.assertEqual(response.status_code, 200)

        # POST /batches/create
        response = self.client.post("/batches/create", data={
            "batch_code": "BTH-SEC-101",
            "batch_name": "Security Batch",
            "course_id": str(course_id),
            "start_date": "2026-10-01",
            "end_date": "2026-10-30",
            "slot_type": "Weekday Morning (9:30 AM - 11:30 AM)",
            "mode": "Offline",
            "max_capacity": "25",
            "status": "Upcoming"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # GET /api/calculate-end-date
        response = self.client.get(f"/api/calculate-end-date?course_id={course_id}&start_date=2026-10-01&slot_type=Weekday%20Morning%20(9:30%20AM%20-%2011:30%20AM)")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("end_date", data)
        self.assertIn("project_date", data)

    # --- Helpers ---
    def _get_or_create_active_course(self, name, tech, duration_hours=40):
        courses = self.course_model.get_all_courses()
        for c in courses:
            if c['course_name'] == name:
                return c['id']
        return self.course_model.create_course(
            course_name=name,
            technology_stack=tech,
            duration_hours=duration_hours,
            description="Test course description",
            status="Active",
            created_by="Tester"
        )

    def _create_test_trainer(self, full_name, email, phone, skills):
        success, msg = create_trainer(
            full_name=full_name,
            email=email,
            phone=phone,
            skills=skills,
            previous_experience=5.0,
            date_of_joining="2026-01-01",
            status="Active",
            created_by="Tester"
        )
        if not success:
            raise RuntimeError(f"Failed to create test trainer: {msg}")
        trainers = get_all_trainers()
        for t in trainers:
            if t['email'] == email:
                return t['trainer_id']
        return None

    def _create_test_student(self, name, email, phone, course_id, batch_id=None):
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "batch_planner.db"))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO student (full_name, email, phone, qualification, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, "B.Tech", "Tester", "Tester"))
        student_id = cursor.lastrowid
        
        status = "assigned" if batch_id else "registered"
        cursor.execute('''
            INSERT INTO student_register (student_id, course_id, batch_id, enrollment_date, status, created_by, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, course_id, batch_id, "2026-07-23", status, "Tester", "Tester"))
        conn.commit()
        conn.close()
        return student_id

    def test_06_student_enrollment_and_filtering(self):
        """Test student enrollment rules, capacity checks, and API filtering routes."""
        course_python = self._get_or_create_active_course("Test Python Course", "Python")
        course_java = self._get_or_create_active_course("Test Java Course", "Java")

        # Create active trainers with aligned skills
        trainer_py = self._create_test_trainer("Trainer Python", "py_trainer@test.com", "9998887770", "Python")
        trainer_jv = self._create_test_trainer("Trainer Java", "jv_trainer@test.com", "9998887771", "Java")

        # Create students for both courses
        s1 = self._create_test_student("Student Py 1", "py1@test.com", "1112223330", course_python)
        s2 = self._create_test_student("Student Py 2", "py2@test.com", "1112223331", course_python)
        s_java = self._create_test_student("Student Java", "jv@test.com", "1112223332", course_java)

        # 1. Test batch creation with multiple valid students
        res = self.batch_service.create_batch(
            batch_code="BTH-PY-AUTO",
            batch_name="Python Automation Batch",
            course_id=course_python,
            trainer_id=trainer_py,
            start_date="2026-09-01",
            end_date="2026-09-30",
            slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
            mode="Offline",
            max_capacity=5,
            student_ids=[s1, s2]
        )
        self.assertTrue(res["success"])
        batch_id = res["batch_id"]

        # Verify enrolled_count is set to 2
        batch = self.batch_model.get_batch_by_id(batch_id)
        self.assertEqual(batch["enrolled_count"], 2)

        # Verify student records updated with batch_id in student_register
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "batch_planner.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT batch_id FROM student_register WHERE student_id = ? AND course_id = ?", (s1, course_python))
        reg1_batch_id = cursor.fetchone()[0]
        cursor.execute("SELECT batch_id FROM student_register WHERE student_id = ? AND course_id = ?", (s2, course_python))
        reg2_batch_id = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(reg1_batch_id, batch_id)
        self.assertEqual(reg2_batch_id, batch_id)

        # 2. Test course restriction validation: enrolling java student in python batch should fail
        with self.assertRaises(ValueError) as ctx:
            self.batch_service.create_batch(
                batch_code="BTH-PY-ERR",
                batch_name="Error Python Batch",
                course_id=course_python,
                trainer_id=trainer_py,
                start_date="2026-09-01",
                end_date="2026-09-30",
                slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
                mode="Offline",
                max_capacity=5,
                student_ids=[s_java]
            )
        self.assertIn("is not enrolled in the selected course", str(ctx.exception))

        # 3. Test capacity validation: enrolling 2 students with max_capacity = 1 should fail
        with self.assertRaises(ValueError) as ctx2:
            self.batch_service.create_batch(
                batch_code="BTH-PY-CAP",
                batch_name="Cap Python Batch",
                course_id=course_python,
                trainer_id=trainer_py,
                start_date="2026-09-01",
                end_date="2026-09-30",
                slot_type="Weekday Midday (11:45 AM - 1:45 PM)",
                mode="Offline",
                max_capacity=1,
                student_ids=[s1, s2]
            )
        self.assertIn("exceeds the batch's max capacity", str(ctx2.exception))

        # 4. Test AJAX api endpoints
        # Fetch trainers for Python course
        response = self.client.get(f"/api/courses/{course_python}/trainers")
        self.assertEqual(response.status_code, 200)
        data_trainers = response.get_json()
        self.assertTrue(data_trainers["success"])
        # Python trainer should be present, Java trainer should NOT be present
        trainer_ids = [t["trainer_id"] for t in data_trainers["trainers"]]
        self.assertIn(trainer_py, trainer_ids)
        self.assertNotIn(trainer_jv, trainer_ids)

        # Fetch students for Python course
        response = self.client.get(f"/api/courses/{course_python}/students")
        self.assertEqual(response.status_code, 200)
        data_students = response.get_json()
        self.assertTrue(data_students["success"])
        # Python students should be present, Java student should NOT
        student_ids = [s["student_id"] for s in data_students["students"]]
        self.assertIn(s1, student_ids)
        self.assertIn(s2, student_ids)
        self.assertNotIn(s_java, student_ids)

        # 5. Test schedule conflict validations on APIs and Backend
        # Test trainer conflict API
        response = self.client.get(f"/api/courses/{course_python}/trainers?slot_type=Weekday%20Morning%20(9:30%20AM%20-%2011:30%20AM)&start_date=2026-09-10&end_date=2026-09-20")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        trainer_item = next(t for t in data["trainers"] if t["trainer_id"] == trainer_py)
        self.assertTrue(trainer_item["has_conflict"])
        self.assertEqual(trainer_item["conflict_batch_name"], "Python Automation Batch")

        # Test student conflict API
        response = self.client.get(f"/api/courses/{course_python}/students?slot_type=Weekday%20Morning%20(9:30%20AM%20-%2011:30%20AM)&start_date=2026-09-10&end_date=2026-09-20")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        student_item = next(s for s in data["students"] if s["student_id"] == s1)
        self.assertTrue(student_item["has_conflict"])
        self.assertEqual(student_item["conflict_batch_name"], "Python Automation Batch")
        self.assertEqual(student_item["conflict_slot"], "Weekday Morning (9:30 AM - 11:30 AM)")

        # Test backend conflict validation: enrolling student with conflict should fail
        with self.assertRaises(ValueError) as ctx3:
            self.batch_service.create_batch(
                batch_code="BTH-PY-CONF",
                batch_name="Conf Batch",
                course_id=course_python,
                trainer_id=trainer_py, 
                start_date="2026-09-10",
                end_date="2026-09-20",
                slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
                mode="Offline",
                max_capacity=5,
                student_ids=[s1] 
            )
        self.assertIn("is already enrolled in 'Python Automation Batch' during that time", str(ctx3.exception))


if __name__ == "__main__":
    unittest.main()
