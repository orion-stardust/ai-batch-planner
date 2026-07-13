from flask import Flask
from routes.trainer_routes import trainer_bp
from routes.course_routes import course_bp

app = Flask(__name__)

app.secret_key = "your-secret-key"

# Register Blueprints
app.register_blueprint(trainer_bp)
app.register_blueprint(course_bp)


@app.route("/")
def hello_world():
    return "<h1>This is the Home Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)