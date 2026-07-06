from flask import Flask
from models import User, StaffProfile, Trek, Booking

from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return "Welcome to the Trekking Management System!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)