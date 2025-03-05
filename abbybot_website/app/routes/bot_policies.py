from flask import Blueprint, render_template

bot_policies_bp = Blueprint('bot_policies', __name__)

@bot_policies_bp.route('/bot-policies')
def bot_policies():
 return render_template('bot_policies.html')