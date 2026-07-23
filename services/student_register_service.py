from models.student_register import StudentRegisterModel
from models.batch import BatchModel
import re

class StudentRegisterService:
    def __init__(self):
        self.model = StudentRegisterModel()
        self.batch_model = BatchModel()

    def _validate_registration(self, student_id, course_id, enrollment_date, status, batch_id=None):
        if not student_id:
            raise ValueError("Student is required.")
        if not course_id:
            raise ValueError("Course is required.")
        if not enrollment_date or not enrollment_date.strip():
            raise ValueError("Enrollment date is required.")
            
        valid_statuses = ['registered', 'registed', 'assigned', 'discontinued', 'break', 'completed', 'hold']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    def create_registration(self, student_id, course_id, enrollment_date, status, batch_id=None, created_by="Admin"):
        # Convert IDs to integers
        student_id = int(student_id)
        course_id = int(course_id)
        batch_id = int(batch_id) if batch_id else None

        # Check if student already has other registrations
        existing_regs = self.model.get_registrations_by_student(student_id)
        if len(existing_regs) > 0:
            # Subsequent course registration: must be hold until batch is assigned
            if status in ['registered', 'registed', 'hold', 'assigned']:
                status = 'assigned' if batch_id else 'hold'
        else:
            # First registration: auto-set status if batch is allocated
            if batch_id and status in ['registered', 'registed']:
                status = 'assigned'

        self._validate_registration(student_id, course_id, enrollment_date, status, batch_id)

        new_id = self.model.create_registration(
            student_id=student_id,
            course_id=course_id,
            batch_id=batch_id,
            enrollment_date=enrollment_date,
            status=status,
            created_by=created_by
        )

        if batch_id:
            self.batch_model.increment_enrolled_count(batch_id)

        return {"success": True, "message": "Registration created successfully.", "register_id": new_id}

    def get_all_registrations(self):
        return self.model.get_all_registrations()

    def get_registration_by_id(self, register_id):
        try:
            register_id = int(register_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid registration ID.")
        return self.model.get_registration_by_id(register_id)

    def update_registration(self, register_id, student_id, course_id, enrollment_date, status, batch_id=None, updated_by="Admin"):
        try:
            register_id = int(register_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid registration ID.")

        student_id = int(student_id)
        course_id = int(course_id)
        batch_id = int(batch_id) if batch_id else None

        # Check if student already has other registrations
        existing_regs = self.model.get_registrations_by_student(student_id)
        other_regs = [r for r in existing_regs if r['register_id'] != register_id]

        if len(other_regs) > 0:
            # Subsequent course registration: must be hold until batch is assigned
            if status in ['registered', 'registed', 'hold', 'assigned']:
                status = 'assigned' if batch_id else 'hold'
        else:
            # First registration: auto-set status if batch is allocated
            if batch_id and status in ['registered', 'registed']:
                status = 'assigned'

        self._validate_registration(student_id, course_id, enrollment_date, status, batch_id)

        existing = self.get_registration_by_id(register_id)
        if not existing:
            raise ValueError("Registration record not found.")

        old_batch_id = existing.get('batch_id')

        success = self.model.update_registration(
            register_id=register_id,
            student_id=student_id,
            course_id=course_id,
            batch_id=batch_id,
            enrollment_date=enrollment_date,
            status=status,
            updated_by=updated_by
        )

        if not success:
            raise ValueError("Failed to update registration database record.")

        # Sync batch enrolled counts if batch allocation changed
        if old_batch_id != batch_id:
            if old_batch_id:
                self.batch_model.decrement_enrolled_count(old_batch_id)
            if batch_id:
                self.batch_model.increment_enrolled_count(batch_id)

        return {"success": True, "message": "Registration updated successfully."}

    def delete_registration(self, register_id):
        try:
            register_id = int(register_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid registration ID.")

        existing = self.get_registration_by_id(register_id)
        if not existing:
            raise ValueError("Registration record not found.")

        old_batch_id = existing.get('batch_id')

        success = self.model.delete_registration(register_id)
        if not success:
            raise ValueError("Failed to delete registration record.")

        if old_batch_id:
            self.batch_model.decrement_enrolled_count(old_batch_id)

        return {"success": True, "message": "Registration deleted successfully."}

    def search_registrations(self, keyword):
        if not keyword or not keyword.strip():
            return self.get_all_registrations()
        return self.model.search_registrations(keyword.strip())
