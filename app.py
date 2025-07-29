"""
Flask API for AI Customer Support Assistant
Comprehensive endpoints for all merchant support scenarios with separate data management
"""
from flask import Flask, request, jsonify, render_template_string
from support_ai import CashfreeSupportAI
from data_manager import MerchantDataManager
from config import Config
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize AI support assistant and data manager
support_ai = CashfreeSupportAI()
data_manager = MerchantDataManager()

@app.route('/')
def home():
    """Comprehensive demo interface with all merchant scenarios"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cashfree AI Support Assistant</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                background: rgba(255, 255, 255, 0.95); 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                color: #333;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .scenario-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .scenario-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
                transition: transform 0.3s ease;
            }
            .scenario-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            }
            .scenario-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 15px;
                color: #333;
            }
            .demo-query {
                background: #f8f9fa;
                padding: 12px;
                margin: 8px 0;
                border-radius: 8px;
                cursor: pointer;
                border: 1px solid #e9ecef;
                transition: all 0.3s ease;
                font-size: 0.9em;
            }
            .demo-query:hover {
                background: #667eea;
                color: white;
                transform: scale(1.02);
            }
            .custom-input {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                margin-top: 20px;
            }
            input[type="text"] { 
                width: 100%; 
                padding: 15px; 
                margin: 10px 0; 
                border: 2px solid #e9ecef; 
                border-radius: 8px; 
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            button { 
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
                transition: transform 0.3s ease;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            .response { 
                background: white; 
                padding: 20px; 
                margin: 20px 0; 
                border-radius: 10px; 
                border-left: 4px solid #667eea;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .loading {
                text-align: center;
                padding: 20px;
                color: #667eea;
                font-size: 1.2em;
            }
            .suggestions {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }
            .suggestions h4 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .suggestions ul {
                margin: 0;
                padding-left: 20px;
            }
            .escalation-warning {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }
            .merchant-data {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                font-family: monospace;
                font-size: 0.9em;
            }
            .data-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            .data-tab {
                padding: 10px 20px;
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .data-tab:hover {
                background: #667eea;
                color: white;
            }
            .data-tab.active {
                background: #667eea;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Cashfree AI Support Assistant</h1>
                <p>Comprehensive AI-powered support for all merchant scenarios</p>
            </div>
            
            <div class="scenario-grid">
                <!-- Account Status & Holds -->
                <div class="scenario-card">
                    <div class="scenario-title">🔐 Account Status & Holds</div>
                    <div class="demo-query" onclick="askQuestion('Why is my account on hold?')">
                        Why is my account on hold?
                    </div>
                    <div class="demo-query" onclick="askQuestion('How can I unlock my account?')">
                        How can I unlock my account?
                    </div>
                    <div class="demo-query" onclick="askQuestion('When will my account be reactivated?')">
                        When will my account be reactivated?
                    </div>
                    <div class="demo-query" onclick="askQuestion('What are the reasons for account suspension?')">
                        What are the reasons for account suspension?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Check if my account is active.')">
                        Check if my account is active.
                    </div>
                </div>

                <!-- KYC & Compliance -->
                <div class="scenario-card">
                    <div class="scenario-title">🪪 KYC & Compliance</div>
                    <div class="demo-query" onclick="askQuestion('How do I complete my KYC?')">
                        How do I complete my KYC?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Upload my PAN card for verification.')">
                        Upload my PAN card for verification.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Check my KYC status.')">
                        Check my KYC status.
                    </div>
                    <div class="demo-query" onclick="askQuestion('What documents are needed for KYC verification?')">
                        What documents are needed for KYC verification?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Why was my KYC rejected?')">
                        Why was my KYC rejected?
                    </div>
                </div>

                <!-- Payout Issues -->
                <div class="scenario-card">
                    <div class="scenario-title">💸 Payout Issues</div>
                    <div class="demo-query" onclick="askQuestion('Why is today\'s payout delayed?')">
                        Why is today's payout delayed?
                    </div>
                    <div class="demo-query" onclick="askQuestion('What\'s the status of my last payout?')">
                        What's the status of my last payout?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Enable instant payouts.')">
                        Enable instant payouts.
                    </div>
                    <div class="demo-query" onclick="askQuestion('When is my next settlement scheduled?')">
                        When is my next settlement scheduled?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Show payout summary for this week.')">
                        Show payout summary for this week.
                    </div>
                </div>

                <!-- Transaction & Limits -->
                <div class="scenario-card">
                    <div class="scenario-title">📈 Transaction & Limits</div>
                    <div class="demo-query" onclick="askQuestion('What is my current transaction limit?')">
                        What is my current transaction limit?
                    </div>
                    <div class="demo-query" onclick="askQuestion('How do I increase my transaction threshold?')">
                        How do I increase my transaction threshold?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Why was my transaction limit reduced?')">
                        Why was my transaction limit reduced?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Apply for a higher settlement cap.')">
                        Apply for a higher settlement cap.
                    </div>
                </div>

                <!-- Support Tickets -->
                <div class="scenario-card">
                    <div class="scenario-title">🧾 Support Tickets</div>
                    <div class="demo-query" onclick="askQuestion('Create a support ticket for payout failure.')">
                        Create a support ticket for payout failure.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Escalate my support ticket to a manager.')">
                        Escalate my support ticket to a manager.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Update my support ticket with more info.')">
                        Update my support ticket with more info.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Show me all open support tickets.')">
                        Show me all open support tickets.
                    </div>
                </div>

                <!-- Self-Help & Action Guides -->
                <div class="scenario-card">
                    <div class="scenario-title">🧠 Self-Help & Action Guides</div>
                    <div class="demo-query" onclick="askQuestion('Give me a step-by-step guide to fix payout issues.')">
                        Give me a step-by-step guide to fix payout issues.
                    </div>
                    <div class="demo-query" onclick="askQuestion('What should I do if my account is frozen?')">
                        What should I do if my account is frozen?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Walk me through the onboarding process.')">
                        Walk me through the onboarding process.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Explain how to verify my documents.')">
                        Explain how to verify my documents.
                    </div>
                </div>

                <!-- Notifications & Preferences -->
                <div class="scenario-card">
                    <div class="scenario-title">📩 Notifications & Preferences</div>
                    <div class="demo-query" onclick="askQuestion('Enable email alerts for KYC updates.')">
                        Enable email alerts for KYC updates.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Notify me when a payout is initiated.')">
                        Notify me when a payout is initiated.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Turn on WhatsApp alerts for account changes.')">
                        Turn on WhatsApp alerts for account changes.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Set daily email summary for my account.')">
                        Set daily email summary for my account.
                    </div>
                </div>

                <!-- Dashboard Insights -->
                <div class="scenario-card">
                    <div class="scenario-title">📊 Dashboard Insights</div>
                    <div class="demo-query" onclick="askQuestion('Show me weekly ticket trend analysis.')">
                        Show me weekly ticket trend analysis.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Which issue occurs most often in my account?')">
                        Which issue occurs most often in my account?
                    </div>
                    <div class="demo-query" onclick="askQuestion('Visualize payout performance in the last month.')">
                        Visualize payout performance in the last month.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Provide a dashboard summary in one message.')">
                        Provide a dashboard summary in one message.
                    </div>
                </div>

                <!-- Admin Functions -->
                <div class="scenario-card">
                    <div class="scenario-title">🛠️ Admin Functions</div>
                    <div class="demo-query" onclick="askQuestion('View all merchant KYC pending list.')">
                        View all merchant KYC pending list.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Show merchants with payout delays today.')">
                        Show merchants with payout delays today.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Create ticket on behalf of merchant ID 4567.')">
                        Create ticket on behalf of merchant ID 4567.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Send compliance reminder to all merchants.')">
                        Send compliance reminder to all merchants.
                    </div>
                </div>

                <!-- Testing & Debugging -->
                <div class="scenario-card">
                    <div class="scenario-title">🧪 Testing & Debugging</div>
                    <div class="demo-query" onclick="askQuestion('Test KYC submission flow.')">
                        Test KYC submission flow.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Simulate payout error and response.')">
                        Simulate payout error and response.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Return a fake ticket summary for testing.')">
                        Return a fake ticket summary for testing.
                    </div>
                    <div class="demo-query" onclick="askQuestion('Run all tools in dry-run mode.')">
                        Run all tools in dry-run mode.
                    </div>
                </div>
            </div>
            
            <div class="custom-input">
                <h3>💬 Ask Your Own Question:</h3>
                <input type="text" id="queryInput" placeholder="Describe your merchant issue or ask any question..." onkeypress="handleKeyPress(event)">
                <button onclick="askQuestion()">Ask AI Assistant</button>
            </div>
            
            <div id="response"></div>
            
            <!-- Data Management Section -->
            <div style="margin-top: 30px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                <h3>📊 Data Management</h3>
                <div class="data-tabs">
                    <div class="data-tab active" onclick="showData('merchant')">Merchant Info</div>
                    <div class="data-tab" onclick="showData('account')">Account Status</div>
                    <div class="data-tab" onclick="showData('kyc')">KYC Status</div>
                    <div class="data-tab" onclick="showData('payout')">Payout Info</div>
                    <div class="data-tab" onclick="showData('tickets')">Support Tickets</div>
                    <div class="data-tab" onclick="showData('limits')">Transaction Limits</div>
                    <div class="data-tab" onclick="showData('notifications')">Notifications</div>
                    <div class="data-tab" onclick="showData('dashboard')">Dashboard Insights</div>
                </div>
                <div id="dataDisplay"></div>
            </div>
        </div>
        
        <script>
            async function askQuestion(question = null) {
                const query = question || document.getElementById('queryInput').value;
                if (!query) return;
                
                document.getElementById('response').innerHTML = '<div class="loading">🤔 AI is thinking...</div>';
                
                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: query })
                    });
                    
                    const data = await response.json();
                    
                    let html = '<div class="response">';
                    html += '<h4>🤖 AI Response:</h4>';
                    html += '<p>' + (data.response || 'No response available').replace(/\\n/g, '<br>') + '</p>';
                    
                    if (data.suggestions && Array.isArray(data.suggestions) && data.suggestions.length > 0) {
                        html += '<div class="suggestions">';
                        html += '<h4>💡 Suggested Actions:</h4><ul>';
                        data.suggestions.forEach(suggestion => {
                            html += '<li>' + (suggestion || '') + '</li>';
                        });
                        html += '</ul></div>';
                    }
                    
                    if (data.escalation_needed) {
                        html += '<div class="escalation-warning">';
                        html += '<strong>⚠️ ESCALATION NEEDED:</strong> This issue may require immediate attention!';
                        html += '</div>';
                    }
                    
                    if (data.merchant_data && Object.keys(data.merchant_data).length > 0) {
                        html += '<div class="merchant-data">';
                        html += '<h4>📊 Relevant Merchant Data:</h4>';
                        html += '<pre>' + JSON.stringify(data.merchant_data, null, 2) + '</pre>';
                        html += '</div>';
                    }
                    
                    html += '</div>';
                    document.getElementById('response').innerHTML = html;
                    
                } catch (error) {
                    document.getElementById('response').innerHTML = '<div class="response" style="color: red;">❌ Error: ' + error.message + '</div>';
                }
            }
            
            async function showData(dataType) {
                // Update active tab
                document.querySelectorAll('.data-tab').forEach(tab => tab.classList.remove('active'));
                event.target.classList.add('active');
                
                try {
                    const response = await fetch(`/api/data/${dataType}`);
                    const data = await response.json();
                    
                    let html = '<div class="merchant-data">';
                    html += `<h4>📊 ${dataType.charAt(0).toUpperCase() + dataType.slice(1)} Data:</h4>`;
                    html += '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    html += '</div>';
                    
                    document.getElementById('dataDisplay').innerHTML = html;
                    
                } catch (error) {
                    document.getElementById('dataDisplay').innerHTML = '<div style="color: red;">❌ Error loading data</div>';
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    askQuestion();
                }
            }
            
            // Load initial data
            window.onload = function() {
                showData('merchant');
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle merchant support queries"""
    try:
        # Get query from request
        data = request.get_json()
        merchant_query = data.get('query', '')
        
        if not merchant_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Get optional ticket history
        ticket_history = data.get('ticket_history', None)
        
        # Generate AI response
        try:
            response_data = support_ai.generate_response(merchant_query, ticket_history)
            return jsonify(response_data)
        except Exception as ai_error:
            # Fallback response when AI is not available
            fallback_response = {
                'response': f"🤖 Demo Mode: I understand your query about '{merchant_query}'. This is a demonstration response since the AI service is not configured.\n\nTo enable full AI functionality, please:\n1. Get an OpenAI API key from https://platform.openai.com/api-keys\n2. Add it to your .env file\n3. Restart the application\n\nFor now, you can explore the data management features below!",
                'suggestions': [
                    'Check your merchant data in the tabs below',
                    'View your account status and KYC information',
                    'Explore payout and transaction data',
                    'Review support tickets and notifications'
                ],
                'escalation_needed': False,
                'merchant_data': data_manager.get_relevant_data_for_query(merchant_query)
            }
            return jsonify(fallback_response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_query():
    """Analyze and categorize merchant query"""
    try:
        data = request.get_json()
        merchant_query = data.get('query', '')
        
        if not merchant_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Analyze query
        analysis = support_ai.analyze_query(merchant_query)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary', methods=['GET'])
def get_conversation_summary():
    """Get summary of conversation history"""
    try:
        summary = support_ai.get_conversation_summary()
        return jsonify({'summary': summary})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenario/<scenario_type>', methods=['POST'])
def handle_scenario(scenario_type):
    """Handle specific merchant scenarios"""
    try:
        data = request.get_json()
        merchant_query = data.get('query', '')
        
        if not merchant_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Handle specific scenario
        response_data = support_ai.handle_specific_scenario(scenario_type, merchant_query)
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Data Management Endpoints
@app.route('/api/data/merchant', methods=['GET'])
def get_merchant_data():
    """Get merchant information"""
    try:
        data = data_manager.get_merchant_info()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/account', methods=['GET'])
def get_account_data():
    """Get account status data"""
    try:
        data = data_manager.get_account_status()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/kyc', methods=['GET'])
def get_kyc_data():
    """Get KYC status data"""
    try:
        data = data_manager.get_kyc_status()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/payout', methods=['GET'])
def get_payout_data():
    """Get payout information"""
    try:
        data = data_manager.get_payout_info()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/tickets', methods=['GET'])
def get_tickets_data():
    """Get support tickets data"""
    try:
        data = data_manager.get_support_tickets()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/limits', methods=['GET'])
def get_limits_data():
    """Get transaction limits data"""
    try:
        data = data_manager.get_transaction_limits()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/notifications', methods=['GET'])
def get_notifications_data():
    """Get notification preferences"""
    try:
        data = data_manager.get_notification_preferences()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard insights"""
    try:
        data = data_manager.get_dashboard_insights()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/summary', methods=['GET'])
def get_all_data_summary():
    """Get comprehensive data summary"""
    try:
        data = data_manager.get_all_data_summary()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/reload', methods=['POST'])
def reload_data():
    """Reload all data from JSON files"""
    try:
        success = data_manager.reload_data()
        if success:
            return jsonify({'message': 'Data reloaded successfully'})
        else:
            return jsonify({'error': 'Failed to reload data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/files', methods=['GET'])
def list_data_files():
    """List all available data files"""
    try:
        import os
        data_folder = "data"
        if not os.path.exists(data_folder):
            return jsonify({'files': [], 'message': 'Data folder not found'})
        
        files = []
        for filename in os.listdir(data_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(data_folder, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    'filename': filename,
                    'size': file_size,
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ticket/create', methods=['POST'])
def create_ticket():
    """Create a new support ticket"""
    try:
        data = request.get_json()
        subject = data.get('subject', '')
        description = data.get('description', '')
        priority = data.get('priority', 'medium')
        
        if not subject or not description:
            return jsonify({'error': 'Subject and description are required'}), 400
        
        ticket = data_manager.create_support_ticket(subject, description, priority)
        return jsonify(ticket)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ticket/<ticket_id>/status', methods=['PUT'])
def update_ticket_status(ticket_id):
    """Update ticket status"""
    try:
        data = request.get_json()
        status = data.get('status', '')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        success = data_manager.update_ticket_status(ticket_id, status)
        if success:
            return jsonify({'message': f'Ticket {ticket_id} status updated to {status}'})
        else:
            return jsonify({'error': 'Ticket not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/kyc/document', methods=['POST'])
def add_kyc_document():
    """Add KYC document"""
    try:
        data = request.get_json()
        document_type = data.get('document_type', '')
        status = data.get('status', 'pending')
        
        if not document_type:
            return jsonify({'error': 'Document type is required'}), 400
        
        success = data_manager.add_kyc_document(document_type, status)
        if success:
            return jsonify({'message': f'Document {document_type} added successfully'})
        else:
            return jsonify({'error': 'Document already exists'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check if OpenAI API key is configured
    if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == 'your_openai_api_key_here':
        print("⚠️  Warning: Please set your OpenAI API key in .env file")
        print("   Copy env_example.txt to .env and add your API key")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_DEBUG
    ) 