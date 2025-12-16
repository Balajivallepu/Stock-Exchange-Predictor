"""
Stock Exchange Prediction Dashboard
Complete Main Application
Combine this with the code from Part 1 and Part 2
"""

# INSTRUCTIONS TO CREATE COMPLETE app.py:
# 1. Copy the entire content from "app.py - Stock Dashboard" artifact
# 2. Remove the comment "# Continue in next artifact..." at the end
# 3. Copy the entire content from "app.py - Part 2" artifact
# 4. Paste Part 2 content right after Part 1 (where the comment was)
# 5. Save as app.py

# The complete app.py should have this structure:

"""
1. Imports and Configuration (from Part 1)
2. Session State Initialization (from Part 1)
3. Sidebar Navigation (from Part 1)
4. Dashboard Page (from Part 1)
5. Live Data Page (from Part 1)
6. Chatbot Page (from Part 1)
7. Predictions Page (from Part 2)
8. Technical Analysis Page (from Part 2)
9. About Page (from Part 2)
10. Footer (from Part 2)
"""

# Quick Tips for Combining:
# - Make sure there are no duplicate imports
# - Keep all session_state initializations together
# - Ensure proper indentation
# - Test after combining

# Alternative: You can also use this simplified version for testing:

import streamlit as st
from utils import *
from chatbot import StockChatbot
from stock_predictor import StockPredictor
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Stock Exchange Prediction Dashboard")

# Initialize
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = StockChatbot()

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to:", ["Dashboard", "Chatbot", "About"])

if page == "Dashboard":
    st.header("Live Stock Data")
    
    symbol = st.selectbox("Select Stock:", 
                         ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS'])
    
    if st.button("Get Data"):
        with st.spinner("Fetching data..."):
            df = fetch_stock_data(symbol)
            
            if df is not None:
                st.success("Data loaded successfully!")
                
                # Display chart
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                ))
                fig.update_layout(title=f"{symbol} - Price Chart", height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                df = calculate_technical_indicators(df)
                latest = df.iloc[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"₹{latest['Close']:.2f}")
                with col2:
                    st.metric("RSI", f"{latest['RSI']:.2f}")
                with col3:
                    st.metric("Recommendation", get_stock_recommendation(df))
            else:
                st.error("Failed to fetch data")

elif page == "Chatbot":
    st.header("🤖 AI Stock Assistant")
    
    user_input = st.text_input("Ask me about stocks:")
    
    if user_input:
        response = st.session_state.chatbot.process_query(user_input)
        st.markdown(response)

elif page == "About":
    st.header("About This Project")
    st.write("""
    This is a Stock Exchange Prediction Dashboard built for PGCET capstone project.
    
    Features:
    - Live stock data
    - AI chatbot
    - Technical analysis
    - Price predictions
    
    Technologies: Python, Streamlit, Alpha Vantage API
    """)

st.markdown("---")
st.caption("© 2025 PGCET Students | Capstone Project")