# Student & Registration UI/Frontend Specification

# 1. Objective
The UI layer provides the visual interface for managing student profiles and course registrations.

---

# 2. Required Pages

## Student Profile Management

### 1. `students.html` (Student Listing Dashboard)
- **Purpose**: Displays the table of student profiles.
- **Components**:
  - Search Input: Search students by name, email, or phone.
  - Data Table columns: Name, Email, Phone, Qualification, and Actions.
  - Actions:
    - **Add Student** button linking to `/students/create`.
    - **Edit** icon linking to `/students/<id>/edit`.
    - **Delete** icon submitting a POST to `/students/<id>/delete` with a JS confirmation dialog.

### 2. `student_form.html` (Create/Edit Profile Form)
- **Purpose**: Unified form for adding or updating a student profile.
- **Form Fields**:
  - Full Name: text input, required.
  - Email Address: email input, required.
  - Phone Number: text input, required (validated on frontend for 10 digits).
  - Qualification: text input, required.

---

## Course Registration Management

### 1. `registrations.html` (Registrations Dashboard)
- **Purpose**: Displays student registrations for courses and batches.
- **Components**:
  - Search Bar: Search registrations by student, course, batch, or status.
  - Data Table columns: Student Name, Course, Batch, Enrollment Date, Status, and Actions.
  - Actions:
    - **Register Student** button linking to `/students/register/create`.
    - **Edit** icon linking to `/students/register/<id>/edit`.
    - **Delete** icon submitting a POST to `/students/register/<id>/delete` with confirmation.

### 2. `register_form.html` (Register/Edit Registration Form)
- **Purpose**: Register a student to a course.
- **Form Fields**:
  - Select Student: dropdown list of all active students.
  - Select Course: dropdown list of all active courses.
  - Enrollment Date: date input, required.
  - Status: dropdown with values: Registered, Assigned, Discontinued, Break, Completed, Hold.
  - *Note*: The batch selection field has been removed to keep batch scheduling and student allocation centralized in the Batch module form.
