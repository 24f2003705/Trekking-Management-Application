from flask import Blueprint, jsonify, request
from utils.decorators import staff_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Trek, Booking
from extensions import db

staff_bp = Blueprint("staff", __name__)

def get_logged_in_staff():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))

@staff_bp.route("/dashboard", methods=["GET"])
@staff_required
def dashboard():
    staff = get_logged_in_staff()

    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
    total_assigned = len(assigned_treks)

    open_treks = sum(1 for trek in assigned_treks if trek.status == "Open")
    completed_treks = sum(1 for trek in assigned_treks if trek.status == "Completed")

    total_participants = 0
    for trek in assigned_treks:
        total_participants += Booking.query.filter_by(trek_id=trek.id).count()

    return jsonify({
        "message": "Welcome Trek Staff",
        "staff_name": staff.name,
        "assigned_treks": total_assigned,
        "open_treks": open_treks,
        "completed_treks": completed_treks,
        "total_participants": total_participants
    }), 200


@staff_bp.route("/treks", methods=["GET"])
@staff_required
def get_assigned_treks():
    staff = get_logged_in_staff()
    treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
    result = []
    for trek in treks:
        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "description": trek.description,
            "duration": trek.duration,
            "difficulty": trek.difficulty,
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "start_date": trek.start_date.strftime("%Y-%m-%d") ,
            "end_date": trek.end_date.strftime("%Y-%m-%d")
        })
    return jsonify({
        "assigned_treks": result
    }), 200


#resource authorization
@staff_bp.route("/treks/<int:trek_id>", methods=["GET"])
@staff_required
def get_single_trek(trek_id):
    staff = get_logged_in_staff()
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"message": "Access denied. This trek is not assigned to you."}), 403
    
    return jsonify({
        "id": trek.id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "description": trek.description,
        "duration": trek.duration,
        "difficulty": trek.difficulty,
        "total_slots": trek.total_slots,
        "available_slots": trek.available_slots,
        "status": trek.status,
        "start_date": trek.start_date.strftime("%Y-%m-%d") ,
        "end_date": trek.end_date.strftime("%Y-%m-%d"),
        "assigned_staff": trek.assigned_staff.name
    }), 200


#update trek status
@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
@staff_required
def update_trek_status(trek_id):
    staff = get_logged_in_staff()
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"})
    
    if trek.assigned_staff_id != staff.id:
        return jsonify({"message": "You are not assigned to this trek"}), 403
    
    data = request.get_json()

    allowed_status = ["Pending", "Open", "Closed", "Ongoing", "Completed"]
    status = data.get("status")

    if status not in allowed_status:
        return jsonify({"message": "Invalid trek status, Use Pending, Open, Closed, Ongoing, Completed"})
    
    trek.status = status
    db.session.commit()

    return jsonify({
        "message": "Trek status updated successfully"
    }), 200


#update available slots

@staff_bp.route("/treks/<int:trek_id>/slots", methods=["PUT"])
@staff_required
def update_slots(trek_id):
    staff = get_logged_in_staff()
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"message": "You are not assigned to this trek"}), 403
    
    data = request.get_json()
    available_slots = data.get("available_slots")
    if available_slots is None:
        return jsonify({"message": "Available slots is required"}), 400
    if available_slots < 0 or available_slots > trek.total_slots:
        return jsonify({"message": "Invalid slot value"}), 400
    trek.available_slots = available_slots

    db.session.commit()
    return jsonify({
        "message": "Available slots updated successfully"
    }), 200


#view trekkers

@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@staff_required
def get_participants(trek_id):
    staff = get_logged_in_staff()
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    if trek.assigned_staff_id != staff.id:
        return jsonify({"message": "You are not assigned to this trek"}), 403
    
    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    participants = []

    for booking in bookings:
        participants.append({
            "booking_id": booking.id,
            "user_id": booking.user.id,
            "name": booking.user.name,
            "email": booking.user.email,
            "phone": booking.user.phone,
            "booking_status": booking.booking_status,
            "payment_status": booking.payment_status
        })
    
    return jsonify({
        "trek_name": trek.trek_name,
        "participants": participants
    }), 200



#Mark trek complete
@staff_bp.route("/treks/<int:trek_id>/complete", methods=["PUT"])
@staff_required
def complete_trek(trek_id):
    staff = get_logged_in_staff()
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    if trek.assigned_staff_id != staff.id:
        return jsonify({"message": "You are not assigned to this trek"}), 403
    
    trek.status = "Completed"

    db.session.commit()

    return jsonify({
        "message": "Trek marked as completed"
    }), 200

        
