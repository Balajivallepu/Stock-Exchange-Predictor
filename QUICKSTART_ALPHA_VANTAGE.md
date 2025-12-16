# 🚀 Quick Start - Alpha Vantage Integration

## ✅ What's New

**All stocks are now connected to Alpha Vantage API!**

**API Key:** `CMLKV2SLOT89UPM9`

## 🎯 How to Use

### Option 1: Via Streamlit App (Easiest)

1. **Run the app:**
   ```powershell
   streamlit run app.py
   ```

2. **Open sidebar** → Navigate to **"🔑 API Settings"**

3. **Select data source:**
   - 📊 **Yahoo Finance (Free)** - Unlimited, no rate limits
   - 🔑 **Alpha Vantage API** - Enhanced features, 5/min, 500/day

4. **Done!** The app will automatically use your selected API for all stock data.

### Option 2: Via Python Code

```python
from utils import fetch_global_quote, fetch_alpha_vantage_daily

# Get real-time quote using Alpha Vantage
quote = fetch_global_quote('AAPL', use_alpha_vantage=True)
print(f"Price: ${quote['05. price']}")

# Get historical data
df = fetch_alpha_vantage_daily('MSFT')
print(df.tail())
```

## 🧪 Test the Integration

```powershell
python test_alpha_vantage_integration.py
```

This will verify:
- ✓ API connection
- ✓ Quote fetching
- ✓ Historical data
- ✓ Company information

## 📊 What You Get

### With Alpha Vantage:
- ✅ Real-time quotes
- ✅ Intraday data (1min, 5min, 15min, 30min, 60min)
- ✅ Historical daily data
- ✅ Company fundamentals (P/E, EPS, Market Cap)
- ✅ Technical indicators

### With Yahoo Finance (Default):
- ✅ Unlimited API calls
- ✅ Real-time quotes
- ✅ Historical data
- ✅ No rate limits

## ⚡ Rate Limits

**Alpha Vantage:**
- 5 API calls per minute
- 500 API calls per day

**Solution:** App automatically falls back to Yahoo Finance if Alpha Vantage limit reached.

## 🎨 Features in App

### Sidebar Indicator:
Shows active API:
- **Yahoo Finance** - Green indicator
- **Alpha Vantage (CMLKV2SLOT89UPM9)** - Blue indicator with API key

### Dashboard:
When using Alpha Vantage, you'll see:
- 🔑 "Fetching from Alpha Vantage API..." indicator
- ✓ Success message when data loaded

## 📝 Quick Examples

### Example 1: Get Current Stock Price
```python
from utils import fetch_alpha_vantage_quote

quote = fetch_alpha_vantage_quote('TSLA')
print(f"Tesla Price: ${quote['05. price']}")
print(f"Change: {quote['09. change']} ({quote['10. change percent']})")
```

### Example 2: Get Company Info
```python
from utils import fetch_alpha_vantage_company_overview

info = fetch_alpha_vantage_company_overview('GOOGL')
print(f"Name: {info['Name']}")
print(f"Sector: {info['Sector']}")
print(f"Market Cap: ${info['MarketCapitalization']}")
print(f"P/E Ratio: {info['PERatio']}")
```

### Example 3: Hybrid Fetching (Best Practice)
```python
from utils import fetch_stock_data_hybrid

# Tries Alpha Vantage first, falls back to Yahoo if needed
df = fetch_stock_data_hybrid('AAPL', prefer_alpha_vantage=True)
print(f"Retrieved {len(df)} days of data")
```

## ✅ Verification

Run these commands to verify setup:

```powershell
# 1. Test Alpha Vantage connection
python -c "from utils import fetch_alpha_vantage_quote; print(fetch_alpha_vantage_quote('AAPL'))"

# 2. Run full test suite
python test_alpha_vantage_integration.py

# 3. Start the app
streamlit run app.py
```

## 🎯 Next Steps

1. **Try both APIs** in the Streamlit app to compare
2. **Use Alpha Vantage** for detailed analysis and company fundamentals
3. **Use Yahoo Finance** for bulk data fetching and real-time monitoring
4. **Read full documentation** in `ALPHA_VANTAGE_INTEGRATION.md`

---

**🎉 Success! All stocks are now connected to Alpha Vantage API: CMLKV2SLOT89UPM9**
