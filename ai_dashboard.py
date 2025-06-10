
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from ai_service import AIService
from datetime import datetime, timedelta

ai_dashboard = Blueprint('ai_dashboard', __name__)

@ai_dashboard.route('/ai-dashboard')
@login_required
def dashboard():
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
        current_app.logger.error(f"AI dashboard error: {str(e)}")
        flash('Unable to load AI dashboard. Please try again later.', 'error')
        return redirect(url_for('index'))

@ai_dashboard.route('/api/ai-insights')
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
        current_app.logger.error(f"AI insights error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to generate insights'})

@ai_dashboard.route('/api/ai-recommendations')
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
        current_app.logger.error(f"AI recommendations error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to generate recommendations'})

@ai_dashboard.route('/api/relapse-risk')
@login_required
def get_relapse_risk():
    """Get current relapse risk assessment"""
    try:
        risk_analysis = AIService.analyze_relapse_risk(current_user)
        return jsonify({
            'success': True,
            'risk_analysis': risk_analysis
        })
    except Exception as e:
        current_app.logger.error(f"Relapse risk analysis error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to analyze relapse risk'})

@ai_dashboard.route('/api/mood-analysis')
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
        current_app.logger.error(f"Mood analysis error: {str(e)}")
        return jsonify({'success': False, 'message': 'Unable to analyze mood patterns'}) 