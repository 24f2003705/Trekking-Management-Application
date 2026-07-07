from flask import Blueprint, jsonify
from utils.decorators import staff_required

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/dashboard")
@staff_required
def dashboard():
    return jsonify({
        "message": "Welcome Staff Dashboard"
    })