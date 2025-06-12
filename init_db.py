from app import app, db, User, DailyGoal, Milestone
from config import Config
import os
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Check if we need to load initial data
        if not User.query.first():
            print("Loading initial data...")
            
            # Create a test user
            test_user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password_hash=User.generate_password_hash("password123"),
                date_of_birth=datetime.now().date() - timedelta(days=365*25),
                country="kenya",
                language="english",
                user_type="individual",
                recovery_goals='["Learn coping strategies", "Track progress"]',
                created_at=datetime.utcnow(),
                sobriety_start_date=datetime.utcnow().date()
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
            print("Initial data loaded successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 