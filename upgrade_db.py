from app import app, db
from models import User
from sqlalchemy import text

def upgrade_database():
    with app.app_context():
        # Alter the 'password' column to have a maximum length of 255 characters
        with db.engine.connect() as connection:
            connection.execute(text('ALTER TABLE user MODIFY password VARCHAR(255);'))
            print("Password column length updated to 255 characters.")
        
        # Add the 'balance' column to the 'user' table if it does not exist
        with db.engine.connect() as connection:
            try:
                connection.execute(text('ALTER TABLE user ADD COLUMN balance FLOAT DEFAULT 0.0;'))
                print("Balance column added to the user table.")
            except Exception as e:
                print(f"Error adding balance column: {e}")
        
        # Create all tables (if not already created)
        db.create_all()
        print("Database schema upgraded successfully.")

if __name__ == '__main__':
    upgrade_database()
