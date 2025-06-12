from app import app, db
from config import Config
import os

def init_render_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_render_db() 