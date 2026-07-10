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
    app.run(debug=True)