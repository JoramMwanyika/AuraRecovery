import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
from datetime import datetime, timedelta
import json
import re
import random

class RelapsePredictor:
    """AI model for predicting relapse risk based on user behavior patterns"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'days_sober', 'mood_variance', 'goal_completion_rate',
            'social_engagement', 'sleep_quality', 'stress_level',
            'support_group_attendance', 'journal_frequency',
            'missed_check_ins', 'negative_mood_streak',
            'recent_mood_avg', 'goal_streak', 'social_isolation_days'
        ]
        self.model_path = 'models/relapse_predictor.joblib'
        self.scaler_path = 'models/relapse_scaler.joblib'
        
    def prepare_features(self, user_data):
        """Extract features from user data for prediction"""
        features = {}
        
        # Calculate days sober
        if user_data.get('sobriety_start_date'):
            if isinstance(user_data['sobriety_start_date'], str):
                sobriety_start = datetime.strptime(user_data['sobriety_start_date'], '%Y-%m-%d')
            else:
                sobriety_start = user_data['sobriety_start_date']
            features['days_sober'] = (datetime.now() - sobriety_start).days
        else:
            features['days_sober'] = 0
            
        # Mood variance and average (higher variance indicates instability)
        mood_scores = user_data.get('recent_moods', [])
        if mood_scores:
            features['mood_variance'] = np.var(mood_scores)
            features['recent_mood_avg'] = np.mean(mood_scores)
        else:
            features['mood_variance'] = 0
            features['recent_mood_avg'] = 3  # neutral
            
        # Goal completion rate and streak
        total_goals = user_data.get('total_goals', 1)
        completed_goals = user_data.get('completed_goals', 0)
        features['goal_completion_rate'] = completed_goals / max(total_goals, 1)
        features['goal_streak'] = user_data.get('goal_streak', 0)
        
        # Social engagement metrics
        features['social_engagement'] = user_data.get('group_messages_count', 0)
        features['support_group_attendance'] = user_data.get('sessions_attended', 0)
        features['social_isolation_days'] = user_data.get('social_isolation_days', 0)
        
        # Health indicators
        features['sleep_quality'] = user_data.get('avg_sleep_quality', 5)
        features['stress_level'] = user_data.get('avg_stress_level', 5)
        
        # Behavioral patterns
        features['journal_frequency'] = user_data.get('journal_entries_week', 0)
        features['missed_check_ins'] = user_data.get('missed_check_ins', 0)
        features['negative_mood_streak'] = user_data.get('negative_mood_streak', 0)
        
        return features
    
    def train_model(self, training_data=None):
        """Train the relapse prediction model"""
        if training_data is None:
            training_data = self._generate_synthetic_data()
        
        # Prepare training data
        X = []
        y = []
        
        for record in training_data:
            features = self.prepare_features(record)
            feature_vector = [features.get(col, 0) for col in self.feature_columns]
            X.append(feature_vector)
            y.append(record.get('relapsed', 0))
        
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train ensemble model
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        print(f"Model accuracy: {accuracy:.3f}")
        print(f"AUC Score: {auc_score:.3f}")
        
        # Save model and scaler
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        return accuracy, auc_score
    
    def _generate_synthetic_data(self, n_samples=2000):
        """Generate synthetic training data"""
        data = []
        
        for i in range(n_samples):
            # Generate realistic user patterns
            days_sober = random.randint(1, 730)  # Up to 2 years
            
            # Early recovery is riskier
            base_risk = 0.7 if days_sober < 30 else 0.4 if days_sober < 90 else 0.2
            
            # Generate correlated features
            mood_stability = random.uniform(0.3, 1.0)
            mood_variance = (1 - mood_stability) * 3
            recent_mood_avg = 2 + mood_stability * 2 + random.uniform(-0.5, 0.5)
            
            goal_discipline = random.uniform(0.2, 1.0)
            goal_completion_rate = goal_discipline + random.uniform(-0.2, 0.2)
            goal_completion_rate = max(0, min(1, goal_completion_rate))
            
            social_connection = random.uniform(0.1, 1.0)
            social_engagement = int(social_connection * 30)
            support_group_attendance = int(social_connection * 10)
            social_isolation_days = int((1 - social_connection) * 14)
            
            # Health factors
            sleep_quality = random.randint(3, 9)
            stress_level = random.randint(2, 9)
            
            # Behavioral patterns
            journal_frequency = int(goal_discipline * 7)
            missed_check_ins = int((1 - goal_discipline) * 5)
            negative_mood_streak = int((1 - mood_stability) * 10)
            goal_streak = int(goal_discipline * 14)
            
            # Calculate relapse probability
            risk_score = base_risk
            risk_score += (1 - mood_stability) * 0.3
            risk_score += (1 - goal_discipline) * 0.25
            risk_score += (1 - social_connection) * 0.2
            risk_score += (stress_level / 10) * 0.15
            risk_score += (1 - sleep_quality / 10) * 0.1
            
            # Add randomness
            risk_score += random.uniform(-0.15, 0.15)
            risk_score = max(0, min(1, risk_score))
            
            # Determine relapse outcome
            relapsed = 1 if random.random() < risk_score else 0
            
            record = {
                'sobriety_start_date': datetime.now() - timedelta(days=days_sober),
                'recent_moods': [recent_mood_avg + random.uniform(-1, 1) for _ in range(7)],
                'total_goals': 10,
                'completed_goals': int(goal_completion_rate * 10),
                'goal_streak': goal_streak,
                'group_messages_count': social_engagement,
                'sessions_attended': support_group_attendance,
                'social_isolation_days': social_isolation_days,
                'avg_sleep_quality': sleep_quality,
                'avg_stress_level': stress_level,
                'journal_entries_week': journal_frequency,
                'missed_check_ins': missed_check_ins,
                'negative_mood_streak': negative_mood_streak,
                'relapsed': relapsed
            }
            
            data.append(record)
        
        return data
    
    def load_model(self):
        """Load trained model and scaler"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict_relapse_risk(self, user_data):
        """Predict relapse risk for a user"""
        if not self.model:
            if not self.load_model():
                # Train model if not available
                self.train_model()
        
        features = self.prepare_features(user_data)
        feature_vector = np.array([[features.get(col, 0) for col in self.feature_columns]])
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Get prediction probability
        risk_probability = self.model.predict_proba(feature_vector_scaled)[0][1]
        
        # Determine risk level
        if risk_probability < 0.3:
            risk_level = 'low'
        elif risk_probability < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # Generate recommendations based on feature importance
        recommendations = self._generate_recommendations(features, risk_probability)
        
        return {
            'risk_level': risk_level,
            'risk_probability': float(risk_probability),
            'confidence': float(risk_probability),
            'recommendations': recommendations,
            'factors': self._get_risk_factors(features),
            'feature_importance': self._get_feature_importance(features)
        }
    
    def _generate_recommendations(self, features, risk_probability):
        """Generate personalized recommendations based on risk factors"""
        recommendations = []
        
        if features['goal_completion_rate'] < 0.5:
            recommendations.append({
                'type': 'goals',
                'message': 'Focus on completing your daily goals. Start with smaller, achievable targets.',
                'priority': 'high',
                'action': 'Set 2-3 simple daily goals and track completion'
            })
        
        if features['social_engagement'] < 5:
            recommendations.append({
                'type': 'social',
                'message': 'Increase engagement with your support groups. Connection is key to recovery.',
                'priority': 'high',
                'action': 'Join a support group discussion or attend a meeting this week'
            })
        
        if features['mood_variance'] > 2:
            recommendations.append({
                'type': 'mood',
                'message': 'Your mood has been fluctuating. Consider speaking with a counselor.',
                'priority': 'medium',
                'action': 'Schedule a session with a mental health professional'
            })
        
        if features['journal_frequency'] < 3:
            recommendations.append({
                'type': 'journaling',
                'message': 'Regular journaling can help process emotions and track progress.',
                'priority': 'medium',
                'action': 'Write in your journal for 10 minutes daily'
            })
        
        if features['sleep_quality'] < 5:
            recommendations.append({
                'type': 'health',
                'message': 'Poor sleep affects recovery. Establish a consistent sleep routine.',
                'priority': 'medium',
                'action': 'Set a regular bedtime and avoid screens 1 hour before sleep'
            })
        
        if risk_probability > 0.7:
            recommendations.append({
                'type': 'urgent',
                'message': 'Consider reaching out to your sponsor or counselor immediately.',
                'priority': 'urgent',
                'action': 'Contact your support network within 24 hours'
            })
        
        return recommendations
    
    def _get_risk_factors(self, features):
        """Identify key risk factors contributing to relapse risk"""
        risk_factors = []
        
        if features['negative_mood_streak'] > 3:
            risk_factors.append('Extended period of negative mood')
        
        if features['missed_check_ins'] > 2:
            risk_factors.append('Missing regular check-ins')
        
        if features['goal_completion_rate'] < 0.3:
            risk_factors.append('Low goal completion rate')
        
        if features['social_engagement'] < 2:
            risk_factors.append('Limited social support engagement')
        
        if features['social_isolation_days'] > 7:
            risk_factors.append('Extended social isolation')
        
        if features['stress_level'] > 7:
            risk_factors.append('High stress levels')
        
        if features['sleep_quality'] < 4:
            risk_factors.append('Poor sleep quality')
        
        return risk_factors
    
    def _get_feature_importance(self, features):
        """Get feature importance for explanation"""
        if not self.model:
            return {}
        
        feature_importance = {}
        importances = self.model.feature_importances_
        
        for i, feature in enumerate(self.feature_columns):
            feature_importance[feature] = {
                'importance': float(importances[i]),
                'value': features.get(feature, 0)
            }
        
        return feature_importance

class AITherapistChatbot:
    """AI-powered therapeutic chatbot for recovery support"""
    
    def __init__(self):
        self.conversation_history = []
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'no reason to live',
            'want to die', 'better off dead', 'hurt myself', 'self-harm',
            'overdose', 'take pills', 'drink myself to death'
        ]
        
        self.intent_keywords = {
            'craving': ['craving', 'urge', 'want to use', 'need a drink', 'need drugs'],
            'anxiety': ['anxious', 'anxiety', 'panic', 'worried', 'stress', 'stressed'],
            'depression': ['depressed', 'sad', 'hopeless', 'empty', 'worthless'],
            'stress': ['stress', 'overwhelmed', 'pressure', 'burnout'],
            'loneliness': ['lonely', 'alone', 'isolated', 'no friends'],
            'motivation': ['motivation', 'unmotivated', 'can\'t do it', 'too hard']
        }
        
        self.response_templates = {
            'craving': [
                "I understand you're experiencing cravings right now. Remember, cravings are temporary and will pass. Would you like to try some grounding techniques or distraction strategies?",
                "Cravings can be intense, but they typically last only 15-20 minutes. Let's focus on getting through this moment. What's one thing you can do right now to take care of yourself?",
                "I hear that you're having cravings. This is a normal part of recovery. Would you like to talk about what triggered these feelings?"
            ],
            'anxiety': [
                "I notice you're feeling anxious. Would you like to try some deep breathing exercises together?",
                "Anxiety can be overwhelming. Let's break this down into smaller, manageable steps. What's one thing that might help you feel more grounded right now?",
                "I understand anxiety can be challenging. Remember, this feeling will pass. Would you like to explore some coping strategies that have worked for you in the past?"
            ],
            'depression': [
                "I hear that you're feeling down. It's important to acknowledge these feelings. Would you like to talk more about what's contributing to these feelings?",
                "Depression can make everything feel more difficult. Remember, it's okay to not be okay. What's one small thing you can do today to take care of yourself?",
                "I understand you're feeling depressed. Let's focus on one step at a time. What's something that usually brings you even a small amount of joy or comfort?"
            ],
            'stress': [
                "Stress can be overwhelming. Let's identify what's causing your stress and explore some healthy ways to manage it.",
                "I hear you're feeling stressed. Would you like to try some stress-reduction techniques together?",
                "Stress is a normal part of life, but it's important to manage it in healthy ways. What's one thing that helps you feel more relaxed?"
            ],
            'loneliness': [
                "I understand you're feeling lonely. Remember, you're not alone in your recovery journey. Would you like to talk about ways to connect with others?",
                "Loneliness can be challenging, especially in recovery. What are some ways you've connected with others in the past that felt meaningful?",
                "I hear that you're feeling isolated. Let's explore some ways to build connections with others who understand your journey."
            ],
            'motivation': [
                "I understand you're feeling unmotivated. Recovery is a journey, and it's okay to have ups and downs. What's one small step you can take today?",
                "Motivation can come and go, but your commitment to recovery is what matters. Let's focus on one thing you can do right now to move forward.",
                "I hear you're struggling with motivation. Remember why you started this journey. What's one thing that would help you feel more motivated?"
            ],
            'general': [
                "I'm here to listen and support you. Would you like to tell me more about what's on your mind?",
                "Thank you for sharing that with me. How are you feeling about this situation?",
                "I understand this is important to you. Let's explore this together. What would be most helpful for you right now?"
            ]
        }
    
    def detect_crisis(self, message):
        """Detect if message indicates crisis situation"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.crisis_keywords)
    
    def get_crisis_response(self):
        """Return crisis intervention response"""
        return {
            'message': "I'm very concerned about your safety right now. Please reach out to a crisis helpline immediately. You matter, and there are people who want to help you.",
            'resources': [
                {
                    'name': 'National Suicide Prevention Lifeline',
                    'phone': '988',
                    'available': '24/7',
                    'description': 'Free and confidential emotional support'
                },
                {
                    'name': 'Crisis Text Line',
                    'text': 'Text HOME to 741741',
                    'available': '24/7',
                    'description': 'Free crisis support via text message'
                },
                {
                    'name': 'SAMHSA National Helpline',
                    'phone': '1-800-662-4357',
                    'available': '24/7',
                    'description': 'Treatment referral and information service'
                }
            ],
            'urgent': True,
            'immediate_actions': [
                'Call 911 if you are in immediate danger',
                'Go to your nearest emergency room',
                'Call a trusted friend or family member',
                'Contact your therapist or counselor'
            ]
        }
    
    def classify_intent(self, message):
        """Classify user message intent using keyword matching and context"""
        message_lower = message.lower()
        
        # Check for multiple intents and prioritize
        detected_intents = []
        
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intents.append(intent)
        
        # Prioritize more serious intents
        priority_order = ['craving', 'depression', 'anxiety', 'stress', 'loneliness', 'motivation']
        
        for intent in priority_order:
            if intent in detected_intents:
                return intent
        
        return 'general'
    
    def generate_response(self, message, user_context=None):
        """Generate therapeutic response to user message"""
        # Check for crisis first
        if self.detect_crisis(message):
            return self.get_crisis_response()
        
        intent = self.classify_intent(message)
        
        # Select appropriate response template
        if intent in self.response_templates:
            responses = self.response_templates[intent]
        else:
            responses = self.response_templates['general']
        
        # Select response based on conversation history or randomly
        base_response = self._select_contextual_response(responses, intent)
        
        # Personalize response with user context
        if user_context:
            personalized_response = self._personalize_response(base_response, user_context, intent)
            return personalized_response
        
        return base_response
    
    def _select_contextual_response(self, responses, intent):
        """Select response based on conversation context"""
        # For now, use random selection, but this could be enhanced with ML
        import random
        return random.choice(responses)
    
    def _personalize_response(self, response, user_context, intent):
        """Personalize response with user context"""
        if not user_context:
            return response
            
        # Add user's name if available
        if user_context.get('first_name'):
            response = f"{user_context['first_name']}, {response.lower()}"
            
        # Add sobriety context if relevant
        if user_context.get('days_sober') and intent in ['craving', 'motivation']:
            response += f" Remember, you've been sober for {user_context['days_sober']} days, which is a significant achievement."
            
        return response
    
    def get_conversation_suggestions(self, intent):
        """Get relevant conversation suggestions based on intent"""
        suggestions = {
            'craving': [
                "What triggered these cravings?",
                "Would you like to try some grounding techniques?",
                "Let's talk about your coping strategies"
            ],
            'anxiety': [
                "What's causing your anxiety?",
                "Would you like to try some breathing exercises?",
                "Let's explore some relaxation techniques"
            ],
            'depression': [
                "How long have you been feeling this way?",
                "What usually helps lift your mood?",
                "Would you like to talk about your support system?"
            ],
            'stress': [
                "What's the main source of your stress?",
                "What stress management techniques have worked for you?",
                "How can we break this down into smaller steps?"
            ],
            'loneliness': [
                "What kind of connections are you looking for?",
                "Have you considered joining a support group?",
                "What activities do you enjoy that might help you meet others?"
            ],
            'motivation': [
                "What's your main goal right now?",
                "What usually helps you stay motivated?",
                "Let's set some small, achievable goals"
            ],
            'general': [
                "How are you feeling today?",
                "What's been on your mind lately?",
                "Would you like to talk about your recovery goals?"
            ]
        }
        
        return suggestions.get(intent, suggestions['general'])

class MoodAnalyzer:
    """AI model for analyzing mood patterns and trends"""
    
    def __init__(self):
        self.mood_mapping = {
            'very_sad': 1,
            'sad': 2,
            'neutral': 3,
            'happy': 4,
            'very_happy': 5
        }
    
    def analyze_mood_trend(self, mood_entries):
        """Analyze mood trend over time with advanced analytics"""
        if not mood_entries:
            return {'trend': 'insufficient_data', 'analysis': 'Not enough mood data to analyze'}
        
        # Convert moods to numerical values with timestamps
        mood_data = []
        
        for entry in mood_entries:
            if entry['mood'] in self.mood_mapping:
                mood_data.append({
                    'value': self.mood_mapping[entry['mood']],
                    'date': entry['created_at'],
                    'notes': entry.get('notes', '')
                })
        
        if len(mood_data) < 3:
            return {'trend': 'insufficient_data', 'analysis': 'Need more mood entries for analysis'}
        
        # Extract mood values for analysis
        mood_values = [entry['value'] for entry in mood_data]
        mood_array = np.array(mood_values)
        
        # Calculate trend using linear regression
        x = np.arange(len(mood_array))
        trend_slope = np.polyfit(x, mood_array, 1)[0]
        
        # Calculate additional metrics
        mood_variance = np.var(mood_values)
        mood_mean = np.mean(mood_values)
        mood_std = np.std(mood_values)
        
        # Determine trend direction and strength
        if trend_slope > 0.1:
            trend = 'improving'
            trend_strength = min(abs(trend_slope) * 2, 1.0)
        elif trend_slope < -0.1:
            trend = 'declining'
            trend_strength = min(abs(trend_slope) * 2, 1.0)
        else:
            trend = 'stable'
            trend_strength = 1.0 - abs(trend_slope)
        
        # Generate analysis text
        analysis = self._generate_mood_analysis(trend, mood_mean, mood_variance, trend_strength)
        
        # Identify patterns
        patterns = self._identify_mood_patterns(mood_data)
        
        return {
            'trend': trend,
            'trend_strength': float(trend_strength),
            'analysis': analysis,
            'average_mood': float(mood_mean),
            'mood_variance': float(mood_variance),
            'mood_stability': float(1.0 / (1.0 + mood_variance)),
            'recent_mood': mood_values[-1] if mood_values else 3,
            'patterns': patterns,
            'recommendations': self._get_mood_recommendations(trend, mood_mean, mood_variance)
        }
    
    def _generate_mood_analysis(self, trend, mood_mean, mood_variance, trend_strength):
        """Generate human-readable mood analysis"""
        if trend == 'improving':
            analysis = f"Your mood has been trending upward with {trend_strength:.0%} consistency. "
            if mood_mean > 3.5:
                analysis += "You're maintaining a positive emotional state. Keep up the great work!"
            else:
                analysis += "You're making progress toward better emotional well-being."
        elif trend == 'declining':
            analysis = f"Your mood has been declining with {trend_strength:.0%} consistency. "
            analysis += "This could indicate increased stress or other challenges that need attention."
        else:
            analysis = "Your mood has been relatively stable. "
            if mood_mean > 3.5:
                analysis += "You're maintaining good emotional balance."
            else:
                analysis += "Consider strategies to improve your overall mood."
        
        # Add variance analysis
        if mood_variance > 1.5:
            analysis += " Your mood has been quite variable - consider tracking triggers and patterns."
        elif mood_variance < 0.5:
            analysis += " Your mood has been very consistent, which is a positive sign."
        
        return analysis
    
    def _identify_mood_patterns(self, mood_data):
        """Identify patterns in mood data"""
        patterns = []
        
        if len(mood_data) < 7:
            return patterns
        
        # Look for weekly patterns
        recent_week = mood_data[-7:]
        week_values = [entry['value'] for entry in recent_week]
        
        # Check for consistent low moods
        low_mood_streak = 0
        for value in reversed(week_values):
            if value <= 2:
                low_mood_streak += 1
            else:
                break
        
        if low_mood_streak >= 3:
            patterns.append({
                'type': 'low_mood_streak',
                'description': f'Consecutive low mood days: {low_mood_streak}',
                'severity': 'high' if low_mood_streak >= 5 else 'medium'
            })
        
        # Check for high variability
        week_variance = np.var(week_values)
        if week_variance > 2.0:
            patterns.append({
                'type': 'high_variability',
                'description': 'Significant mood swings detected',
                'severity': 'medium'
            })
        
        # Check for improvement pattern
        if len(week_values) >= 5:
            recent_trend = np.polyfit(range(5), week_values[-5:], 1)[0]
            if recent_trend > 0.3:
                patterns.append({
                    'type': 'recent_improvement',
                    'description': 'Mood improving over recent days',
                    'severity': 'positive'
                })
        
        return patterns
    
    def _get_mood_recommendations(self, trend, mood_mean, mood_variance):
        """Generate mood-based recommendations"""
        recommendations = []
        
        if trend == 'declining':
            recommendations.append({
                'type': 'intervention',
                'message': 'Consider reaching out to your support network or counselor',
                'priority': 'high'
            })
        
        if mood_mean < 2.5:
            recommendations.append({
                'type': 'mental_health',
                'message': 'Your mood has been consistently low. Professional support may be helpful',
                'priority': 'high'
            })
        
        if mood_variance > 1.5:
            recommendations.append({
                'type': 'stability',
                'message': 'Try to identify triggers for mood changes and develop coping strategies',
                'priority': 'medium'
            })
        
        # Positive reinforcement
        if trend == 'improving':
            recommendations.append({
                'type': 'encouragement',
                'message': 'Your mood is improving! Continue with the strategies that are working',
                'priority': 'positive'
            })
        
        return recommendations
    
    def get_mood_insights(self, mood_entries, goals_data=None):
        """Generate comprehensive mood insights"""
        mood_analysis = self.analyze_mood_trend(mood_entries)
        insights = []
        
        # Add insights based on analysis
        if mood_analysis['trend'] == 'declining':
            insights.append({
                'type': 'warning',
                'message': 'Your mood has been declining recently. This could indicate increased stress or other challenges.',
                'recommendation': 'Consider scheduling time with a counselor or increasing self-care activities.',
                'data': {'trend_strength': mood_analysis.get('trend_strength', 0)}
            })
        
        if mood_analysis['mood_variance'] > 1.5:
            insights.append({
                'type': 'observation',
                'message': 'Your mood has been fluctuating significantly.',
                'recommendation': 'Try to identify triggers for mood changes and develop coping strategies.',
                'data': {'variance': mood_analysis['mood_variance']}
            })
        
        if mood_analysis['average_mood'] < 2.5:
            insights.append({
                'type': 'concern',
                'message': 'Your average mood has been quite low.',
                'recommendation': 'Please consider reaching out to your support network or a mental health professional.',
                'data': {'average_mood': mood_analysis['average_mood']}
            })
        
        # Positive insights
        if mood_analysis['trend'] == 'improving':
            insights.append({
                'type': 'positive',
                'message': 'Your mood has been improving! This is a great sign of progress.',
                'recommendation': 'Continue with the strategies and activities that are working for you.',
                'data': {'trend_strength': mood_analysis.get('trend_strength', 0)}
            })
        
        if mood_analysis['mood_stability'] > 0.7:
            insights.append({
                'type': 'positive',
                'message': 'Your mood has been stable, which indicates good emotional regulation.',
                'recommendation': 'Keep up the good work with your current coping strategies.',
                'data': {'stability': mood_analysis['mood_stability']}
            })
        
        return {
            'analysis': mood_analysis,
            'insights': insights,
            'patterns': mood_analysis.get('patterns', []),
            'recommendations': mood_analysis.get('recommendations', [])
        }

# Initialize AI models
relapse_predictor = RelapsePredictor()
ai_chatbot = AITherapistChatbot()
mood_analyzer = MoodAnalyzer()
