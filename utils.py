"""
Utility functions for Stock Exchange Prediction Dashboard
WITH LIVE DATA - Yahoo Finance API (NO RATE LIMITS!)
Alpha Vantage API Integration for Enhanced Data
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# ============================================================================
# API CONFIGURATION - Alpha Vantage Integration
# ============================================================================
ALPHA_VANTAGE_API_KEY = "CMLKV2SLOT89UPM9"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# ============================================================================
# ALPHA VANTAGE API FUNCTIONS
# ============================================================================

def fetch_alpha_vantage_quote(symbol):
    """
    Fetch real-time quote from Alpha Vantage API
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'RELIANCE.NS')
    
    Returns:
        dict: Quote data from Alpha Vantage
    """
    try:
        # Remove .NS or .BO suffix for Alpha Vantage (it uses different format)
        clean_symbol = symbol.replace('.NS', '.BSE').replace('.BO', '.BSE')
        if '.BSE' in clean_symbol:
            clean_symbol = clean_symbol.replace('.BSE', '')  # Alpha Vantage uses plain symbols
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': clean_symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            return data['Global Quote']
        else:
            print(f"Alpha Vantage: No data for {symbol}")
            return None
            
    except Exception as e:
        print(f"Alpha Vantage API error for {symbol}: {e}")
        return None

def fetch_alpha_vantage_intraday(symbol, interval='5min'):
    """
    Fetch intraday data from Alpha Vantage
    
    Args:
        symbol: Stock symbol
        interval: Time interval (1min, 5min, 15min, 30min, 60min)
    
    Returns:
        DataFrame with intraday data
    """
    try:
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': clean_symbol,
            'interval': interval,
            'apikey': ALPHA_VANTAGE_API_KEY,
            'outputsize': 'compact'
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        time_series_key = f'Time Series ({interval})'
        if time_series_key in data:
            df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                '1. open': 'Open',
                '2. high': 'High',
                '3. low': 'Low',
                '4. close': 'Close',
                '5. volume': 'Volume'
            })
            df = df.astype(float)
            return df.sort_index()
        else:
            print(f"Alpha Vantage intraday: No data for {symbol}")
            return None
            
    except Exception as e:
        print(f"Alpha Vantage intraday error: {e}")
        return None

def fetch_alpha_vantage_daily(symbol, outputsize='compact'):
    """
    Fetch daily historical data from Alpha Vantage
    
    Args:
        symbol: Stock symbol
        outputsize: 'compact' (100 days) or 'full' (20+ years)
    
    Returns:
        DataFrame with daily data
    """
    try:
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': clean_symbol,
            'apikey': ALPHA_VANTAGE_API_KEY,
            'outputsize': outputsize
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                '1. open': 'Open',
                '2. high': 'High',
                '3. low': 'Low',
                '4. close': 'Close',
                '5. volume': 'Volume'
            })
            df = df.astype(float)
            return df.sort_index()
        else:
            print(f"Alpha Vantage daily: No data for {symbol}")
            return None
            
    except Exception as e:
        print(f"Alpha Vantage daily error: {e}")
        return None

def fetch_alpha_vantage_company_overview(symbol):
    """
    Fetch company overview/fundamental data from Alpha Vantage
    
    Args:
        symbol: Stock symbol
    
    Returns:
        dict: Company overview data
    """
    try:
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        params = {
            'function': 'OVERVIEW',
            'symbol': clean_symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if data and 'Symbol' in data:
            return data
        else:
            return None
            
    except Exception as e:
        print(f"Alpha Vantage overview error: {e}")
        return None

# ============================================================================
# HYBRID DATA FETCHING - Alpha Vantage + Yahoo Finance
# ============================================================================

def fetch_stock_data_hybrid(symbol, prefer_alpha_vantage=True):
    """
    Fetch stock data using both Alpha Vantage and Yahoo Finance
    Falls back to Yahoo Finance if Alpha Vantage fails
    
    Args:
        symbol: Stock symbol
        prefer_alpha_vantage: Try Alpha Vantage first if True
    
    Returns:
        DataFrame with stock data
    """
    if prefer_alpha_vantage:
        # Try Alpha Vantage first
        df = fetch_alpha_vantage_daily(symbol, outputsize='compact')
        if df is not None and len(df) > 0:
            print(f"✓ Data from Alpha Vantage for {symbol}")
            return df
        
        # Fallback to Yahoo Finance
        print(f"Falling back to Yahoo Finance for {symbol}")
        return fetch_stock_data(symbol)
    else:
        # Use Yahoo Finance (default behavior)
        return fetch_stock_data(symbol)

# ============================================================================
# LIVE STOCK DATA - Yahoo Finance (Real-time, No limits!)
# ============================================================================

def fetch_stock_data(symbol):
    """
    Fetch LIVE stock data from Yahoo Finance
    Enhanced error handling for NSE stocks
    
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS', 'TCS.NS', 'AAPL')
    
    Returns:
        DataFrame with stock data
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get historical data (last 3 months for better analysis)
        df = ticker.history(period='3mo', interval='1d')
        
        # If no data, try with different period
        if df is None or len(df) == 0:
            print(f"Trying alternate period for {symbol}")
            df = ticker.history(period='1mo', interval='1d')
        
        # Still no data? Try daily data
        if df is None or len(df) == 0:
            print(f"Trying shorter period for {symbol}")
            df = ticker.history(period='5d', interval='1d')
        
        if df is None or len(df) == 0:
            print(f"No data available for {symbol}")
            return None
        
        # Reset index to make Date a column
        df = df.reset_index()
        df = df.set_index('Date')
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in df.columns:
                print(f"Missing column {col} for {symbol}")
                return None
        
        return df[required_cols]
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def fetch_global_quote(symbol, use_alpha_vantage=False):
    """
    Fetch LIVE current quote for a stock
    Real-time prices from Alpha Vantage or Yahoo Finance!
    
    Args:
        symbol: Stock symbol
        use_alpha_vantage: If True, use Alpha Vantage API; otherwise use Yahoo Finance
    """
    # Try Alpha Vantage first if requested
    if use_alpha_vantage:
        av_quote = fetch_alpha_vantage_quote(symbol)
        if av_quote:
            return av_quote
        print(f"Alpha Vantage failed, falling back to Yahoo Finance for {symbol}")
    
    # Yahoo Finance implementation (default)
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get current price and calculate change
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        change_percent = (change / prev_close * 100) if prev_close != 0 else 0
        
        # Get today's high/low
        day_high = info.get('dayHigh', current_price)
        day_low = info.get('dayLow', current_price)
        volume = info.get('volume', 0)
        
        # Return in Alpha Vantage format for compatibility
        return {
            '01. symbol': symbol,
            '02. open': str(info.get('regularMarketOpen', current_price)),
            '03. high': str(day_high),
            '04. low': str(day_low),
            '05. price': str(current_price),
            '06. volume': str(volume),
            '07. latest trading day': datetime.now().strftime('%Y-%m-%d'),
            '08. previous close': str(prev_close),
            '09. change': str(change),
            '10. change percent': f"{change_percent:.2f}%"
        }
        
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return None

def get_live_price(symbol):
    """
    Get INSTANT live price (fastest method)
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d', interval='1m')
        
        if data is None or len(data) == 0:
            # Fallback to info
            info = ticker.info
            return info.get('currentPrice', info.get('regularMarketPrice', 0))
        
        return data['Close'].iloc[-1]
    except:
        return None

def get_stock_info(symbol):
    """
    Get detailed stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'name': info.get('longName', 'Unknown'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            '52_week_high': info.get('fiftyTwoWeekHigh', 0),
            '52_week_low': info.get('fiftyTwoWeekLow', 0),
            'avg_volume': info.get('averageVolume', 0)
        }
    except:
        return None

def fetch_intraday_data(symbol, interval='5m'):
    """
    Fetch LIVE intraday data (for real-time charts)
    
    Intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period='1d', interval=interval)
        
        if df is None or len(df) == 0:
            return None
        
        return df[['Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception as e:
        print(f"Error fetching intraday data: {e}")
        return None

# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

def calculate_technical_indicators(df):
    """Calculate technical indicators for stock analysis"""
    if df is None or len(df) < 20:
        return df
    
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # Exponential Moving Average
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (std * 2)
    
    return df

def get_stock_recommendation(df):
    """Generate buy/sell/hold recommendation based on indicators"""
    if df is None or len(df) < 50:
        return "Insufficient Data"
    
    latest = df.iloc[-1]
    score = 0
    
    # RSI Analysis
    if latest['RSI'] < 30:
        score += 2  # Oversold - Buy signal
    elif latest['RSI'] > 70:
        score -= 2  # Overbought - Sell signal
    
    # MACD Analysis
    if latest['MACD'] > latest['Signal_Line']:
        score += 1  # Bullish
    else:
        score -= 1  # Bearish
    
    # Moving Average Analysis
    if latest['Close'] > latest['SMA_20']:
        score += 1
    else:
        score -= 1
    
    # Bollinger Bands
    if latest['Close'] < latest['BB_Lower']:
        score += 1  # Potential bounce
    elif latest['Close'] > latest['BB_Upper']:
        score -= 1  # Potential pullback
    
    # Generate recommendation
    if score >= 3:
        return "🟢 STRONG BUY"
    elif score >= 1:
        return "🟢 BUY"
    elif score <= -3:
        return "🔴 STRONG SELL"
    elif score <= -1:
        return "🔴 SELL"
    else:
        return "🟡 HOLD"

# ============================================================================
# STOCK LISTS - Using Yahoo Finance symbols
# ============================================================================

# Popular Indian stocks (NSE) - VERIFIED WORKING SYMBOLS
INDIAN_STOCKS = {
    'NSE': {
        'RELIANCE.NS': 'Reliance Industries Ltd',
        'TCS.NS': 'Tata Consultancy Services',
        'HDFCBANK.NS': 'HDFC Bank Ltd',
        'INFY.NS': 'Infosys Ltd',
        'ICICIBANK.NS': 'ICICI Bank Ltd',
        'HINDUNILVR.NS': 'Hindustan Unilever Ltd',
        'ITC.NS': 'ITC Ltd',
        'SBIN.NS': 'State Bank of India',
        'BHARTIARTL.NS': 'Bharti Airtel Ltd',
        'KOTAKBANK.NS': 'Kotak Mahindra Bank',
        'LT.NS': 'Larsen & Toubro Ltd',
        'AXISBANK.NS': 'Axis Bank Ltd',
        'MARUTI.NS': 'Maruti Suzuki India Ltd',
        'TITAN.NS': 'Titan Company Ltd',
        'WIPRO.NS': 'Wipro Ltd',
        'BAJFINANCE.NS': 'Bajaj Finance Ltd',
        'ASIANPAINT.NS': 'Asian Paints Ltd',
        'HCLTECH.NS': 'HCL Technologies Ltd',
        'ULTRACEMCO.NS': 'UltraTech Cement Ltd',
        'NESTLEIND.NS': 'Nestle India Ltd',
        'SUNPHARMA.NS': 'Sun Pharmaceutical Industries',
        'TATAMOTORS.NS': 'Tata Motors Ltd',
        'TATASTEEL.NS': 'Tata Steel Ltd',
        'ADANIGREEN.NS': 'Adani Green Energy Ltd',
        'ADANIPORTS.NS': 'Adani Ports and SEZ Ltd',
        'ONGC.NS': 'Oil and Natural Gas Corporation',
        'NTPC.NS': 'NTPC Ltd',
        'POWERGRID.NS': 'Power Grid Corporation',
        'COALINDIA.NS': 'Coal India Ltd',
        'JSWSTEEL.NS': 'JSW Steel Ltd',
        'HINDALCO.NS': 'Hindalco Industries Ltd',
        'VEDL.NS': 'Vedanta Ltd',
        'INDUSINDBK.NS': 'IndusInd Bank Ltd',
        'BAJAJFINSV.NS': 'Bajaj Finserv Ltd',
        'M&M.NS': 'Mahindra & Mahindra Ltd',
        'TECHM.NS': 'Tech Mahindra Ltd',
        'DRREDDY.NS': 'Dr. Reddys Laboratories',
        'CIPLA.NS': 'Cipla Ltd',
        'DIVISLAB.NS': 'Divi\'s Laboratories Ltd',
        'EICHERMOT.NS': 'Eicher Motors Ltd',
        'HEROMOTOCO.NS': 'Hero MotoCorp Ltd',
        'BAJAJ-AUTO.NS': 'Bajaj Auto Ltd',
        'GRASIM.NS': 'Grasim Industries Ltd',
        'BRITANNIA.NS': 'Britannia Industries Ltd',
        'DABUR.NS': 'Dabur India Ltd',
        'GODREJCP.NS': 'Godrej Consumer Products',
        'SHREECEM.NS': 'Shree Cement Ltd',
        'ADANIENT.NS': 'Adani Enterprises Ltd',
        'APOLLOHOSP.NS': 'Apollo Hospitals Enterprise'
    },
    'BSE': {
        'RELIANCE.BO': 'Reliance Industries Ltd',
        'TCS.BO': 'Tata Consultancy Services',
        'HDFCBANK.BO': 'HDFC Bank Ltd',
        'INFY.BO': 'Infosys Ltd',
        'ICICIBANK.BO': 'ICICI Bank Ltd',
        'HINDUNILVR.BO': 'Hindustan Unilever Ltd',
        'ITC.BO': 'ITC Ltd',
        'SBIN.BO': 'State Bank of India',
        'BHARTIARTL.BO': 'Bharti Airtel Ltd',
        'KOTAKBANK.BO': 'Kotak Mahindra Bank',
        'LT.BO': 'Larsen & Toubro Ltd',
        'AXISBANK.BO': 'Axis Bank Ltd',
        'MARUTI.BO': 'Maruti Suzuki India Ltd',
        'TITAN.BO': 'Titan Company Ltd',
        'WIPRO.BO': 'Wipro Ltd',
        'BAJFINANCE.BO': 'Bajaj Finance Ltd',
        'ASIANPAINT.BO': 'Asian Paints Ltd',
        'HCLTECH.BO': 'HCL Technologies Ltd',
        'ULTRACEMCO.BO': 'UltraTech Cement Ltd',
        'NESTLEIND.BO': 'Nestle India Ltd',
        'SUNPHARMA.BO': 'Sun Pharmaceutical Industries',
        'TATAMOTORS.BO': 'Tata Motors Ltd',
        'TATASTEEL.BO': 'Tata Steel Ltd',
        'ADANIGREEN.BO': 'Adani Green Energy Ltd',
        'ADANIPORTS.BO': 'Adani Ports and SEZ Ltd',
        'ONGC.BO': 'Oil and Natural Gas Corporation',
        'NTPC.BO': 'NTPC Ltd',
        'POWERGRID.BO': 'Power Grid Corporation',
        'COALINDIA.BO': 'Coal India Ltd',
        'JSWSTEEL.BO': 'JSW Steel Ltd',
        'HINDALCO.BO': 'Hindalco Industries Ltd',
        'VEDL.BO': 'Vedanta Ltd',
        'INDUSINDBK.BO': 'IndusInd Bank Ltd',
        'BAJAJFINSV.BO': 'Bajaj Finserv Ltd',
        'M&M.BO': 'Mahindra & Mahindra Ltd',
        'TECHM.BO': 'Tech Mahindra Ltd',
        'DRREDDY.BO': 'Dr. Reddys Laboratories',
        'CIPLA.BO': 'Cipla Ltd',
        'DIVISLAB.BO': 'Divi\'s Laboratories Ltd',
        'EICHERMOT.BO': 'Eicher Motors Ltd',
        'HEROMOTOCO.BO': 'Hero MotoCorp Ltd',
        'BAJAJ-AUTO.BO': 'Bajaj Auto Ltd',
        'GRASIM.BO': 'Grasim Industries Ltd',
        'BRITANNIA.BO': 'Britannia Industries Ltd',
        'DABUR.BO': 'Dabur India Ltd',
        'GODREJCP.BO': 'Godrej Consumer Products',
        'SHREECEM.BO': 'Shree Cement Ltd',
        'ADANIENT.BO': 'Adani Enterprises Ltd',
        'APOLLOHOSP.BO': 'Apollo Hospitals Enterprise'
    }
}

# US stocks
US_STOCKS = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms Inc.',
    'NVDA': 'NVIDIA Corporation',
    'JPM': 'JPMorgan Chase & Co.',
    'V': 'Visa Inc.',
    'WMT': 'Walmart Inc.',
    'JNJ': 'Johnson & Johnson',
    'PG': 'Procter & Gamble',
    'MA': 'Mastercard',
    'HD': 'Home Depot',
    'BAC': 'Bank of America',
    'NFLX': 'Netflix Inc.',
    'DIS': 'The Walt Disney Company',
    'ADBE': 'Adobe Inc.',
    'CRM': 'Salesforce Inc.',
    'INTC': 'Intel Corporation',
    'AMD': 'Advanced Micro Devices',
    'CSCO': 'Cisco Systems Inc.',
    'PEP': 'PepsiCo Inc.',
    'KO': 'The Coca-Cola Company',
    'ORCL': 'Oracle Corporation',
    'NKE': 'Nike Inc.',
    'MCD': 'McDonald\'s Corporation',
    'PYPL': 'PayPal Holdings Inc.',
    'ABT': 'Abbott Laboratories',
    'CVX': 'Chevron Corporation',
    'PFE': 'Pfizer Inc.',
    'TMO': 'Thermo Fisher Scientific',
    'COST': 'Costco Wholesale',
    'AVGO': 'Broadcom Inc.',
    'UNH': 'UnitedHealth Group',
    'XOM': 'Exxon Mobil Corporation',
    'LLY': 'Eli Lilly and Company',
    'ABBV': 'AbbVie Inc.',
    'ACN': 'Accenture plc',
    'TXN': 'Texas Instruments',
    'QCOM': 'QUALCOMM Incorporated',
    'WFC': 'Wells Fargo & Company',
    'IBM': 'IBM Corporation',
    'GS': 'Goldman Sachs Group',
    'UBER': 'Uber Technologies Inc.',
    'SBUX': 'Starbucks Corporation',
    'NOW': 'ServiceNow Inc.',
    'BKNG': 'Booking Holdings Inc.',
    'BA': 'Boeing Company',
    'CAT': 'Caterpillar Inc.'
}

# ============================================================================
# MARKET INDICES
# ============================================================================

MARKET_INDICES = {
    '^NSEI': 'NIFTY 50',
    '^BSESN': 'SENSEX',
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow Jones',
    '^IXIC': 'NASDAQ'
}

def get_market_overview():
    """
    Get overview of major market indices
    """
    overview = {}
    
    for symbol, name in MARKET_INDICES.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current = info.get('regularMarketPrice', 0)
            prev_close = info.get('previousClose', current)
            change = current - prev_close
            change_percent = (change / prev_close * 100) if prev_close != 0 else 0
            
            overview[name] = {
                'symbol': symbol,
                'price': current,
                'change': change,
                'change_percent': change_percent
            }
        except:
            continue
    
    return overview

# ============================================================================
# CRYPTO SUPPORT (BONUS!)
# ============================================================================

CRYPTO = {
    'BTC-USD': 'Bitcoin',
    'ETH-USD': 'Ethereum',
    'BNB-USD': 'Binance Coin',
    'XRP-USD': 'Ripple',
    'ADA-USD': 'Cardano',
    'DOGE-USD': 'Dogecoin',
    'SOL-USD': 'Solana',
    'MATIC-USD': 'Polygon'
}

def get_trending_stocks():
    """
    Get trending stocks (most active)
    """
    try:
        # Get S&P 500 most active stocks
        sp500 = yf.Ticker("^GSPC")
        # This is a placeholder - in production you'd use a proper API
        return ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    except:
        return []