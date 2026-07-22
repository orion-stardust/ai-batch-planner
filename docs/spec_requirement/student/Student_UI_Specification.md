#Student UI/Frontend Specification

#1. Objective
The UI layer provides the visual interface for users to interact with the Student Management module. It relies on HTML templates rendered via Flask's Jinja2 engine, styled with CSS, and enhanced with Javascript.

#2. Template Structure
All UI files should reside in the templates/ directory and extend a common base.html layout that includes the site navigation header, footer, and flash message container.

#3. Required Pages

#3.1 students.html (Student Dashboard)
-Purpose: Displays the comprehensive list of students and allows for search/filtering.
-Components:
-Search & Filter Bar: A form submitting GET requests to /students/ with inputs for keyword text and a status dropdown.
-Data Table: A grid/table displaying students (Name, Email, Phone, Enrollment Date, Status, Actions).
-Action Buttons:
-Add New Student button linking to /students/create.
-Edit button for each row linking to /students/<id>/edit.
-Delete form/button for each row (submitting POST to /students/<id>/delete with a JS confirmation).

#3.2 student_form.html (Create/Edit Form)
-Purpose: A dual-purpose form used for both creating a new student and editing an existing one.
-Logic:
-Uses Jinja2 conditions to determine if it should post to the create endpoint or the edit endpoint.
-Pre-fills input values if a student object is passed in context.
-Form Fields:
-Full Name: text input, required
-Email Address: email input, required
-Phone Number: text input, required
-Enrollment Date: date input, required
-Status: select dropdown with Active, Inactive, Alumni, Dropped
-Actions:
-Submit Button
-Cancel Button

#4. Flash Messages
-The UI must have a dedicated section that iterates over Flask's get_flashed_messages to display success or error banners.

#5. Javascript Interactions
-Delete Confirmation: Prompt users before submitting a delete action.
-Client-side Validation: Ensure required fields are filled out.
-Dynamic UI: Highlight rows or badges based on Active/Inactive status.
