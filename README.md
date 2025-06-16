# Flask Personal Finance Tracker

A multi-user personal finance web application built with Flask. Users can register, log in, add incomes and expenses, and see a dashboard with summaries and transaction history.

## Features

- User registration and authentication
- Dashboard with total income, total expenses, and balance
- Add, edit, and delete transactions (income or expense)
- User-specific data privacy
- Flash messages for user feedback
- Responsive design using Bootstrap 5
- SQLite database for local development

## Technologies Used

- Python 3.x
- Flask
- Flask-Login
- SQLAlchemy
- Bootstrap 5
- SQLite

## Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/flask-personal-finance-tracker.git
   cd flask-personal-finance-tracker


Create and activate a virtual environment:

python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

### Install dependencies:


pip install -r requirements.txt

### Initialize the database:

from app import db
db.create_all()
Run the Flask app:


flask run
Open your browser and go to: http://127.0.0.1:5000

### Contribution
Feel free to fork this repo, improve the app, and submit pull requests.

### License
This project is licensed under the MIT License.

**Created by Mauricio Narváez.**
