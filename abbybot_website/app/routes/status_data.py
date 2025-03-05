from flask import Blueprint
from ..utilities.db_connections import execute_query
import mysql.connector

status_data_bp = Blueprint('status_data', __name__)

@status_data_bp.route('/status_data')
def status_data():
    try:

        bot_info_list = execute_query("api", "SELECT bot_name, version, status, last_updated FROM bot_info;")
        bot_name = bot_info_list[0]['bot_name'] if bot_info_list and bot_info_list[0]['bot_name'] is not None else "no data available"
        version = bot_info_list[0]['version'] if bot_info_list and bot_info_list[0]['version'] is not None else "no data available"
        status = bot_info_list[0]['status'] if bot_info_list and bot_info_list[0]['status'] is not None else "no data available"
        last_updated = bot_info_list[0]['last_updated'] if bot_info_list and bot_info_list[0]['last_updated'] is not None else "no data available"

        server_list = execute_query("discord", "SELECT COUNT(guild_id) AS counter FROM server_settings;")
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"

        return {
            "bot_name": bot_name,
            "version": version,
            "status": status,
            "last_updated": last_updated,
            "server_count": server_count
        }
    
    except mysql.connector.Error as err:
        return {"error": f"Database connection failed: {err}"}, 500