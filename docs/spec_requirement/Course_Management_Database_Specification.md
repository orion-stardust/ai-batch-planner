# Course Management Database Specification:

#Module Name
Course Management

#Purpose 
The Course Management module stores and manages all course-related information within the AI Batch Planner system. It supports course creation, modification, activation/deactivation, lookup, listing, and future batch mapping.

#Database
-Engine: SQLite3
-Database File: batch_planner.db

#Table: Course

#Fields
1.id
-Integer
-Primary Key
-Auto Increment
-Unique course identifier.

2.course_name
-Text
-Required
-Unique
-Official course name.

3.technology_stack
-Text
-Required
-Technology category of the course.

4.duration_hours
-Integer
-Required
-Must be greater than 0.

5.description
-Text
-Optional
-Course description.

6.status
-Text
-Required
-Default: Active
-Allowed values: Active, Inactive.

7.created_at
-DateTime
-Automatically generated using CURRENT_TIMESTAMP.

8.updated_at
-DateTime
-Automatically initialized using CURRENT_TIMESTAMP.
-Should be updated whenever the course is modified.

9.created_by
-Text
-Optional
-Stores creator information.

10.updated_by
-Text
-Optional
-Stores last modifier information.

#Indexes
#idx_course_status
Optimizes filtering by course status.

#idx_course_technology_stack
Optimizes filtering by technology stack.

#Business Rules
-Course name must be unique.
-Technology stack is mandatory.
-Duration must be greater than zero.
-Status must be either Active or Inactive.
-Each course receives an auto-generated ID.
-Creation timestamp is automatically recorded.
-Update timestamp should be refreshed during updates.

#Future Relationships
-Batch
-Trainer (indirect)
-Student (indirect)
-Assessment
-Reports

#Database Initialization
The db.py module initializes the SQLite database by executing schema.sql, committing changes, and closing the connection.
