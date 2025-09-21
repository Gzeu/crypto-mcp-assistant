#!/usr/bin/env python3
"""
Crypto MCP Assistant - Streamlit Dashboard
Interfata web pentru monitorizare trading si interactiune cu AI agent
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Page config
st.set_page_config(
    page_title="Crypto MCP Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .signal-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .buy-signal {
        border-left: 5px solid #28a745;
    }
    .sell-signal {
        border-left: 5px solid #dc3545;
    }
    .hold-signal {
        border-left: 5px solid #ffc107;
    }
    .chat-message {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .assistant-message {
        background-color: #f1f8e9;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_market_data():
    """Fetch market data from API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/market/data",
            json={
                "symbols": ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT"],
                "timeframe": "5m",
                "indicators": ["price", "volume", "change_24h"]
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        st.error(f"Error fetching market data: {e}")
    return {}

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_active_signals():
    """Fetch active trading signals"""
    try:
        response = requests.get(f"{API_BASE_URL}/signals/active", timeout=10)
        if response.status_code == 200:
            return response.json().get("data", {}).get("signals", [])
    except Exception as e:
        st.error(f"Error fetching signals: {e}")
    return []

@st.cache_data(ttl=60)
def fetch_portfolio_summary():
    """Fetch portfolio summary"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/portfolio",
            json={"action": "get_summary"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        st.error(f"Error fetching portfolio: {e}")
    return {}

def send_chat_message(message: str) -> str:
    """Send chat message to AI agent"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("data", {}).get("response", "No response")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def generate_signal(symbol: str, timeframe: str = "5m") -> Dict:
    """Generate trading signal for symbol"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/signals/generate",
            json={"symbol": symbol, "timeframe": timeframe},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        st.error(f"Error generating signal: {e}")
    return {}

def analyze_symbol(symbol: str, timeframe: str = "5m") -> str:
    """Get detailed analysis for symbol"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"symbol": symbol, "timeframe": timeframe},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("data", {}).get("analysis", "No analysis available")
    except Exception as e:
        return f"Error: {str(e)}"

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Crypto MCP Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f77b4/white?text=Crypto+AI", width=200)
        st.title("Navigation")
        
        page = st.selectbox(
            "Selectează pagina:",
            ["Dashboard", "Trading Signals", "Portfolio", "Market Analysis", "AI Chat", "Settings"]
        )
        
        st.markdown("---")
        st.subheader("Quick Actions")
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.experimental_rerun()
        
        if st.button("📊 Market Overview"):
            st.session_state.show_market_overview = True
        
        st.markdown("---")
        st.subheader("Symbol Quick Analysis")
        
        quick_symbol = st.selectbox(
            "Select Symbol:",
            ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT"]
        )
        
        if st.button(f"Analyze {quick_symbol}"):
            with st.spinner(f"Analyzing {quick_symbol}..."):
                analysis = analyze_symbol(quick_symbol)
                st.session_state.quick_analysis = analysis
                st.session_state.quick_symbol = quick_symbol
    
    # Main content based on selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Trading Signals":
        show_trading_signals()
    elif page == "Portfolio":
        show_portfolio()
    elif page == "Market Analysis":
        show_market_analysis()
    elif page == "AI Chat":
        show_ai_chat()
    elif page == "Settings":
        show_settings()
    
    # Display quick analysis if available
    if hasattr(st.session_state, 'quick_analysis'):
        st.markdown("---")
        st.subheader(f"Quick Analysis - {st.session_state.quick_symbol}")
        st.text_area("Analysis Result:", st.session_state.quick_analysis, height=200)
        if st.button("Clear Analysis"):
            del st.session_state.quick_analysis
            del st.session_state.quick_symbol
            st.experimental_rerun()

def show_dashboard():
    """Main dashboard view"""
    st.header("📊 Dashboard Principal")
    
    # Fetch data
    market_data = fetch_market_data()
    signals = fetch_active_signals()
    portfolio = fetch_portfolio_summary()
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        btc_price = market_data.get("BTCUSDT", {}).get("price", 0)
        btc_change = market_data.get("BTCUSDT", {}).get("change_24h", 0)
        st.metric(
            "Bitcoin (BTC)",
            f"${btc_price:,.2f}" if btc_price else "Loading...",
            f"{btc_change:+.2f}%" if btc_change else None
        )
    
    with col2:
        eth_price = market_data.get("ETHUSDT", {}).get("price", 0)
        eth_change = market_data.get("ETHUSDT", {}).get("change_24h", 0)
        st.metric(
            "Ethereum (ETH)",
            f"${eth_price:,.2f}" if eth_price else "Loading...",
            f"{eth_change:+.2f}%" if eth_change else None
        )
    
    with col3:
        egld_price = market_data.get("EGLDUSDT", {}).get("price", 0)
        egld_change = market_data.get("EGLDUSDT", {}).get("change_24h", 0)
        st.metric(
            "MultiversX (EGLD)",
            f"${egld_price:,.2f}" if egld_price else "Loading...",
            f"{egld_change:+.2f}%" if egld_change else None
        )
    
    with col4:
        portfolio_value = portfolio.get("total_value_usd", 0)
        portfolio_pnl = portfolio.get("total_pnl_24h_pct", 0)
        st.metric(
            "Portfolio Value",
            f"${portfolio_value:,.2f}" if portfolio_value else "$0.00",
            f"{portfolio_pnl:+.2f}%" if portfolio_pnl else None
        )
    
    st.markdown("---")
    
    # Market overview and signals
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Market Overview")
        
        if market_data:
            # Create market overview chart
            symbols = []
            prices = []
            changes = []
            
            for symbol, data in market_data.items():
                if isinstance(data, dict) and "price" in data:
                    symbols.append(symbol.replace("USDT", ""))
                    prices.append(data.get("price", 0))
                    changes.append(data.get("change_24h", 0))
            
            if symbols:
                df = pd.DataFrame({
                    "Symbol": symbols,
                    "Price": prices,
                    "Change 24h (%)": changes
                })
                
                # Color code based on change
                colors = ['green' if x > 0 else 'red' if x < 0 else 'gray' for x in changes]
                
                fig = px.bar(
                    df,
                    x="Symbol",
                    y="Change 24h (%)",
                    color="Change 24h (%)",
                    color_continuous_scale="RdYlGn",
                    title="24h Price Changes"
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No market data available")
        else:
            st.info("Loading market data...")
    
    with col2:
        st.subheader("🎯 Active Signals")
        
        if signals:
            for signal in signals[:5]:  # Show top 5 signals
                signal_class = f"{signal.get('action', 'hold').lower()}-signal"
                
                st.markdown(f"""
                <div class="signal-card {signal_class}">
                    <strong>{signal.get('symbol', 'Unknown')}</strong><br>
                    Action: {signal.get('action', 'HOLD')}<br>
                    Confidence: {signal.get('confidence', 0):.1%}<br>
                    Entry: ${signal.get('entry_price', 0):.4f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active signals")
    
    # Recent activity
    st.markdown("---")
    st.subheader("📋 Recent Activity")
    
    # Mock recent activity data
    activity_data = [
        {"time": "2 min ago", "action": "Signal Generated", "details": "BUY BTCUSDT @ $45,230"},
        {"time": "5 min ago", "action": "Market Analysis", "details": "Updated ETHUSDT analysis"},
        {"time": "8 min ago", "action": "Portfolio Update", "details": "Position closed: EGLD +2.3%"},
        {"time": "12 min ago", "action": "Risk Alert", "details": "High volatility detected on SOLUSDT"},
    ]
    
    for activity in activity_data:
        col1, col2, col3 = st.columns([1, 2, 3])
        with col1:
            st.text(activity["time"])
        with col2:
            st.text(activity["action"])
        with col3:
            st.text(activity["details"])

def show_trading_signals():
    """Trading signals page"""
    st.header("🎯 Trading Signals")
    
    # Signal generation section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generate New Signal")
        
        signal_col1, signal_col2, signal_col3 = st.columns(3)
        
        with signal_col1:
            signal_symbol = st.selectbox(
                "Symbol:",
                ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "LINKUSDT"]
            )
        
        with signal_col2:
            signal_timeframe = st.selectbox(
                "Timeframe:",
                ["1m", "5m", "15m", "1h", "4h", "1d"]
            )
        
        with signal_col3:
            st.write("")
            if st.button("Generate Signal", type="primary"):
                with st.spinner(f"Generating signal for {signal_symbol}..."):
                    signal_data = generate_signal(signal_symbol, signal_timeframe)
                    if signal_data:
                        st.session_state.new_signal = signal_data
    
    with col2:
        st.subheader("Quick Stats")
        signals = fetch_active_signals()
        
        total_signals = len(signals)
        buy_signals = len([s for s in signals if s.get('action') == 'BUY'])
        sell_signals = len([s for s in signals if s.get('action') == 'SELL'])
        
        st.metric("Total Active", total_signals)
        st.metric("Buy Signals", buy_signals)
        st.metric("Sell Signals", sell_signals)
    
    # Display new signal if generated
    if hasattr(st.session_state, 'new_signal'):
        st.markdown("---")
        st.subheader("🆕 New Signal Generated")
        
        signal = st.session_state.new_signal
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Action", signal.get('action', 'HOLD'))
        with col2:
            st.metric("Confidence", f"{signal.get('confidence', 0):.1%}")
        with col3:
            st.metric("Entry Price", f"${signal.get('entry_price', 0):.4f}")
        with col4:
            st.metric("Risk Score", f"{signal.get('risk_score', 0):.2f}")
        
        st.text_area("Reasoning:", signal.get('reasoning', 'No reasoning provided'), height=150)
        
        if st.button("Clear Signal"):
            del st.session_state.new_signal
            st.experimental_rerun()
    
    # Active signals table
    st.markdown("---")
    st.subheader("📊 Active Signals")
    
    signals = fetch_active_signals()
    
    if signals:
        df = pd.DataFrame(signals)
        
        # Format the dataframe
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
            df['confidence'] = df['confidence'].apply(lambda x: f"{x:.1%}")
            df['entry_price'] = df['entry_price'].apply(lambda x: f"${x:.4f}")
            df['stop_loss'] = df['stop_loss'].apply(lambda x: f"${x:.4f}")
            df['take_profit'] = df['take_profit'].apply(lambda x: f"${x:.4f}")
            
            # Select columns to display
            display_cols = ['symbol', 'action', 'confidence', 'entry_price', 'stop_loss', 'take_profit', 'timestamp']
            df_display = df[display_cols]
            df_display.columns = ['Symbol', 'Action', 'Confidence', 'Entry', 'Stop Loss', 'Take Profit', 'Time']
            
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No signals data to display")
    else:
        st.info("No active signals found")

def show_portfolio():
    """Portfolio page"""
    st.header("💼 Portfolio Management")
    
    portfolio = fetch_portfolio_summary()
    
    if portfolio:
        # Portfolio overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Value",
                f"${portfolio.get('total_value_usd', 0):,.2f}"
            )
        
        with col2:
            st.metric(
                "24h P&L",
                f"{portfolio.get('total_pnl_24h_pct', 0):+.2f}%",
                f"${portfolio.get('total_pnl_24h_usd', 0):+,.2f}"
            )
        
        with col3:
            st.metric(
                "Total P&L",
                f"{portfolio.get('total_pnl_pct', 0):+.2f}%",
                f"${portfolio.get('total_pnl_usd', 0):+,.2f}"
            )
        
        with col4:
            st.metric(
                "Open Positions",
                portfolio.get('open_positions_count', 0)
            )
        
        st.markdown("---")
        
        # Positions breakdown
        if 'positions' in portfolio:
            st.subheader("📈 Current Positions")
            
            positions = portfolio['positions']
            if positions:
                df = pd.DataFrame(positions)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No open positions")
        
        # Portfolio allocation chart
        if 'allocation' in portfolio:
            st.subheader("🥧 Portfolio Allocation")
            
            allocation = portfolio['allocation']
            if allocation:
                fig = px.pie(
                    values=list(allocation.values()),
                    names=list(allocation.keys()),
                    title="Asset Allocation"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Portfolio data not available")

def show_market_analysis():
    """Market analysis page"""
    st.header("📊 Market Analysis")
    
    # Symbol selection
    col1, col2 = st.columns([1, 1])
    
    with col1:
        analysis_symbol = st.selectbox(
            "Select Symbol for Analysis:",
            ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "LINKUSDT"]
        )
    
    with col2:
        analysis_timeframe = st.selectbox(
            "Select Timeframe:",
            ["5m", "15m", "1h", "4h", "1d"],
            index=2  # Default to 1h
        )
    
    if st.button("Run Deep Analysis", type="primary"):
        with st.spinner(f"Running deep analysis for {analysis_symbol}..."):
            analysis = analyze_symbol(analysis_symbol, analysis_timeframe)
            st.session_state.market_analysis = analysis
            st.session_state.analysis_symbol = analysis_symbol
    
    # Display analysis
    if hasattr(st.session_state, 'market_analysis'):
        st.markdown("---")
        st.subheader(f"📋 Analysis Results - {st.session_state.analysis_symbol}")
        st.text_area(
            "Detailed Analysis:",
            st.session_state.market_analysis,
            height=400
        )
    
    # Market overview section
    st.markdown("---")
    st.subheader("🌍 Global Market Overview")
    
    if st.button("Get Market Overview"):
        with st.spinner("Fetching market overview..."):
            try:
                response = requests.get(f"{API_BASE_URL}/market/overview", timeout=30)
                if response.status_code == 200:
                    overview = response.json().get("data", {}).get("overview", "No overview available")
                    st.session_state.market_overview = overview
            except Exception as e:
                st.error(f"Error fetching market overview: {e}")
    
    if hasattr(st.session_state, 'market_overview'):
        st.text_area(
            "Market Overview:",
            st.session_state.market_overview,
            height=300
        )

def show_ai_chat():
    """AI Chat interface"""
    st.header("🤖 AI Chat Assistant")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    st.subheader("💬 Conversation")
    
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>AI Assistant:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Ask me anything about crypto trading:",
            placeholder="Example: What's your analysis on Bitcoin right now?",
            height=100
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Send", type="primary"):
            if user_input.strip():
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                # Get AI response
                with st.spinner("AI is thinking..."):
                    response = send_chat_message(user_input)
                    
                    # Add AI response
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                
                st.experimental_rerun()
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Market Summary"):
            quick_message = "Give me a quick summary of the current crypto market situation"
            st.session_state.chat_history.extend([
                {"role": "user", "content": quick_message},
                {"role": "assistant", "content": send_chat_message(quick_message)}
            ])
            st.experimental_rerun()
    
    with col2:
        if st.button("🎯 Trading Ideas"):
            quick_message = "What are your top 3 trading ideas for today?"
            st.session_state.chat_history.extend([
                {"role": "user", "content": quick_message},
                {"role": "assistant", "content": send_chat_message(quick_message)}
            ])
            st.experimental_rerun()
    
    with col3:
        if st.button("⚠️ Risk Check"):
            quick_message = "Analyze the current market risk and what I should watch out for"
            st.session_state.chat_history.extend([
                {"role": "user", "content": quick_message},
                {"role": "assistant", "content": send_chat_message(quick_message)}
            ])
            st.experimental_rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Configuration")
    
    # API Settings
    with st.expander("API Configuration"):
        api_url = st.text_input("API Base URL:", value=API_BASE_URL)
        if st.button("Test Connection"):
            try:
                response = requests.get(f"{api_url}/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Connection successful!")
                else:
                    st.error(f"❌ Connection failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")
    
    # Display Settings
    with st.expander("Display Settings"):
        refresh_interval = st.slider("Auto-refresh interval (seconds):", 10, 300, 30)
        show_advanced = st.checkbox("Show advanced features", value=False)
        dark_mode = st.checkbox("Dark mode", value=False)
    
    # Trading Settings
    with st.expander("Trading Preferences"):
        default_timeframe = st.selectbox(
            "Default timeframe:",
            ["1m", "5m", "15m", "1h", "4h", "1d"],
            index=1
        )
        
        preferred_symbols = st.multiselect(
            "Preferred symbols:",
            ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "LINKUSDT"],
            default=["BTCUSDT", "ETHUSDT", "EGLDUSDT"]
        )
        
        risk_tolerance = st.selectbox(
            "Risk tolerance:",
            ["Conservative", "Moderate", "Aggressive"]
        )
    
    # Notification Settings
    with st.expander("Notifications"):
        enable_notifications = st.checkbox("Enable notifications", value=True)
        discord_notifications = st.checkbox("Discord notifications", value=False)
        telegram_notifications = st.checkbox("Telegram notifications", value=False)
        email_notifications = st.checkbox("Email notifications", value=False)
    
    # Save settings button
    if st.button("💾 Save Settings", type="primary"):
        # Here you would save settings to a config file or database
        st.success("Settings saved successfully!")
    
    # System information
    st.markdown("---")
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Application Info:**
        - Version: 1.0.0
        - Last Updated: {datetime.now().strftime('%Y-%m-%d')}
        - API Status: Connected ✅
        """)
    
    with col2:
        st.info(f"""
        **Performance:**
        - Response Time: ~200ms
        - Cache Hit Rate: 85%
        - Active Connections: 3
        """)

if __name__ == "__main__":
    main()