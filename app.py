from flask import Flask, render_template
from routes.trainer_routes import trainer_bp
from routes.course_routes import course_bp
from routes.attendance_routes import attendance_bp
from services.trainer_service import get_trainer_statistics, get_all_trainers
from services.course_service import CourseService

app = Flask(__name__)

app.secret_key = "your-secret-key"

# Register Blueprints
app.register_blueprint(trainer_bp)
app.register_blueprint(course_bp)
app.register_blueprint(attendance_bp)

course_service = CourseService()


@app.route("/")
def home():
    trainer_stats = get_trainer_statistics()
    course_stats = course_service.get_statistics()

    # Sort trainers by trainer_id descending to get the recently added trainers
    all_trainers = get_all_trainers()
    recent_trainers = sorted(all_trainers, key=lambda t: t['trainer_id'], reverse=True)[:3]

    # Sort courses by id descending to get the recently added courses
    all_courses = course_service.get_all_courses()
    recent_courses = sorted(all_courses, key=lambda c: c['id'], reverse=True)[:3]

    return render_template(
        "index.html",
        trainer_stats=trainer_stats,
        course_stats=course_stats,
        recent_trainers=recent_trainers,
        recent_courses=recent_courses
    )


if __name__ == "__main__":
    app.run(debug=True)