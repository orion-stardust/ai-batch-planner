# Student Management Database Specification

# Module Name
Student Management & Registration

# Purpose 
The Student Management module stores and manages all student-related information and their registrations for courses and batches. It supports student profiles, course registrations, status tracking, and batch enrollment mapping.

# Database
- Engine: SQLite3
- Database File: batch_planner.db

# Table: student
Stores the base profiles of the students.

## Fields
1. `student_id`: INTEGER PRIMARY KEY AUTOINCREMENT
2. `full_name`: TEXT NOT NULL
3. `email`: TEXT NOT NULL UNIQUE
4. `phone`: TEXT NOT NULL UNIQUE
5. `qualification`: TEXT NOT NULL
6. `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
7. `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
8. `created_by`: TEXT
9. `updated_by`: TEXT

# Table: student_register
Junction table managing student course registrations and batch allocations.

## Fields
1. `register_id`: INTEGER PRIMARY KEY AUTOINCREMENT
2. `student_id`: INTEGER NOT NULL (References student.student_id, ON DELETE CASCADE)
3. `course_id`: INTEGER NOT NULL (References Course.id, ON DELETE CASCADE)
4. `batch_id`: INTEGER (References batch.batch_id, ON DELETE SET NULL)
5. `enrollment_date`: TEXT NOT NULL (YYYY-MM-DD format)
6. `status`: TEXT NOT NULL (Allowed values: 'registered', 'registed', 'assigned', 'discontinued', 'break', 'completed', 'hold')
7. `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
8. `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
9. `created_by`: TEXT DEFAULT 'Admin'
10. `updated_by`: TEXT DEFAULT 'Admin'

# Indexes
- `idx_student_email`: Optimizes search and lookup by email.
- Foreign Key indexes on `student_id`, `course_id`, and `batch_id` in `student_register`.

# Business Rules
- Email must be unique.
- Phone number must be unique.
- Full name and Qualification are mandatory.
- Student registrations are course-specific.
- When `batch_id` is assigned to a registration, status automatically transitions to `'assigned'`. If `batch_id` is set to `NULL`, status transitions to `'hold'` (subsequent courses) or `'registered'`.

# Relationships
- student (Parent) -> student_register (Child) (1-to-many relationship, cascade delete).
- Course (Parent) -> student_register (Child) (1-to-many relationship, cascade delete).
- batch (Parent) -> student_register (Child) (1-to-many relationship, set null on delete).
