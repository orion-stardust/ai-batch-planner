from models.student import StudentModel
from models.batch import BatchModel
import re

class StudentService:
    def __init__(self):
        self.model = StudentModel()

    def _validate_student_data(self, full_name, email, phone, qualification, student_id=None):
        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty.")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty.")
        if not phone or not phone.strip():
            raise ValueError("Phone cannot be empty.")
        if not qualification or not qualification.strip():
            raise ValueError("Qualification cannot be empty.")
            
        # Validate Email Format
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")

        # Validate Phone Digits
        phone_digits = re.sub(r'\D', '', phone)
        if len(phone_digits) < 7 or len(phone_digits) > 15:
            raise ValueError("Phone must contain between 7 and 15 digits.")

        # Check for duplicates using the Model
        if self.model.student_exists(email=email.strip(), exclude_id=student_id):
            raise ValueError(f"A student with email '{email}' already exists.")
        if self.model.student_exists(phone=phone.strip(), exclude_id=student_id):
            raise ValueError(f"A student with phone '{phone}' already exists.")

    def create_student(self, full_name, email, phone, qualification, created_by="Admin"):
        self._validate_student_data(full_name, email, phone, qualification)
        
        new_id = self.model.create_student(
            full_name=full_name.strip(),
            email=email.strip(),
            phone=phone.strip(),
            qualification=qualification.strip(),
            created_by=created_by
        )
        
        return {"success": True, "message": "Student created successfully.", "student_id": new_id}

    def get_all_students(self):
        return self.model.get_all_students()

    def get_student_by_id(self, student_id):
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid student ID.")
            
        student = self.model.get_student_by_id(student_id)
        if not student:
            raise ValueError("Student not found.")
        return student

    def update_student(self, student_id, full_name, email, phone, qualification, updated_by="Admin"):
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid student ID.")

        # Verify student exists before attempting to update
        self.get_student_by_id(student_id)
        
        # Validate input
        self._validate_student_data(full_name, email, phone, qualification, student_id=student_id)

        success = self.model.update_student(
            student_id=student_id,
            full_name=full_name.strip(),
            email=email.strip(),
            phone=phone.strip(),
            qualification=qualification.strip(),
            updated_by=updated_by
        )
        if not success:
             raise ValueError("Failed to update student. Database error.")

        return {"success": True, "message": "Student updated successfully."}

    def delete_student(self, student_id):
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid student ID.")
            
        # Verify student exists before deletion
        self.get_student_by_id(student_id)
        
        success = self.model.delete_student(student_id)
        if not success:
            raise ValueError("Failed to delete student.")
            
        return {"success": True, "message": "Student deleted successfully."}

    def search_students(self, keyword):
        if not keyword or not keyword.strip():
            return self.get_all_students()
        return self.model.search_students(keyword.strip())

    def filter_students(self, status):
        valid_statuses = ["Active", "Inactive", "Alumni", "Dropped"]
        if status not in valid_statuses:
            raise ValueError("Invalid status filter.")
        return self.model.filter_students(status)

    def get_students_by_batch(self, batch_id):
        try:
            batch_id = int(batch_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid batch ID.")
        return self.model.get_students_by_batch(batch_id)
