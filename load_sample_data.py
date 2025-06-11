from app import app, db, SupportGroup, Professional, User, generate_object_id
from datetime import datetime
from werkzeug.security import generate_password_hash

def load_sample_data():
    with app.app_context():
        # Create sample support groups
        groups = [
            {
                'name': 'Downtown Recovery Circle',
                'description': 'A welcoming community for individuals in early recovery. We meet weekly to share experiences and support each other.',
                'group_type': 'AA',
                'addiction_focus': 'alcohol',
                'meeting_type': 'hybrid',
                'city': 'New York',
                'state': 'NY',
                'country': 'USA',
                'address': '123 Main St, New York, NY',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'meeting_days': '["Monday", "Wednesday", "Friday"]',
                'meeting_time': '19:00',
                'timezone': 'America/New_York',
                'language': 'english',
                'facilitator_name': 'John Smith',
                'contact_email': 'john@recoverycircle.org'
            },
            {
                'name': 'Online Recovery Network',
                'description': 'Global online support group for people in recovery from various addictions.',
                'group_type': 'SMART',
                'addiction_focus': 'general',
                'meeting_type': 'online',
                'meeting_days': '["Daily"]',
                'meeting_time': '12:00',
                'timezone': 'UTC',
                'language': 'english',
                'facilitator_name': 'Sarah Johnson',
                'contact_email': 'sarah@onlinerecovery.org'
            }
        ]

        for group_data in groups:
            existing = SupportGroup.query.filter_by(name=group_data['name']).first()
            if not existing:
                group = SupportGroup(**group_data)
                db.session.add(group)

        # Create sample professionals
        professionals = [
            {
                'name': 'Dr. Michael Chen',
                'role': 'therapist',
                'specialization': 'Addiction Recovery',
                'bio': 'Licensed therapist with 15 years of experience in addiction recovery.',
                'email': 'mchen@therapy.com',
                'phone': '+1-555-0123',
                'availability': 'Mon-Fri 9AM-5PM',
                'rating': 4.8,
                'language': 'english',
                'gender': 'male',
                'is_verified': True
            },
            {
                'name': 'Dr. Lisa Rodriguez',
                'role': 'doctor',
                'specialization': 'Addiction Medicine',
                'bio': 'Board-certified addiction medicine specialist with 10 years of experience.',
                'email': 'lrodriguez@medicine.com',
                'phone': '+1-555-0124',
                'availability': 'Mon-Thu 10AM-6PM',
                'rating': 4.9,
                'language': 'english,spanish',
                'gender': 'female',
                'is_verified': True
            }
        ]

        for prof_data in professionals:
            existing = Professional.query.filter_by(email=prof_data['email']).first()
            if not existing:
                professional = Professional(**prof_data)
                db.session.add(professional)

        # Create a sample user for testing
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                password_hash=generate_password_hash('test123'),
                country='USA',
                language='english',
                user_type='individual',
                recovery_goals='["Maintain sobriety", "Build healthy habits"]',
                sobriety_start_date=datetime.now().date()
            )
            db.session.add(test_user)

        try:
            db.session.commit()
            print("Sample data loaded successfully!")
        except Exception as e:
            print(f"Error loading sample data: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    load_sample_data() 