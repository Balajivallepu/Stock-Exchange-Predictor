# 📊 Stock Exchange Prediction Dashboard

## Complete Installation & Setup Guide

### 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Visual Studio Code (recommended)
- Internet connection

---

## 🚀 Step-by-Step Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
```bash
python --version
```

### Step 2: Install VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install Python extension in VS Code
3. Restart VS Code

### Step 3: Create Project Folder

```bash
# Create project directory
mkdir stock-prediction-dashboard
cd stock-prediction-dashboard
```

### Step 4: Create Project Files

Create the following files with the code provided:

1. **requirements.txt** - Dependencies
2. **utils.py** - Helper functions
3. **chatbot.py** - AI Chatbot
4. **stock_predictor.py** - ML Predictions
5. **app.py** - Main application (combine Part 1 & Part 2)

### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit
- pandas
- numpy
- requests
- plotly
- scikit-learn
- yfinance
- python-dotenv
- ta

### Step 7: Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📁 Complete File Structure

```
stock-prediction-dashboard/
│
├── venv/                  # Virtual environment (auto-generated)
├── data/                  # Data storage (auto-generated)
│
├── app.py                 # Main Streamlit application
├── utils.py              # Utility functions & API calls
├── chatbot.py            # AI Chatbot functionality
├── stock_predictor.py    # ML prediction models
├── requirements.txt      # Dependencies
└── README.md            # This file
```

---

## 🔑 API Keys Setup

Your Alpha Vantage API keys are already configured in the `utils.py` file:
- Key 1: `4FTSL912D28NL2OV`
- Key 2: `CMLKV2SLOT89UPM9`

The app automatically rotates between these keys to avoid rate limits.

---

## 🎯 Features Overview

### 1. 🏠 Dashboard
- Live stock quotes
- Interactive price charts
- Technical indicators (RSI, MACD, Bollinger Bands)
- Trading recommendations

### 2. 📡 Live Data
- Real-time multi-stock tracking
- Auto-refresh every 60 seconds
- Grid view with key metrics

### 3. 🤖 AI Chatbot
- Natural language queries
- Stock price lookups
- Technical analysis
- Buy/sell recommendations

### 4. 🔮 Predictions
- 7-14 day price forecasts
- Machine learning models
- Support/Resistance levels
- Confidence metrics

### 5. 📊 Technical Analysis
- Trend analysis with moving averages
- Momentum indicators (RSI, MACD)
- Volume analysis
- Detailed reports

### 6. ℹ️ About
- Project information
- Features list
- Technology stack

---

## 💡 Usage Examples

### Dashboard
1. Select market (NSE/BSE/US)
2. Choose a stock from dropdown
3. View live prices and charts
4. Check recommendations

### Chatbot
Ask questions like:
- "What's the price of RELIANCE?"
- "Should I buy TCS?"
- "Analyze INFY stock"
- "What's the RSI of HDFCBANK?"

### Predictions
1. Select a stock
2. Choose prediction period (1-14 days)
3. Click "Generate Predictions"
4. View forecast chart and confidence

---

## 🔧 Troubleshooting

### Issue: Module not found
**Solution:** Make sure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Issue: API rate limit exceeded
**Solution:** Wait 1 minute or use the second API key. The app rotates automatically.

### Issue: Stock data not loading
**Solution:** 
- Check internet connection
- Verify stock symbol is correct
- Try different stock or market

### Issue: Port already in use
**Solution:** Run on different port:
```bash
streamlit run app.py --server.port 8502
```

---

## 📊 Supported Stocks

### NSE (National Stock Exchange)
- RELIANCE - Reliance Industries
- TCS - Tata Consultancy Services
- HDFCBANK - HDFC Bank
- INFY - Infosys
- ICICIBANK - ICICI Bank
- And more...

### BSE (Bombay Stock Exchange)
- Same stocks with .BO suffix

### US Markets
- AAPL - Apple Inc.
- MSFT - Microsoft
- GOOGL - Alphabet
- AMZN - Amazon
- TSLA - Tesla
- And more...

---

## 📚 Python Concepts Demonstrated

✅ Variables and data types
✅ Conditional statements (if-else)
✅ Loops (for, while)
✅ Functions and parameters
✅ Lists, tuples, dictionaries
✅ File handling
✅ Object-Oriented Programming (Classes)
✅ API integration
✅ Data processing with Pandas
✅ Machine Learning with Scikit-learn
✅ Web development with Streamlit

---

## ⚠️ Disclaimer

This application is for **educational purposes only**. 

- Not financial advice
- Always do your own research
- Consult financial advisors before investing
- Past performance ≠ future results

---

## 🎓 Project Deliverables

### 1. ✅ Python Code
- All files are properly structured
- Comments added throughout
- Runs without errors

### 2. ✅ Features
- Live data fetching
- AI chatbot
- ML predictions
- Technical analysis
- Multi-market support

### 3. 📊 PPT Presentation (Create separately)
Your PPT should include:
1. Title slide with team names
2. Problem statement
3. Objectives
4. Technologies used
5. System architecture/flowchart
6. Code snippets
7. Output screenshots
8. Challenges faced
9. Learning outcomes
10. Conclusion

### 4. 📄 Project Report (Create separately)
Your report should include:
- Abstract (project summary)
- Introduction
- Features list
- Technical implementation
- Screenshots with explanations
- Code explanations
- Challenges and solutions
- Future enhancements
- Conclusion

---

## 🎯 Evaluation Criteria

| Component | Marks | Status |
|-----------|-------|--------|
| Code & Execution | 15 | ✅ Complete |
| PPT Presentation | 10 | 📝 To be created |
| Project Report | 10 | 📝 To be created |
| Creativity & Complexity | 5 | ✅ High complexity |

---

## 🔄 Future Enhancements

- [ ] Portfolio tracking
- [ ] News integration
- [ ] Email/SMS alerts
- [ ] Backtesting strategies
- [ ] Social sentiment analysis
- [ ] Mobile app version

---

## 🤝 Contributing

This is a student project. For improvements:
1. Test thoroughly
2. Add comments
3. Follow Python best practices
4. Update documentation

---

## 📞 Support

For issues or questions:
- Check troubleshooting section
- Review code comments
- Contact project team members
- Consult course instructor

---

## 📜 License

Educational project for PGCET course.

---

## 🙏 Acknowledgments

- **Alpha Vantage** - Stock market data API
- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Scikit-learn** - Machine learning library
- **Course Instructors** - Guidance and support

---

## 📸 Screenshots

Take screenshots of:
1. Dashboard with live data
2. Chatbot conversations
3. Prediction charts
4. Technical analysis
5. Different stocks/markets

Use these in your PPT and report!

---

## 🎉 Getting Started Checklist

- [ ] Python installed
- [ ] VS Code installed
- [ ] Project folder created
- [ ] All files created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] App running successfully
- [ ] Tested all features
- [ ] Screenshots taken
- [ ] PPT created
- [ ] Report written

---

**🚀 You're all set! Run `streamlit run app.py` and explore your Stock Dashboard!**

---

*Developed by PGCET Students | December 2025*