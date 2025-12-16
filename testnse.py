"""
Test NSE Stock Data Connection
Run this to verify which stocks are working
"""

import yfinance as yf
from datetime import datetime

print("="*60)
print("🔍 Testing NSE Stock Data Connection")
print("="*60)

# List of NSE stocks to test
nse_stocks = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'ITC.NS': 'ITC Ltd',
    'SBIN.NS': 'State Bank of India',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank'
}

print(f"\nTesting {len(nse_stocks)} NSE stocks...\n")

working_stocks = []
failed_stocks = []

for symbol, name in nse_stocks.items():
    try:
        print(f"Testing {symbol}...", end=" ")
        
        # Create ticker
        ticker = yf.Ticker(symbol)
        
        # Get 1 day data
        data = ticker.history(period='1d')
        
        if data is not None and len(data) > 0:
            price = data['Close'].iloc[-1]
            print(f"✅ WORKING - Price: ₹{price:.2f}")
            working_stocks.append({
                'symbol': symbol,
                'name': name,
                'price': price
            })
        else:
            print(f"❌ NO DATA")
            failed_stocks.append(symbol)
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:50]}")
        failed_stocks.append(symbol)

print("\n" + "="*60)
print(f"📊 RESULTS")
print("="*60)
print(f"✅ Working: {len(working_stocks)}/{len(nse_stocks)}")
print(f"❌ Failed: {len(failed_stocks)}/{len(nse_stocks)}")

if working_stocks:
    print("\n✅ WORKING STOCKS:")
    for stock in working_stocks:
        print(f"   {stock['symbol']} - {stock['name']} - ₹{stock['price']:.2f}")

if failed_stocks:
    print("\n❌ FAILED STOCKS:")
    for symbol in failed_stocks:
        print(f"   {symbol}")

print("\n" + "="*60)

# Test US stocks for comparison
print("\n🇺🇸 Testing US Stocks (for comparison)...")
us_stocks = ['AAPL', 'MSFT', 'GOOGL']

for symbol in us_stocks:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if data is not None and len(data) > 0:
            price = data['Close'].iloc[-1]
            print(f"✅ {symbol} - ${price:.2f}")
    except:
        print(f"❌ {symbol} failed")

print("\n" + "="*60)
print("Test Complete!")
print("="*60)