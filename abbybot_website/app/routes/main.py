from flask import Flask, Blueprint, render_template, abort
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
        server_list = execute_query("discord", "SELECT FORMAT(counter, 0) AS counter, FORMAT(full_members, 0) AS full_members, FORMAT(total_xp, 0) AS total_xp FROM (SELECT COUNT(guild_id) AS counter, SUM(member_count) AS full_members FROM server_settings) AS ss, (SELECT SUM(xp_total) AS total_xp FROM user_profile) AS up;")
        
        # Get the data or assign 0 if there are no results
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"
        total_members = server_list[0]['full_members'] if server_list and server_list[0]['full_members'] is not None else "no data available"
        total_xp = server_list[0]['total_xp'] if server_list and server_list[0]['total_xp'] is not None else "no data available"

        return render_template('index.html', server_count=server_count, total_members=total_members, total_xp=total_xp)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        error_message = "We are currently unable to load the AbbyBot data. Please try again later."
        return render_template('index.html', error_message=error_message)


@main_bp.route('/status_data')
def status_data():
    try:
        # Use 'Wishlist' Database
        bot_info_list = execute_query("api", "SELECT bot_name, version, status, last_updated FROM bot_info;")
        bot_name = bot_info_list[0]['bot_name'] if bot_info_list and bot_info_list[0]['bot_name'] is not None else "no data available"
        version = bot_info_list[0]['version'] if bot_info_list and bot_info_list[0]['version'] is not None else "no data available"
        status = bot_info_list[0]['status'] if bot_info_list and bot_info_list[0]['status'] is not None else "no data available"
        last_updated = bot_info_list[0]['last_updated'] if bot_info_list and bot_info_list[0]['last_updated'] is not None else "no data available"

        # Use 'Rei' Database
        server_list = execute_query("discord", "SELECT COUNT(guild_id) AS counter FROM server_settings;")
        server_count = server_list[0]['counter'] if server_list and server_list[0]['counter'] is not None else "no data available"

        # Return JSON
        return {
            "bot_name": bot_name,
            "version": version,
            "status": status,
            "last_updated": last_updated,
            "server_count": server_count
        }
    
    except mysql.connector.Error as err:
        return {"error": f"Database connection failed: {err}"}, 500


@main_bp.route('/status')
def bot_status():
    try:
        response = execute_query("wishlist", "SELECT 1")
        if response:
            return render_template('bot-status.html')
        else:
            raise mysql.connector.Error("Failed to ping database")
    except mysql.connector.Error as err:
        error_message = f"At this time we are unable to verify the current status of AbbyBot. Please come back later."
        return render_template('bot-status.html', error_message=error_message)


# News list
@main_bp.route('/abbybot-news')
def news_list():
    query = """
    SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at, news.slug
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    ORDER BY news.created_at DESC
    """
    news_items = execute_query("api", query)
    return render_template('news_list.html', news=news_items)


# News detail 
@main_bp.route('/abbybot-news/<string:slug>')
def news_detail(slug):
    query = """
    SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    WHERE news.slug = %s
    """
    news_item = execute_query("api", query, (slug,), fetchall=False)
    
    if not news_item:
        abort(404)  # If no news found, return 404
    return render_template('news_detail.html', news=news_item)


@main_bp.route('/socials')
def socials():
 return render_template('socials.html')

@main_bp.route('/user-responsibilities')
def user_responsibilities():
 return render_template('user_responsibilities.html')

@main_bp.route('/bot-policies')
def bot_policies():
 return render_template('bot_policies.html')

# commands endpoint

@main_bp.route('/commands')
def commands_site():
    try:
        # Fetch all categories and commands
        categories_query = """
            SELECT hc.id AS category_id, hc.category_name, h.command_code, h.command_description, h.usage
            FROM help_categories hc
            LEFT JOIN help h ON hc.id = h.category_id
            WHERE h.language_id = 1
            ORDER BY hc.id, h.command_code
        """
        results = execute_query("discord", categories_query)

        if not results:
            raise ValueError("No command data available")

        # Organize commands by category
        command_categories = {}
        for row in results:
            category_id = row['category_id']
            if category_id not in command_categories:
                command_categories[category_id] = {
                    'category_name': row['category_name'],
                    'commands': []
                }
            command_categories[category_id]['commands'].append({
                'command_code': row['command_code'],
                'command_description': row['command_description'],
                'usage': row['usage']
            })

        # Convert to list for easier template rendering
        command_categories = list(command_categories.values())

        return render_template('commands.html', command_categories=command_categories)

    except (mysql.connector.Error, ValueError) as err:
        print(f"Error: {err}")
        error_message = "We are currently unable to load the AbbyBot commands. Please try again later."
        return render_template('commands.html', error_message=error_message)


app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True)
