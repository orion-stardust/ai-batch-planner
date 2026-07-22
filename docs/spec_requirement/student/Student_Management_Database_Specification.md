# Student Management Database Specification:

#Module Name
Student Management

#Purpose 
The Student Management module stores and manages all student-related information within the AI Batch Planner system. It supports student registration, modification, status tracking, lookup, listing, and future batch enrollment mapping.

#Database
-Engine: SQLite3
-Database File: batch_planner.db

#Table: student

#Fields
1.student_id
-Integer
-Primary Key
-Auto Increment
-Unique student identifier.

2.full_name
-Text
-Required
-Full name of the student.

3.email
-Text
-Required
-Unique
-Contact email address. Used for notifications and unique identification.

4.phone
-Text
-Required
-Unique
-Contact phone number.

5.enrollment_date
-Text
-Required
-The date the student was enrolled in the system.

6.status
-Text
-Required
-Default: Active
-Allowed values: Active, Inactive, Alumni, Dropped.

7.created_at
-DateTime
-Automatically generated using CURRENT_TIMESTAMP.

8.updated_at
-DateTime
-Automatically initialized using CURRENT_TIMESTAMP.
-Should be updated whenever the student is modified.

9.created_by
-Text
-Optional
-Stores creator information.

10.updated_by
-Text
-Optional
-Stores last modifier information.

#Indexes
#idx_student_status
Optimizes filtering by student status.

#idx_student_email
Optimizes filtering by student email.

#Business Rules
-Email must be unique.
-Phone number must be unique.
-Full name is mandatory.
-Status must be one of: Active, Inactive, Alumni, Dropped.
-Each student receives an auto-generated ID.
-Creation timestamp is automatically recorded.
-Update timestamp should be refreshed during updates.

#Future Relationships
-Batch (Enrollment)
-Course (indirect)

#Database Initialization
The db.py module initializes the SQLite database by executing schema.sql, committing changes, and closing the connection.
