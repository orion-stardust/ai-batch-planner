#Student Service Specification

#1. Objective
The Student Service acts as the business logic layer. It sits between the Routes (Controllers) and the Model.
Its responsibilities are to enforce business rules, validate data types, handle exceptions, and structure responses before they reach the routing layer.

#2. Service Responsibilities
The Student Service is responsible for:
-Enforcing business rules (e.g., checking if email is formatted correctly, phone number is correct length).
-Preventing duplicate students by calling the Model's existence checks.
-Handling empty or invalid inputs by raising 'ValueError'.
-Returning normalized dictionary responses with success flags and messages where applicable.
-Exposing model functionalities (search, filter) safely to the routes.

The service must *never*:
-Execute raw SQL queries (delegated to the Model).
-Render HTML templates (delegated to the Routes).
-Directly parse 'request.form'or 'request.args' (delegated to the Routes).

#3. Method Specifications

#3.1 'create_student(full_name, email, phone, enrollment_date, status, created_by)'
-*Validation*: 
-'full_name', 'email', 'phone' must not be empty.
-'email' must match email regex format.
-'phone' must contain between 7 and 15 digits.
-'status' must be one of: "Active", "Inactive", "Alumni", "Dropped".
-Email and phone must not already exist in the database.
-*Action*: Calls 'StudentModel.create_student()'.
-*Returns*: '{"success": True, "message": "Student created successfully.", "student_id": new_id}'
-*Raises*: 'ValueError' on validation failure.

#3.2 get_all_students()
-*Action*: Retrieves all students from the model.
-*Returns*: List of student dictionaries.

#3.3 get_student_by_id(student_id)
-*Validation*: student_id must cast to 'int'. Student must exist.
-*Action*: Retrieves student dictionary from the model.
-*Returns*: Student dictionary.
-*Raises*: ValueError if ID is invalid or student not found.

#3.4 'update_student(student_id, full_name, email, phone, status, updated_by)'
-*Validation*: 
-Validates all fields similar to create_student.
-Checks if the new 'email' or 'phone' already exists for a *different* student_id (duplicate check).
-*Action*: Calls 'StudentModel.update_student()'.
-*Returns*: "success": True, "message": "Student updated successfully."
-*Raises*: 'ValueError'on validation failure or if the student does not exist to be updated.

#3.5 'delete_student(student_id)'
-*Validation*: Verifies student exists before deletion.
-*Action*: Calls 'StudentModel.delete_student()'.
-*Returns*:"success": True, "message": "Student deleted successfully."
-*Raises*: 'ValueError' if the student does not exist.

#3.6 Proxy Methods
-search_students(keyword)
-filter_students(status)

All proxy methods pass arguments to the model and return the raw output (Lists/Dicts).

#4.Error Handling
All methods in the service layer should gracefully trap predictable errors and raise a standardized 'ValueError' with a user-friendly string message. The Route layer will catch this and display it to the user.
