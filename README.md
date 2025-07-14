# AuraRecovery

**Project Title:** AI-Powered Addiction Recovery Support System

**Live Demo:** [aurarecovery.render.com](https://aurarecovery.render.com)

## Project Overview

AuraRecovery is an AI-powered addiction recovery support platform that provides personalized assistance, educational resources, and community support for individuals on their recovery journey. The system leverages artificial intelligence to offer real-time support, progress tracking, and personalized recovery plans to help users maintain their sobriety and achieve long-term recovery goals.

## Key Features of the Project

- **AI-Powered Recovery Support**: Intelligent chatbot that provides 24/7 emotional support and guidance
- **Educational Resources**: Comprehensive library of recovery materials, courses, and therapeutic content
- **Support Group Connections**: Virtual and in-person support group management and coordination
- **Progress Tracking**: Advanced analytics and visualization of recovery milestones and achievements
- **Virtual Assistance**: AI-driven recommendations and personalized recovery strategies
- **Professional Portal**: Dedicated interface for healthcare professionals to manage clients
- **Real-Time Monitoring**: Continuous support and relapse prevention through AI analysis
- **Personalized Recovery Plans**: Custom-tailored strategies based on individual needs and progress

## Project Implementation Steps

### 1. Define the Problem and Scope

**Objective**: Build an AI-powered system that provides comprehensive addiction recovery support through personalized assistance, educational resources, and community connections.

**Target Users**: 
- Individuals seeking addiction recovery support
- Healthcare professionals managing recovery programs
- Support group facilitators and coordinators

**Key Features to Monitor**:
- Recovery progress and milestones
- Emotional state and triggers
- Support group participation
- Educational resource engagement
- Relapse risk factors

### 2. Data Collection and Management

**Data Sources**: 
- User interactions with AI therapist
- Progress tracking submissions
- Support group participation records
- Educational resource usage
- Professional portal activities

**Data Preprocessing**: Clean and normalize user data for AI analysis while maintaining privacy standards.

**Python Example: Simulating Recovery Data**
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate recovery progress data
data = {
    'user_id': range(1, 101),
    'days_sober': np.random.randint(1, 365, 100),
    'mood_score': np.random.randint(1, 10, 100),
    'support_sessions_attended': np.random.randint(0, 50, 100),
    'educational_resources_completed': np.random.randint(0, 20, 100),
    'relapse_risk_score': np.random.uniform(0, 1, 100),
    'ai_interactions_count': np.random.randint(5, 100, 100)
}

df = pd.DataFrame(data)
print(df.head())
```

### 3. Model Selection and AI Integration

**Task**: Recovery support, relapse prediction, and personalized recommendations.

**Algorithms**: 
- **GPT Models** for intelligent conversation and emotional support
- **Random Forest** for relapse risk classification
- **LSTM Networks** for time-series analysis of recovery patterns
- **Sentiment Analysis** for emotional state monitoring

**Libraries**: OpenAI API, scikit-learn, TensorFlow, and Flask for web framework.

**Python Example: Relapse Risk Detection**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Prepare features for relapse prediction
features = ['days_sober', 'mood_score', 'support_sessions_attended', 
           'educational_resources_completed', 'ai_interactions_count']

X = df[features]
y = (df['relapse_risk_score'] > 0.7).astype(int)  # High risk threshold

# Train relapse prediction model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

# Predict relapse risk
df['predicted_risk'] = model.predict_proba(X_scaled)[:, 1]
print(df[['user_id', 'relapse_risk_score', 'predicted_risk']].head())
```

### 4. Model Training and Evaluation

**Training**: Split recovery data into training and testing sets (80-20 split).

**Evaluation Metrics**: Use accuracy, precision, recall, and F1-score for relapse prediction tasks.

**Cross-Validation**: Ensure the model generalizes well to different user populations.

**Python Example: Model Evaluation**
```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Split data for relapse prediction
X = df[features]
y = (df['relapse_risk_score'] > 0.7).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train and evaluate the model
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Relapse Prediction Model Performance:")
print(classification_report(y_test, y_pred))
```

### 5. Build User Interface and Web Application

**Platform**: Flask web application with responsive design for desktop and mobile access.

**Features**:
- Real-time AI therapist chat interface
- Progress tracking dashboard with visualizations
- Support group management and scheduling
- Educational resource library
- Professional portal for healthcare providers

**Python Example: Flask Web App Structure**
```python
from flask import Flask, render_template, request, jsonify
from flask_login import login_required, current_user

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ai-therapist')
@login_required
def ai_therapist():
    return render_template('ai_therapist.html')

@app.route('/progress')
@login_required
def progress():
    # Get user's recovery progress data
    progress_data = {
        'days_sober': current_user.days_sober,
        'mood_trend': get_mood_trend(current_user.id),
        'milestones': get_milestones(current_user.id),
        'risk_score': calculate_risk_score(current_user.id)
    }
    return render_template('progress.html', data=progress_data)

@app.route('/support-groups')
@login_required
def support_groups():
    groups = get_available_groups()
    return render_template('support_groups.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True)
```

### 6. Deployment and Infrastructure

**Cloud Platform**: Deployed on Render cloud platform for scalability and reliability.

**Steps**:
- Containerize the Flask app using gunicorn
- Set up PostgreSQL database for data persistence
- Configure environment variables for API keys and secrets
- Implement automated deployment pipeline

**Deployment Example on Render**:
1. Connect GitHub repository to Render
2. Configure build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`
4. Add environment variables for OpenAI API, database, and email services
5. Initialize database with `python init_render_db.py`

### 7. Testing and Validation

**Unit Testing**: Test individual components (AI responses, relapse prediction, user authentication).

**Integration Testing**: Ensure end-to-end functionality (user registration → AI support → progress tracking).

**User Testing**: Collect feedback from recovery community to improve system effectiveness.

**Python Example: Testing AI Therapist**
```python
import unittest
from ai_service import AIService

class TestAIService(unittest.TestCase):
    def setUp(self):
        self.ai_service = AIService()
    
    def test_emotional_support_response(self):
        response = self.ai_service.get_response("I'm feeling triggered today")
        self.assertIsNotNone(response)
        self.assertIn("support", response.lower())
    
    def test_relapse_prevention_advice(self):
        response = self.ai_service.get_response("I'm thinking about using again")
        self.assertIsNotNone(response)
        self.assertIn("help", response.lower())

if __name__ == '__main__':
    unittest.main()
```

### 8. Documentation and Reporting

**Document**: Comprehensive documentation of the AI-powered recovery support system.

**Visualize**: Include screenshots of the interface, progress charts, and system architecture.

**Present**: Prepare demonstrations showcasing the platform's capabilities to stakeholders.

## Handling Challenges

**Data Privacy**: Ensure HIPAA compliance and secure handling of sensitive recovery information.

**Model Accuracy**: Continuously improve AI responses and relapse prediction through user feedback.

**Scalability**: Design the system to handle multiple users while maintaining personalized support.

**User Engagement**: Develop features that encourage consistent participation in recovery activities.

## Expected Outcomes

- A functional AI-powered addiction recovery support platform
- Improved recovery outcomes through personalized assistance
- Enhanced access to support groups and educational resources
- Professional tools for healthcare providers managing recovery programs

## Why This Project?

**Relevance**: Addiction recovery support is a critical application of AI with real-world impact on individuals and families.

**Innovation**: Combines AI technology with evidence-based recovery methodologies.

**Accessibility**: Provides 24/7 support to individuals who may not have access to traditional recovery resources.

## Project Implementation

### 1. Core Technologies
- **Backend**: Python Flask framework
- **AI Integration**: OpenAI GPT models for intelligent responses
- **Database**: PostgreSQL for data persistence
- **Frontend**: HTML, CSS, JavaScript with responsive design
- **Deployment**: Render cloud platform

### 2. AI-Powered Features
- **Intelligent Chatbot**: GPT-powered virtual therapist for emotional support
- **Relapse Prediction**: Machine learning models to identify risk factors
- **Personalized Recommendations**: AI-driven content and resource suggestions
- **Sentiment Analysis**: Real-time emotional state monitoring

### 3. User Experience
- **Intuitive Interface**: Clean, accessible design for all user types
- **Mobile Responsive**: Optimized for desktop and mobile devices
- **Accessibility**: Designed with accessibility standards in mind
- **Multi-language Support**: Framework for internationalization

### 4. Security & Privacy
- **Data Encryption**: Secure handling of sensitive health information
- **User Authentication**: Robust login and session management
- **HIPAA Compliance**: Privacy-focused design for healthcare data
- **Regular Backups**: Automated data protection and recovery

## Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/JoramMwanyika/AuraRecovery.git
cd AuraRecovery
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize the database:**
```bash
python init_db.py
```

6. **Run the application:**
```bash
flask run
```

## Deployment on Render

### 1. Render Setup
1. Create a Render account at [render.com](https://render.com)
2. Create a new Web Service:
   - Connect your GitHub repository
   - Select the repository
   - Configure as follows:
     - Name: `aurarecovery`
     - Environment: `Python`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Plan: Free

### 2. Environment Variables
Add the following environment variables in Render dashboard:
- `SECRET_KEY`: Flask secret key
- `MAIL_SERVER`: SMTP server
- `MAIL_PORT`: SMTP port
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password
- `OPENAI_API_KEY`: OpenAI API key
- `ZOOM_API_KEY`: Zoom API key
- `ZOOM_API_SECRET`: Zoom API secret
- `GOOGLE_MEET_API_KEY`: Google Meet API key

### 3. Database Setup
1. Create a PostgreSQL Database:
   - Click "New +" and select "PostgreSQL"
   - Name: `aurarecovery-db`
   - Database: `aurarecovery`
   - User: `aurarecovery`
   - Plan: Free
   - Region: Choose closest to your users

2. Initialize the Database:
   - After deployment, open the shell in Render dashboard
   - Run: `python init_render_db.py`

## Environment Variables

Required environment variables:
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL database URL (automatically set by Render)
- `MAIL_SERVER`: SMTP server for emails
- `MAIL_PORT`: SMTP port
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password
- `OPENAI_API_KEY`: OpenAI API key
- `ZOOM_API_KEY`: Zoom API key
- `ZOOM_API_SECRET`: Zoom API secret
- `GOOGLE_MEET_API_KEY`: Google Meet API key

## Project Architecture

### Frontend Components
- **Templates**: HTML templates with Jinja2 templating
- **Static Assets**: CSS, JavaScript, and media files
- **Responsive Design**: Mobile-first approach

### Backend Services
- **Flask Application**: Main web framework
- **AI Service**: OpenAI integration for intelligent responses
- **Database Models**: SQLAlchemy ORM for data management
- **Authentication**: User session and security management

### AI Integration
- **GPT Therapist**: OpenAI-powered virtual counselor
- **Relapse Prediction**: Machine learning models for risk assessment
- **Content Recommendation**: AI-driven resource suggestions

## Testing and Validation

- **Unit Testing**: Individual component testing
- **Integration Testing**: End-to-end system validation
- **User Acceptance Testing**: Real-world user feedback
- **Performance Testing**: Load and stress testing

## Future Enhancements

- **Mobile App**: Native iOS and Android applications
- **Advanced Analytics**: Deep learning for better predictions
- **Telemedicine Integration**: Video consultation capabilities
- **Wearable Device Integration**: Health monitoring features
- **Multi-language Support**: International accessibility

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
- Open an issue in the GitHub repository
- Contact the development team
- Visit the live application at [aurarecovery.render.com](https://aurarecovery.render.com)

## Acknowledgments

- OpenAI for AI capabilities
- Render for hosting infrastructure
- The recovery community for inspiration and feedback 