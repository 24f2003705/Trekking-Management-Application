from flask import Blueprint, jsonify, request
from utils.decorators import admin_required
from models import User, Trek, Booking, StaffProfile
from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_users = User.query.filter_by(role="Trekker").count()
    total_staff = User.query.filter_by(role="Trek Staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    return jsonify({
        "message": "Welcome Admin Dashboard",
        "total_users": total_users,
        "total_staff": total_staff,
        "total_treks": total_treks,
        "total_bookings": total_bookings
    }), 200

@admin_bp.route("/treks", methods=["POST"])
@admin_required
def create_trek():
    data = request.get_json()
    trek_name = data.get("trek_name")
    location = data.get("location")
    description = data.get("description")
    difficulty = data.get("difficulty")
    duration = data.get("duration")
    total_slots = data.get("total_slots")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([trek_name, location, difficulty, duration, total_slots, start_date, end_date]):
        return jsonify({"message": "All required fields are mandatory"}), 400
    
    allowed = ["Easy", "Moderate", "Hard"]
    if difficulty not in allowed:
        return jsonify({"message": "Difficulty must be one of: Easy, Moderate, Hard"}), 400
    
    trek = Trek(
        trek_name=trek_name,
        location=location,
        description=description,
        difficulty=difficulty,
        duration=duration,
        total_slots=total_slots,
        available_slots=total_slots,
        start_date=datetime.strptime(start_date, "%Y-%m-%d"),
        end_date=datetime.strptime(end_date, "%Y-%m-%d"),
        status="Pending"
    )

    db.session.add(trek)
    db.session.commit()
    return jsonify({"message": "Trek created successfully", "trek_id": trek.id}), 201

@admin_bp.route("/treks", methods=["GET"])
@admin_required
def get_all_treks():
    treks = Trek.query.all()
    trek_list = []
    for trek in treks:
        trek_list.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "description": trek.description,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "start_date": trek.start_date.strftime("%Y-%m-%d"),
            "end_date": trek.end_date.strftime("%Y-%m-%d") 
        })
    return jsonify({"treks": trek_list}), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["GET"])
@admin_required
def get_trek(trek_id):
    trek = db.session.get(Trek, trek_id)
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
        "start_date": trek.start_date.strftime("%Y-%m-%d"),
        "end_date": trek.end_date.strftime("%Y-%m-%d"),
        "assigned_staff_id": trek.assigned_staff_id
    }), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@admin_required
def update_trek(trek_id):
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    data = request.get_json()
    trek.trek_name = data.get("trek_name", trek.trek_name)
    trek.location = data.get("location", trek.location)
    trek.description = data.get("description", trek.description)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.duration = data.get("duration", trek.duration)
    trek.total_slots = data.get("total_slots", trek.total_slots)
    trek.available_slots = data.get("available_slots", trek.available_slots)
    trek.status = data.get("status", trek.status)
    trek.assigned_staff_id = data.get("assigned_staff_id", trek.assigned_staff_id)
    if data.get("start_date"):
        trek.start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    if data.get("end_date"):
        trek.end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    
    db.session.commit()
    return jsonify({"message": "Trek updated successfully"}), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@admin_required
def delete_trek(trek_id):
    trek = db.session.get(Trek, trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"}), 200


#route to create staff
@admin_bp.route("/staff", methods=["POST"])
@admin_required
def create_staff():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered."}), 409
    
    staff = User(
        name = data["name"],
        email = data["email"],
        password = generate_password_hash(data["password"]),
        role = "Trek Staff",
        phone = data.get("phone"),
        status = "Active"
    )
    db.session.add(staff)
    db.session.flush()  # Flush to get the staff ID before committing

    profile = StaffProfile(
        user_id = staff.id,
        contact_details = data.get("contact_details"),
        experience = data.get("experience", 0),
        status = "Available"
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({ "message": "Staff created successfully"}), 201

@admin_bp.route("/staff", methods=["GET"])
@admin_required
def get_staff():
    staffs = User.query.filter_by(role="Trek Staff").all()
    result = []
    for staff in staffs:
        result.append({
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "phone": staff.phone,
            "status": staff.status
        })
    return jsonify({"staffs": result}), 200


@admin_bp.route("/staff/<int:id>", methods=["GET"])
@admin_required
def get_staff_by_id(id):
    staff = User.query.filter_by(id=id, role="Trek Staff").first()
    if not staff:
        return jsonify({"message": "Staff not found"}), 404
    
    return jsonify({
        "id": staff.id,
        "name": staff.name,
        "email": staff.email,
        "phone": staff.phone,
        "status": staff.status
    }), 200


@admin_bp.route("/staff/<int:id>", methods=["PUT"])
@admin_required
def update_staff(id):
    staff = User.query.filter_by(id=id, role="Trek Staff").first()
    if not staff:
        return jsonify({"message": "Staff not found"}), 404
    
    data = request.get_json()
    staff.name = data.get("name", staff.name)
    staff.phone = data.get("phone", staff.phone)
    staff.status = data.get("status", staff.status)

    db.session.commit()

    return jsonify({"message": "Staff updated successfully"}), 200


@admin_bp.route("/staff/<int:id>", methods =["DELETE"])
@admin_required
def delete_staff(id):
    staff = User.query.filter_by(id=id, role="Trek Staff").first()
    if not staff:
        return jsonify({"message": "Staff not found"}), 404
    
    if profile := StaffProfile.query.filter_by(user_id=id).first():
        db.session.delete(profile)
    
    db.session.delete(staff)
    db.session.commit()

    return jsonify({"message": "Staff deleted successfully"}), 200


#assign staff to trek
@admin_bp.route("/treks/<int:trek_id>/assign_staff", methods=["PUT"])
@admin_required
def assign_staff(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404
    
    data = request.get_json()
    staff = User.query.filter_by(id=data.get("staff_id"), role="Trek Staff").first()
    if not staff:
        return jsonify({"message": "Staff not found"}), 404
    
    trek.assigned_staff_id = staff.id
    db.session.commit()
    return jsonify({"message": "Staff assigned to trek successfully"}), 200


#view users
@admin_bp.route("/users", methods=["GET"])
@admin_required
def get_users():
    users = User.query.filter_by(role="Trekker").all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "status": user.status
        })
    return jsonify({"users": result}), 200

#blacklist/activate user
@admin_bp.route("/users/<int:id>/status", methods=["PUT"])
@admin_required
def update_user_status(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    user.status = data.get("status")
    db.session.commit()
    return jsonify({"message": "User status updated successfully"}), 200


@admin_bp.route("/search", methods=["GET"])
@admin_required
def search():
    query = request.args.get("q", "")
    users = User.query.filter(User.name.ilike(f"%{query}%")).all()
    treks = Trek.query.filter(Trek.trek_name.ilike(f"%{query}%")).all()

    return jsonify({
        "users": [{"id": u.id, "name": u.name, "email": u.email} for u in users],
        "treks": [{"id": t.id, "trek_name": t.trek_name, "location": t.location} for t in treks]
    })


#view all bookings
@admin_bp.route("/bookings", methods=["GET"])
@admin_required
def get_bookings():
    bookings = Booking.query.all()
    result = []
    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "user": booking.user.name,
            "trek": booking.trek.trek_name,
            "booking_status": booking.booking_status,
            "payment_status": booking.payment_status,
        })
    return jsonify({"bookings": result}), 200