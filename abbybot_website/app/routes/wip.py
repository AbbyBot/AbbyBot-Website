from flask import Blueprint, render_template

wip_bp = Blueprint('wip', __name__)

@wip_bp.route('/wip')
def wip():
 return render_template('wip.html')