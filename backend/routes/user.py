from flask import Blueprint, jsonify, request
from utils.decorators import trekker_required
from flask_jwt_extended import get_jwt_identity
from models import User, Trek, Booking
from extensions import db
from datetime import date


user_bp = Blueprint("user", __name__)
def get_logged_in_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))

@user_bp.route("/dashboard", methods=["GET"])
@trekker_required
def dashboard():
    user = get_logged_in_user()
    bookings = Booking.query.filter_by(user_id=user.id).all()
    total_bookings = len(bookings)

    active_bookings = sum(
        1 for booking in bookings
        if booking.booking_status == "Booked"
        and booking.trek_status != "Completed"
    )

    completed_treks = sum(
        1 for booking in bookings
        if booking.booking_status == "Completed"
    )

    cancelled_bookings = sum(
        1 for booking in bookings
        if booking.booking_status == "Cancelled" 
    )

    return jsonify({
        "message": f"Welcome {user.name}",
        "total_bookings": total_bookings,
        "active_bookings": active_bookings,
        "completed_treks": completed_treks,
        "cancelled_bookings": cancelled_bookings
    }), 200


#view available and open treks
@user_bp.route("/treks", methods=["GET"])
@trekker_required
def get_open_treks():
    treks = Trek.query.filter_by(status ="Open").all()
    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "description": trek.description,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "start_date": trek.start_date,
            "end_date": trek.end_date
        })

    return jsonify(result), 200


#view single trek
@user_bp.route("/treks/<int:trek_id>", methods =["GET"])
@trekker_required
def get_single_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id, status="Open").first()
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    return jsonify({
        "id": trek.id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "description": trek.description,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "status": trek.status,
        "start_date": trek.start_date,
        "end_date": trek.end_date
    }), 200


#search treks
@user_bp.route("/search", methods=["GET"])
@trekker_required
def search_trek():
    trek_name = request.args.get("name")

    treks = Trek.query.filter(Trek.status =="Open", Trek.trek_name.ilike(f"%{trek_name}%")).all()
    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration
        })
    return jsonify(result), 200


#filter by location difficulty duration
@user_bp.route("/filter", methods=["GET"])
@trekker_required
def filter_trek():
    query = Trek.query.filter_by(status="Open")
    difficulty = request.args.get("difficulty")
    location = request.args.get("location")
    duration = request.args.get("duration")

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))
    if duration:
        query = query.filter(Trek.duration == int(duration))

    treks = query.all()

    result=[]
    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration
        })

    return jsonify(result), 200


#trekker booking 
@user_bp.route("/book", methods=["POST"])
@trekker_required
def book_trek():
    user = get_logged_in_user()
    data = request.get_json()
    trek = Trek.query.get(data.get("trek_id"))
    if not data or not data.get("trek_id"):
        return jsonify({"message": "trek_id is required"}), 400

    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    if trek.status != "Open":
        return jsonify({"message": " Trek is not open for booking"}), 400
    
    if trek.available_slots <= 0:
        return jsonify({"message": "No slots available"}), 400
    
    existing_booking = Booking.query.filter_by(
        user_id = user.id,
        trek_id = trek.id
    ).first()

    if existing_booking:
        return jsonify({"message": "You have already booked this trek"}), 400
    booking = Booking(
        user_id = user.id,
        trek_id = trek.id,
        booking_date = date.today(),
        payment_status = "Pending"
    )
    
    db.session.add(booking)
    trek.available_slots -=1
    db.session.commit()

    return jsonify({
        "message": "Trek booked successfully"
    }), 201


#my bookings
@user_bp.route("/bookings", methods=["GET"])
@trekker_required
def my_bookings():
    user = get_logged_in_user()
    bookings = Booking.query.filter_by(user_id=user.id).all()

    result=[]
    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "booking_date": booking.booking_date,
            "booking_status": booking.booking_status,
            "payment_status": booking.payment_status,
            "trek_status": booking.trek.status,
            "start_date": booking.trek.start_date,
            "end_date": booking.trek.end_date
        })

    return jsonify(result), 200


#update Profile
@user_bp.route("/profile", methods=["PUT"])
@trekker_required
def update_profile():

    user = get_logged_in_user()
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "phone" in data:
        user.phone = data["phone"]
    
    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200


#cancel booking
@user_bp.route("/cancel_booking/<int:booking_id>", methods=["PUT"])
@trekker_required
def cancel_booking(booking_id):
    user = get_logged_in_user()

    booking = Booking.query.filter_by(
        id = booking_id,
        user_id = user.id
    ).first()

    if booking.trek.start_date <= date.today():
        return jsonify({
            "message": "Cannot cancel, trek has started"
        }), 400

    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    if booking.booking_status == "Cancelled":
        return jsonify({"message": "Booking already cancelled"}), 400
    if booking.booking_status == "Completed":
        return jsonify({"message": "Completed trek cannot be cancelled"}), 400
    
    booking.booking_status == "Cancelled"
    booking.trek.available_slots += 1

    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully"
    }), 200


#trek history
@user_bp.route("/history", methods=["GET"])
@trekker_required
def trekking_history():
    user = get_logged_in_user()

    bookings= Booking.query.filter_by(
        user_id = user.id,
        booking_status = "Completed"
    ).all()

    result = []

    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "booking_date": booking.booking_date,
            "start_date": booking.trek.start_date,
            "end_date": booking.trek.end_date,
            "status": booking.booking_status
        })
    return jsonify(result), 200