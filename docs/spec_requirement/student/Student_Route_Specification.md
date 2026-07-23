# Student & Registration Route Specification

# 1. Objective
The Student Route module acts as the Controller layer, handling incoming HTTP requests, interacting with the services, setting flash messages, and rendering templates or redirecting.

---

# 2. Route Endpoints

## Student Profile Routes (Prefix: `/students`)

### GET `/students/`
- **Purpose**: Displays student listing and supports search.
- **Action**: Calls `student_service.search_students(keyword)` or `student_service.get_all_students()`.
- **Response**: Renders `students.html`.

### GET `/students/create`
- **Purpose**: Displays empty form to create a student.
- **Response**: Renders `student_form.html`.

### POST `/students/create`
- **Purpose**: Submits new student details.
- **Form Data**: `full_name`, `email`, `phone`, `qualification`.
- **Response**: Redirects to student listing on success, else re-renders form with errors.

### GET `/students/<int:student_id>/edit`
- **Purpose**: Displays pre-populated form to edit student profile.
- **Response**: Renders `student_form.html` with student context.

### POST `/students/<int:student_id>/edit`
- **Purpose**: Submits student profile edits.
- **Form Data**: `full_name`, `email`, `phone`, `qualification`.
- **Response**: Redirects to student listing on success, else re-renders form with errors.

### POST `/students/<int:student_id>/delete`
- **Purpose**: Deletes student profile.
- **Response**: Redirects to student listing.

---

## Course Registration Routes (Prefix: `/students/register`)

### GET `/students/register`
- **Purpose**: Displays list of student registrations and supports keyword search.
- **Response**: Renders `registrations.html`.

### GET `/students/register/create`
- **Purpose**: Displays form to register a student to a course.
- **Response**: Renders `register_form.html`.

### POST `/students/register/create`
- **Purpose**: Submits registration.
- **Form Data**: `student_id`, `course_id`, `enrollment_date`, `status`. (Note: `batch_id` input is omitted).
- **Response**: Redirects to registrations list.

### GET `/students/register/<int:register_id>/edit`
- **Purpose**: Displays form to edit an existing registration.
- **Response**: Renders `register_form.html` with registration context.

### POST `/students/register/<int:register_id>/edit`
- **Purpose**: Submits registration edits.
- **Form Data**: `student_id`, `course_id`, `enrollment_date`, `status`.
- **Response**: Redirects to registrations list.

### POST `/students/register/<int:register_id>/delete`
- **Purpose**: Deletes registration.
- **Response**: Redirects to registrations list.
