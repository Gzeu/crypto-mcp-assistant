#!/usr/bin/env python3
"""
Crypto MCP Assistant - FastAPI Backend
API server pentru interfata web si integrari externe
"""

import asyncio
import sys
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.ai_agent import CryptoAIAgent, TradingSignal
from src.trading.binance_client import BinanceClient
from src.trading.portfolio_tracker import PortfolioTracker
from src.data.data_fetcher import DataFetcher

# Global agent instance
agent: Optional[CryptoAIAgent] = None
portfolio_tracker: Optional[PortfolioTracker] = None
data_fetcher: Optional[DataFetcher] = None
binance_client: Optional[BinanceClient] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management pentru FastAPI app"""
    global agent, portfolio_tracker, data_fetcher, binance_client
    
    # Startup
    logger.info("Starting Crypto MCP Assistant API...")
    try:
        agent = CryptoAIAgent()
        portfolio_tracker = PortfolioTracker()
        data_fetcher = DataFetcher()
        binance_client = BinanceClient()
        
        logger.info("All components initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Crypto MCP Assistant API...")
    try:
        if agent:
            await agent.stop_trading_session()
        logger.info("Shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# FastAPI app initialization
app = FastAPI(
    title="Crypto MCP Assistant API",
    description="AI-powered cryptocurrency trading assistant with MCP integration",
    version="1.0.0",
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

# Security
security = HTTPBearer(auto_error=False)

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="Mesajul utilizatorului")
    context: Optional[str] = Field(None, description="Context additional")

class TradingSignalRequest(BaseModel):
    symbol: str = Field(..., description="Simbolul crypto (ex: BTCUSDT)")
    timeframe: Optional[str] = Field("5m", description="Timeframe pentru analiza")
    force_analysis: Optional[bool] = Field(False, description="Forteaza analiza noua")

class PortfolioRequest(BaseModel):
    action: str = Field(..., description="Actiunea: get_summary, get_positions, get_performance")
    symbol: Optional[str] = Field(None, description="Simbol specific (optional)")
    timeframe: Optional[str] = Field("24h", description="Perioada pentru performance")

class NotificationRequest(BaseModel):
    type: str = Field(..., description="Tipul notificarii: discord, telegram")
    message: str = Field(..., description="Mesajul de trimis")
    urgent: Optional[bool] = Field(False, description="Notificare urgenta")

class MarketDataRequest(BaseModel):
    symbols: List[str] = Field(..., description="Lista de simboluri")
    timeframe: Optional[str] = Field("5m", description="Timeframe")
    indicators: Optional[List[str]] = Field(["price", "volume"], description="Indicatori dorii")

# Response models
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class TradingSignalResponse(BaseModel):
    symbol: str
    action: str
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    reasoning: str
    risk_score: float
    position_size_usd: float
    timestamp: datetime

# Dependency functions
async def get_current_agent() -> CryptoAIAgent:
    """Dependency pentru a obtine agentul curent"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificare token pentru autentificare (optional)"""
    # Implement proper authentication in production
    return True

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "components": {
            "agent": agent is not None,
            "portfolio_tracker": portfolio_tracker is not None,
            "data_fetcher": data_fetcher is not None,
            "binance_client": binance_client is not None
        }
    }

# Main endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Crypto MCP Assistant API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

# =============================================================================
# CHAT & AI ENDPOINTS
# =============================================================================

@app.post("/api/v1/chat", response_model=APIResponse)
async def chat_with_agent(
    request: ChatRequest,
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Chat cu agentul AI pentru analiza crypto"""
    try:
        response = await current_agent.manual_analysis(request.message)
        
        return APIResponse(
            success=True,
            data={"response": response, "context": request.context},
            message="Analysis completed successfully"
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze", response_model=APIResponse)
async def analyze_symbol(
    request: TradingSignalRequest,
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Analiza detaliata pentru un simbol specific"""
    try:
        query = f"""
        Analizeaza {request.symbol} pe timeframe {request.timeframe}:
        1. Analiza tehnica completa
        2. Indicatori: RSI, MACD, Bollinger Bands
        3. Support si resistance
        4. Volumul si momentum
        5. Recomandarile de trading cu niveluri exacte
        
        Vreau o analiza detaliata cu nivele concrete de intrare, stop loss si take profit.
        """
        
        analysis = await current_agent.manual_analysis(query)
        
        return APIResponse(
            success=True,
            data={
                "symbol": request.symbol,
                "timeframe": request.timeframe,
                "analysis": analysis,
                "timestamp": datetime.now()
            },
            message=f"Analysis completed for {request.symbol}"
        )
    except Exception as e:
        logger.error(f"Error analyzing {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# TRADING SIGNALS ENDPOINTS
# =============================================================================

@app.post("/api/v1/signals/generate", response_model=APIResponse)
async def generate_trading_signal(
    request: TradingSignalRequest,
    background_tasks: BackgroundTasks,
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Genereaza semnal de trading pentru un simbol"""
    try:
        # Generate signal using the agent's signal generator
        query = f"""
        Genereaza un semnal de trading precis pentru {request.symbol}:
        1. Analiza pe timeframe {request.timeframe}
        2. Actiunea recomandata: BUY/SELL/HOLD
        3. Nivele exacte: entry, stop loss, take profit
        4. Confidence score (0-100)
        5. Raționamentul complet
        6. Risk assessment
        
        Format: ACTION|ENTRY_PRICE|STOP_LOSS|TAKE_PROFIT|CONFIDENCE|REASONING
        """
        
        response = await current_agent.manual_analysis(query)
        
        # Parse response to extract signal data
        signal_data = _parse_signal_response(response, request.symbol)
        
        return APIResponse(
            success=True,
            data=signal_data,
            message=f"Signal generated for {request.symbol}"
        )
    except Exception as e:
        logger.error(f"Error generating signal for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/signals/active", response_model=APIResponse)
async def get_active_signals(
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Obtine semnalele active de trading"""
    try:
        active_signals = await current_agent.get_active_signals()
        
        signals_data = [
            {
                "symbol": signal.symbol,
                "action": signal.action,
                "confidence": signal.confidence,
                "entry_price": signal.entry_price,
                "stop_loss": signal.stop_loss,
                "take_profit": signal.take_profit,
                "reasoning": signal.reasoning,
                "timestamp": signal.timestamp,
                "risk_score": signal.risk_score,
                "position_size_usd": signal.position_size_usd
            }
            for signal in active_signals
        ]
        
        return APIResponse(
            success=True,
            data={"signals": signals_data, "count": len(signals_data)},
            message=f"Retrieved {len(signals_data)} active signals"
        )
    except Exception as e:
        logger.error(f"Error getting active signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# PORTFOLIO ENDPOINTS
# =============================================================================

@app.post("/api/v1/portfolio", response_model=APIResponse)
async def portfolio_operations(
    request: PortfolioRequest,
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Operatiuni cu portofoliul"""
    try:
        if request.action == "get_summary":
            portfolio_summary = await current_agent.get_portfolio_summary()
            return APIResponse(
                success=True,
                data=portfolio_summary,
                message="Portfolio summary retrieved"
            )
        
        elif request.action == "get_positions":
            if portfolio_tracker:
                positions = await portfolio_tracker.get_open_positions()
                return APIResponse(
                    success=True,
                    data={"positions": positions},
                    message="Open positions retrieved"
                )
            else:
                raise HTTPException(status_code=503, detail="Portfolio tracker not available")
        
        elif request.action == "get_performance":
            if portfolio_tracker:
                performance = await portfolio_tracker.get_performance_metrics(request.timeframe)
                return APIResponse(
                    success=True,
                    data=performance,
                    message=f"Performance metrics for {request.timeframe} retrieved"
                )
            else:
                raise HTTPException(status_code=503, detail="Portfolio tracker not available")
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
    
    except Exception as e:
        logger.error(f"Error in portfolio operations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# MARKET DATA ENDPOINTS
# =============================================================================

@app.post("/api/v1/market/data", response_model=APIResponse)
async def get_market_data(request: MarketDataRequest):
    """Obtine date de piata pentru simbolurile specificate"""
    try:
        if not data_fetcher:
            raise HTTPException(status_code=503, detail="Data fetcher not available")
        
        market_data = {}
        
        for symbol in request.symbols:
            try:
                data = await data_fetcher.get_symbol_data(
                    symbol=symbol,
                    timeframe=request.timeframe,
                    indicators=request.indicators
                )
                market_data[symbol] = data
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                market_data[symbol] = {"error": str(e)}
        
        return APIResponse(
            success=True,
            data=market_data,
            message=f"Market data retrieved for {len(request.symbols)} symbols"
        )
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/overview", response_model=APIResponse)
async def get_market_overview(
    current_agent: CryptoAIAgent = Depends(get_current_agent)
):
    """Obtine overview general al pietei crypto"""
    try:
        query = """
        Furnizeaza un overview complet al pietei crypto:
        1. Sentiment general (Fear & Greed Index)
        2. Dominanta Bitcoin si Ethereum
        3. Volumul total de trading
        4. Top gainers si losers
        5. Evenimente importante din ultimele 24h
        6. Trend general pe timeframes multiple
        
        Concentreaza-te pe informatii actionabile pentru trading.
        """
        
        overview = await current_agent.manual_analysis(query)
        
        return APIResponse(
            success=True,
            data={"overview": overview, "timestamp": datetime.now()},
            message="Market overview retrieved"
        )
    except Exception as e:
        logger.error(f"Error getting market overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# NOTIFICATIONS ENDPOINTS
# =============================================================================

@app.post("/api/v1/notifications/send", response_model=APIResponse)
async def send_notification(request: NotificationRequest):
    """Trimite notificare prin canalul specificat"""
    try:
        # Implement notification sending logic
        # This would integrate with Discord/Telegram bots
        
        return APIResponse(
            success=True,
            data={"type": request.type, "sent": True},
            message=f"Notification sent via {request.type}"
        )
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# WEBSOCKET ENDPOINTS
# =============================================================================

@app.websocket("/ws/market-updates")
async def websocket_market_updates(websocket: WebSocket):
    """WebSocket pentru updates real-time"""
    await websocket.accept()
    
    try:
        while True:
            # Send market updates every 30 seconds
            if data_fetcher:
                try:
                    # Get quick market update
                    btc_price = await data_fetcher.get_current_price("BTCUSDT")
                    eth_price = await data_fetcher.get_current_price("ETHUSDT")
                    
                    update = {
                        "type": "market_update",
                        "timestamp": datetime.now().isoformat(),
                        "data": {
                            "BTCUSDT": btc_price,
                            "ETHUSDT": eth_price
                        }
                    }
                    
                    await websocket.send_json(update)
                except Exception as e:
                    logger.error(f"Error sending WebSocket update: {e}")
            
            await asyncio.sleep(30)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def _parse_signal_response(response: str, symbol: str) -> Dict[str, Any]:
    """Parse raspunsul AI pentru a extrage datele semnalului"""
    try:
        # Simple parsing logic - in production this would be more sophisticated
        lines = response.strip().split('\n')
        
        # Look for action keywords
        action = "HOLD"
        confidence = 0.5
        entry_price = 0.0
        stop_loss = 0.0
        take_profit = 0.0
        reasoning = response
        
        response_lower = response.lower()
        
        if "buy" in response_lower or "long" in response_lower:
            action = "BUY"
            confidence = 0.7
        elif "sell" in response_lower or "short" in response_lower:
            action = "SELL"
            confidence = 0.7
        
        if "strong" in response_lower or "confident" in response_lower:
            confidence = min(confidence + 0.2, 1.0)
        
        return {
            "symbol": symbol,
            "action": action,
            "confidence": confidence,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "reasoning": reasoning,
            "timestamp": datetime.now(),
            "risk_score": 1.0 - confidence
        }
    
    except Exception as e:
        logger.error(f"Error parsing signal response: {e}")
        return {
            "symbol": symbol,
            "action": "HOLD",
            "confidence": 0.0,
            "entry_price": 0.0,
            "stop_loss": 0.0,
            "take_profit": 0.0,
            "reasoning": f"Error parsing response: {str(e)}",
            "timestamp": datetime.now(),
            "risk_score": 1.0
        }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )