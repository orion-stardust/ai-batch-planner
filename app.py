from flask import Flask, render_template
from routes.trainer_routes import trainer_bp
from routes.course_routes import course_bp
from routes.attendance_routes import attendance_bp
from routes.batch_routes import batch_bp
from routes.student_routes import student_bp
from services.trainer_service import get_trainer_statistics, get_all_trainers
from services.course_service import CourseService
from services.batch_service import BatchService

app = Flask(__name__)

app.secret_key = "your-secret-key"

# Register Blueprints
app.register_blueprint(trainer_bp)
app.register_blueprint(course_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(student_bp)

course_service = CourseService()
from services.student_service import StudentService
student_service = StudentService()
batch_service = BatchService()


@app.route("/")
def home():
    trainer_stats = get_trainer_statistics()
    course_stats = course_service.get_statistics()
    total_students = len(student_service.get_all_students())
    batch_stats = batch_service.get_statistics()

    # Sort trainers by trainer_id descending to get the recently added trainers
    all_trainers = get_all_trainers()
    recent_trainers = sorted(all_trainers, key=lambda t: t['trainer_id'], reverse=True)[:3]

    # Sort courses by id descending to get the recently added courses
    all_courses = course_service.get_all_courses()
    recent_courses = sorted(all_courses, key=lambda c: c['id'], reverse=True)[:3]

    # Sort batches by batch_id descending to get recently added batches
    all_batches = batch_service.get_all_batches()
    recent_batches = all_batches[:3]

    return render_template(
        "index.html",
        trainer_stats=trainer_stats,
        course_stats=course_stats,
        batch_stats=batch_stats,
        recent_trainers=recent_trainers,
        recent_courses=recent_courses,
        recent_batches=recent_batches
    )


if __name__ == "__main__":
    app.run(debug=True)