"""
Test Alpha Vantage API Integration
API Key: CMLKV2SLOT89UPM9
"""

from utils import (
    fetch_alpha_vantage_quote,
    fetch_alpha_vantage_intraday,
    fetch_alpha_vantage_daily,
    fetch_alpha_vantage_company_overview,
    fetch_stock_data_hybrid,
    fetch_global_quote
)

def test_alpha_vantage_quote():
    """Test Alpha Vantage quote fetching"""
    print("\n" + "="*60)
    print("Testing Alpha Vantage Quote (AAPL)")
    print("="*60)
    
    quote = fetch_alpha_vantage_quote('AAPL')
    if quote:
        print("✓ Success! Quote data:")
        for key, value in quote.items():
            print(f"  {key}: {value}")
    else:
        print("✗ Failed to fetch quote")

def test_alpha_vantage_daily():
    """Test Alpha Vantage daily data"""
    print("\n" + "="*60)
    print("Testing Alpha Vantage Daily Data (MSFT)")
    print("="*60)
    
    df = fetch_alpha_vantage_daily('MSFT', outputsize='compact')
    if df is not None and len(df) > 0:
        print(f"✓ Success! Retrieved {len(df)} days of data")
        print("\nLast 5 days:")
        print(df.tail())
    else:
        print("✗ Failed to fetch daily data")

def test_alpha_vantage_intraday():
    """Test Alpha Vantage intraday data"""
    print("\n" + "="*60)
    print("Testing Alpha Vantage Intraday Data (GOOGL - 5min)")
    print("="*60)
    
    df = fetch_alpha_vantage_intraday('GOOGL', interval='5min')
    if df is not None and len(df) > 0:
        print(f"✓ Success! Retrieved {len(df)} intraday intervals")
        print("\nLast 5 intervals:")
        print(df.tail())
    else:
        print("✗ Failed to fetch intraday data")

def test_company_overview():
    """Test company overview"""
    print("\n" + "="*60)
    print("Testing Alpha Vantage Company Overview (TSLA)")
    print("="*60)
    
    overview = fetch_alpha_vantage_company_overview('TSLA')
    if overview:
        print("✓ Success! Company overview:")
        key_fields = ['Symbol', 'Name', 'Description', 'Sector', 'Industry', 
                      'MarketCapitalization', 'PERatio', 'DividendYield']
        for field in key_fields:
            if field in overview:
                value = overview[field]
                if field == 'Description' and len(value) > 100:
                    value = value[:100] + "..."
                print(f"  {field}: {value}")
    else:
        print("✗ Failed to fetch company overview")

def test_hybrid_fetching():
    """Test hybrid data fetching (Alpha Vantage + Yahoo Finance fallback)"""
    print("\n" + "="*60)
    print("Testing Hybrid Fetching (Alpha Vantage first, Yahoo fallback)")
    print("="*60)
    
    # Test with Alpha Vantage
    print("\n1. Testing AAPL (should use Alpha Vantage):")
    df = fetch_stock_data_hybrid('AAPL', prefer_alpha_vantage=True)
    if df is not None and len(df) > 0:
        print(f"   ✓ Success! Retrieved {len(df)} days")
    else:
        print("   ✗ Failed")
    
    # Test Indian stock (might fallback to Yahoo)
    print("\n2. Testing RELIANCE.NS (might fallback to Yahoo):")
    df = fetch_stock_data_hybrid('RELIANCE.NS', prefer_alpha_vantage=True)
    if df is not None and len(df) > 0:
        print(f"   ✓ Success! Retrieved {len(df)} days")
    else:
        print("   ✗ Failed")

def test_global_quote_with_api():
    """Test global quote with Alpha Vantage option"""
    print("\n" + "="*60)
    print("Testing Global Quote with Alpha Vantage Option")
    print("="*60)
    
    print("\n1. Using Alpha Vantage API (META):")
    quote = fetch_global_quote('META', use_alpha_vantage=True)
    if quote:
        print(f"   ✓ Price: {quote.get('05. price', 'N/A')}")
        print(f"   Change: {quote.get('09. change', 'N/A')} ({quote.get('10. change percent', 'N/A')})")
    else:
        print("   ✗ Failed")
    
    print("\n2. Using Yahoo Finance (default - NVDA):")
    quote = fetch_global_quote('NVDA', use_alpha_vantage=False)
    if quote:
        print(f"   ✓ Price: {quote.get('05. price', 'N/A')}")
        print(f"   Change: {quote.get('09. change', 'N/A')} ({quote.get('10. change percent', 'N/A')})")
    else:
        print("   ✗ Failed")

def test_indian_stocks():
    """Test Indian stocks with Alpha Vantage"""
    print("\n" + "="*60)
    print("Testing Indian Stocks")
    print("="*60)
    
    indian_stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
    
    for symbol in indian_stocks:
        print(f"\nTesting {symbol}:")
        quote = fetch_alpha_vantage_quote(symbol)
        if quote:
            print(f"  ✓ Alpha Vantage: Success")
        else:
            print(f"  ⚠ Alpha Vantage: No data (trying Yahoo Finance)")
            quote = fetch_global_quote(symbol, use_alpha_vantage=False)
            if quote:
                print(f"  ✓ Yahoo Finance: Success - Price: {quote.get('05. price', 'N/A')}")

if __name__ == "__main__":
    print("="*60)
    print("ALPHA VANTAGE API INTEGRATION TEST")
    print("API Key: CMLKV2SLOT89UPM9")
    print("="*60)
    
    # Run all tests
    test_alpha_vantage_quote()
    test_alpha_vantage_daily()
    test_alpha_vantage_intraday()
    test_company_overview()
    test_hybrid_fetching()
    test_global_quote_with_api()
    test_indian_stocks()
    
    print("\n" + "="*60)
    print("TESTING COMPLETE!")
    print("="*60)
    print("\nNote: Alpha Vantage has rate limits:")
    print("  • 5 API calls per minute")
    print("  • 500 API calls per day")
    print("  • Yahoo Finance is used as fallback (no limits)")
    print("="*60)
