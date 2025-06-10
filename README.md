# AuraRecovery

AuraRecovery is an AI-powered addiction recovery support platform that provides personalized assistance, educational resources, and community support for individuals on their recovery journey.

## Features

- AI-powered recovery support
- Educational resources and courses
- Support group connections
- Progress tracking
- Virtual assistance
- Personalized recovery plans

## Setup Instructions

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

4. Initialize the database:
```bash
python init_db.py
```

5. Load educational resources:
```bash
python load_resources.py
```

6. Run the application:
```bash
flask run
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
ZOOM_API_KEY=your-zoom-api-key
ZOOM_API_SECRET=your-zoom-api-secret
GOOGLE_MEET_API_KEY=your-google-api-key
```

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