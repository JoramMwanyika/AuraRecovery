from app import app, db, EducationalResource
import json

def load_educational_resources():
    resources = [
        {
            'title': 'Understanding Addiction',
            'description': 'A comprehensive guide to understanding the science behind addiction and recovery.',
            'resource_type': 'book',
            'addiction_type': 'general',
            'author': 'Dr. Sarah Johnson',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Mindfulness in Recovery',
            'description': 'Learn how mindfulness practices can support your recovery journey.',
            'resource_type': 'course',
            'addiction_type': 'general',
            'duration': '4 weeks',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Coping Strategies Workshop',
            'description': 'Practical workshop on developing healthy coping mechanisms.',
            'resource_type': 'workshop',
            'addiction_type': 'general',
            'duration': '2 hours',
            'difficulty_level': 'intermediate'
        },
        {
            'title': 'Family Support Guide',
            'description': 'A guide for families supporting loved ones in recovery.',
            'resource_type': 'book',
            'addiction_type': 'general',
            'author': 'Family Recovery Network',
            'difficulty_level': 'beginner'
        },
        {
            'title': 'Nutrition and Recovery',
            'description': 'How proper nutrition supports the recovery process.',
            'resource_type': 'article',
            'addiction_type': 'general',
            'difficulty_level': 'beginner'
        },
        {
            'title': 'Sleep and Recovery',
            'description': 'Understanding the importance of sleep in the recovery process.',
            'resource_type': 'article',
            'addiction_type': 'general',
            'difficulty_level': 'beginner'
        },
        {
            'title': 'Exercise and Mental Health',
            'description': 'The role of physical activity in maintaining sobriety.',
            'resource_type': 'article',
            'addiction_type': 'general',
            'difficulty_level': 'beginner'
        },
        {
            'title': 'Relapse Prevention',
            'description': 'Strategies and techniques for preventing relapse.',
            'resource_type': 'course',
            'addiction_type': 'general',
            'duration': '6 weeks',
            'difficulty_level': 'intermediate',
            'featured': True
        },
        {
            'title': 'Building Healthy Relationships',
            'description': 'Guide to developing and maintaining healthy relationships in recovery.',
            'resource_type': 'workshop',
            'addiction_type': 'general',
            'duration': '3 hours',
            'difficulty_level': 'intermediate'
        },
        {
            'title': 'Financial Recovery',
            'description': 'Managing finances and rebuilding financial health during recovery.',
            'resource_type': 'course',
            'addiction_type': 'general',
            'duration': '4 weeks',
            'difficulty_level': 'beginner'
        }
    ]

    with app.app_context():
        for resource_data in resources:
            existing = EducationalResource.query.filter_by(title=resource_data['title']).first()
            if not existing:
                resource = EducationalResource(**resource_data)
                db.session.add(resource)
        
        db.session.commit()
        print("Educational resources loaded successfully!")

if __name__ == '__main__':
    load_educational_resources() 