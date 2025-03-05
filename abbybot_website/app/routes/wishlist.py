from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
import re
import requests
from flask_mail import Message
from ..utilities.db_connections import execute_query
from app import mail  # Import the mail instance
import mysql.connector  # Import mysql.connector to handle MySQL errors

wishlist_bp = Blueprint('wishlist', __name__)

# Email regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
DISCORD_REGEX = r'^[\w.]{2,32}$'  # New format without hashtags, allows letters, numbers, underscores, and periods.

@wishlist_bp.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    turnstile_site_key = os.getenv('TURNSTILE_SITE_KEY')
    if request.method == 'POST':
        # Get form data with .get() to avoid KeyErrors
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        discord_username = request.form.get('discord_username', '').strip()
        reason = request.form.get('reason', '').strip()
        how_learned = request.form.get('how_learned', '').strip()
        terms_accepted = request.form.get('terms', None)
        turnstile_response = request.form.get('cf-turnstile-response')  # Get Turnstile response

        # Create an errors dictionary to pass to the template
        errors = {}

        # Validate Turnstile response
        turnstile_secret = os.getenv('TURNSTILE_SECRET_KEY')
        turnstile_verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        turnstile_data = {
            'secret': turnstile_secret,
            'response': turnstile_response
        }
        turnstile_verification = requests.post(turnstile_verify_url, data=turnstile_data).json()
        if not turnstile_verification.get('success'):
            errors['turnstile'] = "Turnstile verification failed. Please try again."

        # Validate required fields
        if not name:
            errors['name'] = "Name is required."

        if not email:
            errors['email'] = "Email is required."
        elif not re.match(EMAIL_REGEX, email):
            errors['email'] = "Invalid email format."

        if not discord_username:
            errors['discord_username'] = "Discord Username is required."
        elif not re.match(DISCORD_REGEX, discord_username):
            errors['discord_username'] = "Invalid Discord username format! Only letters, numbers, underscores, and periods are allowed."

        # Validate checkbox
        if not terms_accepted:
            errors['terms'] = "You must accept the terms and conditions."

        # Check if there are any errors
        if errors:
            flash("Please correct the errors in the form.", 'danger')
            return render_template('wishlist.html', name=name, email=email, discord_username=discord_username, reason=reason, how_learned=how_learned, errors=errors, terms_accepted=terms_accepted, turnstile_site_key=turnstile_site_key)

        try:
            # Check if the user already exists in the wishlist database
            existing_users = execute_query("wishlist", """
                SELECT * FROM wishlist WHERE discord_username = %s
            """, (discord_username,))

            if existing_users:
                flash("This user is already registered in the wishlist.", 'danger')
                return render_template('wishlist.html', name=name, email=email, discord_username=discord_username, reason=reason, how_learned=how_learned, errors=errors, terms_accepted=terms_accepted, turnstile_site_key=turnstile_site_key)

            # Insert the data into the wishlist database
            execute_query("wishlist", """
                INSERT INTO wishlist (name, email, discord_username, reason, how_learned)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, discord_username, reason, how_learned), fetchall=False, commit=True)
            
            # Send confirmation email
            msg = Message(
                subject="Thank you for adding AbbyBot to your wishlist!",
                recipients=[email]
            )
            msg.html = render_template('emails/wishlist_added.html', username=discord_username)
            mail.send(msg)
            
            flash("Your wishlist submission has been received successfully!", 'success')
            return redirect(url_for('main.index', modal='show'))

        except mysql.connector.Error as err:
            flash(f"Database Error: {err}", 'danger')
            print(f"Database Error: {err}")

        except Exception as e:
            flash(f"Unexpected Error: {e}", 'danger')
            print(f"Unexpected Error: {e}")

    return render_template('wishlist.html', errors={}, turnstile_site_key=turnstile_site_key)
