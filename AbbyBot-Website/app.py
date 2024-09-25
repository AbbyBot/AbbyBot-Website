import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# Load dotenv variables
load_dotenv()

# Start Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Consolidated DB connection function
def get_db_connection(db_type="main"):
    if db_type == "main":
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    elif db_type == "wishlist":
        return mysql.connector.connect(
            host=os.getenv("WISHLIST_DB_HOST"),
            user=os.getenv("WISHLIST_DB_USER"),
            password=os.getenv("WISHLIST_DB_PASSWORD"),
            database=os.getenv("WISHLIST_DB_NAME")
        )

# Context Manager for both DBs
@contextmanager
def db_connection(db_type="main"):
    conn = get_db_connection(db_type)
    try:
        yield conn
    finally:
        conn.close()

# Helper function to execute queries
def execute_query(db_type, query, params=None, fetchall=True, commit=False):
    with db_connection(db_type) as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
        if fetchall:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()
    return result


# Home route
@app.route('/')
def home():
    try:
        server_list = execute_query("main", "SELECT COUNT(guild_id) as counter FROM abbybot.server_settings;")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")
    
    return render_template('home.html', server_list=server_list)

# Overview route
@app.route('/overview')
def overview():
    return render_template('overview.html')

# About her route
@app.route('/about-her')
def abouther():
    return render_template('about-her.html')

# Contribute route
@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

# Commands list route
@app.route('/commands-list')
def commands_list():
    try:
        en_commands_list = execute_query("main", "SELECT * FROM abbybot.help WHERE language_id = 1;")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")
    
    return render_template('commands-list.html', commands=en_commands_list)

# Wishlist route - handles form submissions
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        # Get form data
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        discord_username = request.form.get('discord_username', '').strip()
        reason = request.form.get('reason', '').strip()
        how_learned = request.form.get('how_learned', '').strip()

        # Validate required fields
        if not name or not email:
            flash("Name and Email are required!", 'danger')
            return redirect(url_for('wishlist'))

        try:
            # Insert the data into the wishlist database
            execute_query("wishlist", """
                INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, discord_username, reason, how_learned), fetchall=False, commit=True)
            
            flash("Your wishlist submission has been received successfully!", 'success')
            return redirect(url_for('home'))

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", 'danger')
            print(f"Database Error: {err}")

        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')
            print(f"Unexpected Error: {e}")

    return render_template('wishlist.html')



# Contact us route
@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        # Get form data
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()

        # Validate required fields
        if not name or not email or not message:
            flash("Name, Email, and Message are required!", 'danger')
            return redirect(url_for('contact_us'))

        try:
            # Insert data into the messages table
            execute_query("wishlist", """
                INSERT INTO messages (name, email, message)
                VALUES (%s, %s, %s)
            """, (name, email, message), fetchall=False, commit=True)

            flash("Thank you for contacting us! We will get back to you soon.", "success")
            return redirect(url_for('home'))

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", 'danger')
            print(f"Database Error: {err}")
        
        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')
            print(f"Unexpected Error: {e}")

    return render_template('contact-us.html')



@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/wip')
def wip():
    return render_template('work-in-progress.html')

# Terms and conditions route
@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('terms-and-conditions.html')

# Hall of fame route
@app.route('/hall-of-fame')
def hall_of_fame():
    try:
        # Fetch hall of fame data
        hall_of_fame_data = execute_query("wishlist", """
            SELECT id, nickname AS name, username as username, user_image AS image_url, custom_nickname 
            FROM contributors
        """)
        users_names_list = execute_query("main", """
            SELECT user_username as bro_username 
            FROM dashboard 
            WHERE guild_id = 1176976421147648061 AND is_bot = 0
        """)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")

    return render_template('hall_of_fame.html', hall_of_fame_data=hall_of_fame_data, users_names_list=users_names_list)


@app.route('/hall-of-fame/contributor/<string:username>')
def person_detail(username):
    try:
        # Inquire for contributor information
        person = execute_query("wishlist", """
            SELECT id, nickname AS name, username, user_image AS image_url, comentary, custom_nickname 
            FROM contributors WHERE username = %s
        """, (username,), fetchall=False)
        
        # If the contributor exists, search for their contributions
        if person:
            # Inquiry for related contributions
            contributions = execute_query("wishlist", """
                SELECT contribution 
                FROM contributions WHERE contributor_id = %s
            """, (person['id'],))
        else:
            return "Person not found", 404
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")
    
    if person:
        return render_template('person_detail.html', person=person, contributions=contributions)
    else:
        return "Person not found", 404


# Error handling route 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="The page you are looking for does not exist."), 404

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
