from flask import Blueprint, render_template


error_handlers_bp = Blueprint('error_handlers', __name__)

@error_handlers_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message="Sorry, the page you are looking for does not exist.", error_code=404), 404

@error_handlers_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', message="An unexpected error occurred. Please try again later.", error_code=500), 500

@error_handlers_bp.app_errorhandler(Exception)
def handle_generic_error(error):
    # Display the error message if available, or a generic message
    return render_template('error.html', message=str(error) if error else "An unexpected error occurred.", error_code=500), 500
