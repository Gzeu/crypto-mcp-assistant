#!/usr/bin/env python3
"""
Crypto MCP Assistant - Simplified FastAPI Backend for Vercel
Optimized pentru deployment pe Vercel cu dependencies minime
"""

import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Mock classes pentru demo
class MockCryptoData:
    """Mock crypto data for demo purposes"""
    
    def __init__(self):
        self.demo_data = {
            "BTCUSDT": {
                "price": 63250.45,
                "change_24h": 2.34,
                "volume_24h": 28500000000,
                "high_24h": 64100.00,
                "low_24h": 61800.00
            },
            "ETHUSDT": {
                "price": 2456.78,
                "change_24h": -1.23,
                "volume_24h": 15200000000,
                "high_24h": 2510.00,
                "low_24h": 2420.00
            },
            "EGLDUSDT": {
                "price": 32.15,
                "change_24h": 5.67,
                "volume_24h": 125000000,
                "high_24h": 33.20,
                "low_24h": 30.40
            }
        }
    
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for symbol"""
        return self.demo_data.get(symbol, {
            "price": 0.0,
            "change_24h": 0.0,
            "volume_24h": 0,
            "high_24h": 0.0,
            "low_24h": 0.0
        })
    
    async def analyze_symbol(self, symbol: str, timeframe: str = "5m") -> Dict[str, Any]:
        """Analyze symbol and return trading insights"""
        price_data = await self.get_price(symbol)
        
        # Mock analysis based on price action
        is_bullish = price_data['change_24h'] > 0
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": price_data['price'],
            "trend": "BULLISH" if is_bullish else "BEARISH",
            "rsi": 67.3 if is_bullish else 32.1,
            "macd": "Bullish Cross" if is_bullish else "Bearish Cross",
            "volume_status": "Above Average" if price_data['volume_24h'] > 1000000 else "Below Average",
            "support_level": price_data['price'] * 0.95,
            "resistance_level": price_data['price'] * 1.05,
            "recommendation": "BUY" if is_bullish and price_data['change_24h'] > 2 else "HOLD",
            "confidence": 0.85 if abs(price_data['change_24h']) > 3 else 0.65,
            "last_updated": datetime.now().isoformat()
        }

class MockAIAgent:
    """Mock AI agent for demo responses"""
    
    def __init__(self):
        self.crypto_data = MockCryptoData()
    
    async def chat_response(self, message: str) -> str:
        """Generate AI response to user message"""
        message_lower = message.lower()
        
        if "btc" in message_lower or "bitcoin" in message_lower:
            return "🔍 **Bitcoin Analysis**: BTC arată semne puternice de bullish momentum. RSI este la 67.3, indicând o poziție neutră cu tendință ascendentă. MACD a făcut un bullish cross recent. Recomand să urmărești breakout-ul peste $64,200 pentru o poziție long cu target $65,500. Risk management: stop loss la $61,800."
        
        elif "eth" in message_lower or "ethereum" in message_lower:
            return "⚡ **Ethereum Analysis**: ETH se consolează după mișcarea recentă. RSI la 45.2 indică posibilitate de rebound. Urmărește volumul pentru confirmarea direcției. Support la $2,420, resistance la $2,510. Neutral bias până la breakout clar."
        
        elif "egld" in message_lower or "elrond" in message_lower or "multiversx" in message_lower:
            return "🇷🇴 **EGLD Analysis**: MultiversX (EGLD) arată momentum puternic cu breakout pattern clar. Ca focus românesc, EGLD are potențial mare de creștere. Entry point bun la $32.15 cu stop loss la $30.50 și target $35.20. Confidence: 78%. Volumul confirmă mișcarea."
        
        elif "strateg" in message_lower or "trading" in message_lower:
            return "📈 **Strategii de Trading**: Pentru piața actuală recomand: 1) DCA pe dips pentru BTC/ETH 2) Swing trading pe EGLD cu focus pe breakout-uri 3) Risk management: max 2% pe trade 4) Urmărește volumele pentru confirmarea breakout-urilor 5) Paper trading first! Patience is key."
        
        elif "risc" in message_lower or "risk" in message_lower:
            return "🛡️ **Risk Management**: Reguli esențiale: 1) Nu investi mai mult decât îți permiți să pierzi 2) Folosește stop loss întotdeauna 3) Diversifică portofoliul 4) Max 2-3% risc pe trade 5) Ține jurnal de trading 6) Controlează emoțiile - greed și fear sunt inamicii traderului."
        
        elif "analiz" in message_lower or "analis" in message_lower:
            return "🔬 **Analiză Tehnică**: Folosesc indicatori multipli: RSI pentru momentum, MACD pentru trend changes, Bollinger Bands pentru volatilitate, Volume pentru confirmarea mișcărilor. Combin analiza tehnică cu fundamentals și sentiment analysis. Timeframes multiple pentru accuracy."
        
        else:
            return "🤖 Înțeleg întrebarea ta despre crypto. Bazat pe analiza actuală de piață: Bitcoin arată bullish, EGLD are momentum bun, iar piața generală este în trend ascendent. Pentru analize specifice, întreabă despre BTC, ETH, EGLD sau strategii de trading. Cum te pot ajuta?"

# Global instances
crypto_data = MockCryptoData()
ai_agent = MockAIAgent()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management pentru FastAPI app"""
    # Startup
    print("🚀 Starting Crypto MCP Assistant API (Vercel)...")
    yield
    # Shutdown
    print("⏹️ Shutting down Crypto MCP Assistant API...")

# FastAPI app initialization
app = FastAPI(
    title="Crypto MCP Assistant API",
    description="AI-powered cryptocurrency trading assistant (Vercel Demo)",
    version="1.0.0-vercel",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="Mesajul utilizatorului")
    context: Optional[str] = Field(None, description="Context additional")

class AnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Simbolul crypto (ex: BTCUSDT)")
    timeframe: Optional[str] = Field("5m", description="Timeframe pentru analiza")

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 Crypto MCP Assistant API (Vercel)",
        "version": "1.0.0-vercel",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "chat": "/api/v1/chat",
            "analyze": "/api/v1/analyze",
            "market": "/api/v1/market/overview",
            "price": "/api/v1/price/{symbol}"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": "vercel",
        "components": {
            "crypto_data": True,
            "ai_agent": True,
            "api": True
        }
    }

# =============================================================================
# CHAT & AI ENDPOINTS
# =============================================================================

@app.post("/api/v1/chat", response_model=APIResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat cu agentul AI pentru analiza crypto"""
    try:
        response = await ai_agent.chat_response(request.message)
        
        return APIResponse(
            success=True,
            data={
                "response": response,
                "context": request.context,
                "message": request.message
            },
            message="Chat response generated successfully"
        )
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze", response_model=APIResponse)
async def analyze_symbol(request: AnalysisRequest):
    """Analiza detaliata pentru un simbol specific"""
    try:
        analysis = await crypto_data.analyze_symbol(request.symbol, request.timeframe)
        
        return APIResponse(
            success=True,
            data=analysis,
            message=f"Analysis completed for {request.symbol}"
        )
    except Exception as e:
        print(f"Error analyzing {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# MARKET DATA ENDPOINTS
# =============================================================================

@app.get("/api/v1/price/{symbol}", response_model=APIResponse)
async def get_symbol_price(symbol: str):
    """Obtine pretul curent pentru un simbol"""
    try:
        price_data = await crypto_data.get_price(symbol.upper())
        
        return APIResponse(
            success=True,
            data={
                "symbol": symbol.upper(),
                "price_data": price_data,
                "last_updated": datetime.now().isoformat()
            },
            message=f"Price data retrieved for {symbol}"
        )
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/overview", response_model=APIResponse)
async def get_market_overview():
    """Obtine overview general al pietei crypto"""
    try:
        # Get data for major symbols
        btc_data = await crypto_data.get_price("BTCUSDT")
        eth_data = await crypto_data.get_price("ETHUSDT")
        egld_data = await crypto_data.get_price("EGLDUSDT")
        
        # Calculate market metrics
        total_volume_24h = btc_data['volume_24h'] + eth_data['volume_24h'] + egld_data['volume_24h']
        avg_change = (btc_data['change_24h'] + eth_data['change_24h'] + egld_data['change_24h']) / 3
        
        market_sentiment = "Bullish" if avg_change > 1 else "Bearish" if avg_change < -1 else "Neutral"
        fear_greed_index = max(25, min(75, 50 + avg_change * 5))  # Mock calculation
        
        overview = {
            "market_sentiment": market_sentiment,
            "fear_greed_index": round(fear_greed_index),
            "total_market_cap": "$2.45T",
            "total_volume_24h": f"${total_volume_24h/1e9:.1f}B",
            "btc_dominance": "52.3%",
            "symbols": {
                "BTCUSDT": btc_data,
                "ETHUSDT": eth_data,
                "EGLDUSDT": egld_data
            },
            "top_gainers": [
                {"symbol": "EGLDUSDT", "change": egld_data['change_24h']},
                {"symbol": "BTCUSDT", "change": btc_data['change_24h']}
            ],
            "analysis": f"Piața crypto arată {market_sentiment.lower()} cu Fear & Greed Index la {round(fear_greed_index)}/100. "
                       f"Bitcoin la ${btc_data['price']:,.0f} (+{btc_data['change_24h']:.1f}%), "
                       f"Ethereum la ${eth_data['price']:,.0f} ({eth_data['change_24h']:+.1f}%), "
                       f"EGLD la ${egld_data['price']:,.2f} (+{egld_data['change_24h']:.1f}%). "
                       f"Volumul total de ${total_volume_24h/1e9:.1f}B indică activitate {('mare' if total_volume_24h > 4e10 else 'moderată')}."
        }
        
        return APIResponse(
            success=True,
            data=overview,
            message="Market overview retrieved successfully"
        )
    except Exception as e:
        print(f"Error getting market overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# TRADING SIGNALS ENDPOINTS
# =============================================================================

@app.get("/api/v1/signals/generate/{symbol}", response_model=APIResponse)
async def generate_trading_signal(symbol: str, timeframe: str = "5m"):
    """Genereaza semnal de trading pentru un simbol"""
    try:
        analysis = await crypto_data.analyze_symbol(symbol.upper(), timeframe)
        price_data = await crypto_data.get_price(symbol.upper())
        
        # Generate trading signal based on analysis
        signal = {
            "symbol": symbol.upper(),
            "timeframe": timeframe,
            "action": analysis["recommendation"],
            "confidence": analysis["confidence"],
            "entry_price": price_data['price'],
            "stop_loss": analysis["support_level"],
            "take_profit": analysis["resistance_level"],
            "current_price": price_data['price'],
            "risk_reward_ratio": round((analysis["resistance_level"] - price_data['price']) / (price_data['price'] - analysis["support_level"]), 2),
            "reasoning": f"Analiza tehnică pentru {symbol}: Trend {analysis['trend']}, RSI {analysis['rsi']:.1f}, MACD {analysis['macd']}, Volum {analysis['volume_status']}. Recomandare: {analysis['recommendation']} cu confidence {analysis['confidence']:.0%}.",
            "indicators": {
                "rsi": analysis["rsi"],
                "macd": analysis["macd"],
                "trend": analysis["trend"],
                "volume_status": analysis["volume_status"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            success=True,
            data=signal,
            message=f"Trading signal generated for {symbol}"
        )
    except Exception as e:
        print(f"Error generating signal for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "environment": "vercel"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "environment": "vercel"
        }
    )

# Export for Vercel
handler = app