from flask import Flask
from models import User, StaffProfile, Trek, Booking
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

from config import Config
from extensions import db, jwt

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/api/auth") 
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(staff_bp, url_prefix="/api/staff")
app.register_blueprint(user_bp, url_prefix="/api/user")

@app.route("/")
def home():
    return "Welcome to the Trekking Management System!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)