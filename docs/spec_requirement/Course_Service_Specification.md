#Course Service Specification

#1. Objective
The Course Service acts as the business logic layer. It sits between the Routes (Controllers) and the Model.
Its responsibilities are to enforce business rules, validate data types, handle exceptions, and structure responses before they reach the routing layer.

#2. Service Responsibilities
The Course Service is responsible for:
-Converting data types (e.g., string from HTTP requests to integers).
-Enforcing business rules (e.g., checking if duration > 0, validating 'Active'/'Inactive' status).
-Preventing duplicate courses by calling the Model's existence checks.
-Handling empty or invalid inputs by raising 'ValueError'.
-Returning normalized dictionary responses with success flags and messages where applicable.
-Exposing model functionalities (search, filter, stats) safely to the routes.

The service must *never*:
-Execute raw SQL queries (delegated to the Model).
-Render HTML templates (delegated to the Routes).
-Directly parse 'request.form'or 'request.args' (delegated to the Routes).

#3. Method Specifications

#3.1 'create_course(course_name, technology_stack, duration_hours, description, status, created_by)'
-*Validation*: 
-'course_name' and 'technology_stack' must not be empty.
-'duration_hours' must safely cast to an 'int' and be > 0.
-'status' must be either "Active" or "Inactive".
-Course name must not already exist in the database.
-*Action*: Calls 'CourseModel.create_course()'.
-*Returns*: '{"success": True, "message": ""Course created successfully."", "course_id": new_id}'
-*Raises*: 'ValueError' on validation failure.

#3.2 get_all_courses()
-*Action*: Retrieves all courses from the model.
-*Returns*: List of course dictionaries.

#3.3 get_course_by_id(course_id)
-*Validation*: course_id must cast to 'int' and be > 0. Course must exist.
-*Action*: Retrieves course dictionary from the model.
-*Returns*: Course dictionary.
-*Raises*: ValueError if ID is invalid or course not found.

#3.4 'update_course(course_id, course_name, technology_stack, duration_hours, description, status, updated_by)'
-*Validation*: 
-Validates all fields similar to create_course.
-Checks if the new 'course_name' already exists for a *different* course_id (duplicate check).
-*Action*: Calls 'CourseModel.update_course()'.
-*Returns*: "success": True, "message": "Course updated successfully."
-*Raises*: 'ValueError'on validation failure or if the course does not exist to be updated.

#3.5 'delete_course(course_id)'
-*Validation*: Verifies course exists before deletion.
-*Action*: Calls 'CourseModel.delete_course()'.
-*Returns*:"success": True, "message": "Course deleted successfully."
-*Raises*: 'ValueError' if the course does not exist.

#3.6 'update_status(course_id, status, updated_by)'
-*Validation*: 'status' must be "Active" or "Inactive".
-*Action*: Calls 'CourseModel.update_status()'.
-*Returns*:"success": True, "message":"Course status updated successfully."
-*Raises*: 'ValueError' on validation failure or missing course.

#3.7Proxy Methods
-search_courses(keyword)
-filter_courses(status, technology, min_duration, max_duration)
-get_statistics()
-get_active_courses()
-get_inactive_courses()
All proxy methods pass arguments to the model and return the raw output (Lists/Dicts).

#4.Error Handling
All methods in the service layer should gracefully trap predictable errors and raise a standardized 'ValueError' with a user-friendly string message. The Route layer will catch this and display it to the user.
