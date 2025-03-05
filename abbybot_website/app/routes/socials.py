from flask import Blueprint, render_template

socials_bp = Blueprint('socials', __name__)

@socials_bp.route('/socials')
def socials():
 return render_template('socials.html')