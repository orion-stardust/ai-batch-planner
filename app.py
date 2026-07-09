from flask import Flask
from routes.trainer_routes import trainer_bp

app = Flask(__name__)

app.secret_key = "your-secret-key"

app.register_blueprint(trainer_bp)

if __name__ == "__main__":
    app.run(debug=True)