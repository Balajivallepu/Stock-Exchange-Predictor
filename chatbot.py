"""
CHATBOT MODULE WITH API INTEGRATION
To be placed in your chatbot folder
API Key: CMLKV2SLOT89UPM9
"""

import requests
import yfinance as yf
from datetime import datetime

class StockChatbot:
    """
    AI-powered stock chatbot with API integration
    """
    
    def __init__(self):
        self.api_key = "CMLKV2SLOT89UPM9"
        self.conversation_history = []
        
    def process_query(self, user_input):
        """
        Process user queries about stocks
        
        Args:
            user_input (str): User's question
            
        Returns:
            str: Bot's response
        """
        query_lower = user_input.lower()
        
        try:
            # Price queries
            if 'price' in query_lower or 'cost' in query_lower or 'trading at' in query_lower:
                return self._handle_price_query(user_input)
            
            # Analysis queries
            elif 'analyze' in query_lower or 'analysis' in query_lower:
                return self._handle_analysis_query(user_input)
            
            # Buy/Sell recommendations
            elif 'buy' in query_lower or 'sell' in query_lower or 'invest' in query_lower:
                return self._handle_recommendation_query(user_input)
            
            # Comparison queries
            elif 'compare' in query_lower or 'vs' in query_lower or 'versus' in query_lower:
                return self._handle_comparison_query(user_input)
            
            # Market queries
            elif 'market' in query_lower or 'markets' in query_lower:
                return self._handle_market_query(user_input)
            
            # Top stocks
            elif 'top' in query_lower or 'best' in query_lower:
                return self._handle_top_stocks_query(user_input)
            
            # News queries
            elif 'news' in query_lower or 'latest' in query_lower:
                return self._handle_news_query(user_input)
            
            # Help queries
            elif 'help' in query_lower or 'what can you' in query_lower:
                return self._get_help_message()
            
            # Default response
            else:
                return self._get_default_response(user_input)
                
        except Exception as e:
            return f"⚠️ Sorry, I encountered an error: {str(e)}\n\nPlease try rephrasing your question or ask for help."
    
    def _handle_price_query(self, query):
        """Handle price-related queries"""
        symbol = self._extract_stock_symbol(query)
        
        if not symbol:
            return "💬 Which stock would you like to know the price of? Please mention the stock symbol (e.g., AAPL, RELIANCE.NS, TCS.NS)"
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            company_name = info.get('longName', symbol)
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            response = f"""
📊 **{company_name} ({symbol})**

💰 **Current Price:** ${current_price:.2f}
{emoji} **Change:** ${change:+.2f} ({change_percent:+.2f}%)
📈 **Day High:** ${info.get('dayHigh', 'N/A')}
📉 **Day Low:** ${info.get('dayLow', 'N/A')}
📦 **Volume:** {info.get('volume', 0):,}

🕐 Last updated: {datetime.now().strftime('%I:%M %p')}

Would you like me to analyze this stock or get more details?
"""
            return response
            
        except Exception as e:
            return f"❌ Sorry, I couldn't fetch the price for {symbol}. Please check the symbol and try again."
    
    def _handle_analysis_query(self, query):
        """Handle analysis queries"""
        symbol = self._extract_stock_symbol(query)
        
        if not symbol:
            return "💬 Which stock would you like me to analyze? Please provide the stock symbol."
        
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period='3mo')
            info = stock.info
            
            if df.empty:
                return f"❌ No data available for {symbol}"
            
            # Calculate basic indicators
            current_price = float(df['Close'].iloc[-1])
            sma_20 = df['Close'].rolling(20).mean().iloc[-1]
            sma_50 = df['Close'].rolling(50).mean().iloc[-1]
            
            # RSI calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Trend
            trend_20 = ((df['Close'].iloc[-1] - df['Close'].iloc[-20]) / df['Close'].iloc[-20]) * 100
            
            # Generate recommendation
            signals = 0
            if rsi < 30:
                signals += 2
            elif rsi < 45:
                signals += 1
            elif rsi > 70:
                signals -= 2
            
            if current_price > sma_20:
                signals += 1
            if sma_20 > sma_50:
                signals += 1
            
            if signals >= 3:
                recommendation = "🟢 STRONG BUY"
            elif signals >= 1:
                recommendation = "🟢 BUY"
            elif signals >= -1:
                recommendation = "🟡 HOLD"
            else:
                recommendation = "🔴 SELL"
            
            response = f"""
📊 **Analysis for {info.get('longName', symbol)} ({symbol})**

💰 **Current Price:** ${current_price:.2f}

**Technical Indicators:**
📈 SMA 20: ${sma_20:.2f}
📈 SMA 50: ${sma_50:.2f}
📊 RSI: {rsi:.2f} {'(Oversold)' if rsi < 30 else '(Overbought)' if rsi > 70 else '(Neutral)'}
📉 20-day Trend: {trend_20:+.2f}%

**AI Recommendation:** {recommendation}

**Key Insights:**
• Price is {'above' if current_price > sma_20 else 'below'} 20-day moving average
• RSI indicates {'oversold conditions - potential buy' if rsi < 30 else 'overbought conditions - caution' if rsi > 70 else 'neutral momentum'}
• {'Bullish' if trend_20 > 0 else 'Bearish'} short-term trend

⚠️ *This is for educational purposes only, not financial advice.*

Would you like more details or compare with another stock?
"""
            return response
            
        except Exception as e:
            return f"❌ Error analyzing {symbol}: {str(e)}"
    
    def _handle_recommendation_query(self, query):
        """Handle buy/sell recommendation queries"""
        symbol = self._extract_stock_symbol(query)
        
        if not symbol:
            return "💬 Which stock are you considering? Please mention the stock symbol."
        
        # Get analysis first
        analysis = self._handle_analysis_query(f"analyze {symbol}")
        
        disclaimer = """

⚠️ **Important Disclaimer:**
This is AI-generated educational content only. I am not a financial advisor. 
Always:
• Do your own research
• Consult with a licensed financial advisor
• Consider your risk tolerance
• Diversify your portfolio
• Never invest money you can't afford to lose
"""
        
        return analysis + disclaimer
    
    def _handle_comparison_query(self, query):
        """Handle stock comparison queries"""
        # Extract multiple symbols
        words = query.upper().split()
        
        # Common Indian stock symbols
        indian_stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']
        # Common US stocks
        us_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        
        symbols = []
        for word in words:
            # Check for .NS suffix
            if word.endswith('.NS') or word.endswith('.BO'):
                symbols.append(word)
            elif word in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA']:
                symbols.append(word)
            elif f"{word}.NS" in indian_stocks:
                symbols.append(f"{word}.NS")
        
        if len(symbols) < 2:
            return """💬 To compare stocks, please mention at least 2 symbols.

**Examples:**
• "Compare AAPL and MSFT"
• "TCS vs INFY"
• "Compare RELIANCE.NS with HDFCBANK.NS"
"""
        
        try:
            comparison_data = []
            
            for symbol in symbols[:3]:  # Limit to 3 stocks
                stock = yf.Ticker(symbol)
                info = stock.info
                df = stock.history(period='1mo')
                
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                previous_close = info.get('previousClose', current_price)
                change_percent = ((current_price - previous_close) / previous_close * 100) if previous_close else 0
                
                comparison_data.append({
                    'symbol': symbol,
                    'name': info.get('longName', symbol),
                    'price': current_price,
                    'change': change_percent,
                    'market_cap': info.get('marketCap', 0),
                    'pe': info.get('trailingPE', 'N/A')
                })
            
            response = "📊 **Stock Comparison**\n\n"
            
            for data in comparison_data:
                emoji = "🟢" if data['change'] >= 0 else "🔴"
                market_cap_b = data['market_cap'] / 1e9 if isinstance(data['market_cap'], (int, float)) else 0
                
                response += f"""
**{data['name']} ({data['symbol']})**
💰 Price: ${data['price']:.2f}
{emoji} Change: {data['change']:+.2f}%
🏢 Market Cap: ${market_cap_b:.2f}B
📊 P/E Ratio: {data['pe']}

---
"""
            
            # Winner
            best_performer = max(comparison_data, key=lambda x: x['change'])
            response += f"\n🏆 **Best Performer:** {best_performer['symbol']} ({best_performer['change']:+.2f}%)"
            
            return response
            
        except Exception as e:
            return f"❌ Error comparing stocks: {str(e)}"
    
    def _handle_market_query(self, query):
        """Handle market overview queries"""
        response = """
📊 **Market Overview**

**Indian Markets:**
🇮🇳 NIFTY 50 - Indian benchmark index
🇮🇳 SENSEX - Bombay Stock Exchange index

**US Markets:**
🇺🇸 S&P 500 - US large-cap index
🇺🇸 NASDAQ - Tech-heavy index
🇺🇸 DOW JONES - Industrial average

**Market Hours:**
• Indian Markets: 9:15 AM - 3:30 PM IST
• US Markets: 9:30 AM - 4:00 PM EST

Would you like to check specific stocks or indices?

**Try asking:**
• "What's the price of RELIANCE.NS?"
• "Analyze TCS"
• "Compare INFY and WIPRO"
"""
        return response
    
    def _handle_top_stocks_query(self, query):
        """Handle top stocks queries"""
        if 'indian' in query.lower() or 'india' in query.lower() or 'nse' in query.lower():
            return """
📈 **Top Indian Stocks to Watch:**

**Technology:**
🖥️ TCS.NS - Tata Consultancy Services
🖥️ INFY.NS - Infosys
🖥️ WIPRO.NS - Wipro

**Banking:**
🏦 HDFCBANK.NS - HDFC Bank
🏦 ICICIBANK.NS - ICICI Bank
🏦 SBIN.NS - State Bank of India

**Conglomerate:**
🏭 RELIANCE.NS - Reliance Industries
🏭 LT.NS - Larsen & Toubro

**FMCG:**
🛒 HINDUNILVR.NS - Hindustan Unilever
🛒 ITC.NS - ITC Limited

Would you like me to analyze any of these stocks?
"""
        else:
            return """
📈 **Top US Tech Stocks:**

**Mega Cap:**
🍎 AAPL - Apple Inc.
🪟 MSFT - Microsoft
🔍 GOOGL - Alphabet (Google)
📦 AMZN - Amazon

**AI & Chips:**
🎮 NVDA - NVIDIA
💻 AMD - Advanced Micro Devices

**EV & Innovation:**
⚡ TSLA - Tesla
🚀 META - Meta Platforms

Would you like me to analyze any of these stocks?
"""
    
    def _handle_news_query(self, query):
        """Handle news queries"""
        return """
📰 **Market News & Updates**

For the latest market news, I recommend:

**Indian Markets:**
• Economic Times - economictimes.com
• MoneyControl - moneycontrol.com
• NSE India - nseindia.com

**US Markets:**
• Bloomberg - bloomberg.com
• CNBC - cnbc.com
• Yahoo Finance - finance.yahoo.com

💡 **Tip:** I can analyze any stock for you in real-time!

Try asking:
• "What's the price of AAPL?"
• "Analyze RELIANCE.NS"
• "Should I buy TCS?"
"""
    
    def _get_help_message(self):
        """Return help message"""
        return """
🤖 **Stock Chatbot - I can help you with:**

📊 **Stock Prices:**
• "What's the price of AAPL?"
• "How much is RELIANCE.NS trading at?"

📈 **Stock Analysis:**
• "Analyze TCS"
• "Give me analysis of MSFT"

💡 **Recommendations:**
• "Should I buy INFY?"
• "Is AAPL a good investment?"

🔄 **Comparisons:**
• "Compare AAPL and MSFT"
• "TCS vs INFY"

🏆 **Top Stocks:**
• "Show me top Indian stocks"
• "Best US tech stocks"

📰 **Market Info:**
• "Market overview"
• "Latest news"

💬 **Just ask me anything about stocks!**

**Example Questions:**
• "What's the price of Tesla?"
• "Analyze RELIANCE"
• "Should I buy Apple stock?"
• "Compare Google and Microsoft"

⚠️ Remember: This is educational content, not financial advice!
"""
    
    def _get_default_response(self, query):
        """Default response when query not understood"""
        return """
💬 I'm not sure I understood that. 

🤖 **I can help you with:**
• Stock prices ("What's the price of AAPL?")
• Stock analysis ("Analyze RELIANCE.NS")
• Buy/Sell recommendations ("Should I buy TCS?")
• Stock comparisons ("Compare INFY and WIPRO")
• Market information ("Market overview")

Type "help" to see all available commands!

Or just ask me anything about stocks! 📊
"""
    
    def _extract_stock_symbol(self, query):
        """Extract stock symbol from query"""
        query_upper = query.upper()
        
        # Common stock symbols
        symbols = {
            # US Stocks
            'APPLE': 'AAPL', 'AAPL': 'AAPL',
            'MICROSOFT': 'MSFT', 'MSFT': 'MSFT',
            'GOOGLE': 'GOOGL', 'GOOGL': 'GOOGL',
            'AMAZON': 'AMZN', 'AMZN': 'AMZN',
            'TESLA': 'TSLA', 'TSLA': 'TSLA',
            'META': 'META', 'FACEBOOK': 'META',
            'NVIDIA': 'NVDA', 'NVDA': 'NVDA',
            'NETFLIX': 'NFLX', 'NFLX': 'NFLX',
            
            # Indian Stocks
            'RELIANCE': 'RELIANCE.NS', 'RELIANCE.NS': 'RELIANCE.NS',
            'TCS': 'TCS.NS', 'TCS.NS': 'TCS.NS',
            'TATA': 'TCS.NS',
            'INFOSYS': 'INFY.NS', 'INFY': 'INFY.NS', 'INFY.NS': 'INFY.NS',
            'HDFC': 'HDFCBANK.NS', 'HDFCBANK': 'HDFCBANK.NS', 'HDFCBANK.NS': 'HDFCBANK.NS',
            'ICICI': 'ICICIBANK.NS', 'ICICIBANK': 'ICICIBANK.NS', 'ICICIBANK.NS': 'ICICIBANK.NS',
            'WIPRO': 'WIPRO.NS', 'WIPRO.NS': 'WIPRO.NS',
            'ITC': 'ITC.NS', 'ITC.NS': 'ITC.NS',
            'SBI': 'SBIN.NS', 'SBIN': 'SBIN.NS', 'SBIN.NS': 'SBIN.NS',
        }
        
        # Check for symbol in query
        for key, value in symbols.items():
            if key in query_upper:
                return value
        
        # Check for .NS or .BO suffix
        words = query_upper.split()
        for word in words:
            if word.endswith('.NS') or word.endswith('.BO'):
                return word
        
        return None
    
    def get_api_info(self):
        """Get API configuration info"""
        return {
            'api_key': self.api_key,
            'status': 'Active',
            'version': '1.0',
            'capabilities': [
                'Stock Price Queries',
                'Technical Analysis',
                'Buy/Sell Recommendations',
                'Stock Comparisons',
                'Market Overview',
                'Real-time Data'
            ]
        }

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize chatbot
    bot = StockChatbot()
    
    print("🤖 Stock Chatbot Initialized!")
    print(f"API Key: {bot.api_key}")
    print("\nTest queries:")
    print("-" * 50)
    
    # Test queries
    test_queries = [
        "What's the price of AAPL?",
        "Analyze RELIANCE.NS",
        "Should I buy TCS?",
        "Compare MSFT and GOOGL",
        "Help"
    ]
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = bot.process_query(query)
        print(f"🤖 Bot: {response[:200]}...")  # First 200 chars
        print("-" * 50)