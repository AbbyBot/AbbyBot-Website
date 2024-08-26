import mysql.connector
from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Load dotenv variables
load_dotenv()

# Start Flask
app = Flask(__name__)

# DB settings
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route('/')
def home():

     # database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Queries

    cursor.execute("select count(guild_id) as counter from abbybot.server_settings; ")
    server_list = cursor.fetchall()

    # Close db
    cursor.close()
    conn.close()


    return render_template('home.html', server_list=server_list)

@app.route('/overview')
def overview():
    # database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Queries

    cursor.execute("SELECT * FROM abbybot.help WHERE language_id = 1; ")
    en_commands_list = cursor.fetchall()

    # Close db
    cursor.close()
    conn.close()

    #get help commands english
    return render_template('overview.html', help_commands=en_commands_list)

if __name__ == '__main__':
    app.run(debug=True)



    # cursor.execute("SELECT COUNT(guild_id) AS total_guilds FROM abbybot.server_settings;")
    # all_servers = cursor.fetchall()