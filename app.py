from flask import Flask
from blueprint.phone_tracker_bp import phone_bp
app = Flask(__name__)
app.register_blueprint(phone_bp)

if __name__ == "__main__":
    app.run(debug=True)
