from flask import Blueprint, jsonify
from utils.decorators import trekker_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/dashboard")
@trekker_required
def dashboard():
    return jsonify({
        "message": "Welcome Trekker Dashboard"
    })