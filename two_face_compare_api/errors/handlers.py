from flask import Blueprint, render_template, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return jsonify({"is_success": False, "message": "This route is not found"}), 404



@errors.app_errorhandler(500)
def error_500(error):
    return jsonify({"is_success": False, "message": "Internal Server Error"}), 500