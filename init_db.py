from app import app, db, User, DailyGoal, Milestone, Professional, EducationalResource, ProfessionalPatient, ProfessionalSession, ProfessionalResource
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
        
        # Create default professionals
        professionals = [
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.johnson@aurarecovery.com',
                'specialization': 'Addiction Counselor',
                'password': 'Aurarecovery123!'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'michael.chen@aurarecovery.com',
                'specialization': 'Clinical Psychologist',
                'password': 'Aurarecovery123!'
            }
        ]

        for prof_data in professionals:
            existing = Professional.query.filter_by(email=prof_data['email']).first()
            if not existing:
                professional = Professional(
                    first_name=prof_data['first_name'],
                    last_name=prof_data['last_name'],
                    email=prof_data['email'],
                    specialization=prof_data['specialization']
                )
                professional.set_password(prof_data['password'])
                db.session.add(professional)
        
        # Create a test patient
        test_patient = User(
            first_name='Test',
            last_name='Patient',
            email='test.patient@example.com',
            password_hash=generate_password_hash('test123'),
            date_of_birth=datetime(1990, 1, 1),
            country='US',
            language='english',
            user_type='individual',
            recovery_goals='["Stay sober", "Improve health"]',
            sobriety_start_date=datetime.utcnow()
        )
        db.session.add(test_patient)

        # Commit the changes
        db.session.commit()
        print("Default professionals and test patient created successfully!")

        # Create some test sessions
        professional = Professional.query.filter_by(email='sarah.johnson@aurarecovery.com').first()
        patient = User.query.filter_by(email='test.patient@example.com').first()

        if professional and patient:
            # Create patient assignment
            assignment = ProfessionalPatient(
                professional_id=professional.id,
                patient_id=patient.id,
                status='active'
            )
            db.session.add(assignment)

            # Create some sessions
            sessions = [
                {
                    'session_date': datetime.now() + timedelta(days=1),
                    'session_type': 'video',
                    'status': 'scheduled'
                },
                {
                    'session_date': datetime.now() + timedelta(days=3),
                    'session_type': 'audio',
                    'status': 'scheduled'
                }
            ]

            for session_data in sessions:
                session = ProfessionalSession(
                    professional_id=professional.id,
                    patient_id=patient.id,
                    session_date=session_data['session_date'],
                    session_type=session_data['session_type'],
                    status=session_data['status']
                )
                db.session.add(session)

            # Create some resources
            resources = [
                {
                    'title': 'Recovery Workbook',
                    'description': 'A comprehensive workbook for addiction recovery',
                    'resource_type': 'document',
                    'file_path': '/resources/workbook.pdf'
                },
                {
                    'title': 'Meditation Guide',
                    'description': 'Guided meditation exercises for stress management',
                    'resource_type': 'audio',
                    'file_path': '/resources/meditation.mp3'
                }
            ]

            for resource_data in resources:
                resource = ProfessionalResource(
                    professional_id=professional.id,
                    title=resource_data['title'],
                    description=resource_data['description'],
                    resource_type=resource_data['resource_type'],
                    file_path=resource_data['file_path']
                )
                db.session.add(resource)

            db.session.commit()
            print("Test data created successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 