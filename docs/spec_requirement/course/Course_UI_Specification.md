#Course UI/Frontend Specification

#1. Objective
The UI layer provides the visual interface for users to interact with the Course Management module. It relies on HTML templates rendered via Flask's Jinja2 engine, styled with CSS, and enhanced with Javascript.

#2. Template Structure
All UI files should reside in the templates/ directory and extend a common base.html layout that includes the site navigation header, footer, and flash message container.

#3. Required Pages

#3.1 courses.html (Course Dashboard)
-Purpose: Displays the comprehensive list of courses and top-level statistics.
-Components:
-Statistics Cards: Top widgets showing total courses, active courses, inactive courses, and average duration.
-Search & Filter Bar: A form submitting GET requests to /courses/ with inputs for keyword text and a status dropdown.
-Data Table: A grid/table displaying courses (Name, Technology, Duration, Status, Actions).
-Action Buttons:
-Add New Course button linking to /courses/create.
-Edit button for each row linking to /courses/<id>/edit.
-Delete form/button for each row (submitting POST to /courses/<id>/delete with a JS confirmation).
-Status toggle button/form (Active/Inactive) submitting POST to /courses/<id>/status.

#3.2 course_form.html (Create/Edit Form)
-Purpose: A dual-purpose form used for both creating a new course and editing an existing one.
-Logic:
-Uses Jinja2 conditions to determine if it should post to the create endpoint or the edit endpoint.
-Pre-fills input values if a course object is passed in context.
-Form Fields:
-Course Name: text input, required
-Technology Stack: text input, required
-Duration (Hours): number input, required, min=1
-Description: textarea
-Status: select dropdown with Active/Inactive
-Actions:
-Submit Button
-Cancel Button

#4. Flash Messages
-The UI must have a dedicated section that iterates over Flask's get_flashed_messages to display success or error banners.

#5. Javascript Interactions
-Delete Confirmation: Prompt users before submitting a delete action.
-Client-side Validation: Ensure numeric inputs are > 0 before submission.
-Dynamic UI: Highlight rows based on Active/Inactive status.
