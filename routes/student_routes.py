from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.student_service import StudentService
from services.course_service import CourseService
from services.batch_service import BatchService
from services.student_register_service import StudentRegisterService

student_bp = Blueprint('student_bp', __name__, url_prefix='/students')
student_service = StudentService()
course_service = CourseService()
batch_service = BatchService()
register_service = StudentRegisterService()

@student_bp.route('/')
def list_students():
    """Display all students, handle searching."""
    keyword = request.args.get('keyword', '').strip()
    
    if keyword:
        students = student_service.search_students(keyword)
    else:
        students = student_service.get_all_students()
        
    return render_template('students.html', students=students)

@student_bp.route('/create', methods=['GET', 'POST'])
def create_student():
    """Handle the creation of a new student."""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        qualification = request.form.get('qualification')
        
        try:
            student_service.create_student(
                full_name=full_name,
                email=email,
                phone=phone,
                qualification=qualification
            )
            flash("Student created successfully.", "success")
            return redirect(url_for('student_bp.list_students'))
        except ValueError as e:
            flash(str(e), "error")
            temp_student = {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'qualification': qualification
            }
            return render_template('student_form.html', student=temp_student)
            
    return render_template('student_form.html', student=None)

@student_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Handle editing an existing student."""
    try:
        student = student_service.get_student_by_id(student_id)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('student_bp.list_students'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        qualification = request.form.get('qualification')
        
        try:
            student_service.update_student(
                student_id=student_id,
                full_name=full_name,
                email=email,
                phone=phone,
                qualification=qualification
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
                'qualification': qualification
            }
            return render_template('student_form.html', student=temp_student)
            
    return render_template('student_form.html', student=student)

@student_bp.route('/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Handle the deletion of a student."""
    try:
        student_service.delete_student(student_id)
        flash("Student deleted successfully.", "success")
    except ValueError as e:
        flash(str(e), "error")
        
    return redirect(url_for('student_bp.list_students'))


@student_bp.route('/register')
def list_register():
    """Display all student registrations, handle searching."""
    keyword = request.args.get('keyword', '').strip()
    if keyword:
        registrations = register_service.search_registrations(keyword)
    else:
        registrations = register_service.get_all_registrations()
    return render_template('registrations.html', registrations=registrations)


@student_bp.route('/register/create', methods=['GET', 'POST'])
def register_student():
    """Register a student to a course and optional batch."""
    students = student_service.get_all_students()
    courses = course_service.get_all_courses()
    batches = batch_service.get_all_batches()

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        enrollment_date = request.form.get('enrollment_date')
        batch_id = request.form.get('batch_id')
        status = request.form.get('status')

        try:
            register_service.create_registration(
                student_id=student_id,
                course_id=course_id,
                enrollment_date=enrollment_date,
                status=status,
                batch_id=batch_id
            )
            flash("Student registered successfully.", "success")
            return redirect(url_for('student_bp.list_register'))
        except ValueError as e:
            flash(str(e), "error")
            temp_reg = {
                'student_id': int(student_id) if student_id else None,
                'course_id': int(course_id) if course_id else None,
                'enrollment_date': enrollment_date,
                'batch_id': int(batch_id) if batch_id else None,
                'status': status
            }
            return render_template('register_form.html', registration=temp_reg, students=students, courses=courses, batches=batches)

    return render_template('register_form.html', registration=None, students=students, courses=courses, batches=batches)


@student_bp.route('/register/<int:register_id>/edit', methods=['GET', 'POST'])
def edit_registration(register_id):
    """Edit an existing student registration."""
    students = student_service.get_all_students()
    courses = course_service.get_all_courses()
    batches = batch_service.get_all_batches()

    try:
        registration = register_service.get_registration_by_id(register_id)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for('student_bp.list_register'))

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        enrollment_date = request.form.get('enrollment_date')
        batch_id = request.form.get('batch_id')
        status = request.form.get('status')

        try:
            register_service.update_registration(
                register_id=register_id,
                student_id=student_id,
                course_id=course_id,
                enrollment_date=enrollment_date,
                status=status,
                batch_id=batch_id
            )
            flash("Registration updated successfully.", "success")
            return redirect(url_for('student_bp.list_register'))
        except ValueError as e:
            flash(str(e), "error")
            temp_reg = {
                'register_id': register_id,
                'student_id': int(student_id) if student_id else None,
                'course_id': int(course_id) if course_id else None,
                'enrollment_date': enrollment_date,
                'batch_id': int(batch_id) if batch_id else None,
                'status': status
            }
            return render_template('register_form.html', registration=temp_reg, students=students, courses=courses, batches=batches)

    return render_template('register_form.html', registration=registration, students=students, courses=courses, batches=batches)


@student_bp.route('/register/<int:register_id>/delete', methods=['POST'])
def delete_registration(register_id):
    """Delete a student registration."""
    try:
        register_service.delete_registration(register_id)
        flash("Registration deleted successfully.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for('student_bp.list_register'))
