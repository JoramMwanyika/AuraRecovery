from ai_service import AIService
from app import User, db
from datetime import datetime
import json

def test_ai_therapist():
    # Create a test user
    test_user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        user_type="patient",
        sobriety_start_date=datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    )
    
    print("\n=== AI Therapist Test Interface ===")
    print("Type 'quit' to exit")
    print("Type 'mood' to get mood analysis")
    print("Type 'risk' to get relapse risk analysis")
    print("Type 'recommendations' to get personalized recommendations")
    print("Type any other message to chat with the AI therapist")
    print("===================================\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'mood':
            mood_analysis = AIService.analyze_mood_patterns(test_user)
            print("\nAI: Mood Analysis Results:")
            print(json.dumps(mood_analysis, indent=2))
        elif user_input.lower() == 'risk':
            risk_analysis = AIService.analyze_relapse_risk(test_user)
            print("\nAI: Relapse Risk Analysis:")
            print(json.dumps(risk_analysis, indent=2))
        elif user_input.lower() == 'recommendations':
            recommendations = AIService.get_personalized_recommendations(test_user)
            print("\nAI: Personalized Recommendations:")
            print(json.dumps(recommendations, indent=2))
        else:
            response = AIService.get_ai_chat_response(user_input, test_user)
            print("\nAI:", response['message'])

if __name__ == "__main__":
    test_ai_therapist() 