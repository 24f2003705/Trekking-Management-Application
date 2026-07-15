from flask import Flask
from models import User, StaffProfile, Trek, Booking
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

from flask_cors import CORS

from config import Config
from extensions import db, jwt, cache, mail


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
db.init_app(app)
jwt.init_app(app)
cache.init_app(app)
mail.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/api/auth") 
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(staff_bp, url_prefix="/api/staff")
app.register_blueprint(user_bp, url_prefix="/api/user")

@app.route("/")
def home():
    return "Welcome to the Trekking Management System!"

from flask_mail import Message
from extensions import mail

@app.route("/test-mail")
def test_mail():

    msg = Message(
        subject="TrekWay Test Email",
        recipients=["aakashrawal1765@gmail.com"]
    )

    msg.body = """
Hello,

This is a test email from TrekWay.

If you received this email, Flask-Mail is configured correctly.

Happy Trekking!
"""

    mail.send(msg)

    return "Email Sent Successfully!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

