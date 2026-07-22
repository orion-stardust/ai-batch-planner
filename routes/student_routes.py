from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.student_service import StudentService
from services.course_service import CourseService
from services.batch_service import BatchService

student_bp = Blueprint('student_bp', __name__, url_prefix='/students')
student_service = StudentService()
course_service = CourseService()
batch_service = BatchService()

@student_bp.route('/')
def list_students():
    """Display all students, handle searching and filtering."""
    keyword = request.args.get('keyword', '').strip()
    status = request.args.get('status', '').strip()
    
    if keyword:
        students = student_service.search_students(keyword)
    elif status:
        students = student_service.filter_students(status)
    else:
        students = student_service.get_all_students()
        
    return render_template('students.html', students=students)

@student_bp.route('/create', methods=['GET', 'POST'])
def create_student():
    """Handle the creation of a new student."""
    courses = course_service.get_all_courses()
    batches = batch_service.get_all_batches()

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        enrollment_date = request.form.get('enrollment_date')
        status = request.form.get('status', 'Active')
        course_id = request.form.get('course_id')
        batch_id = request.form.get('batch_id')
        
        try:
            student_service.create_student(
                full_name=full_name,
                email=email,
                phone=phone,
                enrollment_date=enrollment_date,
                status=status,
                course_id=course_id,
                batch_id=batch_id
            )
            flash("Student created successfully.", "success")
            return redirect(url_for('student_bp.list_students'))
        except ValueError as e:
            flash(str(e), "error")
            temp_student = {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'enrollment_date': enrollment_date,
                'status': status,
                'course_id': int(course_id) if course_id else None,
                'batch_id': int(batch_id) if batch_id else None
            }
            return render_template('student_form.html', student=temp_student, courses=courses, batches=batches)
            
    return render_template('student_form.html', student=None, courses=courses, batches=batches)

@student_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Handle editing an existing student."""
    courses = course_service.get_all_courses()
    batches = batch_service.get_all_batches()

    try:
        student = student_service.get_student_by_id(student_id)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('student_bp.list_students'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        status = request.form.get('status')
        course_id = request.form.get('course_id')
        batch_id = request.form.get('batch_id')
        
        try:
            student_service.update_student(
                student_id=student_id,
                full_name=full_name,
                email=email,
                phone=phone,
                status=status,
                course_id=course_id,
                batch_id=batch_id
            )
            flash("Student updated successfully.", "success")
            return redirect(url_for('student_bp.list_students'))
        except ValueError as e:
            flash(str(e), "error")
            temp_student = {
                'student_id': student_id,
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'enrollment_date': student.get('enrollment_date'),
                'status': status,
                'course_id': int(course_id) if course_id else None,
                'batch_id': int(batch_id) if batch_id else None
            }
            return render_template('student_form.html', student=temp_student, courses=courses, batches=batches)
            
    return render_template('student_form.html', student=student, courses=courses, batches=batches)

@student_bp.route('/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Handle the deletion of a student."""
    try:
        student_service.delete_student(student_id)
        flash("Student deleted successfully.", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('student_bp.list_students'))
