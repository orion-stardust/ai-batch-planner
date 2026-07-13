#Course Route Specification

#1. Objective
The Course Route module acts as the Controller layer. It intercepts HTTP requests from the browser, extracts parameters and form data, invokes the 'CourseService', manages flash messaging, and returns rendered HTML templates or redirects.

#2. Route Responsibilities
The Course Routes are responsible for:
-Registering a Flask Blueprint ('course_bp') with a 'courses' URL prefix.
-Handling GET and POST requests.
-Reading user input from 'request.args' (URL parameters) and 'request.form' (POST bodies).
-Passing extracted data to the Service Layer.
-Catching 'ValueError'exceptions raised by the Service layer and converting them into UI error messages via 'flash()'.
-Returning HTTP redirects or rendering specific Jinja2 templates.

The route must *never*:
-Execute SQL queries.
-Contain complex business logic (e.g., checking if duration > 0).
-Directly access the Database Model.

#3.Endpoints

#3.1GET /courses/
-*Purpose*: Display the list of all courses, handle search/filtering, and show module statistics.
-Query Parameters:
-keyword (optional): Search term.
-status (optional): "Active" or "Inactive".
-*Action*: 
-If 'keyword' exists, call course_service.search_courses().
-If 'status' exists, call course_service.filter_courses().
-Else, call course_service.get_all_courses().
-Fetch stats via 'course_service.get_statistics().
-*Response*: Renders 'courses.html  passing courses and stats.

#3.2 GET /courses/create
-*Purpose*: Show the HTML form to create a new course.
-*Response*: Renders 'course_form.html' passing course=None.
-
#3.3 POST /courses/create
-*Purpose**: Process the form submission for a new course.
-*Form Data**: course_name, technology_stack, duration_hours, description, status.
-*Action**: Calls `course_service.create_course().
-*Response**: 
-On Success: flash success message, redirect to courses.
-On Error: flash error message from ValueError, re-render course_form.html.

#3.4 GET /courses/course_id/edit
-*Purpose*: Show the HTML form pre-populated with an existing course's details.
-*Action*: Calls 'course_service.get_course_by_id(course_id).
-*Response*: 
-On Success: Renders 'course_form.html' passing the 'course' dictionary.
-On Error: Redirects to 'courses' with an error message.

#3.5 POST /courses/course_id/edit
-*Purpose*: Process the form submission to update an existing course.
-*Form Data*: Same as create.
-*Action*: Calls 'course_service.update_course()'.
-*Response*:
-On Success: 'flash' success message, redirect to 'courses'`.
-On Error: 'flash' error message, re-render 'course_form.html'.

#3.6 POST /courses/course_id/delete
-*Purpose*: Securely delete a course.
-*Action*: Calls 'course_service.delete_course()'.
-*Response*: Redirect to 'courses' with success/error flash message.

#3.7 POST /courses/course_id/status
-*Purpose*: Toggle or explicitly set the "Active"/"Inactive" status of a course.
-*Form Data*: 'status'.
-*Action*: Calls 'course_service.update_status()'.
-*Response*: Redirect to 'courses' with success/error flash message.
