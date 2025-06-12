from app import app, db, User, DailyGoal, Milestone
from config import Config
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if we need to create initial data
        if not User.query.first():
            print("Creating initial test user...")
            test_user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password_hash=generate_password_hash("password123"),
                date_of_birth=datetime(1990, 1, 1),
                country="US",
                language="english",
                user_type="individual",
                recovery_goals=["Stay sober", "Improve health"],
                created_at=datetime.utcnow(),
                sobriety_start_date=datetime.utcnow()
            )
            db.session.add(test_user)
            
            # Create some default goals
            goals = [
                DailyGoal(
                    user=test_user,
                    title="Morning Meditation",
                    category="Wellness",
                    description="Start each day with 10 minutes of meditation",
                    status="pending"
                ),
                DailyGoal(
                    user=test_user,
                    title="Exercise",
                    category="Physical Health",
                    description="30 minutes of physical activity",
                    status="pending"
                )
            ]
            db.session.add_all(goals)
            
            # Create some milestones
            milestones = [
                Milestone(
                    user=test_user,
                    title="First Week Complete",
                    description="Successfully completed first week of recovery",
                    target_date=datetime.utcnow().date() + timedelta(days=7),
                    status="pending"
                ),
                Milestone(
                    user=test_user,
                    title="One Month Milestone",
                    description="Reach one month of sobriety",
                    target_date=datetime.utcnow().date() + timedelta(days=30),
                    status="pending"
                )
            ]
            db.session.add_all(milestones)
            
            # Commit all changes
            db.session.commit()
            print("Initial test user created successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 