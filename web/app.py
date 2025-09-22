#!/usr/bin/env python3
"""
Crypto MCP Assistant - Main Streamlit App for Vercel
Optimized pentru deployment pe Vercel
"""

import streamlit as st
import asyncio
import sys
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import requests
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
except ImportError as e:
    st.error(f"Required dependency missing: {e}")
    st.stop()

# Page configuration
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
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #FF6B35, #F7931E, #FFD23F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}

.status-good {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.status-warning {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.sidebar-content {
    padding: 1rem;
}

.crypto-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    background: white;
}
</style>
""", unsafe_allow_html=True)

def get_demo_market_data():
    """Get demo market data for display"""
    return {
        "BTCUSDT": {
            "price": 63250.45,
            "change_24h": 2.34,
            "volume_24h": 28500000000,
            "market_cap": 1245000000000
        },
        "ETHUSDT": {
            "price": 2456.78,
            "change_24h": -1.23,
            "volume_24h": 15200000000,
            "market_cap": 295000000000
        },
        "EGLDUSDT": {
            "price": 32.15,
            "change_24h": 5.67,
            "volume_24h": 125000000,
            "market_cap": 850000000
        }
    }

def create_price_chart(symbol_data, symbol):
    """Create a simple price chart"""
    # Generate sample data for demo
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    base_price = symbol_data['price']
    
    # Create sample price movements
    prices = []
    current_price = base_price * 0.95
    for i in range(30):
        change = (hash(f"{symbol}{i}") % 200 - 100) / 1000  # Pseudo-random change
        current_price *= (1 + change)
        prices.append(current_price)
    
    fig = go.Figure(data=go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name=symbol,
        line=dict(color='#FF6B35', width=3)
    ))
    
    fig.update_layout(
        title=f"{symbol} Price Trend (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Price (USDT)",
        template="plotly_white",
        height=400
    )
    
    return fig

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Crypto MCP Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            AI-powered cryptocurrency trading assistant with MCP integration
        </p>
        <p style="color: #999;">🇷🇴 Made with ❤️ in Romania | Powered by AI & MCP</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        
        # Trading mode
        trading_mode = st.selectbox(
            "Trading Mode",
            ["Paper Trading (Safe)", "Live Trading (Expert Only)"],
            index=0
        )
        
        # Risk settings
        st.markdown("### 🛡️ Risk Management")
        risk_percentage = st.slider("Risk per Trade (%)", 0.5, 5.0, 2.0, 0.1)
        max_positions = st.slider("Max Open Positions", 1, 10, 3)
        
        # Favorite symbols
        st.markdown("### ⭐ Favorite Symbols")
        symbols = st.multiselect(
            "Select symbols to monitor",
            ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"],
            default=["BTCUSDT", "ETHUSDT", "EGLDUSDT"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Market Overview", "🎯 Trading Signals", "💼 Portfolio", "📈 Analysis", "🤖 AI Chat"])
    
    # Market Overview Tab
    with tab1:
        st.markdown("### 📊 Market Overview")
        
        market_data = get_demo_market_data()
        
        # Market metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card status-good">
                <h3>📈 Market Sentiment</h3>
                <h2>Bullish</h2>
                <p>Fear & Greed: 72/100</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>💰 Total Market Cap</h3>
                <h2>$2.45T</h2>
                <p>+3.2% (24h)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 24h Volume</h3>
                <h2>$85.6B</h2>
                <p>-1.4% (24h)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card status-warning">
                <h3>⚡ Active Signals</h3>
                <h2>3</h2>
                <p>2 Buy, 1 Hold</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Price cards for selected symbols
        st.markdown("### 💎 Monitored Symbols")
        
        cols = st.columns(len(symbols))
        for i, symbol in enumerate(symbols):
            if symbol in market_data:
                data = market_data[symbol]
                change_color = "green" if data['change_24h'] > 0 else "red"
                change_symbol = "+" if data['change_24h'] > 0 else ""
                
                with cols[i]:
                    st.markdown(f"""
                    <div class="crypto-card">
                        <h4 style="margin-bottom: 0.5rem;">{symbol.replace('USDT', '/USDT')}</h4>
                        <h2 style="color: #333; margin: 0.5rem 0;">${data['price']:,.2f}</h2>
                        <p style="color: {change_color}; font-weight: bold; margin: 0;">
                            {change_symbol}{data['change_24h']:.2f}% (24h)
                        </p>
                        <p style="color: #666; font-size: 0.9rem; margin: 0.25rem 0;">
                            Vol: ${data['volume_24h']/1e9:.1f}B
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Price charts
        st.markdown("---")
        st.markdown("### 📈 Price Charts")
        
        chart_symbol = st.selectbox("Select symbol for detailed chart", symbols)
        if chart_symbol in market_data:
            fig = create_price_chart(market_data[chart_symbol], chart_symbol)
            st.plotly_chart(fig, use_container_width=True)
    
    # Trading Signals Tab
    with tab2:
        st.markdown("### 🎯 AI Trading Signals")
        
        # Signal generation
        col1, col2 = st.columns([3, 1])
        with col1:
            signal_symbol = st.selectbox("Generate signal for:", symbols, key="signal_symbol")
        with col2:
            if st.button("🎯 Generate Signal", type="primary"):
                with st.spinner("Analyzing market data..."):
                    # Simulate signal generation
                    st.success("Signal generated successfully!")
        
        # Demo signals
        st.markdown("#### 📋 Active Trading Signals")
        
        signals = [
            {
                "symbol": "BTCUSDT",
                "action": "BUY",
                "confidence": 0.85,
                "entry": 63250,
                "stop_loss": 61800,
                "take_profit": 65500,
                "reasoning": "Strong bullish momentum with RSI oversold recovery"
            },
            {
                "symbol": "EGLDUSDT", 
                "action": "BUY",
                "confidence": 0.78,
                "entry": 32.15,
                "stop_loss": 30.50,
                "take_profit": 35.20,
                "reasoning": "Romanian focus + technical breakout pattern"
            }
        ]
        
        for signal in signals:
            confidence_color = "green" if signal['confidence'] > 0.7 else "orange" if signal['confidence'] > 0.5 else "red"
            action_color = "green" if signal['action'] == "BUY" else "red" if signal['action'] == "SELL" else "orange"
            
            st.markdown(f"""
            <div class="crypto-card" style="border-left: 4px solid {action_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: {action_color};">📊 {signal['symbol']} - {signal['action']}</h4>
                    <span style="background: {confidence_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 15px; font-size: 0.8rem;">
                        {signal['confidence']:.0%} Confidence
                    </span>
                </div>
                <div style="margin: 1rem 0; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                    <div><strong>Entry:</strong> ${signal['entry']:,.2f}</div>
                    <div><strong>Stop Loss:</strong> ${signal['stop_loss']:,.2f}</div>
                    <div><strong>Take Profit:</strong> ${signal['take_profit']:,.2f}</div>
                </div>
                <p style="margin: 0.5rem 0 0 0; color: #666; font-style: italic;">{signal['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Portfolio Tab
    with tab3:
        st.markdown("### 💼 Portfolio Management")
        
        # Portfolio summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Portfolio Value", "$12,450.30", "+3.2%")
        with col2:
            st.metric("Total P&L", "+$1,245.67", "+11.4%")
        with col3:
            st.metric("Win Rate", "68%", "+5%")
        with col4:
            st.metric("Active Positions", "2", "")
        
        st.markdown("---")
        
        # Positions table
        st.markdown("#### 📈 Open Positions")
        
        positions_data = {
            "Symbol": ["BTCUSDT", "EGLDUSDT"],
            "Side": ["LONG", "LONG"],
            "Entry Price": [61800.0, 30.50],
            "Current Price": [63250.45, 32.15],
            "Quantity": [0.1, 15.0],
            "P&L ($)": [145.05, 24.75],
            "P&L (%)": [2.35, 5.41]
        }
        
        df = pd.DataFrame(positions_data)
        
        # Color code P&L
        def color_pnl(val):
            if isinstance(val, (int, float)):
                color = 'green' if val > 0 else 'red' if val < 0 else 'black'
                return f'color: {color}'
            return ''
        
        st.dataframe(
            df.style.applymap(color_pnl, subset=['P&L ($)', 'P&L (%)']),
            use_container_width=True
        )
    
    # Analysis Tab  
    with tab4:
        st.markdown("### 📈 Technical Analysis")
        
        analysis_symbol = st.selectbox("Select symbol for analysis:", symbols, key="analysis_symbol")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Technical Indicators")
            
            # Mock technical analysis data
            indicators = {
                "RSI (14)": {"value": 67.3, "signal": "Neutral", "color": "orange"},
                "MACD": {"value": "Bullish Cross", "signal": "Buy", "color": "green"},
                "SMA 20/50": {"value": "Golden Cross", "signal": "Buy", "color": "green"},
                "Bollinger Bands": {"value": "Mid Band", "signal": "Neutral", "color": "orange"},
                "Volume": {"value": "Above Average", "signal": "Bullish", "color": "green"}
            }
            
            for indicator, data in indicators.items():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem; border: 1px solid #ddd; margin: 0.25rem 0; border-radius: 5px;">
                    <span><strong>{indicator}</strong></span>
                    <span style="color: {data['color']};">{data['signal']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎯 Support & Resistance")
            
            levels = {
                "Strong Resistance": 65500,
                "Resistance": 64200,
                "Current Price": 63250,
                "Support": 62100,
                "Strong Support": 60800
            }
            
            for level, price in levels.items():
                color = "red" if "Resistance" in level else "green" if "Support" in level else "blue"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem; border: 1px solid {color}; margin: 0.25rem 0; border-radius: 5px; background: rgba({"255,0,0" if "Resistance" in level else "0,255,0" if "Support" in level else "0,0,255"}, 0.1);">
                    <span><strong>{level}</strong></span>
                    <span style="color: {color}; font-weight: bold;">${price:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
    
    # AI Chat Tab
    with tab5:
        st.markdown("### 🤖 AI Trading Assistant")
        st.markdown("Chat with your AI trading assistant for market insights and analysis.")
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "👋 Salut! Sunt asistentul tău AI pentru crypto trading. Cum te pot ajuta azi?"}
            ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Întreabă despre piața crypto, analiza tehnică sau strategii de trading..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    # Simulate AI response based on prompt
                    if "btc" in prompt.lower() or "bitcoin" in prompt.lower():
                        response = "🔍 **Bitcoin Analysis**: BTC arată semne puternice de bullish momentum. RSI este la 67.3, indicând o poziție neutră cu tendință ascendentă. MACD a făcut un bullish cross recent. Recomand să urmărești breakout-ul peste $64,200 pentru o poziție long cu target $65,500."
                    elif "egld" in prompt.lower() or "elrond" in prompt.lower():
                        response = "🇷🇴 **EGLD Analysis**: MultiversX (EGLD) shows strong momentum cu un breakout pattern clar. Ca focus românesc, EGLD are potential mare de creștere. Entry point bun la $32.15 cu stop loss la $30.50 și target $35.20. Confidence: 78%"
                    elif "strateg" in prompt.lower():
                        response = "📈 **Strategii de Trading**: Pentru piața actuală recomand: 1) DCA pe dips pentru BTC/ETH 2) Swing trading pe EGLD 3) Risk management: max 2% pe trade 4) Urmărește volumele pentru confirmarea breakout-urilor. Paper trading first!"
                    else:
                        response = "🤖 Înțeleg întrebarea ta despre crypto. Bazat pe analiza actuală de piață, Bitcoin arată bullish, EGLD are momentum bun, iar piața generală este în trend ascendent. Ai nevoie de o analiză specifică pentru un anumit symbol?"
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>⚠️ <strong>Disclaimer</strong>: Acest software este doar pentru scopuri educaționale. 
        Crypto trading implică riscuri financiare semnificative. Nu investiți mai mult decât vă puteți permite să pierdeți.</p>
        <p>🇷🇴 <strong>Made with ❤️ in Romania</strong> | 
        <a href="https://github.com/Gzeu/crypto-mcp-assistant" target="_blank">GitHub Repository</a> | 
        Powered by AI & MCP</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()