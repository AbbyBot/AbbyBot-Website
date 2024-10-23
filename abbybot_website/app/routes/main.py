from flask import Flask, Blueprint, render_template
import mysql.connector
from dotenv import load_dotenv
from ..utilities.db_connections import execute_query

# Load dotenv variables
load_dotenv()

# Flask instance
app = Flask(__name__)

# Main blueprint
main_bp = Blueprint('main', __name__)

# Blueprint routes
@main_bp.route('/')
def index():
    try:
        # Make Query
        server_list = execute_query("rei", "SELECT FORMAT(counter, 0) AS counter, FORMAT(full_members, 0) AS full_members, FORMAT(total_xp, 0) AS total_xp FROM (SELECT COUNT(guild_id) AS counter, SUM(member_count) AS full_members FROM server_settings) AS ss, (SELECT SUM(xp_total) AS total_xp FROM user_profile) AS up;")
        
        # Get the data or assign 0 if there are no results
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"
        total_members = server_list[0]['full_members'] if server_list and server_list[0]['full_members'] is not None else "no data available"
        total_xp = server_list[0]['total_xp'] if server_list and server_list[0]['total_xp'] is not None else "no data available"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")

    return render_template('index.html', server_count=server_count, total_members=total_members, total_xp=total_xp)


@main_bp.route('/status_data')
def status_data():
    try:
        # Use 'Asuka' Database
        bot_info_list = execute_query("asuka", "SELECT bot_name, version, version_code, status, last_updated FROM bot_info;")
        bot_name = bot_info_list[0]['bot_name'] if bot_info_list and bot_info_list[0]['bot_name'] is not None else "no data available"
        version = bot_info_list[0]['version'] if bot_info_list and bot_info_list[0]['version'] is not None else "no data available"
        version_code = bot_info_list[0]['version_code'] if bot_info_list and bot_info_list[0]['version_code'] is not None else "no data available"
        status = bot_info_list[0]['status'] if bot_info_list and bot_info_list[0]['status'] is not None else "no data available"
        last_updated = bot_info_list[0]['last_updated'] if bot_info_list and bot_info_list[0]['last_updated'] is not None else "no data available"

        # Use 'Rei' Database
        server_list = execute_query("rei", "SELECT COUNT(guild_id) AS counter FROM server_settings;")
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"

        # Return JSON
        return {
            "bot_name": bot_name,
            "version": version,
            "version_code": version_code,
            "status": status,
            "last_updated": last_updated,
            "server_count": server_count
        }
    
    except mysql.connector.Error as err:
        return {"error": f"Database connection failed: {err}"}, 500


@main_bp.route('/status')
def bot_status():
    return render_template('bot-status.html')


app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True)
