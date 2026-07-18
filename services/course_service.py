from models.course import CourseModel


class CourseService:

    def __init__(self):
        self.course_model = CourseModel()
    
    # 1. Create Course
    def create_course(
        self,
        course_name,
        technology_stack,
        duration_hours,
        description,
        status,
        created_by
    ):

        if not course_name.strip():
            raise ValueError("Course Name is required.")

        if not technology_stack.strip():
            raise ValueError("Technology Stack is required.")

        try:
            duration_hours = int(duration_hours)
        except (ValueError, TypeError):
            raise ValueError("Duration must be a valid number.")

        if duration_hours <= 0:
            raise ValueError("Duration must be greater than zero.")

        if status not in ("Active", "Inactive"):
            raise ValueError("Invalid status.")

        if self.course_model.course_exists(course_name):
            raise ValueError("Course already exists.")

        new_id = self.course_model.create_course(
            course_name,
            technology_stack,
            duration_hours,
            description,
            status,
            created_by
        )

        return {
            "success": True,
            "message": "Course created successfully.",
            "course_id": new_id
        }

    # 2. Get All Courses   
    def get_all_courses(self):
        """Get all courses with basic validation."""
        return self.course_model.get_all_courses()

    # 3. Get Course By ID
    def get_course_by_id(self, course_id):
        """Get a course by its ID with validation."""
        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Course ID format.")

        if course_id <= 0:
            raise ValueError("Invalid Course ID.")

        course = self.course_model.get_course_by_id(course_id)
        
        if not course:
            raise ValueError(f"Course with ID {course_id} not found.")
        
        return course

    # 4. Update Course
    def update_course(
        self, 
        course_id,
        course_name,
        technology_stack,
        duration_hours,
        description,
        status,
        updated_by
    ):
        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Course ID format.")

        if course_id <= 0:
            raise ValueError("Invalid Course ID.")

        if not course_name.strip():
            raise ValueError("Course name is required.")

        if not technology_stack.strip():
            raise ValueError("Technology stack is required.")

        try:
            duration_hours = int(duration_hours)
        except (ValueError, TypeError):
            raise ValueError("Duration must be a valid number.")

        if duration_hours <= 0:
            raise ValueError("Duration must be positive.")

        if status not in ("Active", "Inactive"):
            raise ValueError("Invalid status.")

        # Check duplicate course name (excluding current course)
        if self.course_model.course_exists(course_name, exclude_id=course_id):
            raise ValueError("Course name already exists.")

        success = self.course_model.update_course(
           course_id,
           course_name,
           technology_stack,
           duration_hours,
           description,
           status,
           updated_by
        )
        
        if not success:
            raise ValueError(f"Course with ID {course_id} not found or could not be updated.")

        return {
           "success": True,
           "message": "Course updated successfully."
        }
    
    # 5. Delete Course
    def delete_course(self, course_id):
        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Course ID format.")

        course = self.course_model.get_course_by_id(course_id)

        if course is None:
            raise ValueError("Course not found.")

        success = self.course_model.delete_course(course_id)
        
        if not success:
            raise ValueError("Failed to delete the course.")

        return {
           "success": True,
           "message": "Course deleted successfully."
        } 

    # 6. Update Status
    def update_status(
        self,
        course_id,
        status,
        updated_by
    ):
        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid Course ID format.")

        if status not in ("Active", "Inactive"):
            raise ValueError("Invalid status.")

        success = self.course_model.update_status(
           course_id,
           status,
           updated_by
        )
        
        if not success:
            raise ValueError(f"Course with ID {course_id} not found or could not be updated.")

        return {
            "success": True,
            "message": "Course status updated successfully."
        }

    # 7. Search Courses
    def search_courses(self, keyword):
        if not keyword or not keyword.strip():
            return self.get_all_courses()
        return self.course_model.search_courses(keyword.strip())

    # 8. Filter Courses
    def filter_courses(self, status=None, technology=None, min_duration=None, max_duration=None, keyword=None):
        return self.course_model.filter_courses(status, technology, min_duration, max_duration, keyword)

    # 9. Get Statistics
    def get_statistics(self):
        return self.course_model.get_statistics()
    
    # 10. Additional Helpers
    def get_active_courses(self):
        return self.course_model.get_active_courses()

    def get_inactive_courses(self):
        return self.course_model.get_inactive_courses()