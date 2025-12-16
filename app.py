"""
Stock Exchange Prediction Dashboard - COMPLETE FIXED VERSION
With Perfect Navbar Alignment - Ready to Use!
Copy this entire code and paste into app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import (
    fetch_stock_data, fetch_global_quote, calculate_technical_indicators,
    get_stock_recommendation, INDIAN_STOCKS, US_STOCKS, fetch_stock_data_hybrid
)
from chatbot import StockChatbot
from stock_predictor import StockPredictor, simple_linear_prediction, calculate_support_resistance

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Stock Exchange Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS WITH PERFECT NAVBAR
# ============================================================================
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background - Professional Dark Gradient */
    .stApp {
        background: linear-gradient(135deg, #1a237e 0%, #283593 25%, #3949ab 50%, #5c6bc0 100%);
        color: white;
    }
    
    /* Sidebar - Modern Dark Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.3);
    }
    
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Navigation Radio Buttons */
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 15px;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* Page Header - Bright and Visible */
    .page-header {
        font-size: 48px;
        font-weight: 900;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        background: linear-gradient(90deg, #ffd700, #ffed4e, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    /* Metric Cards - White with Shadow */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 3px solid #64b5f6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(100, 181, 246, 0.5);
    }
    
    /* Buttons - Bright and Visible */
    .stButton > button {
        background: linear-gradient(90deg, #ff6f00 0%, #ff8f00 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 6px 20px rgba(255, 111, 0, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 111, 0, 0.6);
        background: linear-gradient(90deg, #ff8f00 0%, #ffa726 100%);
    }
    
    /* Text colors - High Contrast (avoid forcing white on all elements) */
    .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Metrics - Bright Colors */
    [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        border-radius: 12px;
        border-left: 6px solid #2196f3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stAlert p, .stAlert div {
        color: #000000 !important;
        text-shadow: none !important;
    }
    
    /* Chat messages - White Background */
    .chat-message-user {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(227, 242, 253, 0.95));
        border-radius: 18px;
        padding: 18px 24px;
        margin: 15px 0;
        border-left: 6px solid #ff6f00;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .chat-message-user p, .chat-message-user strong {
        color: #000000 !important;
        text-shadow: none !important;
    }
    
    .chat-message-bot {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(200, 230, 201, 0.95));
        border-radius: 18px;
        padding: 18px 24px;
        margin: 15px 0;
        border-left: 6px solid #4caf50;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    .chat-message-bot p, .chat-message-bot strong, .chat-message-bot div {
        color: #000000 !important;
        text-shadow: none !important;
    }
    
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        margin: 20px 0;
    }
    
    .chat-header {
        background: linear-gradient(90deg, #ff6f00, #ff8f00);
        color: white;
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(255, 111, 0, 0.4);
    }
    
    .chat-header h3, .chat-header p {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Select boxes and inputs */
    .stSelectbox label, .stTextInput label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Data frames and tables */
    .stDataFrame {
        background: white;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 10px;
    }
    
    .streamlit-expanderHeader p {
        color: white !important;
        font-weight: 600 !important;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# TOP NAVBAR - STREAMLIT NATIVE (NO HTML ISSUES)
# ============================================================================
from datetime import datetime
import pytz

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist)
current_hour = current_time_ist.hour
current_minute = current_time_ist.minute
current_day = current_time_ist.weekday()  # 0=Monday, 6=Sunday

# Market open: Monday-Friday, 9:15 AM - 3:30 PM IST
is_weekday = current_day < 5  # Monday to Friday
is_market_hours = (current_hour == 9 and current_minute >= 15) or (10 <= current_hour <= 14) or (current_hour == 15 and current_minute <= 30)
is_market_open = is_weekday and is_market_hours

market_status_text = '🟢 Market Open' if is_market_open else '🔴 Market Closed'
current_time = current_time_ist.strftime('%I:%M %p IST')

# Create navbar using Streamlit columns with better visibility
navbar_container = st.container()
with navbar_container:
    # Add a bright orange background container
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #ff6f00 0%, #ff8f00 50%, #ff9800 100%);
                padding: 30px 40px;
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 8px 30px rgba(255, 111, 0, 0.5);
                border: 3px solid #e65100;'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 300px;'>
                <h1 style='color: white !important; 
                           margin: 0; 
                           font-size: 42px;
                           font-weight: 900;
                           text-shadow: 3px 3px 8px rgba(0,0,0,0.6);
                           letter-spacing: 1px;'>
                    📈 Stock Exchange Dashboard
                </h1>
                <p style='color: rgba(255,255,255,0.95) !important; 
                          margin: 8px 0 0 0; 
                          font-size: 18px; 
                          font-weight: 600;
                          text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>
                    ⚡ Real-time Market Analysis & AI Predictions
                </p>
            </div>
            <div style='display: flex; gap: 30px; align-items: center; margin-top: 10px;'>
                <div style='background: rgba(255,255,255,0.2);
                            padding: 15px 25px;
                            border-radius: 12px;
                            backdrop-filter: blur(10px);
                            border: 2px solid rgba(255,255,255,0.3);'>
                    <h3 style='color: white !important; 
                               margin: 0; 
                               font-size: 22px;
                               font-weight: 700;
                               text-shadow: 2px 2px 6px rgba(0,0,0,0.6);'>
                        {market_status_text}
                    </h3>
                </div>
                <div style='background: rgba(255,255,255,0.2);
                            padding: 15px 25px;
                            border-radius: 12px;
                            backdrop-filter: blur(10px);
                            border: 2px solid rgba(255,255,255,0.3);'>
                    <h3 style='color: white !important; 
                               margin: 0; 
                               font-size: 22px;
                               font-weight: 700;
                               text-shadow: 2px 2px 6px rgba(0,0,0,0.6);'>
                        🕐 {current_time}
                    </h3>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 2px solid rgba(255,255,255,0.3); margin: 20px 0;'>", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = StockChatbot()
if 'predictor' not in st.session_state:
    st.session_state.predictor = StockPredictor()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'use_alpha_vantage' not in st.session_state:
    st.session_state.use_alpha_vantage = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'market' not in st.session_state:
    st.session_state.market = "NSE (India)"

# ============================================================================
# TOP NAVIGATION BUTTONS
# ============================================================================
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("🏠 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
        st.session_state.current_page = "Dashboard"
        st.rerun()

with nav_col2:
    if st.button("📈 Live Data", use_container_width=True, type="primary" if st.session_state.current_page == "Live Data" else "secondary"):
        st.session_state.current_page = "Live Data"
        st.rerun()

with nav_col3:
    if st.button("🤖 AI Chatbot", use_container_width=True, type="primary" if st.session_state.current_page == "AI Chatbot" else "secondary"):
        st.session_state.current_page = "AI Chatbot"
        st.rerun()

with nav_col4:
    if st.button("🔮 Predictions", use_container_width=True, type="primary" if st.session_state.current_page == "Predictions" else "secondary"):
        st.session_state.current_page = "Predictions"
        st.rerun()

with nav_col5:
    if st.button("📊 Analysis", use_container_width=True, type="primary" if st.session_state.current_page == "Technical Analysis" else "secondary"):
        st.session_state.current_page = "Technical Analysis"
        st.rerun()

with nav_col6:
    if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
        st.session_state.current_page = "About"
        st.rerun()

page = st.session_state.current_page

# Settings
with st.expander("⚙️ Settings", expanded=False):
    set_col1, set_col2 = st.columns(2)
    with set_col1:
        st.session_state.market = st.selectbox("Market:", ["NSE (India)", "BSE (India)", "US Markets"], key="market_select")
    with set_col2:
        api_source = st.radio("API:", ["Yahoo Finance", "Alpha Vantage"], label_visibility="collapsed")
        st.session_state.use_alpha_vantage = (api_source == "Alpha Vantage")

market = st.session_state.market

# ============================================================================
# PAGES
# ============================================================================

if "Dashboard" in page:
    st.markdown('<h1 class="page-header">📊 Live Market Dashboard</h1>', unsafe_allow_html=True)
    
    # FIXED: Visible Orange Info Bar
    st.markdown("""
    <div style='background: linear-gradient(90deg, #FF9800, #FF5722); 
                color: white; 
                padding: 20px; 
                border-radius: 12px; 
                margin: 20px 0;
                border-left: 6px solid #E65100;
                box-shadow: 0 4px 12px rgba(255, 152, 0, 0.4);'>
        <h3 style='color: white; margin: 0; font-size: 22px;'>
            💡 Select stocks to view real-time data, charts, and AI recommendations
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if market == "NSE (India)":
            stock_options = INDIAN_STOCKS['NSE']
        elif market == "BSE (India)":
            stock_options = INDIAN_STOCKS['BSE']
        else:
            stock_options = US_STOCKS
        
        selected_stock = st.selectbox(
            "🔍 Select Stock:",
            options=list(stock_options.keys()),
            format_func=lambda x: f"{x} - {stock_options[x]}"
        )
    
    with col2:
        timeframe = st.selectbox("📅 Timeframe:", ["1 Day", "5 Days", "1 Month", "3 Months"])
    
    with col3:
        st.markdown("###")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    if selected_stock:
        with st.spinner(f"Loading data for {selected_stock}..."):
            # Use selected API source
            if st.session_state.use_alpha_vantage:
                from utils import fetch_stock_data_hybrid
                st.info("🔑 Fetching from Alpha Vantage API...")
                quote = fetch_global_quote(selected_stock, use_alpha_vantage=True)
                df = fetch_stock_data_hybrid(selected_stock, prefer_alpha_vantage=True)
            else:
                quote = fetch_global_quote(selected_stock)
                df = fetch_stock_data(selected_stock)
        
        if quote and df is not None:
            # Key Metrics Row
            col1, col2, col3, col4, col5 = st.columns(5)
            
            current_price = float(quote.get('05. price', 0))
            change = float(quote.get('09. change', 0))
            change_percent = quote.get('10. change percent', '0%').replace('%', '')
            
            with col1:
                st.metric("💰 Price", f"₹{current_price:.2f}", f"{change:.2f}")
            with col2:
                st.metric("📊 Change", f"{change_percent}%")
            with col3:
                st.metric("📈 High", f"₹{quote.get('03. high', 'N/A')}")
            with col4:
                st.metric("📉 Low", f"₹{quote.get('04. low', 'N/A')}")
            with col5:
                st.metric("📦 Volume", f"{float(quote.get('06. volume', 0))/1000000:.2f}M")
            
            st.markdown("---")
            
            # Technical Analysis
            df = calculate_technical_indicators(df)
            recommendation = get_stock_recommendation(df)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### 🎯 AI Recommendation: {recommendation}")
            
            with col2:
                latest = df.iloc[-1]
                rsi_value = latest['RSI']
                if rsi_value > 70:
                    st.error("⚠️ Overbought Zone")
                elif rsi_value < 30:
                    st.success("✅ Oversold - Buy Signal")
                else:
                    st.info("🟡 Neutral Zone")
            
            # Price Chart
            st.markdown("### 📈 Live Price Chart")
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name='OHLC'
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df['SMA_20'], name='SMA 20',
                line=dict(color='orange', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df['SMA_50'], name='SMA 50',
                line=dict(color='red', width=2)
            ))
            
            fig.update_layout(
                title=f"{stock_options[selected_stock]} - Live Price Movement",
                yaxis_title="Price (₹)", xaxis_title="Date",
                height=600, template="plotly_white",
                plot_bgcolor='rgba(255,255,255,0.8)',
                paper_bgcolor='rgba(255,255,255,0.6)',
                font=dict(color='#0D47A1')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Technical Indicators Grid
            st.markdown("### 📊 Technical Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("#### RSI")
                st.metric("Value", f"{latest['RSI']:.2f}")
                st.progress(min(latest['RSI'] / 100, 1.0))
            
            with col2:
                st.markdown("#### MACD")
                st.metric("MACD", f"{latest['MACD']:.4f}")
                st.metric("Signal", f"{latest['Signal_Line']:.4f}")
            
            with col3:
                st.markdown("#### Bollinger Bands")
                st.metric("Upper", f"₹{latest['BB_Upper']:.2f}")
                st.metric("Lower", f"₹{latest['BB_Lower']:.2f}")
            
            with col4:
                st.markdown("#### Moving Avg")
                st.metric("SMA 20", f"₹{latest['SMA_20']:.2f}")
                st.metric("SMA 50", f"₹{latest['SMA_50']:.2f}")
        else:
            st.error(f"⚠️ Unable to fetch data for {selected_stock}")
elif "Live Data" in page:
    st.markdown('<h1 class="page-header">📡 Live Market Feed</h1>', unsafe_allow_html=True)
    
    if market == "NSE (India)":
        stock_options = INDIAN_STOCKS['NSE']
    elif market == "BSE (India)":
        stock_options = INDIAN_STOCKS['BSE']
    else:
        stock_options = US_STOCKS
    
    selected_stocks = st.multiselect(
        "Select stocks to track:",
        list(stock_options.keys()),
        default=list(stock_options.keys())[:3]
    )
    
    if selected_stocks:
        if st.button("🔄 Refresh All", use_container_width=True):
            st.rerun()
        
        data_rows = []
        for stock in selected_stocks:
            quote = fetch_global_quote(stock)
            if quote:
                data_rows.append({
                    'Symbol': stock,
                    'Name': stock_options[stock],
                    'Price': f"₹{float(quote.get('05. price', 0)):.2f}",
                    'Change': quote.get('09. change', 'N/A'),
                    'Change %': quote.get('10. change percent', 'N/A'),
                    'Volume': quote.get('06. volume', 'N/A')
                })
        
        if data_rows:
            st.markdown(f"### 🕐 Last Updated: {datetime.now().strftime('%I:%M:%S %p')}")
            st.dataframe(pd.DataFrame(data_rows), use_container_width=True, hide_index=True)
            
            st.markdown("### 📊 Visual Grid")
            cols = st.columns(3)
            for idx, row in enumerate(data_rows):
                with cols[idx % 3]:
                    change_val = float(row['Change']) if row['Change'] != 'N/A' else 0
                    change_icon = "🟢" if change_val > 0 else "🔴"
                    change_color = "#00e676" if change_val > 0 else "#ff1744"
                    bg_color = "rgba(0, 230, 118, 0.1)" if change_val > 0 else "rgba(255, 23, 68, 0.1)"
                    border_color = "#00e676" if change_val > 0 else "#ff1744"
                    
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {bg_color}, rgba(255,255,255,0.95));
                                padding: 25px;
                                border-radius: 15px;
                                border: 3px solid {border_color};
                                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                                margin: 10px 0;
                                transition: transform 0.3s ease;'>
                        <h3 style='color: #ffffff; 
                                   margin: 0 0 15px 0; 
                                   font-size: 20px;
                                   font-weight: 700;
                                   text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
                                   background: linear-gradient(90deg, #ff6f00, #ff8f00);
                                   padding: 10px;
                                   border-radius: 8px;'>
                            {row['Symbol']}
                        </h3>
                        <h2 style='color: #ffd700;
                                   margin: 15px 0;
                                   font-size: 36px;
                                   font-weight: 900;
                                   text-shadow: 2px 2px 6px rgba(0,0,0,0.5);'>
                            {row['Price']}
                        </h2>
                        <p style='color: {change_color};
                                  margin: 10px 0 0 0;
                                  font-size: 18px;
                                  font-weight: 700;
                                  text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>
                            {change_icon} {row['Change']} ({row['Change %']})
                        </p>
                        <p style='color: #ffffff;
                                  margin: 10px 0 0 0;
                                  font-size: 14px;
                                  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                            Volume: {row.get('Volume', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

elif "Chatbot" in page:
    st.markdown('<h1 class="page-header">🤖 AI Stock Assistant</h1>', unsafe_allow_html=True)
    
    # Enhanced header
    st.markdown("""
    <div class="chat-header">
        <h3 style='margin: 0; color: white;'>💬 Ask me anything about stocks, markets, or trading!</h3>
        <p style='margin: 5px 0 0 0; color: rgba(255,255,255,0.9); font-size: 14px;'>
            Powered by Alpha Vantage API (CMLKV2SLOT89UPM9)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container with better styling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message-user">
                <strong style='color: #0D47A1; font-size: 16px;'>🧑 You:</strong>
                <p style='margin: 8px 0 0 0; color: #1976D2; font-size: 15px;'>{msg['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-bot">
                <strong style='color: #1976D2; font-size: 16px;'>🤖 AI Assistant:</strong>
                <div style='margin: 8px 0 0 0; color: #333; font-size: 14px; line-height: 1.6;'>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("💭 Type your question here...")
    
    if user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        with st.spinner("🤔 Analyzing your question..."):
            response = st.session_state.chatbot.process_query(user_input)
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 RELIANCE Price", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "What's the price of RELIANCE.NS?"})
            response = st.session_state.chatbot.process_query("What's the price of RELIANCE.NS?")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col2:
        if st.button("📊 Analyze TCS", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "Analyze TCS.NS"})
            response = st.session_state.chatbot.process_query("Analyze TCS.NS")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col3:
        if st.button("🎯 INFY Tips", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "Should I buy INFY.NS?"})
            response = st.session_state.chatbot.process_query("Should I buy INFY.NS?")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    # Additional quick questions
    st.markdown("### 💡 More Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📈 AAPL Price", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "What's the price of AAPL?"})
            response = st.session_state.chatbot.process_query("What's the price of AAPL?")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col2:
        if st.button("🔍 Compare Stocks", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "Compare AAPL vs MSFT"})
            response = st.session_state.chatbot.process_query("Compare AAPL vs MSFT")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col3:
        if st.button("📰 Market News", use_container_width=True):
            st.session_state.chat_history.append({'role': 'user', 'content': "What's the latest market news?"})
            response = st.session_state.chatbot.process_query("What's the latest market news?")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col4:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Help section
    with st.expander("❓ How to use the AI Assistant"):
        st.markdown("""
        **Ask me questions like:**
        - "What's the current price of AAPL?"
        - "Analyze RELIANCE.NS stock"
        - "Should I buy TCS.NS?"
        - "Compare INFY vs WIPRO"
        - "What's the market trend today?"
        - "Tell me about Microsoft stock"
        
        **Features:**
        - 💰 Real-time stock prices
        - 📊 Technical analysis (RSI, MACD, Moving Averages)
        - 🎯 Buy/Sell recommendations
        - 📈 Stock comparisons
        - 📰 Market insights
        - 🔍 Company information
        
        **Note:** All recommendations are for educational purposes only, not financial advice.
        """)

elif "Predictions" in page:
    st.markdown('<h1 class="page-header">🔮 AI Price Predictions</h1>', unsafe_allow_html=True)
    st.warning("⚠️ Educational purposes only. Not financial advice!")
    
    if market == "NSE (India)":
        stock_options = INDIAN_STOCKS['NSE']
    elif market == "BSE (India)":
        stock_options = INDIAN_STOCKS['BSE']
    else:
        stock_options = US_STOCKS
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        selected_stock = st.selectbox("Stock:", list(stock_options.keys()))
    with col2:
        days = st.slider("Forecast Days:", 1, 14, 7)
    with col3:
        st.markdown("###")
        predict_btn = st.button("🔮 Predict", use_container_width=True)
    
    if predict_btn:
        with st.spinner("Generating predictions..."):
            df = fetch_stock_data(selected_stock)
            
            if df is not None and len(df) > 50:
                df = calculate_technical_indicators(df)
                pred = simple_linear_prediction(df, days=days)
                
                if pred:
                    st.success(f"✅ {days}-day forecast generated!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current", f"₹{pred['current_price']:.2f}")
                    with col2:
                        st.metric("Predicted", f"₹{pred['predictions'][-1]:.2f}")
                    with col3:
                        st.metric("Change", f"{pred['predicted_change']:.2f}%")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df.index[-60:], y=df['Close'][-60:],
                        name='Historical', line=dict(color='blue')
                    ))
                    fig.add_trace(go.Scatter(
                        x=pred['dates'], y=pred['predictions'],
                        name='Predicted', line=dict(color='red', dash='dash')
                    ))
                    fig.update_layout(title="Price Forecast", height=500)
                    st.plotly_chart(fig, use_container_width=True)

elif "Technical Analysis" in page:
    st.markdown('<h1 class="page-header">📊 Technical Analysis</h1>', unsafe_allow_html=True)
    
    if market == "NSE (India)":
        stock_options = INDIAN_STOCKS['NSE']
    elif market == "BSE (India)":
        stock_options = INDIAN_STOCKS['BSE']
    else:
        stock_options = US_STOCKS
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_stock = st.selectbox("Stock:", list(stock_options.keys()))
    with col2:
        st.markdown("###")
        analyze_btn = st.button("📊 Analyze", use_container_width=True)
    
    if analyze_btn:
        df = fetch_stock_data(selected_stock)
        if df is not None and len(df) > 50:
            df = calculate_technical_indicators(df)
            
            tab1, tab2 = st.tabs(["📈 Charts", "🎯 Summary"])
            
            with tab1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
                fig.add_hline(y=70, line_dash="dash", line_color="red")
                fig.add_hline(y=30, line_dash="dash", line_color="green")
                fig.update_layout(title="RSI Indicator", height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                latest = df.iloc[-1]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RSI", f"{latest['RSI']:.2f}")
                with col2:
                    st.metric("MACD", f"{latest['MACD']:.4f}")
                with col3:
                    st.metric("Price", f"₹{latest['Close']:.2f}")
                
                st.markdown(f"### 🎯 Recommendation: {get_stock_recommendation(df)}")

elif "About" in page:
    st.markdown('<h1 class="page-header">ℹ️ About This Project</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Stock Exchange Dashboard
        
        **Real-Time Stock Market Analysis Platform**
        
        #### ✨ Features:
        - 📈 Live market data
        - 🤖 AI chatbot
        - 🔮 Price predictions
        - 📊 Technical analysis
        - 🌐 Multi-market support
        
        #### 🛠️ Technologies:
        - Python 3.10+
        - Streamlit
        - Yahoo Finance API
        - Plotly
        - Scikit-learn
        """)
    
    with col2:
        st.markdown("""
        ### 👥 Team
        - Student Vallepu Balaji
        - Student Sreeja
        - Student Prasanth . B
        
        ### 🎓 Course
        **Mastering Python (PGCET)**  
        Capstone Project
        
        ### 📚 Learning Outcomes
        ✅ API integration  
        ✅ Web development  
        ✅ Machine learning  
        ✅ Data visualization  
        ✅ OOP concepts  
        
        ### 📞 Contact
        Course Instructor: PGCET
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Yahoo Finance API - Active")
    with col2:
        st.success("✅ Streamlit - Running")
    with col3:
        st.success(f"✅ Updated: {datetime.now().strftime('%I:%M %p')}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #0D47A1; font-weight: 600; padding: 20px;'>
    <p>© 2025 Stock Exchange Dashboard | PGCET Capstone Project | Powered by Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)
"""

"""

if "Bulk Scanner" in page:
    # Header with white text on blue background
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1976D2, #2196F3); 
                padding: 30px; border-radius: 15px; margin-bottom: 20px; text-align: center;'>
        <h1 style='color: white; margin: 0; font-size: 48px;'>📡 Bulk Stock Scanner</h1>
        <p style='color: white; font-size: 20px; margin: 10px 0 0 0;'>
            View 200+ stocks across all markets in real-time
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock Categories - COMPLETE LIST
    ALL_STOCKS = {
        "🇺🇸 US Tech Giants": {
            'AAPL': 'Apple Inc.', 'MSFT': 'Microsoft', 'GOOGL': 'Google',
            'AMZN': 'Amazon', 'META': 'Meta', 'NVDA': 'NVIDIA',
            'TSLA': 'Tesla', 'NFLX': 'Netflix', 'AMD': 'AMD',
            'INTC': 'Intel', 'ORCL': 'Oracle', 'IBM': 'IBM',
            'CRM': 'Salesforce', 'ADBE': 'Adobe', 'CSCO': 'Cisco'
        },
        "🏦 US Financial": {
            'JPM': 'JPMorgan Chase', 'BAC': 'Bank of America', 
            'WFC': 'Wells Fargo', 'GS': 'Goldman Sachs', 
            'MS': 'Morgan Stanley', 'C': 'Citigroup',
            'V': 'Visa', 'MA': 'Mastercard', 
            'AXP': 'American Express', 'BLK': 'BlackRock'
        },
        "🏥 US Healthcare": {
            'JNJ': 'Johnson & Johnson', 'UNH': 'UnitedHealth', 
            'PFE': 'Pfizer', 'ABBV': 'AbbVie', 
            'TMO': 'Thermo Fisher', 'ABT': 'Abbott',
            'MRK': 'Merck', 'LLY': 'Eli Lilly', 
            'DHR': 'Danaher', 'BMY': 'Bristol Myers'
        },
        "🛒 US Consumer": {
            'WMT': 'Walmart', 'HD': 'Home Depot', 
            'PG': 'Procter & Gamble', 'KO': 'Coca-Cola', 
            'PEP': 'PepsiCo', 'COST': 'Costco',
            'NKE': 'Nike', 'MCD': 'McDonalds', 
            'SBUX': 'Starbucks', 'DIS': 'Disney'
        },
        "🇮🇳 NSE Top Stocks": {
            'RELIANCE.NS': 'Reliance Industries', 
            'TCS.NS': 'Tata Consultancy', 
            'INFY.NS': 'Infosys',
            'HDFCBANK.NS': 'HDFC Bank', 
            'ICICIBANK.NS': 'ICICI Bank',
            'HINDUNILVR.NS': 'Hindustan Unilever', 
            'ITC.NS': 'ITC Limited', 
            'SBIN.NS': 'State Bank of India',
            'BHARTIARTL.NS': 'Bharti Airtel', 
            'KOTAKBANK.NS': 'Kotak Mahindra Bank',
            'LT.NS': 'Larsen & Toubro', 
            'AXISBANK.NS': 'Axis Bank', 
            'MARUTI.NS': 'Maruti Suzuki',
            'TITAN.NS': 'Titan Company', 
            'WIPRO.NS': 'Wipro',
            'BAJFINANCE.NS': 'Bajaj Finance', 
            'ASIANPAINT.NS': 'Asian Paints', 
            'HCLTECH.NS': 'HCL Technologies',
            'ULTRACEMCO.NS': 'UltraTech Cement', 
            'NESTLEIND.NS': 'Nestle India'
        },
        "💰 Cryptocurrency": {
            'BTC-USD': 'Bitcoin', 
            'ETH-USD': 'Ethereum', 
            'BNB-USD': 'Binance Coin',
            'XRP-USD': 'Ripple', 
            'ADA-USD': 'Cardano', 
            'DOGE-USD': 'Dogecoin',
            'SOL-USD': 'Solana', 
            'MATIC-USD': 'Polygon', 
            'DOT-USD': 'Polkadot'
        }
    }
    
    # White background container
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 15px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;'>
    """, unsafe_allow_html=True)
    
    # Selection Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("<h3 style='color: #1976D2;'>📂 Select Category</h3>", unsafe_allow_html=True)
        selected_category = st.selectbox(
            "Choose market category:",
            list(ALL_STOCKS.keys()),
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<h3 style='color: #1976D2;'>📊 Number</h3>", unsafe_allow_html=True)
        num_stocks = st.slider(
            "How many stocks:",
            5, 25, 10,
            label_visibility="collapsed"
        )
    
    with col3:
        st.markdown("<h3 style='color: #1976D2;'>&nbsp;</h3>", unsafe_allow_html=True)
        load_button = st.button("🔄 Load Live Data", use_container_width=True, type="primary")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Load and Display Data
    if load_button:
        import yfinance as yf
        
        stocks_to_load = ALL_STOCKS[selected_category]
        
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        data_rows = []
        total_stocks = min(num_stocks, len(stocks_to_load))
        
        # Fetch data
        for idx, (symbol, company_name) in enumerate(list(stocks_to_load.items())[:num_stocks]):
            try:
                status_text.markdown(f"**Loading {symbol}... ({idx+1}/{total_stocks})**")
                
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                previous_close = info.get('previousClose', current_price)
                change = current_price - previous_close if previous_close else 0
                change_percent = (change / previous_close * 100) if previous_close else 0
                volume = info.get('volume', 0)
                
                # Format price based on currency
                if symbol.endswith('-USD'):
                    price_formatted = f"${current_price:,.2f}"
                elif '.NS' in symbol or '.BO' in symbol:
                    price_formatted = f"₹{current_price:,.2f}"
                else:
                    price_formatted = f"${current_price:,.2f}"
                
                # Status emoji
                status_emoji = '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
                
                data_rows.append({
                    '': status_emoji,
                    'Symbol': symbol,
                    'Company': company_name,
                    'Price': price_formatted,
                    'Change': f"{change:+.2f}",
                    'Change %': f"{change_percent:+.2f}%",
                    'Volume': f"{volume:,}"
                })
                
                progress_bar.progress((idx + 1) / total_stocks)
                
            except Exception as e:
                continue
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Display Results
        if data_rows:
            # Success message
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #4CAF50, #66BB6A); 
                        color: white; padding: 20px; border-radius: 12px; 
                        margin: 20px 0; text-align: center;
                        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);'>
                <h2 style='margin: 0; color: white; font-size: 28px;'>
                    ✅ Successfully Loaded {len(data_rows)} Stocks
                </h2>
                <p style='margin: 10px 0 0 0; color: white; font-size: 18px;'>
                    Category: {selected_category} | Updated: {datetime.now().strftime('%I:%M:%S %p')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Table View
            st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 20px 0;'>
            """, unsafe_allow_html=True)
            
            st.markdown("<h2 style='color: #1976D2; margin-bottom: 15px;'>📊 Table View</h2>", unsafe_allow_html=True)
            
            df_display = pd.DataFrame(data_rows)
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Grid View
            st.markdown("""
            <div style='background: white; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 20px 0;'>
            """, unsafe_allow_html=True)
            
            st.markdown("<h2 style='color: #1976D2; margin-bottom: 15px;'>📱 Grid View</h2>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            
            for idx, row in enumerate(data_rows):
                with cols[idx % 3]:
                    # Determine card colors with vibrant scheme
                    if row['Change'].startswith('+'):
                        border_color = '#00e676'
                        bg_color = 'linear-gradient(135deg, rgba(0, 230, 118, 0.15), rgba(255, 255, 255, 0.95))'
                        text_color = '#00c853'
                        icon = '🟢'
                    elif row['Change'].startswith('-'):
                        border_color = '#ff1744'
                        bg_color = 'linear-gradient(135deg, rgba(255, 23, 68, 0.15), rgba(255, 255, 255, 0.95))'
                        text_color = '#d50000'
                        icon = '🔴'
                    else:
                        border_color = '#ffc107'
                        bg_color = 'linear-gradient(135deg, rgba(255, 193, 7, 0.15), rgba(255, 255, 255, 0.95))'
                        text_color = '#ff6f00'
                        icon = '🟡'
                    
                    st.markdown(f"""
                    <div style='background: {bg_color}; 
                                padding: 25px; 
                                border-radius: 15px; 
                                border: 3px solid {border_color};
                                margin: 10px 0;
                                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                                transition: transform 0.3s ease;'>
                        <h3 style='color: #ffffff; 
                                   margin: 0 0 10px 0; 
                                   font-size: 20px;
                                   font-weight: 700;
                                   text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
                                   background: linear-gradient(90deg, #ff6f00, #ff8f00);
                                   padding: 10px;
                                   border-radius: 8px;'>
                            {row['']} {row['Symbol']}
                        </h3>
                        <h2 style='color: #ffd700; 
                                   margin: 15px 0; 
                                   font-size: 38px; 
                                   font-weight: 900;
                                   text-shadow: 2px 2px 6px rgba(0,0,0,0.5);'>
                            {row['Price']}
                        </h2>
                        <p style='color: {text_color}; 
                                  margin: 10px 0; 
                                  font-size: 20px; 
                                  font-weight: 700;
                                  text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>
                            {icon} {row['Change']} ({row['Change %']})
                        </p>
                        <p style='color: #ffffff; 
                                  margin: 8px 0; 
                                  font-size: 14px;
                                  font-weight: 600;
                                  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                            📊 Volume: {row.get('Volume', 'N/A')}
                        </p>
                        <p style='color: rgba(255,255,255,0.9); 
                                  margin: 5px 0 0 0; 
                                  font-size: 13px;
                                  text-shadow: 1px 1px 2px rgba(0,0,0,0.4);'>
                            {row.get('Company', row.get('Name', 'N/A'))}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            st.error("❌ No data loaded. Please try again or select a different category.")
    
    # Information Section
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 15px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 20px 0;'>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #1976D2; margin-bottom: 20px;'>📋 Available Stock Categories</h2>", unsafe_allow_html=True)
    
    for category_name, stocks_dict in ALL_STOCKS.items():
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #E3F2FD, #BBDEFB); 
                    padding: 18px; border-radius: 12px; 
                    margin: 12px 0; border-left: 5px solid #1976D2;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <p style='color: #0D47A1; margin: 0; font-size: 18px; font-weight: bold;'>
                {category_name}
            </p>
            <p style='color: #1976D2; margin: 5px 0 0 0; font-size: 16px;'>
                📊 {len(stocks_dict)} stocks available
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Total count
    total_available = sum(len(stocks) for stocks in ALL_STOCKS.values())
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #1976D2, #2196F3); 
                padding: 25px; border-radius: 12px; margin: 20px 0; text-align: center;
                box-shadow: 0 4px 15px rgba(25, 118, 210, 0.4);'>
        <h2 style='color: white; margin: 0; font-size: 32px;'>
            📊 Total Available: {total_available} Stocks
        </h2>
        <p style='color: white; margin: 10px 0 0 0; font-size: 16px;'>
            Across 6 different market categories
        </p>
    </div>
    """, unsafe_allow_html=True)