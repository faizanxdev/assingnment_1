"""
Data Manager for Cashfree AI Support Assistant
Handles all merchant data, mock data, and data operations from JSON files
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import random
import os

class MerchantDataManager:
    """Manages all merchant data and mock data operations from JSON files"""
    
    def __init__(self):
        """Initialize data manager with data from JSON files"""
        self.data_folder = "data"
        self.merchant_data = self._load_data_from_file("merchant_data.json")
        self.ticket_data = self._load_data_from_file("ticket_data.json")
        self.kyc_data = self._load_data_from_file("kyc_data.json")
        self.payout_data = self._load_data_from_file("payout_data.json")
        self.transaction_data = self._load_data_from_file("transaction_data.json")
        self.notification_data = self._load_data_from_file("notification_data.json")
        self.dashboard_data = self._load_data_from_file("dashboard_data.json")
    
    def _load_data_from_file(self, filename: str) -> Dict[str, Any]:
        """Load data from JSON file in data folder"""
        file_path = os.path.join(self.data_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"⚠️  Warning: {filename} not found in data folder. Using default data.")
            return self._get_default_data(filename)
        except json.JSONDecodeError:
            print(f"⚠️  Warning: Invalid JSON in {filename}. Using default data.")
            return self._get_default_data(filename)
    
    def _get_default_data(self, filename: str) -> Dict[str, Any]:
        """Get default data if file is not found or invalid"""
        defaults = {
            "merchant_data.json": {
                "merchant_id": "MERCH123456",
                "business_name": "Default Business",
                "account_status": "active",
                "account_type": "business",
                "registration_date": "2023-06-15",
                "last_activity": "2024-01-15T10:30:00Z",
                "compliance_status": "pending",
                "risk_score": "low",
                "contact_info": {
                    "email": "default@business.com",
                    "phone": "+91-0000000000",
                    "address": "Default Address"
                }
            },
            "ticket_data.json": {
                "open_tickets": 0,
                "total_tickets": 0,
                "resolved_tickets": 0,
                "average_resolution_time": "24 hours",
                "tickets": []
            },
            "kyc_data.json": {
                "merchant_id": "MERCH123456",
                "kyc_status": "pending",
                "kyc_level": "basic",
                "verification_progress": 0,
                "pending_documents": [],
                "uploaded_documents": [],
                "rejected_documents": [],
                "kyc_history": []
            },
            "payout_data.json": {
                "merchant_id": "MERCH123456",
                "payout_schedule": "T+2",
                "last_payout": "2024-01-15",
                "next_settlement": "2024-01-17",
                "total_payouts": 0,
                "payout_amount": 0,
                "pending_payouts": 0,
                "payout_history": [],
                "bank_accounts": []
            },
            "transaction_data.json": {
                "merchant_id": "MERCH123456",
                "transaction_limit": 50000,
                "daily_limit": 100000,
                "monthly_limit": 2000000,
                "current_usage": 0,
                "limit_utilization": 0,
                "transaction_count": 0,
                "average_transaction": 0,
                "limit_history": [],
                "recent_transactions": []
            },
            "notification_data.json": {
                "merchant_id": "MERCH123456",
                "email_notifications": {
                    "kyc_updates": True,
                    "payout_alerts": True,
                    "account_changes": True,
                    "ticket_updates": True,
                    "daily_summary": False,
                    "marketing_emails": False
                },
                "whatsapp_notifications": {
                    "kyc_updates": False,
                    "payout_alerts": True,
                    "account_changes": True,
                    "ticket_updates": False,
                    "transaction_alerts": True
                },
                "sms_notifications": {
                    "kyc_updates": False,
                    "payout_alerts": True,
                    "account_changes": False,
                    "ticket_updates": False,
                    "otp_verification": True
                },
                "notification_history": []
            },
            "dashboard_data.json": {
                "merchant_id": "MERCH123456",
                "weekly_trends": {
                    "transactions": [0, 0, 0, 0, 0, 0, 0],
                    "payouts": [0, 0, 0, 0, 0, 0, 0],
                    "tickets": [0, 0, 0, 0, 0, 0, 0],
                    "dates": ["2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15"]
                },
                "issue_frequency": {
                    "payout_delays": 0,
                    "kyc_issues": 0,
                    "technical_problems": 0,
                    "limit_increases": 0,
                    "account_holds": 0
                },
                "performance_metrics": {
                    "uptime": 99.8,
                    "response_time": "2.3s",
                    "success_rate": 98.5,
                    "customer_satisfaction": 4.2,
                    "average_resolution_time": "24 hours"
                },
                "monthly_summary": {
                    "total_transactions": 0,
                    "total_amount": 0,
                    "successful_transactions": 0,
                    "failed_transactions": 0,
                    "total_payouts": 0,
                    "total_tickets": 0,
                    "resolved_tickets": 0
                }
            }
        }
        return defaults.get(filename, {})
    
    def _save_data_to_file(self, filename: str, data: Dict[str, Any]) -> bool:
        """Save data to JSON file in data folder"""
        try:
            # Ensure data folder exists
            os.makedirs(self.data_folder, exist_ok=True)
            
            file_path = os.path.join(self.data_folder, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving {filename}: {str(e)}")
            return False
    
    def get_merchant_info(self, merchant_id: Optional[str] = None) -> Dict[str, Any]:
        """Get merchant information"""
        if merchant_id and merchant_id != self.merchant_data["merchant_id"]:
            return {"error": "Merchant not found"}
        return self.merchant_data.copy()
    
    def get_account_status(self) -> Dict[str, Any]:
        """Get account status information"""
        return {
            "merchant_id": self.merchant_data["merchant_id"],
            "account_status": self.merchant_data["account_status"],
            "compliance_status": self.merchant_data["compliance_status"],
            "risk_score": self.merchant_data["risk_score"],
            "last_activity": self.merchant_data["last_activity"]
        }
    
    def get_kyc_status(self) -> Dict[str, Any]:
        """Get KYC status and details"""
        return {
            "merchant_id": self.kyc_data["merchant_id"],
            "kyc_status": self.kyc_data["kyc_status"],
            "kyc_level": self.kyc_data["kyc_level"],
            "verification_progress": self.kyc_data["verification_progress"],
            "pending_documents": self.kyc_data["pending_documents"],
            "uploaded_documents": self.kyc_data["uploaded_documents"],
            "rejected_documents": self.kyc_data["rejected_documents"]
        }
    
    def get_payout_info(self) -> Dict[str, Any]:
        """Get payout and settlement information"""
        return {
            "merchant_id": self.payout_data["merchant_id"],
            "last_payout": self.payout_data["last_payout"],
            "next_settlement": self.payout_data["next_settlement"],
            "payout_schedule": self.payout_data["payout_schedule"],
            "total_payouts": self.payout_data["total_payouts"],
            "payout_amount": self.payout_data["payout_amount"],
            "pending_payouts": self.payout_data["pending_payouts"]
        }
    
    def get_transaction_limits(self) -> Dict[str, Any]:
        """Get transaction limit information"""
        return {
            "merchant_id": self.transaction_data["merchant_id"],
            "transaction_limit": self.transaction_data["transaction_limit"],
            "daily_limit": self.transaction_data["daily_limit"],
            "monthly_limit": self.transaction_data["monthly_limit"],
            "current_usage": self.transaction_data["current_usage"],
            "limit_utilization": self.transaction_data["limit_utilization"]
        }
    
    def get_support_tickets(self) -> Dict[str, Any]:
        """Get support ticket information"""
        return {
            "merchant_id": self.ticket_data.get("merchant_id", "MERCH123456"),
            "open_tickets": self.ticket_data["open_tickets"],
            "total_tickets": self.ticket_data["total_tickets"],
            "resolved_tickets": self.ticket_data["resolved_tickets"],
            "average_resolution_time": self.ticket_data["average_resolution_time"],
            "tickets": self.ticket_data["tickets"]
        }
    
    def get_notification_preferences(self) -> Dict[str, Any]:
        """Get notification preferences"""
        return {
            "merchant_id": self.notification_data["merchant_id"],
            "email_notifications": self.notification_data["email_notifications"],
            "whatsapp_notifications": self.notification_data["whatsapp_notifications"],
            "sms_notifications": self.notification_data["sms_notifications"]
        }
    
    def get_dashboard_insights(self) -> Dict[str, Any]:
        """Get dashboard analytics and insights"""
        return {
            "merchant_id": self.dashboard_data["merchant_id"],
            "weekly_trends": self.dashboard_data["weekly_trends"],
            "issue_frequency": self.dashboard_data["issue_frequency"],
            "performance_metrics": self.dashboard_data["performance_metrics"]
        }
    
    def get_relevant_data_for_query(self, query: str) -> Dict[str, Any]:
        """Get relevant data based on query keywords"""
        query_lower = query.lower()
        
        # Account Status & Holds
        if any(word in query_lower for word in ["account", "hold", "freeze", "status", "unlock"]):
            return self.get_account_status()
        
        # KYC & Compliance
        elif any(word in query_lower for word in ["kyc", "verification", "document", "pan", "address", "compliance"]):
            return self.get_kyc_status()
        
        # Payout Issues
        elif any(word in query_lower for word in ["payout", "settlement", "payment", "delay"]):
            return self.get_payout_info()
        
        # Transaction & Limits
        elif any(word in query_lower for word in ["limit", "transaction", "threshold", "increase"]):
            return self.get_transaction_limits()
        
        # Support Tickets
        elif any(word in query_lower for word in ["ticket", "support", "escalate", "create"]):
            return self.get_support_tickets()
        
        # Notifications & Preferences
        elif any(word in query_lower for word in ["alert", "notification", "email", "whatsapp", "preference"]):
            return self.get_notification_preferences()
        
        # Dashboard Insights
        elif any(word in query_lower for word in ["dashboard", "trend", "analysis", "performance", "summary"]):
            return self.get_dashboard_insights()
        
        # Default merchant info
        else:
            return {"merchant_id": self.merchant_data["merchant_id"]}
    
    def update_merchant_data(self, field: str, value: Any) -> bool:
        """Update merchant data and save to file"""
        if field in self.merchant_data:
            self.merchant_data[field] = value
            return self._save_data_to_file("merchant_data.json", self.merchant_data)
        return False
    
    def create_support_ticket(self, subject: str, description: str, priority: str = "medium") -> Dict[str, Any]:
        """Create a new support ticket and save to file"""
        ticket_id = f"TKT{random.randint(100, 999)}"
        new_ticket = {
            "ticket_id": ticket_id,
            "subject": subject,
            "description": description,
            "status": "open",
            "priority": priority,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "merchant_id": self.merchant_data["merchant_id"]
        }
        
        self.ticket_data["tickets"].append(new_ticket)
        self.ticket_data["open_tickets"] += 1
        self.ticket_data["total_tickets"] += 1
        
        # Save updated ticket data to file
        self._save_data_to_file("ticket_data.json", self.ticket_data)
        
        return new_ticket
    
    def update_ticket_status(self, ticket_id: str, status: str) -> bool:
        """Update ticket status and save to file"""
        for ticket in self.ticket_data["tickets"]:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = status
                ticket["last_updated"] = datetime.now().isoformat()
                
                if status == "resolved":
                    self.ticket_data["open_tickets"] = max(0, self.ticket_data["open_tickets"] - 1)
                    self.ticket_data["resolved_tickets"] += 1
                
                self._save_data_to_file("ticket_data.json", self.ticket_data)
                return True
        return False
    
    def add_kyc_document(self, document_type: str, status: str = "pending") -> bool:
        """Add KYC document and save to file"""
        if document_type not in self.kyc_data["uploaded_documents"]:
            self.kyc_data["uploaded_documents"].append(document_type)
            
            # Update KYC history
            history_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "action": f"Document uploaded: {document_type}",
                "status": status,
                "document_type": document_type
            }
            self.kyc_data["kyc_history"].append(history_entry)
            
            # Update verification progress
            total_docs = len(self.kyc_data["pending_documents"]) + len(self.kyc_data["uploaded_documents"])
            self.kyc_data["verification_progress"] = int((len(self.kyc_data["uploaded_documents"]) / total_docs) * 100)
            
            self._save_data_to_file("kyc_data.json", self.kyc_data)
            return True
        return False
    
    def get_all_data_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of all merchant data"""
        return {
            "merchant_info": self.get_merchant_info(),
            "account_status": self.get_account_status(),
            "kyc_status": self.get_kyc_status(),
            "payout_info": self.get_payout_info(),
            "transaction_limits": self.get_transaction_limits(),
            "support_tickets": self.get_support_tickets(),
            "notification_preferences": self.get_notification_preferences(),
            "dashboard_insights": self.get_dashboard_insights()
        }
    
    def reload_data(self) -> bool:
        """Reload all data from JSON files"""
        try:
            self.merchant_data = self._load_data_from_file("merchant_data.json")
            self.ticket_data = self._load_data_from_file("ticket_data.json")
            self.kyc_data = self._load_data_from_file("kyc_data.json")
            self.payout_data = self._load_data_from_file("payout_data.json")
            self.transaction_data = self._load_data_from_file("transaction_data.json")
            self.notification_data = self._load_data_from_file("notification_data.json")
            self.dashboard_data = self._load_data_from_file("dashboard_data.json")
            return True
        except Exception as e:
            print(f"❌ Error reloading data: {str(e)}")
            return False 