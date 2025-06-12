# AuraRecovery

AuraRecovery is an AI-powered addiction recovery support platform that provides personalized assistance, educational resources, and community support for individuals on their recovery journey.

## Features

- AI-powered recovery support
- Educational resources and courses
- Support group connections
- Progress tracking
- Virtual assistance
- Personalized recovery plans

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/JoramMwanyika/AuraRecovery.git
cd AuraRecovery
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
flask run
```

## Render Deployment

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

3. Add Environment Variables in Render dashboard:
   - `SECRET_KEY`: Flask secret key
   - `MAIL_SERVER`: SMTP server
   - `MAIL_PORT`: SMTP port
   - `MAIL_USERNAME`: Email username
   - `MAIL_PASSWORD`: Email password
   - `OPENAI_API_KEY`: OpenAI API key
   - `ZOOM_API_KEY`: Zoom API key
   - `ZOOM_API_SECRET`: Zoom API secret
   - `GOOGLE_MEET_API_KEY`: Google Meet API key

4. Create a PostgreSQL Database:
   - Click "New +" and select "PostgreSQL"
   - Name: `aurarecovery-db`
   - Database: `aurarecovery`
   - User: `aurarecovery`
   - Plan: Free
   - Region: Choose closest to your users

5. Initialize the Database:
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team. 