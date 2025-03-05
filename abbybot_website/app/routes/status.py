from flask import Blueprint, render_template

status_bp = Blueprint('status', __name__)

@status_bp.route('/status')
def bot_status():
    return render_template('bot-status.html')