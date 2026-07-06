from datetime import datetime
from extensions import db

class Booking(db.Model):
    __tablename__ = "bookings"
    __table_args__ = (db.UniqueConstraint('user_id', 'trek_id', name='unique_user_trek'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_status = db.Column(db.String(20), default="Booked", nullable=False) #Booked, Cancelled, Completed
    payment_status = db.Column(db.String(20), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("bookings", lazy=True))
    trek = db.relationship("Trek", backref=db.backref("bookings", lazy=True))
