from flask import Flask, Blueprint, render_template
import mysql.connector
from dotenv import load_dotenv
from ..utilities.db_connections import execute_query
from flask import Flask, flash, redirect, url_for, render_template, request, abort
import re



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

@main_bp.route('/abbybot-privileges')
def abbybot_privileges():
    try:
        # Make Query
        server_list = execute_query("rei", "SELECT privilege_name, value, rol_meaning, how_to_get, xp_multiplier, exclusive_access FROM privileges;")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")

    return render_template('abbybot-privileges.html', privileges=server_list)


# Email regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
DISCORD_REGEX = r'^[\w.]{2,32}$'  # New format without hashtags, allows letters, numbers, underscores, and periods.

@main_bp.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        # Get form data with .get() to avoid KeyErrors
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        discord_username = request.form.get('discord_username', '').strip()
        reason = request.form.get('reason', '').strip()
        how_learned = request.form.get('how_learned', '').strip()
        terms_accepted = request.form.get('terms', None)

        # Create an errors dictionary to pass to the template
        errors = {}

        # Validate required fields
        if not name:
            errors['name'] = "Name is required."

        if not email:
            errors['email'] = "Email is required."
        elif not re.match(EMAIL_REGEX, email):
            errors['email'] = "Invalid email format."

        # Validate Discord username if provided
        if discord_username and not re.match(DISCORD_REGEX, discord_username):
            errors['discord_username'] = "Invalid Discord username format! Only letters, numbers, underscores, and periods are allowed."

        # Validate checkbox
        if not terms_accepted:
            errors['terms'] = "You must accept the terms and conditions."

        # Check if there are any errors
        if errors:
            flash("Please correct the errors in the form.", 'danger')
            return render_template('wishlist.html', name=name, email=email, discord_username=discord_username, reason=reason, how_learned=how_learned, errors=errors, terms_accepted=terms_accepted)

        try:
            # Insert the data into the wishlist database
            execute_query("asuka", """
                INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, discord_username, reason, how_learned), fetchall=False, commit=True)
            
            flash("Your wishlist submission has been received successfully!", 'success')
            return redirect(url_for('main.index', modal='show'))

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", 'danger')
            print(f"Database Error: {err}")

        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')
            print(f"Unexpected Error: {e}")

    return render_template('wishlist.html', errors={}) 


# News views

@main_bp.route('/abbybot-news')
def news_list():
    query = """
    SELECT news.id, news.title, news.description, news.content, news.image_url, categories.name AS category, news.created_at
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    ORDER BY news.created_at DESC
    """
    news_items = execute_query("asuka", query)
    return render_template('news_list.html', news=news_items)

# News detail
@main_bp.route('/abbybot-news/<int:news_id>')
def news_detail(news_id):
    
    query = """
    SELECT news.id, news.title, news.content, news.image_url, categories.name AS category, news.created_at
    FROM news
    LEFT JOIN categories ON news.category_id = categories.id
    WHERE news.id = %s
    """
    news_item = execute_query("asuka", query, (news_id,), fetchall=False)
    
    if not news_item:
        abort(404)  # If no new, return 404
    return render_template('news_detail.html', news=news_item)

@main_bp.route('/wip')
def wip():
 return render_template('wip.html')

# Error handlers

@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message="Sorry, the page you are looking for does not exist."), 404

@main_bp.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', message="An unexpected error occurred. Please try again later."), 500

@main_bp.app_errorhandler(Exception)
def handle_generic_error(error):
    # Display the error message if available, or a generic message
    return render_template('error.html', message=str(error) if error else "An unexpected error occurred."), 500


app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True)
