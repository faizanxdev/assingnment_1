"""
Configuration settings for the AI Customer Support Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # AI model settings
    MODEL_NAME = "gpt-3.5-turbo"  # Using GPT-3.5 for cost efficiency
    MAX_TOKENS = 1000  # Limit response length
    
    # Support context
    MERCHANT_ISSUES = {
        "account_hold": "Account freeze or limit holds",
        "payment_failure": "Payment processing failures", 
        "verification": "KYC/document verification issues",
        "settlement": "Settlement delays",
        "technical": "Technical integration problems"
    } 