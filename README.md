# 🤖 Cashfree AI Customer Support Assistant

A simple AI-powered customer support assistant for Cashfree merchants using LangChain and Google Gemini. This bot helps merchants resolve account issues, payment problems, and technical queries with intelligent responses.

## 🎯 Problem Solved

Merchants face account freezes, limit holds, and poor support experiences. This AI assistant provides:
- **Intelligent query analysis** and categorization
- **Step-by-step action guides** for common issues
- **Smart suggestions** before escalation
- **Conversation history** and summaries
- **Separated data management** with file-based storage
- **Persistent data storage** in JSON files

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone or download the project
cd assingnment

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env_example.txt .env
# Edit .env and add your Google Gemini API key
```

### 2. Configure Google Gemini API

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit `.env` file and add your API key:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   ```

### 3. Run the Application

#### Option A: Web Interface (Recommended)
```bash
python app.py
```
Then open http://localhost:5000 in your browser

#### Option B: Command Line Demo
```bash
# Run the demo
python demo.py

# Or run interactive mode
python demo.py interactive
```

## 🌐 Deploy to Vercel (Free)

### Prerequisites
1. **GitHub Account**: Create a free GitHub account
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) (free)
3. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Deployment Steps

#### Step 1: Push to GitHub
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub and push
git remote add origin https://github.com/yourusername/cashfree-ai-support.git
git push -u origin main
```

#### Step 2: Deploy to Vercel
1. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Environment Variables**:
   - In Vercel dashboard, go to your project
   - Click "Settings" → "Environment Variables"
   - Add the following variables:
     ```
     GEMINI_API_KEY=your-actual-gemini-api-key-here
     FLASK_ENV=production
     FLASK_DEBUG=False
     ```

3. **Deploy**:
   - Click "Deploy" in Vercel dashboard
   - Wait for build to complete (2-3 minutes)
   - Your app will be live at `https://your-project-name.vercel.app`

### Alternative Free Deployment Options

#### 1. **Railway** (Free Tier)
- Sign up at [railway.app](https://railway.app)
- Connect GitHub repository
- Add environment variables
- Deploy automatically

#### 2. **Render** (Free Tier)
- Sign up at [render.com](https://render.com)
- Connect GitHub repository
- Add environment variables
- Deploy as web service

#### 3. **Heroku** (Free Tier - Limited)
- Sign up at [heroku.com](https://heroku.com)
- Install Heroku CLI
- Add `Procfile`:
  ```
  web: gunicorn app:app
  ```
- Deploy with `git push heroku main`

#### 4. **PythonAnywhere** (Free Tier)
- Sign up at [pythonanywhere.com](https://pythonanywhere.com)
- Upload files via web interface
- Configure WSGI file
- Set environment variables

### Environment Variables for Deployment

Make sure to set these environment variables in your deployment platform:

```bash
GEMINI_API_KEY=your-actual-gemini-api-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🎮 Demo Examples

### Example 1: Account Hold Issue
**Query:** "Why is my account on hold?"

**AI Response:**
- Analyzes account status
- Provides step-by-step resolution guide
- Suggests required documents
- Indicates escalation if needed

### Example 2: Payment Failures
**Query:** "My payments are failing, what should I do?"

**AI Response:**
- Checks payment gateway configuration
- Reviews transaction logs
- Suggests testing procedures
- Provides technical troubleshooting steps

### Example 3: Settlement Delays
**Query:** "When will my settlement arrive?"

**AI Response:**
- Checks settlement schedule
- Verifies bank account details
- Reviews transaction volume limits
- Provides timeline estimates

## 📁 Project Structure

```
assingnment/
├── app.py                 # Flask web application
├── support_ai.py         # Core AI assistant logic
├── data_manager.py       # Separate data management layer
├── config.py             # Configuration settings
├── demo.py               # Command-line demo
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── runtime.txt          # Python runtime version
├── .gitignore           # Git ignore file
├── env_example.txt      # Environment variables template
├── data/                 # Data folder with JSON files
│   ├── merchant_data.json
│   ├── ticket_data.json
│   ├── kyc_data.json
│   ├── payout_data.json
│   ├── transaction_data.json
│   ├── notification_data.json
│   └── dashboard_data.json
└── README.md            # This file
```

## 🔧 API Endpoints

### Web Interface
- `GET /` - Demo interface with data management
- `POST /api/query` - Handle merchant queries
- `POST /api/analyze` - Analyze and categorize queries
- `GET /api/summary` - Get conversation summary

### Data Management Endpoints
- `GET /api/data/merchant` - Get merchant information
- `GET /api/data/account` - Get account status data
- `GET /api/data/kyc` - Get KYC status data
- `GET /api/data/payout` - Get payout information
- `GET /api/data/tickets` - Get support tickets data
- `GET /api/data/limits` - Get transaction limits data
- `GET /api/data/notifications` - Get notification preferences
- `GET /api/data/dashboard` - Get dashboard insights
- `GET /api/data/summary` - Get comprehensive data summary
- `POST /api/data/reload` - Reload all data from files
- `GET /api/data/files` - List all data files

### Ticket Management
- `POST /api/ticket/create` - Create new support ticket
- `PUT /api/ticket/<ticket_id>/status` - Update ticket status

### KYC Management
- `POST /api/kyc/document` - Add KYC document

### Example API Usage
```bash
# Test the API directly
curl -X POST https://your-app.vercel.app/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is my account on hold?"}'

# Get merchant data
curl https://your-app.vercel.app/api/data/merchant

# Create a support ticket
curl -X POST https://your-app.vercel.app/api/ticket/create \
  -H "Content-Type: application/json" \
  -d '{"subject": "Payout issue", "description": "My payout is delayed", "priority": "high"}'

# Update ticket status
curl -X PUT https://your-app.vercel.app/api/ticket/TKT001/status \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'

# Add KYC document
curl -X POST https://your-app.vercel.app/api/kyc/document \
  -H "Content-Type: application/json" \
  -d '{"document_type": "PAN Card", "status": "pending"}'

# Reload data from files
curl -X POST https://your-app.vercel.app/api/data/reload

# List data files
curl https://your-app.vercel.app/api/data/files
```

## 🧠 AI Features

### 1. Query Analysis
- Categorizes issues (account_hold, kyc_compliance, payout_issue, etc.)
- Determines priority levels
- Identifies key concerns

### 2. Intelligent Responses
- Generates context-aware solutions
- Provides step-by-step action guides
- Suggests relevant documentation

### 3. Smart Suggestions
- Keyword-based suggestion generation
- Contextual action items
- Preventive measures

### 4. Escalation Detection
- Identifies urgent issues
- Flags cases needing human intervention
- Prioritizes critical problems

## 📊 Data Management

### File-Based Data Storage
- **`data/` folder** - Contains all JSON data files
- **Persistent storage** - Data persists between application restarts
- **Easy editing** - Modify JSON files directly
- **Version control** - Track data changes in git
- **Backup friendly** - Simple file-based backup

### Data Files Structure
```
data/
├── merchant_data.json     # Merchant basic information
├── ticket_data.json      # Support tickets and status
├── kyc_data.json         # KYC documents and progress
├── payout_data.json      # Payout schedules and history
├── transaction_data.json # Transaction limits and usage
├── notification_data.json # Notification preferences
└── dashboard_data.json   # Analytics and insights
```

### Data Categories
1. **Merchant Info** - Basic merchant details and contact info
2. **Account Status** - Account status, compliance, risk score
3. **KYC Status** - Verification progress, documents, history
4. **Payout Info** - Settlement schedules, history, bank accounts
5. **Support Tickets** - Open tickets, resolution times, status
6. **Transaction Limits** - Current limits, usage, history
7. **Notifications** - Email, WhatsApp, SMS preferences
8. **Dashboard Insights** - Trends, analytics, performance metrics

### Data Operations
- **Load from files** - Automatic loading on startup
- **Save to files** - Persistent changes to JSON files
- **Reload data** - Refresh from files without restart
- **Error handling** - Fallback to default data if files missing
- **File validation** - JSON format validation

## 🛠️ Technical Details

### Dependencies
- **LangChain**: AI framework for LLM integration
- **Google Gemini**: Gemini-1.5-flash for natural language processing
- **Flask**: Lightweight web framework
- **Python-dotenv**: Environment variable management
- **Gunicorn**: WSGI server for production deployment

### Configuration
- Model: Gemini-1.5-flash (cost-efficient)
- Max tokens: 1000 (response length limit)
- Temperature: 0.7 (balanced creativity)

### Architecture
- **Separation of Concerns**: AI logic separate from data management
- **File-Based Storage**: JSON files for persistent data
- **Modular Design**: Easy to extend and maintain
- **Data-Driven**: AI responses based on actual merchant data
- **Scalable**: Can easily add new data sources

## 🎨 Features

- ✅ **Simple and clean** - No unnecessary complexity
- ✅ **Fast responses** - Optimized for quick support
- ✅ **Beautiful UI** - Modern, responsive interface
- ✅ **Easy to understand** - Clear, actionable responses
- ✅ **Production ready** - Error handling and validation
- ✅ **Extensible** - Easy to add new features
- ✅ **Separated data** - Clean data management architecture
- ✅ **File-based storage** - Persistent data in JSON files
- ✅ **Comprehensive coverage** - All merchant scenarios handled
- ✅ **Free deployment** - Deploy to Vercel, Railway, Render, etc.

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ Error: Please set your Google Gemini API key in .env file
   ```
   **Solution:** Add your Google Gemini API key to the `.env` file or environment variables

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   **Solution:** Install dependencies with `pip install -r requirements.txt`

3. **Data File Errors**
   ```
   Warning: merchant_data.json not found in data folder
   ```
   **Solution:** Check that data folder exists and contains JSON files

4. **Deployment Issues**
   ```
   Build failed on Vercel
   ```
   **Solution:** 
   - Check `requirements.txt` has all dependencies
   - Ensure `vercel.json` is properly configured
   - Verify environment variables are set in Vercel dashboard

5. **Port Already in Use**
   ```
   Address already in use
   ```
   **Solution:** Change port in `app.py` or kill existing process

## 🚀 Next Steps

1. **Add more issue types** - Expand merchant problem categories
2. **Integration with real data** - Connect to actual merchant databases
3. **Multi-language support** - Add regional language support
4. **Advanced analytics** - Track resolution rates and satisfaction
5. **Human handoff** - Seamless escalation to human agents
6. **Database integration** - Replace JSON files with real database
7. **Real-time updates** - Live data synchronization
8. **Advanced reporting** - Detailed analytics and insights
9. **Data validation** - Schema validation for JSON files
10. **Data migration** - Tools to migrate between data formats

## 📝 License

This project is for demonstration purposes. Feel free to modify and extend for your needs.

---

**Built with ❤️ for better merchant support experiences** 