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