#!/usr/bin/env python3
"""
Crypto MCP Assistant - Core AI Agent
Agent principal pentru analiza crypto si generare semnale de trading
"""

import asyncio
import os
import json
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

from mcp_use import MCPAgent, MCPClient
from loguru import logger

# Local imports
from .market_analyzer import MarketAnalyzer
from .risk_manager import RiskManager
from ..trading.signal_generator import SignalGenerator
from ..trading.portfolio_tracker import PortfolioTracker
from ..notifications.discord_bot import DiscordNotifier
from ..data.data_fetcher import DataFetcher

load_dotenv()

@dataclass
class TradingSignal:
    """Clasa pentru semnalele de trading"""
    symbol: str
    action: str  # BUY, SELL, HOLD
    confidence: float  # 0.0 - 1.0
    entry_price: float
    stop_loss: float
    take_profit: float
    timeframe: str
    reasoning: str
    timestamp: datetime
    risk_score: float
    position_size_usd: float

class CryptoAIAgent:
    """Agent AI principal pentru trading crypto cu integrare MCP"""
    
    def __init__(self, config_path: str = "config/trading_config.yaml"):
        self.config = self._load_config(config_path)
        self.symbols_config = self._load_symbols_config()
        
        # Initialize core components
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory(return_messages=True)
        self.mcp_client = self._initialize_mcp_client()
        
        # Initialize specialized components
        self.market_analyzer = MarketAnalyzer()
        self.risk_manager = RiskManager(self.config)
        self.signal_generator = SignalGenerator(self.config)
        self.portfolio_tracker = PortfolioTracker()
        self.data_fetcher = DataFetcher()
        
        # Initialize notifications
        self.discord_notifier = DiscordNotifier() if self.config.get('notifications', {}).get('channels', {}).get('discord', {}).get('enabled') else None
        
        # Agent state
        self.active_signals: List[TradingSignal] = []
        self.market_sentiment = "neutral"
        self.is_running = False
        
        logger.info("Crypto AI Agent initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Incarca configuratia din fisierul YAML"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def _load_symbols_config(self) -> Dict[str, Any]:
        """Incarca configuratia simbolurilor"""
        try:
            with open("config/symbols.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading symbols config: {e}")
            return {}
    
    def _initialize_llm(self) -> ChatGroq:
        """Initializeaza modelul Groq LLM"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        return ChatGroq(
            model="llama-3.1-70b-versatile",  # Model mai performant pentru trading
            api_key=api_key,
            temperature=0.3,  # Lower temperature pentru decizii mai consistente
            max_tokens=2000,
            streaming=False
        )
    
    def _initialize_mcp_client(self) -> MCPClient:
        """Initializeaza clientul MCP cu serverele crypto"""
        mcp_config_path = os.getenv("MCP_CONFIG_PATH", "config/mcp_config.json")
        
        try:
            client = MCPClient.from_config_file(mcp_config_path)
            logger.info("MCP Client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Error initializing MCP client: {e}")
            raise
    
    async def start_trading_session(self) -> None:
        """Porneste o sesiune de trading"""
        self.is_running = True
        logger.info("Starting crypto trading session...")
        
        try:
            # Initialize MCP agent
            mcp_agent = MCPAgent(
                llm=self.llm,
                client=self.mcp_client,
                max_steps=20,
                memory_enabled=True
            )
            
            # Start main trading loop
            await self._main_trading_loop(mcp_agent)
            
        except Exception as e:
            logger.error(f"Error in trading session: {e}")
            await self.stop_trading_session()
    
    async def _main_trading_loop(self, mcp_agent: MCPAgent) -> None:
        """Loop principal de trading"""
        while self.is_running:
            try:
                # 1. Analiza piata generala
                market_overview = await self._analyze_market_overview(mcp_agent)
                
                # 2. Scanare simboluri pentru oportunitati
                opportunities = await self._scan_for_opportunities(mcp_agent)
                
                # 3. Generare semnale de trading
                new_signals = await self._generate_trading_signals(mcp_agent, opportunities)
                
                # 4. Evaluare risc si management pozitii
                filtered_signals = await self._evaluate_and_filter_signals(new_signals)
                
                # 5. Executie semnale (daca auto-trading este activat)
                if self.config.get('advanced', {}).get('auto_trading', False):
                    await self._execute_signals(filtered_signals)
                
                # 6. Update portofoliu si pozitii
                await self._update_portfolio_status()
                
                # 7. Trimite notificari
                await self._send_notifications(filtered_signals, market_overview)
                
                # 8. Wait for next iteration
                await asyncio.sleep(self.config.get('analysis', {}).get('scan_interval', 300))  # 5 minutes default
                
            except Exception as e:
                logger.error(f"Error in main trading loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def _analyze_market_overview(self, mcp_agent: MCPAgent) -> Dict[str, Any]:
        """Analizeaza starea generala a pietei"""
        try:
            # Folosim MCP pentru a obtine date de piata
            query = """
            Analizeaza starea generala a pietei crypto. Vreau sa stiu:
            1. Sentiment general (fear/greed index)
            2. Volumul de trading total
            3. Dominanta Bitcoin
            4. Trend-ul general pe timeframe-uri multiple
            5. Evenimente importante din news
            
            Concentreaza-te pe BTCUSDT, ETHUSDT si EGLDUSDT ca simboluri principale.
            """
            
            response = await mcp_agent.run(query)
            
            # Parse response si extrage informatii importante
            market_data = {
                "timestamp": datetime.now(),
                "sentiment": self._extract_sentiment_from_response(response),
                "trend": self._extract_trend_from_response(response),
                "volume_status": self._extract_volume_status(response),
                "news_impact": self._extract_news_impact(response),
                "raw_analysis": response
            }
            
            self.market_sentiment = market_data["sentiment"]
            logger.info(f"Market overview updated: {market_data['sentiment']} sentiment, {market_data['trend']} trend")
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error analyzing market overview: {e}")
            return {"error": str(e), "timestamp": datetime.now()}
    
    async def _scan_for_opportunities(self, mcp_agent: MCPAgent) -> List[Dict[str, Any]]:
        """Scaneaza simbolurile pentru oportunitati de trading"""
        opportunities = []
        
        # Get symbols to scan based on priority and enabled status
        symbols_to_scan = self._get_priority_symbols()
        
        for symbol in symbols_to_scan:
            try:
                # Analiza tehnica pentru fiecare simbol
                query = f"""
                Analizeaza {symbol} pentru oportunitati de trading:
                1. Analiza tehnica pe timeframes 5m, 15m, 1h, 4h
                2. Indicatori: RSI, MACD, Bollinger Bands, EMA
                3. Support si resistance levels
                4. Pattern recognition
                5. Volume analysis
                6. Momentum si trend strength
                
                Genereaza o evaluare clara: BUY/SELL/HOLD cu confidence score.
                """
                
                response = await mcp_agent.run(query)
                
                opportunity = {
                    "symbol": symbol,
                    "analysis": response,
                    "timestamp": datetime.now(),
                    "action": self._extract_action_from_response(response),
                    "confidence": self._extract_confidence_from_response(response),
                    "price_levels": self._extract_price_levels(response)
                }
                
                opportunities.append(opportunity)
                
                # Rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error scanning {symbol}: {e}")
                continue
        
        logger.info(f"Scanned {len(opportunities)} symbols for opportunities")
        return opportunities
    
    async def _generate_trading_signals(self, mcp_agent: MCPAgent, opportunities: List[Dict]) -> List[TradingSignal]:
        """Genereaza semnale de trading pe baza oportunitatilor"""
        signals = []
        
        for opp in opportunities:
            if opp["confidence"] < 0.6:  # Skip low confidence opportunities
                continue
            
            try:
                # Folosim signal generator pentru a crea semnale structurate
                signal = await self.signal_generator.generate_signal(
                    symbol=opp["symbol"],
                    market_data=opp,
                    market_sentiment=self.market_sentiment
                )
                
                if signal:
                    signals.append(signal)
                    
            except Exception as e:
                logger.error(f"Error generating signal for {opp['symbol']}: {e}")
                continue
        
        logger.info(f"Generated {len(signals)} trading signals")
        return signals
    
    async def _evaluate_and_filter_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Evalueaza si filtreaza semnalele pe baza risk management"""
        filtered_signals = []
        
        for signal in signals:
            try:
                # Risk evaluation
                risk_assessment = await self.risk_manager.evaluate_signal_risk(signal)
                
                if risk_assessment["approved"]:
                    # Calculate position size
                    position_size = await self.risk_manager.calculate_position_size(
                        signal.symbol,
                        signal.entry_price,
                        signal.stop_loss
                    )
                    
                    signal.position_size_usd = position_size
                    signal.risk_score = risk_assessment["risk_score"]
                    filtered_signals.append(signal)
                    
                    logger.info(f"Signal approved: {signal.symbol} {signal.action} @ {signal.entry_price}")
                else:
                    logger.info(f"Signal rejected: {signal.symbol} - {risk_assessment['reason']}")
                    
            except Exception as e:
                logger.error(f"Error evaluating signal {signal.symbol}: {e}")
                continue
        
        self.active_signals.extend(filtered_signals)
        return filtered_signals
    
    async def _execute_signals(self, signals: List[TradingSignal]) -> None:
        """Executa semnalele de trading (doar daca auto-trading este activat)"""
        if not self.config.get('features', {}).get('auto_trading', False):
            logger.info("Auto-trading disabled, signals generated for manual review")
            return
        
        for signal in signals:
            try:
                logger.warning(f"AUTO-TRADING: Executing {signal.action} for {signal.symbol}")
                # Here would be the actual order execution logic
                # This is intentionally not implemented for safety
                
            except Exception as e:
                logger.error(f"Error executing signal {signal.symbol}: {e}")
    
    async def _update_portfolio_status(self) -> None:
        """Actualizeaza statusul portofoliului"""
        try:
            await self.portfolio_tracker.update_positions()
            portfolio_status = await self.portfolio_tracker.get_portfolio_summary()
            logger.info(f"Portfolio updated: {portfolio_status.get('total_value_usd', 0):.2f} USD")
            
        except Exception as e:
            logger.error(f"Error updating portfolio: {e}")
    
    async def _send_notifications(self, signals: List[TradingSignal], market_overview: Dict) -> None:
        """Trimite notificari pentru semnale si analiza"""
        if not signals and not market_overview.get("important_update"):
            return
        
        try:
            if self.discord_notifier:
                await self.discord_notifier.send_trading_update(signals, market_overview)
                
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")
    
    def _get_priority_symbols(self) -> List[str]:
        """Obtine lista de simboluri prioritare pentru scanare"""
        symbols = []
        
        # Add major pairs first
        major_pairs = self.symbols_config.get("crypto_symbols", {}).get("major_pairs", {})
        for symbol, config in major_pairs.items():
            if config.get("enabled", False):
                symbols.append(symbol)
        
        # Add enabled altcoins
        altcoins = self.symbols_config.get("crypto_symbols", {}).get("altcoins", {})
        for symbol, config in altcoins.items():
            if config.get("enabled", False):
                symbols.append(symbol)
        
        # Sort by priority
        symbols.sort(key=lambda x: self._get_symbol_priority(x))
        
        return symbols[:10]  # Limit to top 10 for performance
    
    def _get_symbol_priority(self, symbol: str) -> int:
        """Obtine prioritatea unui simbol"""
        all_symbols = {**self.symbols_config.get("crypto_symbols", {}).get("major_pairs", {}),
                      **self.symbols_config.get("crypto_symbols", {}).get("altcoins", {})}
        
        return all_symbols.get(symbol, {}).get("priority", 999)
    
    def _extract_sentiment_from_response(self, response: str) -> str:
        """Extrage sentiment din raspunsul AI"""
        response_lower = response.lower()
        if any(word in response_lower for word in ["bullish", "positive", "optimistic", "green"]):
            return "bullish"
        elif any(word in response_lower for word in ["bearish", "negative", "pessimistic", "red"]):
            return "bearish"
        else:
            return "neutral"
    
    def _extract_trend_from_response(self, response: str) -> str:
        """Extrage trend din raspunsul AI"""
        response_lower = response.lower()
        if "uptrend" in response_lower or "up trend" in response_lower:
            return "uptrend"
        elif "downtrend" in response_lower or "down trend" in response_lower:
            return "downtrend"
        else:
            return "sideways"
    
    def _extract_volume_status(self, response: str) -> str:
        """Extrage statusul volumului"""
        response_lower = response.lower()
        if "high volume" in response_lower or "increased volume" in response_lower:
            return "high"
        elif "low volume" in response_lower or "decreased volume" in response_lower:
            return "low"
        else:
            return "normal"
    
    def _extract_news_impact(self, response: str) -> str:
        """Extrage impactul news-urilor"""
        response_lower = response.lower()
        if any(word in response_lower for word in ["major news", "important", "significant"]):
            return "high"
        elif any(word in response_lower for word in ["minor", "small impact"]):
            return "low"
        else:
            return "neutral"
    
    def _extract_action_from_response(self, response: str) -> str:
        """Extrage actiunea recomandata"""
        response_lower = response.lower()
        if "buy" in response_lower or "long" in response_lower:
            return "BUY"
        elif "sell" in response_lower or "short" in response_lower:
            return "SELL"
        else:
            return "HOLD"
    
    def _extract_confidence_from_response(self, response: str) -> float:
        """Extrage confidence score din raspuns"""
        # Simple heuristic based on keywords
        response_lower = response.lower()
        if any(word in response_lower for word in ["strong", "confident", "clear"]):
            return 0.8
        elif any(word in response_lower for word in ["weak", "uncertain", "mixed"]):
            return 0.4
        else:
            return 0.6
    
    def _extract_price_levels(self, response: str) -> Dict[str, float]:
        """Extrage nivelurile de pret din raspuns"""
        # This would need more sophisticated parsing
        # For now, return empty dict
        return {"support": 0, "resistance": 0}
    
    async def stop_trading_session(self) -> None:
        """Opreste sesiunea de trading"""
        self.is_running = False
        
        try:
            if self.mcp_client and hasattr(self.mcp_client, 'sessions'):
                await self.mcp_client.close_all_sessions()
                logger.info("MCP sessions closed")
        except Exception as e:
            logger.error(f"Error closing MCP sessions: {e}")
        
        logger.info("Trading session stopped")
    
    async def get_portfolio_summary(self) -> Dict[str, Any]:
        """Obtine sumar portofoliu"""
        return await self.portfolio_tracker.get_portfolio_summary()
    
    async def get_active_signals(self) -> List[TradingSignal]:
        """Obtine semnalele active"""
        return self.active_signals
    
    async def manual_analysis(self, query: str) -> str:
        """Analiza manuala cu MCP agent"""
        try:
            mcp_agent = MCPAgent(
                llm=self.llm,
                client=self.mcp_client,
                max_steps=15,
                memory_enabled=True
            )
            
            response = await mcp_agent.run(query)
            return response
            
        except Exception as e:
            logger.error(f"Error in manual analysis: {e}")
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test run
    async def main():
        agent = CryptoAIAgent()
        
        # Test manual analysis
        result = await agent.manual_analysis("Care este pretul curent al Bitcoin si ce recomanzi?")
        print(result)
        
        await agent.stop_trading_session()
    
    asyncio.run(main())