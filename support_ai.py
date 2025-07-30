"""
AI Customer Support Assistant for Cashfree Merchant Issues
Uses LangChain + Google Gemini to provide intelligent responses for all merchant scenarios
"""
from typing import Dict, List, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from config import Config
from data_manager import MerchantDataManager
import json
from datetime import datetime, timedelta
import random

class CashfreeSupportAI:
    """AI-powered customer support assistant for Cashfree merchants"""
    
    def __init__(self):
        """Initialize the AI support assistant with Google Gemini model"""
        # Check if we have a valid API key
        self.demo_mode = not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == 'your_gemini_api_key_here' or 'demo' in Config.GEMINI_API_KEY.lower()
        
        if not self.demo_mode:
            # Initialize Google Gemini chat model
            self.llm = ChatGoogleGenerativeAI(
                model=Config.MODEL_NAME,
                google_api_key=Config.GEMINI_API_KEY,
                max_output_tokens=Config.MAX_TOKENS,
                temperature=0.7  # Balanced creativity and accuracy
            )
        else:
            self.llm = None
        
        # Initialize data manager
        self.data_manager = MerchantDataManager()
        
        # Define comprehensive system prompt for all merchant scenarios
        self.system_prompt = """
        You are an expert Cashfree merchant support assistant. Your role is to help merchants resolve ALL types of issues.
        
        You handle these categories:
        
        🔐 ACCOUNT STATUS & HOLDS:
        - Account freezes and limit holds
        - Account reactivation requests
        - Account suspension reasons
        - Account status checks
        
        🪪 KYC & COMPLIANCE:
        - KYC completion guidance
        - Document upload instructions
        - KYC status checks
        - Document requirements
        - KYC rejection reasons
        - Pending KYC tasks
        
        💸 PAYOUT ISSUES:
        - Payout delays and status
        - Instant payout enablement
        - Payout scheduling
        - Settlement schedules
        - Payout summaries
        
        📈 TRANSACTION & LIMITS:
        - Transaction limit queries
        - Limit increase requests
        - Limit reduction explanations
        - Settlement cap applications
        
        🧾 SUPPORT TICKETS:
        - Ticket creation
        - Ticket escalation
        - Ticket updates
        - Ticket closure
        - Ticket summaries
        - Open ticket lists
        
        🧠 SELF-HELP & ACTION GUIDES:
        - Step-by-step troubleshooting
        - Process explanations
        - Document verification guides
        - Compliance error explanations
        
        📩 NOTIFICATIONS & PREFERENCES:
        - Alert configurations
        - Notification settings
        - Email/WhatsApp preferences
        - Summary settings
        
        📊 DASHBOARD INSIGHTS:
        - Trend analysis
        - Issue frequency analysis
        - Performance visualization
        - Dashboard summaries
        
        🛠️ ADMIN FUNCTIONS:
        - Merchant lists
        - Bulk operations
        - Ticket creation on behalf
        - Compliance reminders
        
        Always provide:
        1. Clear step-by-step solutions
        2. Relevant documentation links
        3. Escalation paths when needed
        4. Preventive measures for future
        5. Specific action items
        
        Be professional, empathetic, and solution-focused.
        """
        
        # Initialize conversation history
        self.conversation_history: List[Dict] = []
    
    def analyze_query(self, merchant_query: str) -> Dict:
        """
        Analyze merchant query and categorize the issue
        
        Args:
            merchant_query: The merchant's question or issue description
            
        Returns:
            Dictionary with analysis results
        """
        # Create comprehensive analysis prompt
        analysis_prompt = f"""
        Analyze this merchant query and categorize the issue:
        
        Query: "{merchant_query}"
        
        Please provide:
        1. Issue category (account_hold, kyc_compliance, payout_issue, transaction_limit, support_ticket, self_help, notification, dashboard_insight, admin_function, testing)
        2. Priority level (high, medium, low)
        3. Key concerns identified
        4. Suggested immediate actions
        5. Required tools/functions to invoke
        
        Format as JSON.
        """
        
        # Get AI analysis
        analysis_response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=analysis_prompt)
        ])
        
        return {
            "query": merchant_query,
            "analysis": analysis_response.content,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_response(self, merchant_query: str, ticket_history: Optional[str] = None) -> Dict:
        """
        Generate intelligent response based on merchant query and ticket history
        
        Args:
            merchant_query: The merchant's current question
            ticket_history: Optional previous conversation history
            
        Returns:
            Dictionary with AI-generated response and suggestions
        """
        # Get relevant data from data manager
        relevant_data = self.data_manager.get_relevant_data_for_query(merchant_query)
        
        # Build context from ticket history if available
        context = ""
        if ticket_history:
            context = f"Previous conversation context:\n{ticket_history}\n\n"
        
        # Add relevant data to context
        data_context = f"Relevant merchant data:\n{json.dumps(relevant_data, indent=2)}\n\n"
        
        # Create comprehensive response generation prompt
        response_prompt = f"""
        {context}{data_context}Merchant Query: "{merchant_query}"
        
        Please provide a comprehensive response including:
        1. Immediate action steps
        2. Required documents/information
        3. Expected timeline
        4. Escalation process if needed
        5. Preventive measures
        6. Specific tools or functions to use
        7. Reference the provided merchant data when relevant
        
        Make it clear, actionable, and merchant-friendly.
        Include specific details from the merchant data when applicable.
        """
        
        # Generate AI response
        if self.demo_mode or not self.llm:
            # Demo mode response
            demo_response = self._generate_demo_response(merchant_query, relevant_data)
            conversation_entry = {
                "query": merchant_query,
                "response": demo_response,
                "timestamp": datetime.now().isoformat()
            }
            self.conversation_history.append(conversation_entry)
            
            return {
                "response": demo_response,
                "suggestions": self._generate_suggestions(merchant_query),
                "escalation_needed": self._check_escalation_needed(merchant_query),
                "conversation_id": len(self.conversation_history),
                "merchant_data": relevant_data,
                "demo_mode": True
            }
        else:
            # Real AI response
            ai_response = self.llm.invoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=response_prompt)
            ])
            
            # Store in conversation history
            conversation_entry = {
                "query": merchant_query,
                "response": ai_response.content,
                "timestamp": datetime.now().isoformat()
            }
            self.conversation_history.append(conversation_entry)
            
            return {
                "response": ai_response.content,
                "suggestions": self._generate_suggestions(merchant_query),
                "escalation_needed": self._check_escalation_needed(merchant_query),
                "conversation_id": len(self.conversation_history),
                "merchant_data": relevant_data
            }
    
    def _generate_suggestions(self, query: str) -> List[str]:
        """Generate relevant suggestions based on query"""
        query_lower = query.lower()
        suggestions = []
        
        # Account Status & Holds
        if any(word in query_lower for word in ["hold", "freeze", "account", "unlock"]):
            suggestions = [
                "Check account verification status in dashboard",
                "Review recent transaction patterns for anomalies",
                "Prepare KYC documents for review",
                "Contact support with merchant ID and transaction details",
                "Check compliance status and pending requirements"
            ]
        
        # KYC & Compliance
        elif any(word in query_lower for word in ["kyc", "verification", "document", "pan", "address"]):
            suggestions = [
                "Upload required documents in merchant portal",
                "Check KYC status in account dashboard",
                "Review document requirements checklist",
                "Contact KYC team for specific guidance",
                "Schedule a verification call if needed"
            ]
        
        # Payout Issues
        elif any(word in query_lower for word in ["payout", "settlement", "payment", "delay"]):
            suggestions = [
                "Check payout schedule in merchant portal",
                "Verify bank account details and status",
                "Review transaction volume and limits",
                "Contact settlement team with merchant ID",
                "Check for any compliance holds"
            ]
        
        # Transaction & Limits
        elif any(word in query_lower for word in ["limit", "threshold", "transaction", "increase"]):
            suggestions = [
                "Review current usage in dashboard",
                "Submit limit increase request with business proof",
                "Check compliance requirements for higher limits",
                "Contact account manager for expedited processing",
                "Monitor transaction patterns for approval"
            ]
        
        # Support Tickets
        elif any(word in query_lower for word in ["ticket", "support", "escalate", "create"]):
            suggestions = [
                "Create ticket with detailed issue description",
                "Attach relevant screenshots and documents",
                "Check ticket status in support portal",
                "Escalate to manager if urgent",
                "Follow up within 24-48 hours"
            ]
        
        # Self-Help & Action Guides
        elif any(word in query_lower for word in ["guide", "step", "how", "explain", "walk"]):
            suggestions = [
                "Follow the step-by-step guide provided",
                "Check our knowledge base for detailed instructions",
                "Watch tutorial videos in merchant portal",
                "Contact support if steps don't work",
                "Save the guide for future reference"
            ]
        
        # Notifications & Preferences
        elif any(word in query_lower for word in ["alert", "notification", "email", "whatsapp", "preference"]):
            suggestions = [
                "Update notification preferences in account settings",
                "Test notification delivery",
                "Review notification history",
                "Set up multiple contact methods",
                "Configure alert frequency and timing"
            ]
        
        # Dashboard Insights
        elif any(word in query_lower for word in ["dashboard", "trend", "analysis", "performance", "summary"]):
            suggestions = [
                "Review dashboard analytics regularly",
                "Export reports for detailed analysis",
                "Set up automated reporting",
                "Compare performance with previous periods",
                "Share insights with your team"
            ]
        
        # Admin Functions
        elif any(word in query_lower for word in ["admin", "list", "bulk", "manager"]):
            suggestions = [
                "Use admin portal for bulk operations",
                "Generate reports for management review",
                "Set up automated compliance checks",
                "Configure team access permissions",
                "Monitor system-wide metrics"
            ]
        
        # Testing & Debugging
        elif any(word in query_lower for word in ["test", "debug", "simulate", "dry-run"]):
            suggestions = [
                "Run tests in sandbox environment",
                "Check system logs for errors",
                "Verify API integrations",
                "Test all workflows thoroughly",
                "Document any issues found"
            ]
        
        else:
            suggestions = [
                "Review account dashboard for current status",
                "Check system status page for any issues",
                "Contact technical support for assistance",
                "Schedule a consultation call",
                "Review our knowledge base for solutions"
            ]
        
        return suggestions
    
    def _generate_demo_response(self, query: str, merchant_data: Dict[str, Any]) -> str:
        """Generate demo response when API key is not available"""
        query_lower = query.lower()
        
        # Account hold issues
        if any(word in query_lower for word in ["hold", "freeze", "account", "unlock"]):
            return f"""🤖 **Demo Mode Response** - Account Hold Issue

I understand you're experiencing account hold issues. Based on your merchant data, here's what I can help you with:

**Current Account Status:**
- Merchant ID: {merchant_data.get('merchant_id', 'MERCH123456')}
- Account Status: {merchant_data.get('account_status', 'active')}
- Compliance Status: {merchant_data.get('compliance_status', 'pending')}

**Immediate Action Steps:**
1. ✅ Check your account verification status in the merchant portal
2. 📋 Review and complete any pending KYC documents
3. 📞 Contact support with your merchant ID: {merchant_data.get('merchant_id', 'MERCH123456')}
4. 📊 Review recent transaction patterns for any anomalies
5. 🔍 Check compliance status and pending requirements

**Expected Timeline:** 24-48 hours for standard review process

**Note:** This is a demo response. For real AI assistance, please add a valid Google Gemini API key to your .env file."""

        # KYC issues
        elif any(word in query_lower for word in ["kyc", "verification", "document"]):
            return f"""🤖 **Demo Mode Response** - KYC Verification

I can help you with your KYC verification process. Here's your current status:

**KYC Progress:**
- Verification Progress: {merchant_data.get('verification_progress', 60)}%
- Pending Documents: {len(merchant_data.get('pending_documents', []))} items
- Uploaded Documents: {len(merchant_data.get('uploaded_documents', []))} items

**Required Actions:**
1. 📤 Upload remaining documents: {', '.join(merchant_data.get('pending_documents', ['PAN Card', 'Address Proof']))}
2. ✅ Verify document quality and clarity
3. 📋 Complete business verification form
4. 📞 Schedule verification call if needed
5. 🔍 Check KYC status in merchant portal

**Timeline:** 3-5 business days for document review

**Note:** This is a demo response. For real AI assistance, please add a valid Google Gemini API key to your .env file."""

        # Payout issues
        elif any(word in query_lower for word in ["payout", "settlement", "payment"]):
            return f"""🤖 **Demo Mode Response** - Payout Issue

I understand you're having payout concerns. Here's your current payout status:

**Payout Information:**
- Payout Schedule: {merchant_data.get('payout_schedule', 'T+2')}
- Last Payout: {merchant_data.get('last_payout', '2024-01-15')}
- Next Settlement: {merchant_data.get('next_settlement', '2024-01-17')}
- Pending Amount: ₹{merchant_data.get('pending_payouts', 0):,}

**Troubleshooting Steps:**
1. 💳 Verify bank account details are correct
2. 📊 Check transaction volume and limits
3. ⏰ Review payout schedule and timing
4. 📞 Contact settlement team with merchant ID
5. 🔍 Check for any compliance holds

**Expected Resolution:** 1-2 business days

**Note:** This is a demo response. For real AI assistance, please add a valid Google Gemini API key to your .env file."""

        # Default response
        else:
            return f"""🤖 **Demo Mode Response**

Thank you for your query: "{query}"

I can help you with various merchant support issues including:
- Account status and holds
- KYC verification and compliance
- Payout and settlement issues
- Transaction limits and processing
- Support ticket management

**Current Merchant Data:**
- Merchant ID: {merchant_data.get('merchant_id', 'MERCH123456')}
- Account Status: {merchant_data.get('account_status', 'active')}
- Open Tickets: {merchant_data.get('open_tickets', 0)}

**Next Steps:**
1. Explore the data management features below
2. Check your merchant dashboard
3. Review account status and KYC progress
4. Create support tickets if needed

**Note:** This is a demo response. For real AI assistance, please add a valid Google Gemini API key to your .env file."""

    def _check_escalation_needed(self, query: str) -> bool:
        """Determine if issue needs escalation"""
        # Comprehensive escalation keywords
        escalation_keywords = [
            "urgent", "critical", "emergency", "blocked", "frozen",
            "legal", "compliance", "regulatory", "fraud", "security",
            "escalate", "manager", "immediate", "serious", "broken",
            "not working", "failed", "error", "issue", "problem"
        ]
        
        return any(keyword in query.lower() for keyword in escalation_keywords)
    
    def get_conversation_summary(self) -> str:
        """Generate summary of conversation history"""
        if not self.conversation_history:
            return "No conversation history available."
        
        # Create summary prompt
        summary_prompt = f"""
        Summarize this support conversation:
        
        {self.conversation_history}
        
        Provide a concise summary of:
        1. Main issues discussed
        2. Solutions provided
        3. Current status
        4. Next steps
        5. Categories of issues handled
        """
        
        # Generate summary
        summary_response = self.llm.invoke([
            SystemMessage(content="You are a support conversation summarizer."),
            HumanMessage(content=summary_prompt)
        ])
        
        return summary_response.content
    
    def handle_specific_scenario(self, scenario_type: str, query: str) -> Dict:
        """
        Handle specific merchant scenarios with tailored responses
        
        Args:
            scenario_type: Type of scenario (account, kyc, payout, etc.)
            query: The merchant query
            
        Returns:
            Dictionary with scenario-specific response
        """
        # Get relevant data for the scenario
        relevant_data = self.data_manager.get_relevant_data_for_query(query)
        
        scenario_prompts = {
            "account_hold": f"""
            Handle account hold scenario for query: "{query}"
            
            Merchant Data: {json.dumps(relevant_data, indent=2)}
            
            Provide:
            1. Account status check
            2. Hold reason analysis
            3. Unlock steps
            4. Required documents
            5. Timeline for resolution
            """,
            
            "kyc_compliance": f"""
            Handle KYC compliance scenario for query: "{query}"
            
            Merchant Data: {json.dumps(relevant_data, indent=2)}
            
            Provide:
            1. KYC status check
            2. Document requirements
            3. Upload instructions
            4. Verification timeline
            5. Rejection reasons if applicable
            """,
            
            "payout_issue": f"""
            Handle payout issue scenario for query: "{query}"
            
            Merchant Data: {json.dumps(relevant_data, indent=2)}
            
            Provide:
            1. Payout status check
            2. Delay reasons
            3. Resolution steps
            4. Schedule information
            5. Contact escalation
            """,
            
            "support_ticket": f"""
            Handle support ticket scenario for query: "{query}"
            
            Merchant Data: {json.dumps(relevant_data, indent=2)}
            
            Provide:
            1. Ticket creation/update steps
            2. Escalation process
            3. Status tracking
            4. Response timeline
            5. Follow-up actions
            """
        }
        
        if scenario_type in scenario_prompts:
            prompt = scenario_prompts[scenario_type]
            response = self.llm.invoke([
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ])
            
            return {
                "scenario_type": scenario_type,
                "query": query,
                "response": response.content,
                "suggestions": self._generate_suggestions(query),
                "escalation_needed": self._check_escalation_needed(query),
                "merchant_data": relevant_data
            }
        
        return self.generate_response(query)
    
    def get_merchant_data_summary(self) -> Dict[str, Any]:
        """Get comprehensive merchant data summary"""
        return self.data_manager.get_all_data_summary()
    
    def create_support_ticket(self, subject: str, description: str, priority: str = "medium") -> Dict[str, Any]:
        """Create a new support ticket using data manager"""
        return self.data_manager.create_support_ticket(subject, description, priority) 