# Student & Registration Service Specification

# 1. Objective
The Student and StudentRegister Services act as the business logic layer, sitting between the Routes and the Models.
Their responsibilities are to enforce business rules, validate data types, handle transitions, and structure responses before reaching the routing layer.

---

# 2. Service Responsibilities

## StudentService
Exposes student profile CRUD operations.

### Method Specifications
- **`create_student(full_name, email, phone, qualification)`**:
  - Enforces mandatory fields: `full_name`, `email`, `phone`, `qualification`.
  - Enforces unique email and phone constraints.
  - Enforces email regex formatting and phone number digit count (exactly 10 digits).
  - Calls `StudentModel.create_student()`.
- **`update_student(student_id, full_name, email, phone, qualification)`**:
  - Enforces validation parameters. Ensures email/phone uniqueness across other student records.
  - Calls `StudentModel.update_student()`.
- **`get_student_by_id(student_id)`**: Retrieves student record.
- **`get_all_students()`**: Retrieves list of all student records.
- **`delete_student(student_id)`**: Removes student profile.

---

## StudentRegisterService
Exposes student course registration and batch allocation operations.

### Method Specifications
- **`create_registration(student_id, course_id, enrollment_date, status, batch_id=None)`**:
  - Validates `student_id`, `course_id`, and `enrollment_date`.
  - Determines enrollment status transition:
    - First registration: Status auto-sets to `'assigned'` if a batch is allocated, else remains `'registered'`.
    - Subsequent registrations: Force status to `'hold'` until a batch is assigned, then transition to `'assigned'`.
  - Updates the batch's `enrolled_count` if `batch_id` is allocated.
  - Calls `StudentRegisterModel.create_registration()`.
- **`update_registration(register_id, student_id, course_id, enrollment_date, status, batch_id=None)`**:
  - Handles batch re-allocation status sync (e.g. increments new batch count and decrements old batch count).
  - Manages transitions back to `'hold'` if `batch_id` is removed.
  - Calls `StudentRegisterModel.update_registration()`.
- **`delete_registration(register_id)`**: Deletes the registration and decrements associated batch count.
- **`search_registrations(keyword)`**: Searches registrations.
