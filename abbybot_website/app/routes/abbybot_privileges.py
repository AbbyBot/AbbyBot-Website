from flask import Blueprint, render_template
import mysql.connector
from ..utilities.db_connections import execute_query

abbybot_privileges_bp = Blueprint('abbybot_privileges', __name__)

@abbybot_privileges_bp.route('/abbybot-privileges')
def abbybot_privileges():
    try:
        # Make Query
        server_list = execute_query("discord", "SELECT privilege_name, value, rol_meaning, how_to_get, xp_multiplier, exclusive_access FROM privileges;")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")

    return render_template('abbybot-privileges.html', privileges=server_list)
