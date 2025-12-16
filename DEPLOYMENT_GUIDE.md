# 🚀 Deployment Guide - Stock Exchange Dashboard

## Quick Deployment Options

### ⭐ Option 1: Streamlit Community Cloud (FREE - RECOMMENDED)

**Best for:** Free hosting, easiest deployment, auto-updates from GitHub

#### Step-by-Step:

1. **Push to GitHub**
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Stock Exchange Dashboard - Ready for deployment"
   
   # Create repository on GitHub.com
   # Then push your code
   git remote add origin https://github.com/YOUR_USERNAME/stock-dashboard.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub account
   - Select your repository: `stock-dashboard`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait 2-3 minutes** - Your app will be live at:
   `https://YOUR_USERNAME-stock-dashboard-app-xyz.streamlit.app`

**✅ Advantages:**
- ✅ 100% FREE
- ✅ Auto-deploys on git push
- ✅ Free SSL certificate
- ✅ Custom domain support
- ✅ Built-in monitoring

---

### 🐍 Option 2: Render (FREE)

**Best for:** Alternative free hosting with more control

#### Steps:

1. **Create `render.yaml`** (already in your project)
2. **Push to GitHub** (same as above)
3. **Deploy on Render:**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT`
   - Click "Create Web Service"

**Live URL:** `https://stock-dashboard.onrender.com`

---

### ☁️ Option 3: Heroku (Paid after free tier)

**Best for:** Production apps with custom domains

#### Setup Files Needed:

**Create `Procfile`:**
```bash
web: sh setup.sh && streamlit run app.py
```

**Create `setup.sh`:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

#### Deploy:
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create stock-exchange-dashboard

# Deploy
git push heroku main

# Open app
heroku open
```

---

### 🐳 Option 4: Docker Deployment

**Best for:** Self-hosting, cloud platforms (AWS, GCP, Azure)

**Create `Dockerfile`:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Deploy:**
```bash
# Build image
docker build -t stock-dashboard .

# Run locally
docker run -p 8501:8501 stock-dashboard

# Push to Docker Hub
docker tag stock-dashboard YOUR_USERNAME/stock-dashboard
docker push YOUR_USERNAME/stock-dashboard

# Deploy to any cloud platform using this image
```

---

### 🌐 Option 5: AWS EC2 (Self-Hosted)

**Best for:** Full control, custom configuration

#### Steps:

1. **Launch EC2 Instance** (Ubuntu 22.04)
2. **SSH into instance**
3. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx -y
   pip3 install -r requirements.txt
   ```

4. **Run with systemd:**
   Create `/etc/systemd/system/streamlit.service`:
   ```ini
   [Unit]
   Description=Streamlit Stock Dashboard
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/stock-dashboard
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start service:**
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   ```

6. **Configure Nginx** as reverse proxy
7. **Add SSL** with Let's Encrypt

---

## 📋 Pre-Deployment Checklist

### Required Files:

✅ **requirements.txt** (already exists)
```txt
streamlit==1.28.1
pandas==2.1.1
numpy==1.24.3
requests==2.31.0
plotly==5.17.0
scikit-learn==1.3.1
yfinance==0.2.28
python-dotenv==1.0.0
ta==0.11.0
```

✅ **app.py** - Main application
✅ **utils.py** - Utility functions
✅ **chatbot.py** - Chatbot module
✅ **stock_predictor.py** - ML predictor

### Optional but Recommended:

**Create `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#ff6f00"
backgroundColor = "#1a237e"
secondaryBackgroundColor = "#283593"
textColor = "#ffffff"

[server]
maxUploadSize = 200
```

**Create `.gitignore`:**
```
__pycache__/
*.pyc
*.pyo
.env
.venv
venv/
*.log
.streamlit/secrets.toml
```

---

## 🔐 Environment Variables (for API Keys)

**For production, use secrets management:**

### Streamlit Cloud:
1. Go to app settings
2. Click "Secrets"
3. Add:
   ```toml
   ALPHA_VANTAGE_API_KEY = "CMLKV2SLOT89UPM9"
   ```

### Heroku:
```bash
heroku config:set ALPHA_VANTAGE_API_KEY=CMLKV2SLOT89UPM9
```

### Docker:
```bash
docker run -e ALPHA_VANTAGE_API_KEY=CMLKV2SLOT89UPM9 -p 8501:8501 stock-dashboard
```

---

## 🎯 Recommended: Streamlit Community Cloud

**Why?**
- ✅ Completely FREE
- ✅ Deploy in 3 clicks
- ✅ Auto-updates from GitHub
- ✅ Built-in secrets management
- ✅ No credit card required
- ✅ Perfect for this project

**Your deployment URL will be:**
`https://YOUR_USERNAME-stock-dashboard-app-xyz.streamlit.app`

---

## 📊 Performance Optimization

**For faster loading:**

1. **Add caching in `utils.py`:**
   ```python
   import streamlit as st
   
   @st.cache_data(ttl=300)  # Cache for 5 minutes
   def fetch_stock_data(symbol):
       # ... existing code
   ```

2. **Enable compression** in `.streamlit/config.toml`:
   ```toml
   [server]
   enableCompression = true
   ```

3. **Use session state** for expensive operations

---

## 🔧 Troubleshooting Deployment

### Common Issues:

**1. Module not found:**
```bash
# Ensure all packages in requirements.txt
pip freeze > requirements.txt
```

**2. Port binding error:**
```bash
# Use environment port
streamlit run app.py --server.port=$PORT
```

**3. Memory issues:**
- Reduce data fetching frequency
- Use pagination for large datasets
- Enable caching

---

## 📱 Mobile Optimization

**Add to `.streamlit/config.toml`:**
```toml
[server]
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

---

## 🚀 Quick Start (Recommended Path)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/stock-dashboard.git
git push -u origin main

# 2. Go to share.streamlit.io
# 3. Connect GitHub
# 4. Deploy app.py
# 5. Done! 🎉
```

**Your app will be live in 2-3 minutes!**

---

## 📞 Support

- **Streamlit Docs:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **GitHub Issues:** Create in your repository

---

**🎉 Happy Deploying!**
