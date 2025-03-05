from flask import Blueprint, render_template, session
import mysql.connector
from ..utilities.db_connections import execute_query

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        server_list = execute_query("discord", "SELECT FORMAT(counter, 0) AS counter, FORMAT(full_members, 0) AS full_members, FORMAT(total_xp, 0) AS total_xp FROM (SELECT COUNT(guild_id) AS counter, SUM(member_count) AS full_members FROM server_settings) AS ss, (SELECT SUM(xp_total) AS total_xp FROM user_profile) AS up;")
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"
        total_members = server_list[0]['full_members'] if server_list and server_list[0]['full_members'] is not None else "no data available"
        total_xp = server_list[0]['total_xp'] if server_list and server_list[0]['total_xp'] is not None else "no data available"
        return render_template('index.html', server_count=server_count, total_members=total_members, total_xp=total_xp)

    except mysql.connector.Error as err:
        error_message = "We are currently unable to load the AbbyBot data. Please try again later."
        return render_template('index.html', error_message=error_message)

@main_bp.route('/clear-flash-messages', methods=['POST'])
def clear_flash_messages():
    session.pop('_flashes', None)
    return '', 204