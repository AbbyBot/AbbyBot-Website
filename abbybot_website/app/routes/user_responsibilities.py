from flask import Blueprint, render_template

user_responsibilities_bp = Blueprint('user_responsibilities', __name__)

@user_responsibilities_bp.route('/user-responsibilities')
def user_responsibilities():
 return render_template('user_responsibilities.html')
