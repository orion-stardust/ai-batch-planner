from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.course_service import CourseService

course_bp = Blueprint('course_bp', __name__, url_prefix='/courses')
course_service = CourseService()

@course_bp.route('/')
def list_courses():
    """Display all courses, handle searching and filtering, and show stats."""
    keyword = request.args.get('keyword', '').strip()
    status = request.args.get('status', '').strip()
    
    if keyword or status:
        courses = course_service.filter_courses(status=status, keyword=keyword)
    else:
        courses = course_service.get_all_courses()
        
    stats = course_service.get_statistics()
    # Expects a templates/courses.html to render
    return render_template('courses.html', courses=courses, stats=stats)

@course_bp.route('/create', methods=['GET', 'POST'])
def create_course():
    """Handle the creation of a new course."""
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        technology_stack = request.form.get('technology_stack')
        duration_hours = request.form.get('duration_hours')
        description = request.form.get('description')
        status = request.form.get('status', 'Active')
        created_by = 'SystemAdmin'  # Placeholder for authenticated user
        
        try:
            course_service.create_course(
                course_name=course_name,
                technology_stack=technology_stack,
                duration_hours=duration_hours,
                description=description,
                status=status,
                created_by=created_by
            )
            flash("Course created successfully.", "success")
            return redirect(url_for('course_bp.list_courses'))
        except ValueError as e:
            flash(str(e), "error")
            temp_course = {
                'course_name': course_name,
                'technology_stack': technology_stack,
                'duration_hours': duration_hours,
                'description': description,
                'status': status
            }
            return render_template('course_form.html', course=temp_course)
            
    # Expects a templates/course_form.html to render
    return render_template('course_form.html', course=None)

@course_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    """Handle editing an existing course."""
    try:
        course = course_service.get_course_by_id(course_id)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('course_bp.list_courses'))

    if request.method == 'POST':
        course_name = request.form.get('course_name')
        technology_stack = request.form.get('technology_stack')
        duration_hours = request.form.get('duration_hours')
        description = request.form.get('description')
        status = request.form.get('status')
        updated_by = 'SystemAdmin'  # Placeholder for authenticated user
        
        try:
            course_service.update_course(
                course_id=course_id,
                course_name=course_name,
                technology_stack=technology_stack,
                duration_hours=duration_hours,
                description=description,
                status=status,
                updated_by=updated_by
            )
            flash("Course updated successfully.", "success")
            return redirect(url_for('course_bp.list_courses'))
        except ValueError as e:
            flash(str(e), "error")
            temp_course = {
                'id': course_id,
                'course_name': course_name,
                'technology_stack': technology_stack,
                'duration_hours': duration_hours,
                'description': description,
                'status': status
            }
            return render_template('course_form.html', course=temp_course)
            
    return render_template('course_form.html', course=course)

@course_bp.route('/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    """Handle the deletion of a course."""
    try:
        course_service.delete_course(course_id)
        flash("Course deleted successfully.", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('course_bp.list_courses'))

@course_bp.route('/<int:course_id>/status', methods=['POST'])
def update_status(course_id):
    """Toggle or update the active/inactive status of a course."""
    status = request.form.get('status')
    updated_by = 'SystemAdmin'
    try:
        course_service.update_status(course_id, status, updated_by)
        flash("Course status updated successfully.", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('course_bp.list_courses'))
