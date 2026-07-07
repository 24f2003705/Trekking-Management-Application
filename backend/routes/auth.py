from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return jsonify({"message": "Authentication route working!"})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not name or not email or not password:
        return jsonify({"message": "All required fields are mandatory."}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered."}), 409
    
    #Hash password
    hashed_password = generate_password_hash(password)

    new_user = User(
        name = name,
        email = email,
        password = hashed_password,
        phone = phone,
        role = "Trekker",
        status = "Active"
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful."}), 201 #create successful

#login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid email or password."}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password."}), 401
    
    if user.status != "Active":
        return jsonify({"message": "User account is not active."}), 403

    # Create access token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful.",
        "access_token": access_token,
        "role": user.role,
        "name": user.name,
        "user_id": user.id
    }), 200