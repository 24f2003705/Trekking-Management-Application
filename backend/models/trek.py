from datetime import datetime
from extensions import db

class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)  # in days
    difficulty = db.Column(db.String(20), nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(20), default="Pending")
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_staff = db.relationship("User", backref=db.backref("assigned_treks", lazy=True))