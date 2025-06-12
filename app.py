from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from config import Config
from functools import wraps
import json
import uuid
import requests
from urllib.parse import urlencode
from sqlalchemy.orm import joinedload
import click
from flask.cli import with_appcontext
import secrets

# Import AI services
from ai_service import AIService

def generate_object_id():
    """Generate a MongoDB-style 24-character ObjectId"""
    import secrets
    return secrets.token_hex(12)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Zoom/Google Meet Integration Settings
app.config['ZOOM_API_KEY'] = os.environ.get('ZOOM_API_KEY', 'your-zoom-api-key')
app.config['ZOOM_API_SECRET'] = os.environ.get('ZOOM_API_SECRET', 'your-zoom-api-secret')
app.config['GOOGLE_MEET_API_KEY'] = os.environ.get('GOOGLE_MEET_API_KEY', 'your-google-api-key')

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String(100))
    language = db.Column(db.String(50))
    user_type = db.Column(db.String(50))
    recovery_goals = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sobriety_start_date = db.Column(db.Date, default=datetime.utcnow().date())
    
    # Location for support groups
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relationships
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)
    daily_goals = db.relationship('DailyGoal', backref='user', lazy=True)
    milestones = db.relationship('Milestone', backref='user', lazy=True)
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True)
    group_memberships = db.relationship('GroupMembership', backref='user', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)
    ai_chat_sessions = db.relationship('AIChatSession', backref='user', lazy=True)
    risk_assessments = db.relationship('RelapseRiskAssessment', backref='user', lazy=True)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    scheduled_time = db.Column(db.String(20))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    date = db.Column(db.Date, default=datetime.utcnow().date())

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_days = db.Column(db.Integer)
    achieved = db.Column(db.Boolean, default=False)
    achieved_at = db.Column(db.DateTime)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('mood_entry.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIChatSession(db.Model):
    """Store AI chat conversations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    messages = db.relationship('AIChatMessage', backref='session', lazy=True)

class AIChatMessage(db.Model):
    """Store individual AI chat messages"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('ai_chat_session.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, nullable=False)  # True if user message, False if AI response
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # AI-specific fields
    intent = db.Column(db.String(50))  # Detected intent
    confidence = db.Column(db.Float)   # AI confidence score
    crisis_detected = db.Column(db.Boolean, default=False)

class RelapseRiskAssessment(db.Model):
    """Store relapse risk assessments"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high
    risk_probability = db.Column(db.Float, nullable=False)
    risk_factors = db.Column(db.Text)  # JSON array of risk factors
    recommendations = db.Column(db.Text)  # JSON array of recommendations
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EducationalResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)
    addiction_type = db.Column(db.String(100))
    url = db.Column(db.String(500))
    author = db.Column(db.String(200))
    duration = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))
    language = db.Column(db.String(50), default='english')
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SupportGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    group_type = db.Column(db.String(100))  # AA, NA, GA, etc.
    addiction_focus = db.Column(db.String(100))  # alcohol, drugs, gambling, general
    meeting_type = db.Column(db.String(50))  # in-person, online, hybrid
    
    # Location details
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    address = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Meeting details
    meeting_days = db.Column(db.String(200))  # JSON array of days
    meeting_time = db.Column(db.String(50))
    timezone = db.Column(db.String(50))
    language = db.Column(db.String(50), default='english')
    
    # Group settings
    is_private = db.Column(db.Boolean, default=False)
    requires_approval = db.Column(db.Boolean, default=True)
    max_members = db.Column(db.Integer, default=50)
    
    # Contact info
    facilitator_name = db.Column(db.String(200))
    contact_email = db.Column(db.String(200))
    contact_phone = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    memberships = db.relationship('GroupMembership', backref='group', lazy=True)
    sessions = db.relationship('GroupSession', backref='group', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='group', lazy=True)

class GroupMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('support_group.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    role = db.Column(db.String(50), default='member')  # member, moderator, facilitator
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

class GroupSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('support_group.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    session_type = db.Column(db.String(50))  # chat, video, hybrid
    
    # Scheduling
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    timezone = db.Column(db.String(50))
    
    # Video integration
    video_platform = db.Column(db.String(50))  # zoom, google_meet, none
    meeting_url = db.Column(db.String(500))
    meeting_id = db.Column(db.String(200))
    meeting_password = db.Column(db.String(100))
    
    # Session settings
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(100))  # weekly, biweekly, monthly
    max_participants = db.Column(db.Integer, default=20)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    attendees = db.relationship('SessionAttendee', backref='session', lazy=True)

class SessionAttendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('group_session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='registered')  # registered, attended, missed
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('support_group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='text')  # text, image, file
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime)

class SupportContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'doctor' or 'therapist'
    specialty = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    availability = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('support_contact.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contact = db.relationship('SupportContact', backref='appointments')

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'doctor' or 'therapist'
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    availability = db.Column(db.String(100))
    rating = db.Column(db.Float, default=5.0)
    language = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=60)  # in minutes
    type = db.Column(db.String(20))  # 'video', 'audio', 'chat'
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'completed', 'cancelled'
    notes = db.Column(db.Text)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='text')  # 'text', 'voice', 'file'
    file_url = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TreatmentPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    summary = db.Column(db.Text)
    goals = db.Column(db.Text)  # JSON string of goals
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Utility to create default admins
@app.cli.command('create_default_admins')
def create_default_admins():
    admins = [
        {'name': 'Admin One', 'email': 'admin1@example.com'},
        {'name': 'Admin Two', 'email': 'admin2@example.com'},
        {'name': 'Admin Three', 'email': 'admin3@example.com'},
        {'name': 'Admin Four', 'email': 'admin4@example.com'},
    ]
    default_password = 'Admin@1234'
    for adm in admins:
        if not Admin.query.filter_by(email=adm['email']).first():
            admin = Admin(name=adm['name'], email=adm['email'])
            admin.set_password(default_password)
            db.session.add(admin)
    db.session.commit()
    print('Default admins created (or already exist).')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper Functions (keeping existing ones and adding new AI-related ones)
def calculate_sobriety_days(user):
    if user.sobriety_start_date:
        return (datetime.utcnow().date() - user.sobriety_start_date).days + 1
    return 0

def get_user_stats(user):
    sobriety_days = calculate_sobriety_days(user)
    
    week_start = datetime.utcnow().date() - timedelta(days=7)
    goals_completed = DailyGoal.query.filter(
        DailyGoal.user_id == user.id,
        DailyGoal.completed == True,
        DailyGoal.date >= week_start
    ).count()
    
    total_goals = DailyGoal.query.filter(
        DailyGoal.user_id == user.id,
        DailyGoal.date >= week_start
    ).count()
    
    mood_entries = MoodEntry.query.filter(
        MoodEntry.user_id == user.id,
        MoodEntry.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    milestones_achieved = Milestone.query.filter(
        Milestone.user_id == user.id,
        Milestone.achieved == True
    ).count()
    
    return {
        'sobriety_days': sobriety_days,
        'goals_completed': goals_completed,
        'total_goals': max(total_goals, 1),
        'mood_entries': mood_entries,
        'milestones_achieved': milestones_achieved
    }

# ... (keeping all existing helper functions)

# NEW AI-POWERED ROUTES

@app.route('/ai-therapist')
@login_required
def ai_therapist():
    return render_template('ai_therapist.html')

@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat_endpoint():
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = AIService.get_ai_chat_response(message, current_user)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/insights')
@login_required
def ai_insights():
    try:
        risk_analysis = AIService.analyze_relapse_risk(current_user)
        mood_analysis = AIService.analyze_mood_patterns(current_user)
        recommendations = AIService.get_personalized_recommendations(current_user)
        
        return jsonify({
            'risk': risk_analysis,
            'mood': mood_analysis,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai-dashboard')
@login_required
def ai_dashboard():
    """AI-powered dashboard with insights and recommendations"""
    try:
        # Get AI insights and recommendations
        insights = AIService.generate_daily_insights(current_user)
        recommendations = AIService.get_personalized_recommendations(current_user)
        risk_analysis = AIService.analyze_relapse_risk(current_user)
        mood_analysis = AIService.analyze_mood_patterns(current_user)
        
        # Ensure all required data is present
        if not all([insights, recommendations, risk_analysis, mood_analysis]):
            raise ValueError("Missing required data for dashboard")
        
        return render_template('ai_dashboard.html',
                             insights=insights,
                             recommendations=recommendations,
                             risk_analysis=risk_analysis,
                             mood_analysis=mood_analysis)
    except Exception as e:
        app.logger.error(f"AI dashboard error: {str(e)}")
        flash('Unable to load AI dashboard. Please try again later.', 'error')
        return redirect(url_for('index'))

@app.route('/api/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    """Handle AI chat messages"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'message': 'Message cannot be empty'}), 400
        
        # Get or create chat session
        session_id = data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            chat_session = AIChatSession(
                user_id=current_user.id,
                session_id=session_id
            )
            db.session.add(chat_session)
            db.session.commit()
        else:
            chat_session = AIChatSession.query.filter_by(
                session_id=session_id,
                user_id=current_user.id
            ).first()
            if not chat_session:
                return jsonify({'success': False, 'message': 'Invalid session'}), 400
        
        # Save user message
        user_message = AIChatMessage(
            session_id=chat_session.id,
            message=message,
            is_user=True
        )
        db.session.add(user_message)
        
        # Get AI response
        ai_response_data = AIService.get_ai_chat_response(message, current_user)
        
        # Save AI response
        ai_message = AIChatMessage(
            session_id=chat_session.id,
            message=ai_response_data['message'],
            is_user=False,
            intent=ai_response_data.get('intent'),
            confidence=ai_response_data.get('confidence'),
            crisis_detected=ai_response_data.get('urgent', False)
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'response': ai_response_data['message'],
            'urgent': ai_response_data.get('urgent', False),
            'suggestions': ai_response_data.get('suggestions', []),
            'resources': ai_response_data.get('resources', [])
        })
        
    except Exception as e:
        app.logger.error(f"AI chat error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred processing your message'}), 500

@app.route('/api/relapse-risk')
@login_required
def get_relapse_risk():
    """Get current relapse risk assessment"""
    try:
        risk_analysis = AIService.analyze_relapse_risk(current_user)
        
        # Save assessment to database
        assessment = RelapseRiskAssessment(
            user_id=current_user.id,
            risk_level=risk_analysis['risk_level'],
            risk_probability=risk_analysis['risk_probability'],
            risk_factors=json.dumps(risk_analysis.get('factors', [])),
            recommendations=json.dumps(risk_analysis.get('recommendations', []))
        )
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'risk_analysis': risk_analysis
        })
        
    except Exception as e:
        app.logger.error(f"Relapse risk analysis error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to analyze relapse risk'})

@app.route('/api/ai-insights')
@login_required
def get_ai_insights():
    """Get AI-powered daily insights"""
    try:
        insights = AIService.generate_daily_insights(current_user)
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        app.logger.error(f"AI insights error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to generate insights'})

@app.route('/api/mood-analysis')
@login_required
def get_mood_analysis():
    """Get AI mood pattern analysis"""
    try:
        mood_analysis = AIService.analyze_mood_patterns(current_user)
        return jsonify({
            'success': True,
            'analysis': mood_analysis
        })
        
    except Exception as e:
        app.logger.error(f"Mood analysis error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to analyze mood patterns'})

@app.route('/api/ai-recommendations')
@login_required
def get_ai_recommendations():
    """Get personalized AI recommendations"""
    try:
        recommendations = AIService.get_personalized_recommendations(current_user)
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        app.logger.error(f"AI recommendations error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to generate recommendations'})

@app.route('/api/ai/risk-analysis')
@login_required
def get_risk_analysis():
    """Get AI risk analysis"""
    try:
        risk_analysis = AIService.analyze_relapse_risk(current_user)
        return jsonify({
            'success': True,
            'analysis': risk_analysis
        })
    except Exception as e:
        app.logger.error(f"Risk analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Unable to analyze risk factors'
        }), 500

def create_default_goals(user):
    default_goals = [
        {'title': 'Morning meditation', 'category': 'Mindfulness', 'time': '8:00 AM'},
        {'title': 'Peer support check-in', 'category': 'Social Support', 'time': '2:00 PM'},
        {'title': 'Evening reflection journal', 'category': 'Self-Care', 'time': '8:00 PM'},
        {'title': 'Gratitude practice', 'category': 'Mindfulness', 'time': '9:00 PM'},
    ]
    
    for goal_data in default_goals:
        goal = DailyGoal(
            user_id=user.id,
            title=goal_data['title'],
            category=goal_data['category'],
            scheduled_time=goal_data['time']
        )
        db.session.add(goal)

def create_default_milestones(user):
    milestones = [
        {'title': '7 Days Sober', 'target_days': 7},
        {'title': '30 Days Sober', 'target_days': 30},
        {'title': '60 Days Sober', 'target_days': 60},
        {'title': '90 Days Sober', 'target_days': 90},
        {'title': '6 Months Sober', 'target_days': 180},
        {'title': '1 Year Sober', 'target_days': 365},
    ]
    
    for milestone_data in milestones:
        milestone = Milestone(
            user_id=user.id,
            title=milestone_data['title'],
            target_days=milestone_data['target_days']
        )
        db.session.add(milestone)

def create_educational_resources():
    resources = [
        # Alcohol Addiction Resources
        {
            'title': 'The Recovery Show Podcast',
            'description': 'Weekly discussions about alcohol addiction recovery, featuring real stories and expert insights.',
            'resource_type': 'podcast',
            'addiction_type': 'alcohol',
            'url': 'https://therecoveryshow.com',
            'author': 'Spencer and Kelli',
            'duration': '45-60 minutes',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'This Naked Mind',
            'description': 'A revolutionary approach to alcohol addiction that helps you escape the alcohol trap.',
            'resource_type': 'book',
            'addiction_type': 'alcohol',
            'author': 'Annie Grace',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Understanding Alcohol Use Disorder',
            'description': 'Comprehensive guide to recognizing and treating alcohol addiction.',
            'resource_type': 'article',
            'addiction_type': 'alcohol',
            'url': 'https://example.com/alcohol-guide',
            'author': 'Dr. Sarah Johnson',
            'difficulty_level': 'intermediate'
        },
        
        # Drug Addiction Resources
        {
            'title': 'The Science of Addiction',
            'description': 'In-depth exploration of how drugs affect the brain and body.',
            'resource_type': 'video',
            'addiction_type': 'drugs',
            'url': 'https://example.com/science-addiction',
            'author': 'Dr. Michael Chen',
            'duration': '30 minutes',
            'difficulty_level': 'intermediate',
            'featured': True
        },
        {
            'title': 'Recovery Roadmap',
            'description': 'Step-by-step guide for drug addiction recovery and relapse prevention.',
            'resource_type': 'ebook',
            'addiction_type': 'drugs',
            'author': 'Recovery Experts Team',
            'difficulty_level': 'beginner'
        },
        
        # Gambling Addiction Resources
        {
            'title': 'Breaking Free from Gambling',
            'description': 'Practical strategies for overcoming gambling addiction.',
            'resource_type': 'book',
            'addiction_type': 'gambling',
            'author': 'Dr. James Wilson',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Gambling Addiction Recovery Podcast',
            'description': 'Weekly episodes featuring success stories and expert advice.',
            'resource_type': 'podcast',
            'addiction_type': 'gambling',
            'url': 'https://example.com/gambling-podcast',
            'duration': '60 minutes',
            'difficulty_level': 'all'
        },
        
        # Internet/Social Media Addiction
        {
            'title': 'Digital Wellbeing Guide',
            'description': 'Comprehensive guide to managing screen time and digital addiction.',
            'resource_type': 'ebook',
            'addiction_type': 'internet',
            'author': 'Digital Wellness Institute',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Social Media Detox Challenge',
            'description': '30-day program to break free from social media addiction.',
            'resource_type': 'course',
            'addiction_type': 'internet',
            'duration': '30 days',
            'difficulty_level': 'beginner'
        },
        
        # Food Addiction Resources
        {
            'title': 'Understanding Food Addiction',
            'description': 'Scientific approach to understanding and overcoming food addiction.',
            'resource_type': 'book',
            'addiction_type': 'food',
            'author': 'Dr. Lisa Thompson',
            'difficulty_level': 'intermediate',
            'featured': True
        },
        {
            'title': 'Healthy Relationship with Food',
            'description': 'Workshop series on developing a healthy relationship with food.',
            'resource_type': 'course',
            'addiction_type': 'food',
            'duration': '8 weeks',
            'difficulty_level': 'beginner'
        },
        
        # Smoking/Nicotine Addiction
        {
            'title': 'Quit Smoking Successfully',
            'description': 'Evidence-based methods for quitting smoking and staying smoke-free.',
            'resource_type': 'course',
            'addiction_type': 'smoking',
            'author': 'Dr. Robert Martinez',
            'duration': '6 weeks',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Nicotine Addiction Recovery',
            'description': 'Understanding nicotine addiction and effective treatment methods.',
            'resource_type': 'article',
            'addiction_type': 'smoking',
            'url': 'https://example.com/nicotine-recovery',
            'difficulty_level': 'intermediate'
        },
        
        # Gaming Addiction
        {
            'title': 'Gaming Addiction Recovery Guide',
            'description': 'Comprehensive guide to overcoming gaming addiction.',
            'resource_type': 'ebook',
            'addiction_type': 'gaming',
            'author': 'Gaming Recovery Institute',
            'difficulty_level': 'beginner',
            'featured': True
        },
        {
            'title': 'Healthy Gaming Habits',
            'description': 'Workshop on developing healthy gaming habits and boundaries.',
            'resource_type': 'workshop',
            'addiction_type': 'gaming',
            'duration': '2 hours',
            'difficulty_level': 'beginner'
        },
        
        # General Recovery Resources
        {
            'title': 'The Recovery Journey',
            'description': 'Comprehensive guide to addiction recovery for all types of addictions.',
            'resource_type': 'book',
            'addiction_type': 'general',
            'author': 'Recovery Experts Team',
            'difficulty_level': 'all',
            'featured': True
        },
        {
            'title': 'Mindfulness in Recovery',
            'description': 'How mindfulness practices can support addiction recovery.',
            'resource_type': 'course',
            'addiction_type': 'general',
            'duration': '4 weeks',
            'difficulty_level': 'beginner'
        }
    ]
    
    for resource_data in resources:
        existing = EducationalResource.query.filter_by(title=resource_data['title']).first()
        if not existing:
            resource = EducationalResource(**resource_data)
            db.session.add(resource)
    
    db.session.commit()

def create_sample_support_groups():
    """Create sample support groups"""
    groups = [
        {
            'name': 'Downtown Recovery Circle',
            'description': 'A welcoming community for individuals in early recovery. We meet weekly to share experiences and support each other.',
            'group_type': 'AA',
            'addiction_focus': 'alcohol',
            'meeting_type': 'hybrid',
            'city': 'Eldoret',
            'state': 'SP',
            'country': 'Kenya',
            'address': 'Rua Augusta, 123 - Centro',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'meeting_days': '["Monday", "Wednesday", "Friday"]',
            'meeting_time': '19:00',
            'timezone': 'East African Time',
            'language': 'English/Swahili',
            'facilitator_name': 'Maria Santos',
            'contact_email': 'maria@recoverysp.org'
        },
        {
            'name': 'Lagos Hope Group',
            'description': 'Supporting families and individuals affected by substance abuse in Lagos community.',
            'group_type': 'NA',
            'addiction_focus': 'drugs',
            'meeting_type': 'in-person',
            'city': 'Lagos',
            'state': 'Lagos',
            'country': 'Nigeria',
            'address': 'Victoria Island Community Center',
            'latitude': 6.4281,
            'longitude': 3.4219,
            'meeting_days': '["Tuesday", "Thursday", "Sunday"]',
            'meeting_time': '18:30',
            'timezone': 'Africa/Lagos',
            'language': 'english',
            'facilitator_name': 'James Okafor',
            'contact_email': 'james@lagoshope.ng'
        },
        {
            'name': 'Mumbai Digital Recovery',
            'description': 'Online support group for tech professionals dealing with various addictions.',
            'group_type': 'SMART',
            'addiction_focus': 'general',
            'meeting_type': 'online',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'country': 'India',
            'latitude': 19.0760,
            'longitude': 72.8777,
            'meeting_days': '["Saturday", "Sunday"]',
            'meeting_time': '20:00',
            'timezone': 'Asia/Kolkata',
            'language': 'english',
            'facilitator_name': 'Dr. Priya Sharma',
            'contact_email': 'priya@mumbairecovery.in'
        },
        {
            'name': 'Global Online Recovery Network',
            'description': 'International online support group welcoming members from all time zones and backgrounds.',
            'group_type': 'Open',
            'addiction_focus': 'general',
            'meeting_type': 'online',
            'meeting_days': '["Daily"]',
            'meeting_time': '12:00',
            'timezone': 'UTC',
            'language': 'english',
            'facilitator_name': 'Recovery Team',
            'contact_email': 'support@globalrecovery.org',
            'max_members': 100
        }
    ]
    
    for group_data in groups:
        existing = SupportGroup.query.filter_by(name=group_data['name']).first()
        if not existing:
            group = SupportGroup(**group_data)
            db.session.add(group)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    import math
    
    if not all([lat1, lon1, lat2, lon2]):
        return float('inf')
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def create_zoom_meeting(title, start_time, duration=60):
    """Create a Zoom meeting (placeholder implementation)"""
    # This would integrate with Zoom API
    meeting_id = f"zoom_{uuid.uuid4().hex[:10]}"
    meeting_url = f"https://zoom.us/j/{meeting_id}"
    return {
        'meeting_id': meeting_id,
        'meeting_url': meeting_url,
        'password': 'recovery123'
    }

def create_google_meet(title, start_time, duration=60):
    meeting_id = f"meet_{uuid.uuid4().hex[:10]}"
    meeting_url = f"https://meet.google.com/{meeting_id}"
    return {
        'meeting_id': meeting_id,
        'meeting_url': meeting_url
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        
        # Validate input
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'})
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            
            # Log successful login
            app.logger.info(f"User {user.id} ({user.email}) logged in successfully")
            
            return jsonify({'success': True, 'redirect': url_for('progress')})
        else:
            # Log failed login attempt
            app.logger.warning(f"Failed login attempt for email: {email}")
            
            return jsonify({'success': False, 'message': 'Invalid email or password'})
    
    return render_template('login.html')

@app.route('/get-started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received registration data:", data)  # Debug log
            
            # Validate required fields
            required_fields = ['firstName', 'lastName', 'email', 'password', 'confirmPassword']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'message': f'Please fill in all required fields: {", ".join(missing_fields)}'
                }), 400
            
            # Validate email format
            import re
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(data.get('email')):
                return jsonify({
                    'success': False,
                    'message': 'Please enter a valid email address'
                }), 400
            
            # Validate password
            if len(data.get('password')) < 6: # Changed back to 6 characters minimum
                return jsonify({
                    'success': False,
                    'message': 'Password must be at least 6 characters long'
                }), 400
            
            # Confirm passwords match
            if data.get('password') != data.get('confirmPassword'):
                return jsonify({'success': False, 'message': 'Passwords do not match'
                }), 400 # Added status code
            
            # Check if email already exists
            existing_user = User.query.filter_by(email=data.get('email')).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already registered. Please login instead.'
                }), 400
            
            # Create new user with all fields
            user = User(
                first_name=data.get('firstName'),
                last_name=data.get('lastName'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password')),
                date_of_birth=datetime.strptime(data.get('dateOfBirth'), '%Y-%m-%d').date() if data.get('dateOfBirth') else None,
                country=data.get('country'),
                language=data.get('language', 'english'),
                user_type=data.get('userType', 'individual'),
                recovery_goals=json.dumps(data.get('recoveryGoals', [])),
                city=data.get('city'), # Added city
                state=data.get('state'), # Added state
                latitude=data.get('latitude'), # Added latitude
                longitude=data.get('longitude'), # Added longitude
                sobriety_start_date=datetime.strptime(data.get('sobrietyStartDate'), '%Y-%m-%d').date() if data.get('sobrietyStartDate') else datetime.utcnow().date() # Added sobriety_start_date
            )
            
            db.session.add(user)
            db.session.commit()
            print(f"User created successfully: {user.email}")  # Debug log
            
            # Create default goals and milestones
            create_default_goals(user)
            create_default_milestones(user)
            db.session.commit()
            print("Default goals and milestones created")  # Debug log
            
            # Log the user in
            login_user(user)
            
            # Log successful registration
            app.logger.info(f"New user registered: {user.id} ({user.email})")
            
            return jsonify({
                'success': True, 
                'message': 'Registration successful',
                'redirect': url_for('progress')
            })
            
        except ValueError as ve:
            db.session.rollback()
            print(f"Validation error: {str(ve)}")  # Debug log
            return jsonify({
                'success': False,
                'message': f'Invalid date format: {str(ve)}. Please use YYYY-MM-DD format.' # More specific error message
            }), 400
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")  # Debug log
            return jsonify({
                'success': False,
                'message': f'An unexpected error occurred during registration: {str(e)}' # More specific error message
            }), 500
    
    return render_template('get_started.html')

@app.route('/api/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'valid': False, 'message': 'Email is required'})
    
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return jsonify({'valid': False, 'message': 'Email already registered'})
    else:
        return jsonify({'valid': True})

@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        return jsonify({
            'firstName': current_user.first_name,
            'lastName': current_user.last_name,
            'email': current_user.email,
            'dateOfBirth': current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
            'country': current_user.country,
            'language': current_user.language,
            'userType': current_user.user_type,
            'recoveryGoals': json.loads(current_user.recovery_goals) if current_user.recovery_goals else []
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        # Update user information
        if 'firstName' in data:
            current_user.first_name = data['firstName']
        if 'lastName' in data:
            current_user.last_name = data['lastName']
        if 'dateOfBirth' in data and data['dateOfBirth']:
            current_user.date_of_birth = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        if 'country' in data:
            current_user.country = data['country']
        if 'language' in data:
            current_user.language = data['language']
        if 'userType' in data:
            current_user.user_type = data['userType']
        if 'recoveryGoals' in data:
            current_user.recovery_goals = json.dumps(data['recoveryGoals'])
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})

@app.route('/progress')
@login_required
def progress():
    stats = get_user_stats(current_user)
    today = datetime.utcnow().date()
    # Check if user has goals for today
    today_goals = DailyGoal.query.filter(
        DailyGoal.user_id == current_user.id,
        DailyGoal.date == today
    ).all()
    if not today_goals:
        # Find the user's first day with goals
        first_goal = DailyGoal.query.filter(
            DailyGoal.user_id == current_user.id
        ).order_by(DailyGoal.date.asc()).first()
        if first_goal:
            first_day = first_goal.date
            first_day_goals = DailyGoal.query.filter(
                DailyGoal.user_id == current_user.id,
                DailyGoal.date == first_day
            ).all()
            for goal in first_day_goals:
                new_goal = DailyGoal(
                    user_id=current_user.id,
                    title=goal.title,
                    category=goal.category,
                    scheduled_time=goal.scheduled_time,
                    date=today
                )
                db.session.add(new_goal)
            db.session.commit()
            today_goals = DailyGoal.query.filter(
                DailyGoal.user_id == current_user.id,
                DailyGoal.date == today
            ).all()
    week_ago = datetime.utcnow() - timedelta(days=7)
    mood_entries = MoodEntry.query.filter(
        MoodEntry.user_id == current_user.id,
        MoodEntry.created_at >= week_ago
    ).order_by(MoodEntry.created_at.desc()).all()
    milestones = Milestone.query.filter_by(user_id=current_user.id).all()
    sobriety_days = stats['sobriety_days']
    for milestone in milestones:
        if not milestone.achieved and sobriety_days >= milestone.target_days:
            milestone.achieved = True
            milestone.achieved_at = datetime.utcnow()
    db.session.commit()
    return render_template('progress.html', 
                         user=current_user,
                         stats=stats,
                         today_goals=today_goals,
                         mood_entries=mood_entries,
                         milestones=milestones)

@app.route('/resources')
@login_required
def resources():
    resource_type = request.args.get('type', 'all')
    addiction_type = request.args.get('addiction', 'all')
    difficulty = request.args.get('difficulty', 'all')
    search = request.args.get('search', '')
    
    query = EducationalResource.query
    
    if resource_type != 'all':
        query = query.filter(EducationalResource.resource_type == resource_type)
    
    if addiction_type != 'all':
        query = query.filter(EducationalResource.addiction_type == addiction_type)
    
    if difficulty != 'all':
        query = query.filter(EducationalResource.difficulty_level == difficulty)
    
    if search:
        query = query.filter(
            db.or_(
                EducationalResource.title.contains(search),
                EducationalResource.description.contains(search),
                EducationalResource.author.contains(search)
            )
        )
    
    featured_resources = EducationalResource.query.filter_by(featured=True).limit(6).all()
    resources = query.order_by(EducationalResource.created_at.desc()).all()
    
    addiction_types = db.session.query(EducationalResource.addiction_type).distinct().all()
    addiction_types = [t[0] for t in addiction_types if t[0]]
    
    return render_template('resources.html',
                         resources=resources,
                         featured_resources=featured_resources,
                         addiction_types=addiction_types,
                         current_filters={
                             'type': resource_type,
                             'addiction': addiction_type,
                             'difficulty': difficulty,
                             'search': search
                         })

@app.route('/support-groups')
@login_required
def support_groups():
    return render_template('support_groups.html')

@app.route('/api/support-groups/search')
@login_required
def search_support_groups():
    # Get search parameters
    location = request.args.get('location', '')
    addiction_type = request.args.get('addiction_type', 'all')
    meeting_type = request.args.get('meeting_type', 'all')
    language = request.args.get('language', 'all')
    radius = int(request.args.get('radius', 50))  # km
    
    query = SupportGroup.query
    
    # Filter by addiction type
    if addiction_type != 'all':
        query = query.filter(SupportGroup.addiction_focus == addiction_type)
    
    # Filter by meeting type
    if meeting_type != 'all':
        query = query.filter(SupportGroup.meeting_type == meeting_type)
    
    # Filter by language
    if language != 'all':
        query = query.filter(SupportGroup.language == language)
    
    groups = query.all()
    
    # Calculate distances if user has location
    if current_user.latitude and current_user.longitude:
        for group in groups:
            if group.latitude and group.longitude:
                group.distance = calculate_distance(
                    current_user.latitude, current_user.longitude,
                    group.latitude, group.longitude
                )
            else:
                group.distance = float('inf')
        
        # Filter by radius for location-based groups
        groups = [g for g in groups if g.meeting_type == 'online' or g.distance <= radius]
        groups.sort(key=lambda x: x.distance)
    
    # Convert to JSON
    groups_data = []
    for group in groups:
        membership = GroupMembership.query.filter_by(
            user_id=current_user.id,
            group_id=group.id
        ).first()
        
        groups_data.append({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'group_type': group.group_type,
            'addiction_focus': group.addiction_focus,
            'meeting_type': group.meeting_type,
            'city': group.city,
            'state': group.state,
            'country': group.country,
            'meeting_days': json.loads(group.meeting_days) if group.meeting_days else [],
            'meeting_time': group.meeting_time,
            'language': group.language,
            'facilitator_name': group.facilitator_name,
            'member_count': len(group.memberships),
            'max_members': group.max_members,
            'distance': getattr(group, 'distance', None),
            'user_membership_status': membership.status if membership else None
        })
    
    return jsonify({'groups': groups_data})

@app.route('/api/support-groups/<int:group_id>/join', methods=['POST'])
@login_required
def join_support_group(group_id):
    group = SupportGroup.query.get_or_404(group_id)
    
    # Check if already a member
    existing_membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()
    
    if existing_membership:
        return jsonify({'success': False, 'message': 'Already a member or request pending'})
    
    # Check if group is full
    current_members = GroupMembership.query.filter_by(
        group_id=group_id,
        status='approved'
    ).count()
    
    if current_members >= group.max_members:
        return jsonify({'success': False, 'message': 'Group is full'})
    
    # Create membership request
    membership = GroupMembership(
        user_id=current_user.id,
        group_id=group_id,
        status='pending' if group.requires_approval else 'approved'
    )
    
    if not group.requires_approval:
        membership.approved_at = datetime.utcnow()
    
    db.session.add(membership)
    db.session.commit()
    
    message = 'Membership request sent' if group.requires_approval else 'Successfully joined group'
    return jsonify({'success': True, 'message': message})

@app.route('/support-groups/<int:group_id>')
@login_required
def group_detail(group_id):
    group = SupportGroup.query.get_or_404(group_id)
    
    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        status='approved'
    ).first()
    
    if not membership:
        return redirect(url_for('support_groups'))
    
    # Get recent chat messages
    messages = ChatMessage.query.filter_by(group_id=group_id)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(50).all()
    messages.reverse()
    
    # Get upcoming sessions
    upcoming_sessions = GroupSession.query.filter(
        GroupSession.group_id == group_id,
        GroupSession.scheduled_date > datetime.utcnow()
    ).order_by(GroupSession.scheduled_date).limit(5).all()
    
    return render_template('group_detail.html',
                         group=group,
                         membership=membership,
                         messages=messages,
                         upcoming_sessions=upcoming_sessions)

@app.route('/api/groups/<int:group_id>/messages', methods=['GET', 'POST'])
@login_required
def group_messages(group_id):
    # Verify membership
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        status='approved'
    ).first()
    
    if not membership:
        return jsonify({'success': False, 'message': 'Not a member of this group'})
    
    if request.method == 'POST':
        data = request.get_json()
        message = ChatMessage(
            group_id=group_id,
            user_id=current_user.id,
            message=data.get('message'),
            is_anonymous=data.get('is_anonymous', False)
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({'success': True, 'message_id': message.id})
    
    else:
        # Get messages
        page = request.args.get('page', 1, type=int)
        messages = ChatMessage.query.filter_by(group_id=group_id)\
            .order_by(ChatMessage.created_at.desc())\
            .paginate(page=page, per_page=20, error_out=False)
        
        messages_data = []
        for msg in messages.items:
            user_name = 'Anonymous' if msg.is_anonymous else f"{msg.user.first_name} {msg.user.last_name[0]}."
            messages_data.append({
                'id': msg.id,
                'user_name': user_name,
                'message': msg.message,
                'created_at': msg.created_at.isoformat(),
                'is_own_message': msg.user_id == current_user.id
            })
        
        return jsonify({
            'messages': messages_data,
            'has_next': messages.has_next,
            'has_prev': messages.has_prev
        })

@app.route('/api/groups/<int:group_id>/sessions', methods=['POST'])
@login_required
def create_group_session(group_id):
    # Check if user is facilitator or moderator
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        status='approved'
    ).first()
    
    if not membership or membership.role not in ['facilitator', 'moderator']:
        return jsonify({'success': False, 'message': 'Insufficient permissions'})
    
    data = request.get_json()
    
    # Create video meeting if requested
    meeting_url = None
    meeting_id = None
    meeting_password = None
    
    if data.get('video_platform') == 'zoom':
        zoom_meeting = create_zoom_meeting(
            data.get('title'),
            data.get('scheduled_date')
        )
        meeting_url = zoom_meeting['meeting_url']
        meeting_id = zoom_meeting['meeting_id']
        meeting_password = zoom_meeting['password']
    elif data.get('video_platform') == 'google_meet':
        meet_data = create_google_meet(
            data.get('title'),
            data.get('scheduled_date')
        )
        meeting_url = meet_data['meeting_url']
        meeting_id = meet_data['meeting_id']
    
    session = GroupSession(
        group_id=group_id,
        title=data.get('title'),
        description=data.get('description'),
        session_type=data.get('session_type'),
        scheduled_date=datetime.fromisoformat(data.get('scheduled_date')),
        duration_minutes=data.get('duration_minutes', 60),
        video_platform=data.get('video_platform'),
        meeting_url=meeting_url,
        meeting_id=meeting_id,
        meeting_password=meeting_password,
        created_by=current_user.id
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'success': True, 'session_id': session.id})

@app.route('/api/sessions/<int:session_id>/join', methods=['POST'])
@login_required
def join_session(session_id):
    session = GroupSession.query.get_or_404(session_id)
    
    # Check if user is a member of the group
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=session.group_id,
        status='approved'
    ).first()
    
    if not membership:
        return jsonify({'success': False, 'message': 'Not a member of this group'})
    
    # Check if already registered
    existing_attendee = SessionAttendee.query.filter_by(
        session_id=session_id,
        user_id=current_user.id
    ).first()
    
    if existing_attendee:
        return jsonify({'success': False, 'message': 'Already registered for this session'})
    
    # Register for session
    attendee = SessionAttendee(
        session_id=session_id,
        user_id=current_user.id
    )
    
    db.session.add(attendee)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'meeting_url': session.meeting_url,
        'meeting_id': session.meeting_id,
        'meeting_password': session.meeting_password
    })

@app.route('/api/mood', methods=['POST'])
@login_required
def log_mood():
    """Log a new mood entry"""
    try:
        data = request.get_json()
        
        # Validate mood value
        valid_moods = ['very_happy', 'happy', 'neutral', 'sad', 'very_sad']
        if data.get('mood') not in valid_moods:
            return jsonify({
                'success': False,
                'message': 'Invalid mood value'
            }), 400
        
        # Create mood entry
        mood_entry = MoodEntry(
            user_id=current_user.id,
            mood=data.get('mood'),
            notes=data.get('notes', '')
        )
        
        db.session.add(mood_entry)
        db.session.commit()
        
        # Get updated mood analysis
        mood_analysis = AIService.analyze_mood_patterns(current_user)
        
        return jsonify({
            'success': True,
            'message': 'Mood logged successfully',
            'analysis': mood_analysis
        })
        
    except Exception as e:
        app.logger.error(f"Error logging mood: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to log mood'
        }), 500

@app.route('/api/mood/history')
@login_required
def get_mood_history():
    """Get mood history for charts"""
    try:
        # Get mood entries from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        mood_entries = MoodEntry.query.filter(
            MoodEntry.user_id == current_user.id,
            MoodEntry.created_at >= thirty_days_ago
        ).order_by(MoodEntry.created_at).all()
        
        # Convert to format for charts
        mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
        
        history_data = []
        for entry in mood_entries:
            history_data.append({
                'date': entry.created_at.strftime('%Y-%m-%d'),
                'mood': mood_mapping.get(entry.mood, 3),
                'notes': entry.notes
            })
        
        # Get mood distribution
        mood_counts = {
            'very_happy': 0,
            'happy': 0,
            'neutral': 0,
            'sad': 0,
            'very_sad': 0
        }
        
        for entry in mood_entries:
            mood_counts[entry.mood] += 1
        
        return jsonify({
            'success': True,
            'history': history_data,
            'distribution': mood_counts
        })
        
    except Exception as e:
        app.logger.error(f"Error getting mood history: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get mood history'
        }), 500

@app.route('/api/mood/trends')
@login_required
def get_mood_trends():
    """Get mood trends and patterns"""
    try:
        mood_analysis = AIService.analyze_mood_patterns(current_user)
        
        return jsonify({
            'success': True,
            'trends': mood_analysis
        })
        
    except Exception as e:
        app.logger.error(f"Error getting mood trends: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get mood trends'
        }), 500

@app.route('/api/goal/<int:goal_id>/toggle', methods=['POST'])
@login_required
def toggle_goal(goal_id):
    goal = DailyGoal.query.filter_by(id=goal_id, user_id=current_user.id).first()
    
    if not goal:
        return jsonify({'success': False, 'message': 'Goal not found'})
    
    goal.completed = not goal.completed
    goal.completed_at = datetime.utcnow() if goal.completed else None
    
    db.session.commit()
    
    return jsonify({'success': True, 'completed': goal.completed})

@app.route('/api/goal', methods=['POST'])
@login_required
def add_goal():
    data = request.get_json()
    
    goal = DailyGoal(
        user_id=current_user.id,
        title=data.get('title'),
        category=data.get('category', 'General'),
        scheduled_time=data.get('time', ''),
        date=datetime.utcnow().date()
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Goal added successfully'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/support-groups', methods=['POST'])
@login_required
def create_support_group():
    data = request.get_json()
    
    group = SupportGroup(
        name=data.get('name'),
        description=data.get('description'),
        group_type=data.get('group_type'),
        addiction_focus=data.get('addiction_focus'),
        meeting_type=data.get('meeting_type'),
        language=data.get('language'),
        facilitator_name=f"{current_user.first_name} {current_user.last_name}",
        contact_email=current_user.email,
        created_by=current_user.id,
        meeting_days='["Monday", "Wednesday", "Friday"]',  # Default schedule
        meeting_time='19:00',
        timezone='UTC'
    )
    
    db.session.add(group)
    db.session.commit()
    
    # Make creator a facilitator
    membership = GroupMembership(
        user_id=current_user.id,
        group_id=group.id,
        status='approved',
        role='facilitator',
        approved_at=datetime.utcnow()
    )
    
    db.session.add(membership)
    db.session.commit()
    
    return jsonify({'success': True, 'group_id': group.id})

@app.route('/profile', methods=['GET'])
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    # Validate input
    if not current_password or not new_password:
        return jsonify({'success': False, 'message': 'Both current and new password are required'})
    
    # Check if current password is correct
    if not check_password_hash(current_user.password_hash, current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'})
    
    # Validate new password
    if len(new_password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters long'})
    
    # Update password
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password updated successfully'})


# NEW ROUTE: Group Management Dashboard
@app.route('/manage-group/<int:group_id>')
@login_required
def manage_group(group_id):
    group = SupportGroup.query.get_or_404(group_id)
    
    # Check if user is facilitator or moderator
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        status='approved'
    ).first()
    
    if not membership or membership.role not in ['facilitator', 'moderator']:
        flash('You do not have permission to manage this group.', 'error')
        return redirect(url_for('support_groups'))
    
    # Get pending membership requests
    pending_requests = GroupMembership.query.filter_by(
        group_id=group_id,
        status='pending'
    ).all()
    
    # Get all approved members
    approved_members = GroupMembership.query.filter_by(
        group_id=group_id,
        status='approved'
    ).all()
    
    return render_template('manage_group.html',
                         group=group,
                         pending_requests=pending_requests,
                         approved_members=approved_members,
                         user_role=membership.role)

# NEW ROUTE: Approve Membership
@app.route('/api/membership/<int:membership_id>/approve', methods=['POST'])
@login_required
def approve_membership(membership_id):
    membership = GroupMembership.query.get_or_404(membership_id)
    
    # Check if current user can approve (facilitator or moderator of the group)
    user_membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=membership.group_id,
        status='approved'
    ).first()
    
    if not user_membership or user_membership.role not in ['facilitator', 'moderator']:
        return jsonify({'success': False, 'message': 'Insufficient permissions'})
    
    # Approve the membership
    membership.status = 'approved'
    membership.approved_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Membership approved successfully'})

# NEW ROUTE: Reject Membership
@app.route('/api/membership/<int:membership_id>/reject', methods=['POST'])
@login_required
def reject_membership(membership_id):
    membership = GroupMembership.query.get_or_404(membership_id)
    
    # Check if current user can reject (facilitator or moderator of the group)
    user_membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=membership.group_id,
        status='approved'
    ).first()
    
    if not user_membership or user_membership.role not in ['facilitator', 'moderator']:
        return jsonify({'success': False, 'message': 'Insufficient permissions'})
    
    # Reject the membership
    membership.status = 'rejected'
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Membership rejected'})

# NEW ROUTE: Remove Member
@app.route('/api/membership/<int:membership_id>/remove', methods=['POST'])
@login_required
def remove_member(membership_id):
    membership = GroupMembership.query.get_or_404(membership_id)
    
    # Check if current user can remove members (facilitator only)
    user_membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=membership.group_id,
        status='approved'
    ).first()
    
    if not user_membership or user_membership.role != 'facilitator':
        return jsonify({'success': False, 'message': 'Only facilitators can remove members'})
    
    # Don't allow removing other facilitators
    if membership.role == 'facilitator' and membership.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Cannot remove other facilitators'})
    
    # Remove the membership
    db.session.delete(membership)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Member removed successfully'})

# Add a custom filter for JSON parsing in templates
@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except:
        return []

# Initialize database
def init_db():
    with app.app_context():
        try:
            db.create_all()
            # Check if we need to load initial data
            if not User.query.first():
                print("Loading initial data...")
                # Create a test user
                test_user = User(
                    first_name="Test",
                    last_name="User",
                    email="test@example.com",
                    password_hash=generate_password_hash("password123"),
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
        except Exception as e:
            print(f"Error initializing database: {str(e)}")

@app.route('/support', methods=['GET'])
@login_required
def support():
    contacts = SupportContact.query.all()
    upcoming_appointments = Appointment.query.options(joinedload(Appointment.contact)).filter(
        Appointment.user_id == current_user.id,
        Appointment.appointment_time >= datetime.utcnow()
    ).order_by(Appointment.appointment_time.asc()).all()
    return render_template('support.html', contacts=contacts, upcoming_appointments=upcoming_appointments)

@app.route('/book-appointment', methods=['POST'])
@login_required
def book_appointment():
    contact_id = request.form.get('contact_id')
    appointment_time = request.form.get('appointment_time')
    reason = request.form.get('reason')
    if not contact_id or not appointment_time:
        flash('Please select a specialist and appointment time.', 'error')
        return redirect(url_for('support'))
    appointment = Appointment(
        user_id=current_user.id,
        contact_id=contact_id,
        appointment_time=datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M'),
        reason=reason
    )
    db.session.add(appointment)
    db.session.commit()
    flash('Appointment booked successfully!', 'success')
    return redirect(url_for('support'))

@click.command('create-tables')
@with_appcontext
def create_tables():
    from app import db
    db.create_all()
    print('All tables created.')

app.cli.add_command(create_tables)

@app.route('/virtual-assistance')
@login_required
def virtual_assistance():
    # Get all verified professionals
    professionals = Professional.query.filter_by(is_verified=True).all()
    
    # Get user's upcoming sessions
    upcoming_sessions = Session.query.filter(
        Session.user_id == current_user.id,
        Session.appointment_time >= datetime.utcnow(),
        Session.status == 'scheduled'
    ).order_by(Session.appointment_time.asc()).all()
    
    # Get active chats
    active_chats = db.session.query(
        Professional,
        Message
    ).join(
        Message,
        Message.professional_id == Professional.id
    ).filter(
        Message.user_id == current_user.id
    ).order_by(
        Message.created_at.desc()
    ).all()
    
    # Get treatment plan
    treatment_plan = TreatmentPlan.query.filter_by(
        user_id=current_user.id
    ).order_by(TreatmentPlan.updated_at.desc()).first()
    treatment_plan_updates = []
    if treatment_plan and treatment_plan.notes:
        try:
            treatment_plan_updates = json.loads(treatment_plan.notes)
        except Exception:
            treatment_plan_updates = []
    # Get past sessions
    past_sessions = Session.query.filter(
        Session.user_id == current_user.id,
        Session.status == 'completed'
    ).order_by(Session.appointment_time.desc()).limit(5).all()
    
    return render_template('virtual_assistance.html',
                         professionals=professionals,
                         upcoming_sessions=upcoming_sessions,
                         active_chats=active_chats,
                         treatment_plan=treatment_plan,
                         treatment_plan_updates=treatment_plan_updates,
                         past_sessions=past_sessions)

@app.route('/book-session', methods=['POST'])
@login_required
def book_session():
    data = request.get_json()
    professional_id = data.get('professional_id')
    appointment_time = data.get('appointment_time')
    session_type = data.get('type', 'video')
    
    if not professional_id or not appointment_time:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    session = Session(
        user_id=current_user.id,
        professional_id=professional_id,
        appointment_time=datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M'),
        type=session_type
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Session booked successfully'})

@app.route('/virtual-assistance/join-session/<int:session_id>')
@login_required
def join_virtual_session(session_id):
    session = Session.query.get_or_404(session_id)
    
    if session.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if session.status != 'scheduled':
        return jsonify({'success': False, 'message': 'Session is not available'})
    
    # Here you would integrate with your video/audio call service
    # For now, we'll just return a success message
    return jsonify({'success': True, 'message': 'Joining session...'})

def is_admin():
    # Simple admin check; adjust as needed for your app
    return hasattr(current_user, 'is_admin') and current_user.is_admin

@app.route('/admin/add-professional', methods=['GET', 'POST'])
@login_required
def add_professional():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        specialization = request.form.get('specialization')
        bio = request.form.get('bio')
        email = request.form.get('email')
        phone = request.form.get('phone')
        availability = request.form.get('availability')
        rating = float(request.form.get('rating', 5.0))
        language = request.form.get('language')
        gender = request.form.get('gender')
        is_verified = bool(request.form.get('is_verified'))

        professional = Professional(
            name=name,
            role=role,
            specialization=specialization,
            bio=bio,
            email=email,
            phone=phone,
            availability=availability,
            rating=rating,
            language=language,
            gender=gender,
            is_verified=is_verified
        )
        db.session.add(professional)
        db.session.commit()
        flash('Professional added successfully!', 'success')
        return redirect(url_for('add_professional'))

    return render_template('admin_add_professional.html')

@app.route('/api/messages/<int:professional_id>')
@login_required
def get_messages(professional_id):
    messages = Message.query.filter_by(user_id=current_user.id, professional_id=professional_id).order_by(Message.created_at.asc()).all()
    return jsonify([
        {
            'id': m.id,
            'content': m.content,
            'type': m.type,
            'file_url': m.file_url,
            'is_read': m.is_read,
            'created_at': m.created_at.strftime('%Y-%m-%d %H:%M'),
            'from_user': m.user_id == current_user.id
        } for m in messages
    ])

@app.route('/api/messages/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    professional_id = data.get('professional_id')
    content = data.get('content')
    if not professional_id or not content:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    message = Message(
        user_id=current_user.id,
        professional_id=professional_id,
        content=content,
        type='text',
        is_read=False
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message sent'})

@app.route('/admin/professionals')
@login_required
def admin_professionals():
    if not is_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    # Instead of showing the list, redirect to add professional page
    return redirect(url_for('add_professional'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/init-db/<init_key>', methods=['GET'])
def initialize_database(init_key):
    # Check if the initialization key matches the environment variable
    if init_key != os.environ.get('INIT_KEY'):
        return jsonify({'error': 'Invalid initialization key'}), 403
    
    try:
        # Create all tables
        db.create_all()
        
        # Check if we need to load initial data
        if not User.query.first():
            # Create a test user
            test_user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                password_hash=generate_password_hash("password123"),
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
        
        return jsonify({
            'success': True,
            'message': 'Database initialized successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Initialize database
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    print("Running app directly, initializing database...") # Debug print
    with app.app_context():
        init_db()
    app.run(debug=True)
