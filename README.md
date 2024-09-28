
# AbbyBot-Website

Welcome to the AbbyBot-Website project! This project is a Flask-based web application that serves as the frontend for AbbyBot, a multipurpose bot for Discord. The webpage provides information about AbbyBot, its features, and allows users to interact with certain aspects of the bot, like the wishlist system.

## Table of Contents

- [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)
- [Development](#development)
- [License](#license)

## Installation

### Dependencies

To set up this project locally, you'll need to install the required dependencies in a virtual environment. Here's how you can do it:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AbbyBot/AbbyBot-Website.git
   ```

2. **Create a virtual environment:**

   - On Windows:

   ```bash
   python -m venv venv
   ```

   - On Linux/MacOS:

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Linux/MacOS:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

You need to create a `.env` file in the root directory of the project to store your environment variables. This file should include both the main database and the wishlist database credentials.

Here's an example of what your `.env` file should look like:

```env
# AbbyBot 'Rei' Database (for getting Discord Bot data like messages, members, etc)
REI_DB_HOST=your_main_db_host
REI_DB_USER=your_main_db_user
REI_DB_PASSWORD=your_main_db_password
REI_DB_NAME=your_main_db_name

# AbbyBot 'Asuka' Database (for forms, contact messages, etc)
ASUKA_DB_HOST=your_wishlist_db_host
ASUKA_DB_USER=your_wishlist_db_user
ASUKA_DB_PASSWORD=your_wishlist_db_password
ASUKA_DB_NAME=your_wishlist_db_name

# Flask secret key
SECRET_KEY=generate_a_secret_key
```

Ensure you replace the placeholders (`your_main_db_host`, `your_main_db_user`, etc.) with your actual database credentials.

**We would like to clarify that we use the code names 'Rei' and 'Asuka' merely for reasons of comfort and ease of remembering, I hope it does not cause you any discomfort.**


- **Save the file:** You must save the .env file in `AbbyBot-Website` directory, between `app.py`



```plaintext
Repository Root
│
├── AbbyBot-Website/
│   ├── app.py
│   └── .env
│
└── README.md
```


## Technologies Used

The AbbyBot webpage project utilizes the following technologies:

- **[Flask](https://flask.palletsprojects.com/):** A lightweight WSGI web application framework in Python, used for building the server-side of this project.
- **[Jinja](https://jinja.palletsprojects.com/):** A templating engine for Python, used in Flask to render dynamic web pages.
- **[python-dotenv](https://pypi.org/project/python-dotenv/):** A Python library to load environment variables from a `.env` file, ensuring that sensitive data like database credentials are kept secure.
- **[MySQL](https://www.mysql.com/):** A relational database management system used to store the data for AbbyBot, including the wishlist functionality.
- **[Bulma CSS](https://bulma.io/):** A modern CSS framework based on Flexbox, used for styling the front-end of the web application.

## Development

If you wish to contribute to the development of AbbyBot's webpage, follow these steps:

1. **Fork the repository** and create a new branch for your feature or bugfix.
2. **Set up the development environment** by following the installation instructions above.
3. **Ensure that your `.env` file is properly configured** with the necessary database credentials.
4. **Run the development server:**

   ```bash
   flask run
   ```

   This will start a local development server where you can view your changes.

5. **Make your changes** and ensure that all tests pass.
6. **Submit a pull request** with a detailed explanation of your changes.

## License

This project is under the MIT license along with an extra clause. See the **[`LICENSE`](https://github.com/AbbyBot/AbbyBot-Website/blob/main/LICENSE):** file for more details.

