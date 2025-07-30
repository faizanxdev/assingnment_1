# 🚀 Deployment Guide - Cashfree AI Support Assistant

This guide will help you deploy your Cashfree AI Customer Support Assistant to various free hosting platforms.

## 📋 Prerequisites

1. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **GitHub Account**: Create at [github.com](https://github.com)
3. **Git**: Install Git on your computer

## 🌐 Option 1: Vercel (Recommended - Free)

### Step 1: Prepare Your Code
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for Vercel deployment"
```

### Step 2: Push to GitHub
```bash
# Create a new repository on GitHub
# Then push your code
git remote add origin https://github.com/yourusername/cashfree-ai-support.git
git push -u origin main
```

### Step 3: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Configure environment variables:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```
6. Click "Deploy"
7. Wait 2-3 minutes for build
8. Your app will be live at `https://your-project-name.vercel.app`

## 🚂 Option 2: Railway (Free Tier)

### Step 1: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Add environment variables:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```
7. Railway will automatically deploy your app

## 🎨 Option 3: Render (Free Tier)

### Step 1: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: cashfree-ai-support
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```
7. Click "Create Web Service"

## 🦸 Option 4: Heroku (Free Tier - Limited)

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create Procfile
```bash
# Create Procfile (no extension)
echo "web: gunicorn app:app" > Procfile
```

### Step 3: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY=your-actual-gemini-api-key-here
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=False

# Deploy
git push heroku main

# Open your app
heroku open
```

## 🐍 Option 5: PythonAnywhere (Free Tier)

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create a free account

### Step 2: Upload Files
1. Go to "Files" tab
2. Upload all your project files
3. Create a new directory for your project

### Step 3: Configure WSGI
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" and Python 3.9
4. Edit the WSGI file:
```python
import sys
path = '/home/yourusername/your-project-directory'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 4: Set Environment Variables
1. Go to "Web" tab
2. Click "Environment variables"
3. Add:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

## 🔧 Environment Variables

For all platforms, make sure to set these environment variables:

```bash
GEMINI_API_KEY=your-actual-gemini-api-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🧪 Testing Your Deployment

After deployment, test your app:

1. **Web Interface**: Visit your app URL
2. **API Testing**: Use curl or Postman
   ```bash
   curl -X POST https://your-app-url/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Why is my account on hold?"}'
   ```

## 🔍 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` has all dependencies
   - Ensure Python version is compatible
   - Verify all files are committed

2. **Environment Variables**
   - Make sure API key is set correctly
   - Check variable names match exactly
   - Restart app after setting variables

3. **Import Errors**
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility
   - Ensure all files are uploaded

4. **App Not Starting**
   - Check logs for error messages
   - Verify WSGI configuration
   - Ensure port is correctly configured

## 📊 Platform Comparison

| Platform | Free Tier | Ease of Use | Custom Domain | SSL | Auto-Deploy |
|----------|-----------|-------------|---------------|-----|-------------|
| **Vercel** | ✅ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Railway** | ✅ | ⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Render** | ✅ | ⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Heroku** | ⚠️ Limited | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **PythonAnywhere** | ✅ | ⭐⭐ | ❌ | ✅ | ❌ |

## 🎯 Recommended Deployment

**For beginners**: Use **Vercel** - it's the easiest and most reliable
**For advanced users**: Use **Railway** or **Render** for more control

## 🚀 Next Steps After Deployment

1. **Set up custom domain** (optional)
2. **Configure monitoring** and logging
3. **Set up CI/CD** for automatic deployments
4. **Add analytics** to track usage
5. **Implement caching** for better performance

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Review error logs
3. Verify environment variables
4. Test locally first
5. Check GitHub issues for similar problems

---

**Happy Deploying! 🎉** 