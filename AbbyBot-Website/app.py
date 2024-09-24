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

# DB settings
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("WISHLIST_DB_HOST"),
        user=os.getenv("WISHLIST_DB_USER"),
        password=os.getenv("WISHLIST_DB_HOST"),
        database=os.getenv("WISHLIST_DB_NAME")
    )

def get_main_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@contextmanager
def db_connection():
    conn = get_main_db_connection()
    try:
        yield conn
    finally:
        conn.close()

# Home route
@app.route('/')
def home():
    try:
        with db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(guild_id) as counter FROM abbybot.server_settings;")
            server_list = cursor.fetchall()
            cursor.close()
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
        with db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM abbybot.help WHERE language_id = 1;")
            en_commands_list = cursor.fetchall()
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', message="Database connection failed.")
    
    return render_template('commands-list.html', commands=en_commands_list)

# wishlist dba

def get_wishlist_db_connection():
    return mysql.connector.connect(
        host=os.getenv("WISHLIST_DB_HOST"),
        user=os.getenv("WISHLIST_DB_USER"),
        password=os.getenv("WISHLIST_DB_PASSWORD"),
        database=os.getenv("WISHLIST_DB_NAME")
    )

# Wishlist route - handles form submissions
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        discord_username = request.form.get('discord_username')
        reason = request.form.get('reason')
        how_learned = request.form.get('how_learned')

        # Validate required fields
        if not name or not email:
            flash("Name and Email are required!", 'danger')
            return redirect(url_for('wishlist'))

        try:
            # Insert the data into the wishlist database
            with get_wishlist_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, email, discord_username, reason, how_learned))
                conn.commit()
                flash("Your details have been submitted successfully!", 'success')
                return redirect(url_for('thank_you'))

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
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            # (temp) Insert data into the messages table
            conn = get_wishlist_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (name, email, message)
                VALUES (%s, %s, %s)
            """, (name, email, message))
            conn.commit()
            cursor.close()
            conn.close()

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

# Hall of frame route
@app.route('/hall-of-fame')
def hall_of_fame():

    # first query: contributors

    connection = get_wishlist_db_connection()
    cursor = connection.cursor(dictionary=True)
    

    cursor.execute("SELECT id, nickname AS name, username as username, user_image AS image_url, contributions FROM contributors")
    hall_of_fame_data = cursor.fetchall()
    
    cursor.close()
    connection.close()

    # second query: users list names

    connection = get_main_db_connection()
    cursor = connection.cursor(dictionary=True)
    

    cursor.execute("select user_username as bro_username from dashboard where guild_id = 1176976421147648061 and is_bot = 0")
    users_names_list = cursor.fetchall()

    return render_template('hall_of_fame.html', hall_of_fame_data=hall_of_fame_data, users_names_list=users_names_list)


@app.route('/hall-of-fame/contributor/<string:username>')
def person_detail(username):

    connection = get_wishlist_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id, nickname AS name, username, user_image AS image_url, contributions, comentary FROM contributors WHERE username = %s", (username,))
    person = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if person:
        return render_template('person_detail.html', person=person)
    else:
        return "Person not found", 404





# Error handling route 404
@app.errorhandler(404)
def page_not_found(e):
    # Redirect error
    return render_template('error.html', message="The page you are looking for does not exist."), 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
