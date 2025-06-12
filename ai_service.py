from flask import current_app
from ai_models import relapse_predictor, ai_chatbot, mood_analyzer
from datetime import datetime, timedelta
import json
import numpy as np
from gpt_therapist import GPTTherapist

class AIService:
    """Service class for AI-powered features"""
    
    @staticmethod
    def get_user_ai_data(user):
        """Collect comprehensive user data for AI analysis"""
        from app import MoodEntry, DailyGoal, GroupMembership, ChatMessage, JournalEntry, GroupSession, SessionAttendee
        
        # Calculate days sober
        days_sober = 0
        if user.sobriety_start_date:
            days_sober = (datetime.utcnow().date() - user.sobriety_start_date).days
        
        # Get recent mood entries (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_moods = MoodEntry.query.filter(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= thirty_days_ago
        ).order_by(MoodEntry.created_at).all()
        
        mood_scores = []
        for mood in recent_moods:
            mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
            if mood.mood in mood_mapping:
                mood_scores.append(mood_mapping[mood.mood])
        
        # Get goal completion data (last 14 days for better analysis)
        two_weeks_ago = datetime.utcnow().date() - timedelta(days=14)
        recent_goals = DailyGoal.query.filter(
            DailyGoal.user_id == user.id,
            DailyGoal.date >= two_weeks_ago
        ).all()
        
        total_goals = len(recent_goals)
        completed_goals = sum(1 for goal in recent_goals if goal.completed)
        
        # Calculate goal streak (consecutive days with completed goals)
        goal_streak = AIService._calculate_goal_streak(user)
        
        # Get social engagement data
        group_messages = ChatMessage.query.filter(
            ChatMessage.user_id == user.id,
            ChatMessage.created_at >= thirty_days_ago
        ).count()
        
        # Get support group attendance
        sessions_attended = SessionAttendee.query.join(GroupSession).filter(
            SessionAttendee.user_id == user.id,
            SessionAttendee.status == 'attended',
            GroupSession.scheduled_date >= thirty_days_ago
        ).count()
        
        # Get journal entries
        journal_entries = JournalEntry.query.filter(
            JournalEntry.user_id == user.id,
            JournalEntry.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Calculate negative mood streak
        negative_mood_streak = AIService._calculate_negative_mood_streak(recent_moods)
        
        # Calculate social isolation days
        social_isolation_days = AIService._calculate_social_isolation(user)
        
        # Estimate sleep quality and stress level (would be better with actual tracking)
        avg_sleep_quality, avg_stress_level = AIService._estimate_health_metrics(recent_moods, completed_goals, total_goals)
        
        return {
            'sobriety_start_date': user.sobriety_start_date.isoformat() if user.sobriety_start_date else None,
            'recent_moods': mood_scores,
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'goal_streak': goal_streak,
            'group_messages_count': group_messages,
            'sessions_attended': sessions_attended,
            'journal_entries_week': journal_entries,
            'negative_mood_streak': negative_mood_streak,
            'social_isolation_days': social_isolation_days,
            'missed_check_ins': AIService._calculate_missed_checkins(user),
            'avg_sleep_quality': avg_sleep_quality,
            'avg_stress_level': avg_stress_level
        }
    
    @staticmethod
    def _calculate_goal_streak(user):
        """Calculate consecutive days with completed goals"""
        from app import DailyGoal
        
        streak = 0
        current_date = datetime.utcnow().date()
        
        for i in range(30):  # Check last 30 days
            check_date = current_date - timedelta(days=i)
            
            daily_goals = DailyGoal.query.filter(
                DailyGoal.user_id == user.id,
                DailyGoal.date == check_date
            ).all()
            
            if daily_goals:
                completed = sum(1 for goal in daily_goals if goal.completed)
                total = len(daily_goals)
                
                if completed / total >= 0.5:  # At least 50% completion
                    streak += 1
                else:
                    break
            else:
                break
        
        return streak
    
    @staticmethod
    def _calculate_negative_mood_streak(mood_entries):
        """Calculate consecutive days of negative mood"""
        if not mood_entries:
            return 0
        
        mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
        streak = 0
        
        for mood in reversed(mood_entries[-14:]):  # Last 14 mood entries
            if mood.mood in mood_mapping and mood_mapping[mood.mood] <= 2:
                streak += 1
            else:
                break
        
        return streak
    
    @staticmethod
    def _calculate_social_isolation(user):
        """Calculate days of social isolation"""
        from app import ChatMessage, GroupMembership
        
        # Check last 14 days for social activity
        two_weeks_ago = datetime.utcnow() - timedelta(days=14)
        
        recent_messages = ChatMessage.query.filter(
            ChatMessage.user_id == user.id,
            ChatMessage.created_at >= two_weeks_ago
        ).count()
        
        # If very low social engagement, calculate isolation days
        if recent_messages < 3:
            return min(14, 14 - recent_messages)
        
        return 0
    
    @staticmethod
    def _calculate_missed_checkins(user):
        """Calculate missed check-ins (simplified)"""
        # This would be more sophisticated with actual check-in tracking
        from app import MoodEntry
        
        week_ago = datetime.utcnow() - timedelta(days=7)
        mood_entries_week = MoodEntry.query.filter(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= week_ago
        ).count()
        
        # Expect at least 3 mood entries per week
        expected_checkins = 7
        actual_checkins = min(mood_entries_week, expected_checkins)
        
        return max(0, expected_checkins - actual_checkins)
    
    @staticmethod
    def _estimate_health_metrics(mood_entries, completed_goals, total_goals):
        """Estimate sleep quality and stress level based on available data"""
        # Default values
        sleep_quality = 5
        stress_level = 5
        
        if mood_entries:
            mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
            recent_mood_scores = []
            
            for mood in mood_entries[-7:]:  # Last week
                if hasattr(mood, 'mood') and mood.mood in mood_mapping:
                    recent_mood_scores.append(mood_mapping[mood.mood])
                elif isinstance(mood, (int, float)):
                    recent_mood_scores.append(mood)
            
            if recent_mood_scores:
                avg_mood = np.mean(recent_mood_scores)
                mood_variance = np.var(recent_mood_scores)
                
                # Estimate sleep quality based on mood stability and average
                sleep_quality = max(1, min(10, 3 + avg_mood * 1.5 - mood_variance))
                
                # Estimate stress level (inverse of mood, higher variance = more stress)
                stress_level = max(1, min(10, 8 - avg_mood + mood_variance))
        
        # Adjust based on goal completion
        if total_goals > 0:
            completion_rate = completed_goals / total_goals
            sleep_quality += (completion_rate - 0.5) * 2
            stress_level -= (completion_rate - 0.5) * 2
        
        return max(1, min(10, sleep_quality)), max(1, min(10, stress_level))
    
    @staticmethod
    def analyze_relapse_risk(user):
        """Analyze user's relapse risk using AI"""
        user_data = AIService.get_user_ai_data(user)
        
        # Get mood data
        from app import MoodEntry
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_moods = MoodEntry.query.filter(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= week_ago
        ).order_by(MoodEntry.created_at.desc()).all()
        
        # Calculate risk factors
        risk_factors = {
            'mood_trend': AIService._analyze_mood_risk(recent_moods),
            'goal_completion': user_data.get('goal_completion_rate', 0.5),
            'social_engagement': user_data.get('social_engagement_rate', 0.5),
            'days_sober': user_data.get('days_sober', 0),
            'recent_triggers': user_data.get('recent_triggers', [])
        }
        
        # Calculate overall risk score
        risk_score = AIService._calculate_risk_score(risk_factors)
        
        # Generate risk analysis
        risk_analysis = {
            'risk_level': AIService._get_risk_level(risk_score),
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'analysis': AIService._generate_risk_analysis(risk_factors),
            'recommendations': AIService._get_risk_recommendations(risk_factors),
            'user_context': {
                'days_sober': user_data.get('days_sober', 0),
                'recent_activity': {
                    'goals_completed': user_data.get('completed_goals', 0),
                    'social_engagement': user_data.get('group_messages_count', 0),
                    'journal_entries': user_data.get('journal_entries_week', 0)
                }
            }
        }
        
        return risk_analysis
    
    @staticmethod
    def _analyze_mood_risk(mood_entries):
        """Analyze mood data for risk factors"""
        if not mood_entries:
            return {'risk_level': 'unknown', 'trend': 'stable'}
        
        mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
        mood_values = [mood_mapping.get(entry.mood, 3) for entry in mood_entries]
        
        # Calculate trend
        if len(mood_values) >= 3:
            trend = np.polyfit(range(len(mood_values)), mood_values, 1)[0]
            trend_direction = 'declining' if trend < -0.2 else 'improving' if trend > 0.2 else 'stable'
        else:
            trend_direction = 'stable'
        
        # Calculate risk level based on recent moods
        recent_mood_avg = np.mean(mood_values[:3]) if mood_values else 3
        if recent_mood_avg <= 2:
            risk_level = 'high'
        elif recent_mood_avg <= 3:
            risk_level = 'moderate'
        else:
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'trend': trend_direction,
            'recent_mood_avg': float(recent_mood_avg)
        }
    
    @staticmethod
    def _calculate_risk_score(risk_factors):
        """Calculate overall risk score from factors"""
        weights = {
            'mood_trend': 0.4,
            'goal_completion': 0.2,
            'social_engagement': 0.2,
            'days_sober': 0.1,
            'recent_triggers': 0.1
        }
        
        # Convert mood risk to score
        mood_risk_map = {'high': 0.8, 'moderate': 0.5, 'low': 0.2, 'unknown': 0.5}
        mood_score = mood_risk_map.get(risk_factors['mood_trend']['risk_level'], 0.5)
        
        # Calculate weighted score
        score = (
            weights['mood_trend'] * mood_score +
            weights['goal_completion'] * (1 - risk_factors['goal_completion']) +
            weights['social_engagement'] * (1 - risk_factors['social_engagement']) +
            weights['days_sober'] * (1 / (1 + risk_factors['days_sober']/30)) +
            weights['recent_triggers'] * (len(risk_factors['recent_triggers']) * 0.2)
        )
        
        return min(max(score, 0), 1)
    
    @staticmethod
    def _get_risk_level(risk_score):
        """Convert risk score to risk level"""
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'moderate'
        else:
            return 'low'
    
    @staticmethod
    def _generate_risk_analysis(risk_factors):
        """Generate human-readable risk analysis"""
        analysis = []
        
        # Mood analysis
        mood_risk = risk_factors['mood_trend']
        if mood_risk['risk_level'] == 'high':
            analysis.append("Your recent mood patterns indicate increased risk. Consider reaching out to your support network.")
        elif mood_risk['trend'] == 'declining':
            analysis.append("Your mood has been declining recently. This could indicate increased vulnerability.")
        
        # Goal completion analysis
        if risk_factors['goal_completion'] < 0.5:
            analysis.append("Your goal completion rate is below average. Struggling with daily goals can increase risk.")
        
        # Social engagement analysis
        if risk_factors['social_engagement'] < 0.3:
            analysis.append("Your social engagement is low. Isolation can increase relapse risk.")
        
        # Days sober context
        if risk_factors['days_sober'] < 30:
            analysis.append("Early recovery is a vulnerable period. Stay connected with your support system.")
        
        # Recent triggers
        if risk_factors['recent_triggers']:
            analysis.append(f"Recent exposure to {len(risk_factors['recent_triggers'])} triggers detected. Stay vigilant.")
        
        return " ".join(analysis) if analysis else "Your current risk factors are well-managed. Keep up the good work!"
    
    @staticmethod
    def _get_risk_recommendations(risk_factors):
        """Generate personalized risk management recommendations"""
        recommendations = []
        
        # Mood-based recommendations
        mood_risk = risk_factors['mood_trend']
        if mood_risk['risk_level'] == 'high':
            recommendations.append({
                'type': 'mood',
                'message': 'Schedule extra support sessions or group meetings',
                'priority': 'high'
            })
        
        # Goal-based recommendations
        if risk_factors['goal_completion'] < 0.5:
            recommendations.append({
                'type': 'goals',
                'message': 'Break down your goals into smaller, more manageable tasks',
                'priority': 'medium'
            })
        
        # Social engagement recommendations
        if risk_factors['social_engagement'] < 0.3:
            recommendations.append({
                'type': 'social',
                'message': 'Increase participation in support groups or recovery activities',
                'priority': 'high'
            })
        
        # General recommendations
        recommendations.append({
            'type': 'general',
            'message': 'Practice self-care and stress management techniques daily',
            'priority': 'medium'
        })
        
        return recommendations
    
    @staticmethod
    def get_ai_chat_response(message, user):
        """Get AI chatbot response using GPT (ChatGPT clone)"""
        # Crisis detection (optional: keep or remove)
        if hasattr(ai_chatbot, 'detect_crisis') and ai_chatbot.detect_crisis(message):
            crisis = ai_chatbot.get_crisis_response()
            return {
                'message': crisis['message'],
                'urgent': True
            }
        
        # Prepare conversation history (for now, just system and user message)
        system_prompt = {
            "role": "system",
            "content": "You are a compassionate, supportive AI therapist. Respond conversationally and empathetically, like a real therapist, and help the user talk through their feelings."
        }
        user_prompt = {"role": "user", "content": message}
        messages = [system_prompt, user_prompt]
        
        gpt = GPTTherapist()
        response = gpt.get_response(messages)
        return {
            'message': response,
            'urgent': False
        }
    
    @staticmethod
    def analyze_mood_patterns(user):
        """Analyze user's mood patterns with enhanced insights"""
        from app import MoodEntry
        
        # Get mood entries from last 60 days for better analysis
        sixty_days_ago = datetime.utcnow() - timedelta(days=60)
        mood_entries = MoodEntry.query.filter(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= sixty_days_ago
        ).order_by(MoodEntry.created_at).all()
        
        # If no mood entries, return default analysis
        if not mood_entries:
            return {
                'analysis': {
                    'trend': 'stable',
                    'trend_strength': 0.5,
                    'analysis': 'No mood data available yet. Start tracking your mood to get personalized insights.',
                    'average_mood': 3,
                    'mood_variance': 0,
                    'mood_stability': 1.0,
                    'recent_mood': 3
                },
                'insights': [],
                'patterns': [],
                'recommendations': [{
                    'type': 'tracking',
                    'message': 'Start tracking your mood daily to get personalized insights',
                    'priority': 'medium'
                }],
                'recovery_context': {
                    'days_sober': 0,
                    'goal_completion_correlation': None,
                    'social_activity_correlation': None
                }
            }
        
        # Convert to format expected by mood analyzer
        mood_data = []
        for entry in mood_entries:
            mood_data.append({
                'mood': entry.mood,
                'created_at': entry.created_at.isoformat(),
                'notes': entry.notes or ''
            })
        
        # Get comprehensive mood insights
        mood_insights = mood_analyzer.get_mood_insights(mood_data)
        
        # Add recovery-specific context
        user_data = AIService.get_user_ai_data(user)
        mood_insights['recovery_context'] = {
            'days_sober': user_data.get('days_sober', 0),
            'goal_completion_correlation': AIService._analyze_mood_goal_correlation(mood_entries, user),
            'social_activity_correlation': AIService._analyze_mood_social_correlation(mood_entries, user)
        }
        
        return mood_insights
    
    @staticmethod
    def _analyze_mood_goal_correlation(mood_entries, user):
        """Analyze correlation between mood and goal completion"""
        from app import DailyGoal
        
        if len(mood_entries) < 7:
            return None
        
        # Get mood and goal data for same time period
        mood_dates = [entry.created_at.date() for entry in mood_entries[-14:]]
        correlations = []
        
        mood_mapping = {'very_sad': 1, 'sad': 2, 'neutral': 3, 'happy': 4, 'very_happy': 5}
        
        for mood_entry in mood_entries[-14:]:
            mood_date = mood_entry.created_at.date()
            mood_score = mood_mapping.get(mood_entry.mood, 3)
            
            # Get goals for that day
            daily_goals = DailyGoal.query.filter(
                DailyGoal.user_id == user.id,
                DailyGoal.date == mood_date
            ).all()
            
            if daily_goals:
                completion_rate = sum(1 for goal in daily_goals if goal.completed) / len(daily_goals)
                correlations.append({'mood': mood_score, 'completion': completion_rate})
        
        if len(correlations) >= 5:
            moods = [c['mood'] for c in correlations]
            completions = [c['completion'] for c in correlations]
            correlation = np.corrcoef(moods, completions)[0, 1]
            
            return {
                'correlation': float(correlation) if not np.isnan(correlation) else 0,
                'interpretation': 'positive' if correlation > 0.3 else 'negative' if correlation < -0.3 else 'weak'
            }
        
        return None
    
    @staticmethod
    def _analyze_mood_social_correlation(mood_entries, user):
        """Analyze correlation between mood and social activity"""
        from app import ChatMessage
        
        if len(mood_entries) < 7:
            return None
        
        # This would be more sophisticated with actual implementation
        return {
            'correlation': 0.4,  # Placeholder
            'interpretation': 'moderate positive correlation between social activity and mood'
        }
    
    @staticmethod
    def get_personalized_recommendations(user):
        """Get comprehensive AI-powered personalized recommendations"""
        risk_analysis = AIService.analyze_relapse_risk(user)
        mood_analysis = AIService.analyze_mood_patterns(user)
        user_data = AIService.get_user_ai_data(user)
        
        recommendations = []
        
        # Add risk-based recommendations
        if risk_analysis.get('recommendations'):
            recommendations.extend(risk_analysis['recommendations'])
        
        # Add mood-based recommendations
        if mood_analysis.get('recommendations'):
            recommendations.extend(mood_analysis['recommendations'])
        
        # Add behavioral recommendations
        recommendations.extend(AIService._get_behavioral_recommendations(user_data))
        
        # Add social recommendations
        recommendations.extend(AIService._get_social_recommendations(user_data))
        
        # Add wellness recommendations
        recommendations.extend(AIService._get_wellness_recommendations(user_data))
        
        # Sort by priority and remove duplicates
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3, 'positive': 4}
        unique_recommendations = []
        seen_messages = set()
        
        for rec in recommendations:
            if rec['message'] not in seen_messages:
                unique_recommendations.append(rec)
                seen_messages.add(rec['message'])
        
        unique_recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return unique_recommendations[:8]  # Return top 8 recommendations
    
    @staticmethod
    def _get_behavioral_recommendations(user_data):
        """Get behavioral pattern recommendations"""
        recommendations = []
        
        if user_data['completed_goals'] / max(user_data['total_goals'], 1) < 0.4:
            recommendations.append({
                'type': 'goals',
                'message': 'Your goal completion rate is low. Try setting smaller, more achievable daily goals.',
                'priority': 'high',
                'action': 'Review and adjust your daily goals to be more realistic'
            })
        
        if user_data['goal_streak'] < 3:
            recommendations.append({
                'type': 'consistency',
                'message': 'Building consistent daily habits is key to recovery success.',
                'priority': 'medium',
                'action': 'Focus on completing at least one goal every day this week'
            })
        
        if user_data['journal_entries_week'] < 2:
            recommendations.append({
                'type': 'reflection',
                'message': 'Regular journaling helps process emotions and track progress.',
                'priority': 'medium',
                'action': 'Set aside 10 minutes daily for journaling'
            })
        
        return recommendations
    
    @staticmethod
    def _get_social_recommendations(user_data):
        """Get social engagement recommendations"""
        recommendations = []
        
        if user_data['group_messages_count'] < 5:
            recommendations.append({
                'type': 'social',
                'message': 'Increase engagement with your support community.',
                'priority': 'high',
                'action': 'Participate in at least one group discussion this week'
            })
        
        if user_data['sessions_attended'] == 0:
            recommendations.append({
                'type': 'support',
                'message': 'Attending support group sessions can significantly improve recovery outcomes.',
                'priority': 'medium',
                'action': 'Schedule and attend a support group session this week'
            })
        
        if user_data['social_isolation_days'] > 7:
            recommendations.append({
                'type': 'connection',
                'message': 'Extended social isolation can impact recovery. Reach out to your support network.',
                'priority': 'high',
                'action': 'Contact a friend, family member, or support group member today'
            })
        
        return recommendations
    
    @staticmethod
    def _get_wellness_recommendations(user_data):
        """Get wellness and health recommendations"""
        recommendations = []
        
        if user_data['avg_sleep_quality'] < 5:
            recommendations.append({
                'type': 'health',
                'message': 'Poor sleep quality can affect mood and recovery. Focus on sleep hygiene.',
                'priority': 'medium',
                'action': 'Establish a consistent bedtime routine and avoid screens before sleep'
            })
        
        if user_data['avg_stress_level'] > 7:
            recommendations.append({
                'type': 'stress',
                'message': 'High stress levels can trigger relapse. Practice stress management techniques.',
                'priority': 'high',
                'action': 'Try meditation, deep breathing, or other relaxation techniques daily'
            })
        
        if user_data['negative_mood_streak'] > 5:
            recommendations.append({
                'type': 'mental_health',
                'message': 'Extended periods of low mood may require professional support.',
                'priority': 'high',
                'action': 'Consider scheduling an appointment with a mental health professional'
            })
        
        return recommendations
    
    @staticmethod
    def generate_daily_insights(user):
        """Generate comprehensive daily AI insights for the user"""
        risk_analysis = AIService.analyze_relapse_risk(user)
        mood_analysis = AIService.analyze_mood_patterns(user)
        user_data = AIService.get_user_ai_data(user)
        
        insights = {
            'risk_assessment': {
                'level': risk_analysis.get('risk_level', 'unknown'),
                'probability': risk_analysis.get('risk_probability', 0),
                'factors': risk_analysis.get('factors', []),
                'trend': AIService._get_risk_trend(user)
            },
            'mood_insights': {
                'trend': mood_analysis['analysis'].get('trend', 'stable'),
                'stability': mood_analysis['analysis'].get('mood_stability', 0.5),
                'patterns': mood_analysis.get('patterns', [])
            },
            'behavioral_insights': {
                'goal_performance': AIService._analyze_goal_performance(user_data),
                'social_engagement': AIService._analyze_social_engagement(user_data),
                'consistency_score': AIService._calculate_consistency_score(user_data)
            },
            'recommendations': AIService.get_personalized_recommendations(user),
            'positive_reinforcement': AIService._get_positive_reinforcement(user_data),
            'areas_for_improvement': AIService._get_improvement_areas(user_data),
            'recovery_milestones': AIService._check_recovery_milestones(user)
        }
        
        return insights
    
    @staticmethod
    def _get_risk_trend(user):
        """Analyze risk trend over time"""
        # This would require historical risk assessments
        # For now, return a placeholder
        return 'stable'
    
    @staticmethod
    def _analyze_goal_performance(user_data):
        """Analyze goal completion performance"""
        completion_rate = user_data.get('completed_goals', 0) / max(user_data.get('total_goals', 1), 1)
        
        if completion_rate >= 0.8:
            performance = 'excellent'
        elif completion_rate >= 0.6:
            performance = 'good'
        elif completion_rate >= 0.4:
            performance = 'fair'
        else:
            performance = 'needs_improvement'
        
        return {
            'performance': performance,
            'completion_rate': completion_rate,
            'streak': user_data.get('goal_streak', 0)
        }
    
    @staticmethod
    def _analyze_social_engagement(user_data):
        """Analyze social engagement levels"""
        messages = user_data.get('group_messages_count', 0)
        sessions = user_data.get('sessions_attended', 0)
        
        engagement_score = min(1.0, (messages * 0.1 + sessions * 0.3))
        
        if engagement_score >= 0.7:
            level = 'high'
        elif engagement_score >= 0.4:
            level = 'moderate'
        else:
            level = 'low'
        
        return {
            'level': level,
            'score': engagement_score,
            'messages': messages,
            'sessions': sessions
        }
    
    @staticmethod
    def _calculate_consistency_score(user_data):
        """Calculate overall consistency score"""
        factors = [
            user_data.get('completed_goals', 0) / max(user_data.get('total_goals', 1), 1),
            min(1.0, user_data.get('journal_entries_week', 0) / 7),
            max(0, 1.0 - user_data.get('missed_check_ins', 0) / 7),
            min(1.0, user_data.get('group_messages_count', 0) / 10)
        ]
        
        return sum(factors) / len(factors)
    
    @staticmethod
    def _get_positive_reinforcement(user_data):
        """Generate positive reinforcement messages"""
        reinforcement = []
        
        if user_data.get('completed_goals', 0) / max(user_data.get('total_goals', 1), 1) > 0.7:
            reinforcement.append("Excellent goal completion rate! You're building strong daily habits.")
        
        if user_data.get('goal_streak', 0) > 7:
            reinforcement.append(f"Amazing {user_data['goal_streak']}-day goal completion streak!")
        
        if user_data.get('group_messages_count', 0) > 15:
            reinforcement.append("Great social engagement with your support community!")
        
        if user_data.get('journal_entries_week', 0) >= 5:
            reinforcement.append("Consistent journaling shows great self-reflection habits!")
        
        days_sober = user_data.get('days_sober', 0)
        if days_sober > 0:
            if days_sober >= 365:
                reinforcement.append(f"Incredible milestone: {days_sober} days sober! You're an inspiration!")
            elif days_sober >= 90:
                reinforcement.append(f"Outstanding achievement: {days_sober} days of sobriety!")
            elif days_sober >= 30:
                reinforcement.append(f"Great progress: {days_sober} days sober and counting!")
            else:
                reinforcement.append(f"Every day counts: {days_sober} days of courage and commitment!")
        
        return reinforcement
    
    @staticmethod
    def _get_improvement_areas(user_data):
        """Identify areas needing improvement"""
        areas = []
        
        if user_data.get('completed_goals', 0) / max(user_data.get('total_goals', 1), 1) < 0.5:
            areas.append("Goal completion consistency")
        
        if user_data.get('group_messages_count', 0) < 5:
            areas.append("Social support engagement")
        
        if user_data.get('journal_entries_week', 0) < 3:
            areas.append("Regular self-reflection through journaling")
        
        if user_data.get('negative_mood_streak', 0) > 3:
            areas.append("Mood management and emotional regulation")
        
        if user_data.get('avg_stress_level', 5) > 7:
            areas.append("Stress management techniques")
        
        return areas
    
    @staticmethod
    def _check_recovery_milestones(user):
        """Check for recovery milestones and achievements"""
        from app import Milestone
        
        milestones = Milestone.query.filter_by(user_id=user.id).all()
        days_sober = (datetime.utcnow().date() - user.sobriety_start_date).days if user.sobriety_start_date else 0
        
        upcoming_milestones = []
        recent_achievements = []
        
        for milestone in milestones:
            if milestone.achieved:
                # Check if achieved recently (last 7 days)
                if milestone.achieved_at and (datetime.utcnow() - milestone.achieved_at).days <= 7:
                    recent_achievements.append(milestone.title)
            else:
                # Check if close to achieving
                if days_sober >= milestone.target_days - 7:
                    days_to_go = milestone.target_days - days_sober
                    upcoming_milestones.append({
                        'title': milestone.title,
                        'days_to_go': days_to_go
                    })
        
        return {
            'recent_achievements': recent_achievements,
            'upcoming_milestones': upcoming_milestones
        }
