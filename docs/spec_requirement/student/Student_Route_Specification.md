#Student Route Specification

#1. Objective
The Student Route module acts as the Controller layer. It intercepts HTTP requests from the browser, extracts parameters and form data, invokes the 'StudentService', manages flash messaging, and returns rendered HTML templates or redirects.

#2. Route Responsibilities
The Student Routes are responsible for:
-Registering a Flask Blueprint ('student_bp') with a 'students' URL prefix.
-Handling GET and POST requests.
-Reading user input from 'request.args' (URL parameters) and 'request.form' (POST bodies).
-Passing extracted data to the Service Layer.
-Catching 'ValueError'exceptions raised by the Service layer and converting them into UI error messages via 'flash()'.
-Returning HTTP redirects or rendering specific Jinja2 templates.

The route must *never*:
-Execute SQL queries.
-Contain complex business logic.
-Directly access the Database Model.

#3.Endpoints

#3.1GET /students/
-*Purpose*: Display the list of all students, handle search/filtering.
-Query Parameters:
-keyword (optional): Search term.
-status (optional): "Active", "Inactive", "Alumni", or "Dropped".
-*Action*: 
-If 'keyword' exists, call student_service.search_students().
-If 'status' exists, call student_service.filter_students().
-Else, call student_service.get_all_students().
-*Response*: Renders 'students.html passing students list.

#3.2 GET /students/create
-*Purpose*: Show the HTML form to create a new student.
-*Response*: Renders 'student_form.html' passing student=None.

#3.3 POST /students/create
-*Purpose**: Process the form submission for a new student.
-*Form Data**: full_name, email, phone, enrollment_date, status.
-*Action**: Calls `student_service.create_student().
-*Response**: 
-On Success: flash success message, redirect to students.
-On Error: flash error message from ValueError, re-render student_form.html.

#3.4 GET /students/student_id/edit
-*Purpose*: Show the HTML form pre-populated with an existing student's details.
-*Action*: Calls 'student_service.get_student_by_id(student_id).
-*Response*: 
-On Success: Renders 'student_form.html' passing the 'student' dictionary.
-On Error: Redirects to 'students' with an error message.

#3.5 POST /students/student_id/edit
-*Purpose*: Process the form submission to update an existing student.
-*Form Data*: Same as create.
-*Action*: Calls 'student_service.update_student()'.
-*Response*:
-On Success: 'flash' success message, redirect to 'students'`.
-On Error: 'flash' error message, re-render 'student_form.html'.

#3.6 POST /students/student_id/delete
-*Purpose*: Securely delete a student.
-*Action*: Calls 'student_service.delete_student()'.
-*Response*: Redirect to 'students' with success/error flash message.
