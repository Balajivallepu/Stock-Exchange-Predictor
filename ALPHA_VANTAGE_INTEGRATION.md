# Alpha Vantage API Integration Guide

## 🔑 API Key Configuration

**Your Alpha Vantage API Key:** `CMLKV2SLOT89UPM9`

This key is now integrated across all stock data fetching functions in the application.

## 📊 Features Enabled

### 1. Real-Time Stock Quotes
```python
from utils import fetch_alpha_vantage_quote

# Get real-time quote for any stock
quote = fetch_alpha_vantage_quote('AAPL')
print(quote)
```

### 2. Daily Historical Data
```python
from utils import fetch_alpha_vantage_daily

# Get daily data (compact = 100 days, full = 20+ years)
df = fetch_alpha_vantage_daily('MSFT', outputsize='compact')
print(df.tail())
```

### 3. Intraday Data (5min, 15min, 30min, 60min)
```python
from utils import fetch_alpha_vantage_intraday

# Get 5-minute interval data
df_intraday = fetch_alpha_vantage_intraday('GOOGL', interval='5min')
print(df_intraday.tail())
```

### 4. Company Fundamental Data
```python
from utils import fetch_alpha_vantage_company_overview

# Get company overview with fundamentals
overview = fetch_alpha_vantage_company_overview('TSLA')
print(f"Market Cap: {overview.get('MarketCapitalization')}")
print(f"P/E Ratio: {overview.get('PERatio')}")
```

### 5. Hybrid Fetching (Alpha Vantage + Yahoo Finance Fallback)
```python
from utils import fetch_stock_data_hybrid

# Tries Alpha Vantage first, falls back to Yahoo Finance if fails
df = fetch_stock_data_hybrid('AAPL', prefer_alpha_vantage=True)

# Or use Yahoo Finance directly
df = fetch_stock_data_hybrid('AAPL', prefer_alpha_vantage=False)
```

## 🎯 Using in Streamlit App

The main app.py now has an **API Settings** section in the sidebar:

1. **Open the sidebar** in the Streamlit app
2. **Navigate to "🔑 API Settings"**
3. **Select your data source:**
   - **Yahoo Finance (Free)** - Unlimited API calls, no rate limits
   - **Alpha Vantage API** - 5 calls/min, 500 calls/day, more features

When you select "Alpha Vantage API":
- ✅ All stock data will be fetched from Alpha Vantage
- ✅ API Key `CMLKV2SLOT89UPM9` is automatically used
- ✅ Falls back to Yahoo Finance if Alpha Vantage fails
- ✅ Status indicator shows active API in sidebar

## ⚠️ Rate Limits

**Alpha Vantage Free Tier:**
- 5 API calls per minute
- 500 API calls per day

**Yahoo Finance:**
- No rate limits
- Free forever

**Strategy:** Use Yahoo Finance for bulk data fetching, Alpha Vantage for specific detailed queries.

## 🧪 Testing the Integration

Run the comprehensive test suite:

```powershell
python test_alpha_vantage_integration.py
```

This will test:
- ✓ Quote fetching
- ✓ Daily data retrieval
- ✓ Intraday data
- ✓ Company overview
- ✓ Hybrid fetching
- ✓ Indian stocks compatibility

## 📝 Code Examples

### Example 1: Get Current Price
```python
from utils import fetch_global_quote

# Using Alpha Vantage
quote = fetch_global_quote('AAPL', use_alpha_vantage=True)
price = quote.get('05. price')
print(f"Current Price: ${price}")

# Using Yahoo Finance (default)
quote = fetch_global_quote('AAPL', use_alpha_vantage=False)
price = quote.get('05. price')
print(f"Current Price: ${price}")
```

### Example 2: Compare Data Sources
```python
from utils import fetch_alpha_vantage_daily, fetch_stock_data
import time

# Fetch from Alpha Vantage
start = time.time()
df_alpha = fetch_alpha_vantage_daily('TSLA')
alpha_time = time.time() - start
print(f"Alpha Vantage: {len(df_alpha)} days in {alpha_time:.2f}s")

# Fetch from Yahoo Finance
start = time.time()
df_yahoo = fetch_stock_data('TSLA')
yahoo_time = time.time() - start
print(f"Yahoo Finance: {len(df_yahoo)} days in {yahoo_time:.2f}s")
```

### Example 3: Get Company Fundamentals
```python
from utils import fetch_alpha_vantage_company_overview

overview = fetch_alpha_vantage_company_overview('NVDA')

print(f"Company: {overview.get('Name')}")
print(f"Sector: {overview.get('Sector')}")
print(f"Industry: {overview.get('Industry')}")
print(f"Market Cap: ${float(overview.get('MarketCapitalization', 0))/1e9:.2f}B")
print(f"P/E Ratio: {overview.get('PERatio')}")
print(f"EPS: ${overview.get('EPS')}")
print(f"Dividend Yield: {overview.get('DividendYield')}")
```

## 🔄 Integration Points

The Alpha Vantage API is integrated in:

1. **utils.py** - Core data fetching functions
   - `fetch_alpha_vantage_quote()`
   - `fetch_alpha_vantage_daily()`
   - `fetch_alpha_vantage_intraday()`
   - `fetch_alpha_vantage_company_overview()`
   - `fetch_stock_data_hybrid()`

2. **chatbot.py** - AI chatbot already uses the same API key
   - Natural language stock queries
   - Price lookups
   - Analysis requests

3. **app.py** - Streamlit UI
   - Sidebar API selector
   - Dynamic data source switching
   - Real-time status display

## 🚀 Next Steps

### Recommended Usage:
1. **For bulk operations:** Use Yahoo Finance (unlimited)
2. **For detailed analysis:** Use Alpha Vantage (company fundamentals, intraday)
3. **For production:** Consider upgrading to Alpha Vantage Premium for higher limits

### Advanced Features Available with Alpha Vantage:
- ✅ Intraday data (1min, 5min, 15min, 30min, 60min)
- ✅ Company fundamentals (P/E, EPS, dividends)
- ✅ Technical indicators (pre-calculated SMA, EMA, RSI, MACD)
- ✅ Crypto currency data
- ✅ Forex data
- ✅ Economic indicators

## 📞 Support

If you encounter issues:
1. Check rate limits (5/min, 500/day)
2. Verify API key: `CMLKV2SLOT89UPM9`
3. Review test output: `python test_alpha_vantage_integration.py`
4. Fall back to Yahoo Finance if needed

## ✅ Success Checklist

- [x] Alpha Vantage API key configured: `CMLKV2SLOT89UPM9`
- [x] All stock data functions support Alpha Vantage
- [x] Hybrid fetching with automatic fallback
- [x] Chatbot uses same API key
- [x] Streamlit app has API selector
- [x] Test suite available
- [x] Documentation complete

---

**All stocks are now connected to Alpha Vantage API with key: CMLKV2SLOT89UPM9**
