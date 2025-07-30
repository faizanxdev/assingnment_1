"""
Simple command-line demo for AI Customer Support Assistant
Test the bot without web interface
"""
from support_ai import CashfreeSupportAI
from config import Config
import json

def run_demo():
    """Run interactive demo of the AI support assistant"""
    
    # Initialize AI assistant
    print("🤖 Initializing Cashfree AI Support Assistant...")
    support_ai = CashfreeSupportAI()
    
    # Check API key
    if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == 'your_gemini_api_key_here':
        print("❌ Error: Please set your Google Gemini API key in .env file")
        print("   Copy env_example.txt to .env and add your API key")
        return
    
    print("✅ AI Assistant ready!")
    print("\n" + "="*50)
    print("🎯 DEMO: Ask 'Why is my account on hold?'")
    print("="*50)
    
    # Demo query
    demo_query = "Why is my account on hold?"
    print(f"\n📝 Merchant Query: {demo_query}")
    
    try:
        # Generate response
        print("\n🤔 AI is analyzing your query...")
        response_data = support_ai.generate_response(demo_query)
        
        # Display response
        print("\n🤖 AI Response:")
        print("-" * 30)
        print(response_data['response'])
        print("-" * 30)
        
        # Display suggestions
        if response_data['suggestions']:
            print("\n💡 Suggested Actions:")
            for i, suggestion in enumerate(response_data['suggestions'], 1):
                print(f"   {i}. {suggestion}")
        
        # Check escalation
        if response_data['escalation_needed']:
            print("\n⚠️  ESCALATION NEEDED: This issue may require immediate attention!")
        
        # Show conversation summary
        print("\n📊 Conversation Summary:")
        print("-" * 30)
        summary = support_ai.get_conversation_summary()
        print(summary)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Make sure your Google Gemini API key is valid and you have credits")

def interactive_mode():
    """Run interactive mode for testing"""
    
    print("🤖 Cashfree AI Support Assistant - Interactive Mode")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    support_ai = CashfreeSupportAI()
    
    while True:
        try:
            # Get user input
            query = input("\n📝 Enter your merchant issue: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Generate response
            print("🤔 AI is thinking...")
            response_data = support_ai.generate_response(query)
            
            # Display response
            print("\n🤖 AI Response:")
            print("-" * 30)
            print(response_data['response'])
            print("-" * 30)
            
            # Display suggestions
            if response_data['suggestions']:
                print("\n💡 Suggestions:")
                for i, suggestion in enumerate(response_data['suggestions'], 1):
                    print(f"   {i}. {suggestion}")
            
            if response_data['escalation_needed']:
                print("\n⚠️  ESCALATION NEEDED!")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        run_demo() 