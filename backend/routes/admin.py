from flask import Blueprint, jsonify
from utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    return jsonify({
        "message": "Welcome Admin Dashboard"
    })