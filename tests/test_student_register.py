import unittest
import sqlite3
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import initialize_database
from models.student import StudentModel
from models.course import CourseModel
from models.batch import BatchModel
from services.student_register_service import StudentRegisterService

class TestStudentRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()
        cls.student_model = StudentModel()
        cls.course_model = CourseModel()
        cls.batch_model = BatchModel()
        cls.register_service = StudentRegisterService()

    def setUp(self):
        # Clear tables
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "batch_planner.db"))
        conn.execute("DELETE FROM student_register")
        conn.execute("DELETE FROM student")
        conn.execute("DELETE FROM batch")
        conn.execute("DELETE FROM Course")
        conn.commit()
        conn.close()

        # Create dummy student
        self.student_id = self.student_model.create_student(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="1234567890",
            qualification="B.Tech",
            created_by="Tester"
        )

        # Create dummy courses
        self.course1_id = self.course_model.create_course(
            course_name="Course One",
            technology_stack="Python",
            duration_hours=40,
            description="Test Description 1",
            status="Active",
            created_by="Tester"
        )
        self.course2_id = self.course_model.create_course(
            course_name="Course Two",
            technology_stack="Java",
            duration_hours=40,
            description="Test Description 2",
            status="Active",
            created_by="Tester"
        )

        # Create dummy batch
        self.batch1_id = self.batch_model.create_batch(
            batch_code="BTH-001",
            batch_name="Batch One",
            course_id=self.course1_id,
            trainer_id=None,
            start_date="2026-08-01",
            end_date="2026-08-30",
            slot_type="Weekday Morning (9:30 AM - 11:30 AM)",
            mode="Offline",
            max_capacity=20,
            status="Upcoming"
        )

    def test_first_registration_without_batch(self):
        """First registration without batch should default to 'registered'."""
        res = self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course1_id,
            enrollment_date="2026-07-23",
            status="registered"
        )
        self.assertTrue(res["success"])
        
        reg = self.register_service.get_registration_by_id(res["register_id"])
        self.assertEqual(reg["status"], "registered")
        self.assertIsNone(reg["batch_id"])

    def test_first_registration_with_batch(self):
        """First registration with batch should auto-transition to 'assigned'."""
        res = self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course1_id,
            enrollment_date="2026-07-23",
            status="registered",
            batch_id=self.batch1_id
        )
        self.assertTrue(res["success"])
        
        reg = self.register_service.get_registration_by_id(res["register_id"])
        self.assertEqual(reg["status"], "assigned")
        self.assertEqual(reg["batch_id"], self.batch1_id)
        
        # Batch enrolled_count should be 1
        batch = self.batch_model.get_batch_by_id(self.batch1_id)
        self.assertEqual(batch["enrolled_count"], 1)

    def test_second_registration_without_batch_holds(self):
        """Subsequent course registration without a batch must automatically go on 'hold'."""
        # Create first registration (active)
        self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course1_id,
            enrollment_date="2026-07-23",
            status="registered"
        )

        # Create second registration without batch
        res2 = self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course2_id,
            enrollment_date="2026-07-23",
            status="registered"  # requested status
        )
        self.assertTrue(res2["success"])
        
        reg2 = self.register_service.get_registration_by_id(res2["register_id"])
        self.assertEqual(reg2["status"], "hold") # forced hold

    def test_second_registration_transitions(self):
        """Subsequent registration should transition from hold to assigned when batch is allocated."""
        # First registration
        self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course1_id,
            enrollment_date="2026-07-23",
            status="registered"
        )

        # Second registration - starts on hold
        res2 = self.register_service.create_registration(
            student_id=self.student_id,
            course_id=self.course2_id,
            enrollment_date="2026-07-23",
            status="registered"
        )
        register_id = res2["register_id"]
        
        # Update registration - assign batch -> should transition to assigned
        self.register_service.update_registration(
            register_id=register_id,
            student_id=self.student_id,
            course_id=self.course2_id,
            enrollment_date="2026-07-23",
            status="hold",
            batch_id=self.batch1_id
        )
        
        reg2 = self.register_service.get_registration_by_id(register_id)
        self.assertEqual(reg2["status"], "assigned")
        self.assertEqual(reg2["batch_id"], self.batch1_id)
        
        # Batch enrolled_count should be 1
        batch = self.batch_model.get_batch_by_id(self.batch1_id)
        self.assertEqual(batch["enrolled_count"], 1)

        # Remove batch -> should transition back to hold
        self.register_service.update_registration(
            register_id=register_id,
            student_id=self.student_id,
            course_id=self.course2_id,
            enrollment_date="2026-07-23",
            status="assigned",
            batch_id=None
        )
        reg2_updated = self.register_service.get_registration_by_id(register_id)
        self.assertEqual(reg2_updated["status"], "hold")
        
        # Batch enrolled_count should be 0
        batch = self.batch_model.get_batch_by_id(self.batch1_id)
        self.assertEqual(batch["enrolled_count"], 0)

if __name__ == "__main__":
    unittest.main()
