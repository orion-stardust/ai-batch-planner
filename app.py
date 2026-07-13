<<<<<<< HEAD
from flask import Flask
from routes.trainer_routes import trainer_bp

app = Flask(__name__)

app.secret_key = "your-secret-key"

app.register_blueprint(trainer_bp)

if __name__ == "__main__":
=======
from flask import Flask
from routes.course_routes import course_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'

# Register Blueprints
app.register_blueprint(course_bp)

@app.route('/')
def hello_world():
    return ("<h1>This is the Home Page</h1>")

if __name__ == '__main__':
>>>>>>> e8568112bbd6275753fba240fe45b17c67c21592
    app.run(debug=True)