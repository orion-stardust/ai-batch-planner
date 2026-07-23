# Student & Registration Model Specification

# 1. Objective
The Student and StudentRegister Models act as the bridge between the application and the database.
Their responsibilities are limited to:
- Executing SQL queries
- Reading, writing, updating, and deleting records from the database
- Returning query results
- Managing database connections

---

# 2. Model Responsibilities

## StudentModel (Table: `student`)
Responsible for managing student profiles.

### CRUD Operations
- **Create**: Insert a new student (`full_name`, `email`, `phone`, `qualification`, `created_by`, `updated_by`).
- **Read**:
  - Retrieve all students (ordered by `student_id` descending)
  - Retrieve single student by ID
- **Update**: Modify `full_name`, `email`, `phone`, `qualification`, `updated_by`, `updated_at`.
- **Delete**: Remove a student record by `student_id`.
- **Search**: Search students using `full_name`, `email`, or `phone`.

---

## StudentRegisterModel (Table: `student_register`)
Responsible for managing course registrations and batch assignments.

### CRUD Operations
- **Create**: Register a student for a course (`student_id`, `course_id`, `batch_id`, `enrollment_date`, `status`, `created_by`, `updated_by`).
- **Read**:
  - Retrieve all registrations (enriched with student, course, and batch names)
  - Retrieve registration by ID
  - Retrieve registrations by student ID
- **Update**: Modify `student_id`, `course_id`, `batch_id`, `enrollment_date`, `status`, `updated_by`, `updated_at`.
- **Delete**: Remove a registration record by `register_id`.
- **Search**: Search registrations using student name, course name, batch name, or status.
