from flask import Blueprint, render_template
import mysql.connector
from ..utilities.db_connections import execute_query


commands_bp = Blueprint('commands', __name__)

@commands_bp.route('/commands')
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