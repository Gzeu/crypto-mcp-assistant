#!/usr/bin/env python3
"""
Crypto MCP Assistant
AI-powered cryptocurrency trading assistant with MCP integration

Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Gzeu"
__email__ = "pricopgeorge@gmail.com"
__description__ = "AI-powered cryptocurrency trading assistant with MCP integration"
__url__ = "https://github.com/Gzeu/crypto-mcp-assistant"

# Package metadata
__all__ = [
    "CryptoAIAgent",
    "MarketAnalyzer", 
    "RiskManager",
    "SignalGenerator",
    "PortfolioTracker",
    "BinanceClient",
    "DataFetcher",
    "__version__"
]

# Import main classes for easy access
try:
    from .core.ai_agent import CryptoAIAgent
    from .core.market_analyzer import MarketAnalyzer
    from .core.risk_manager import RiskManager
    from .trading.signal_generator import SignalGenerator
    from .trading.portfolio_tracker import PortfolioTracker
    from .trading.binance_client import BinanceClient
    from .data.data_fetcher import DataFetcher
except ImportError:
    # Handle import errors gracefully during development
    pass

# Package configuration
CONFIG = {
    "default_config_path": "config/trading_config.yaml",
    "mcp_config_path": "config/mcp_config.json",
    "symbols_config_path": "config/symbols.json",
    "log_file": "logs/crypto_assistant.log",
    "data_directory": "data/",
    "backup_directory": "backups/"
}

# Version info
version_info = tuple(map(int, __version__.split('.')))

def get_version():
    """Return the version string"""
    return __version__

def get_package_info():
    """Return package information"""
    return {
        "name": "crypto-mcp-assistant",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "description": __description__,
        "url": __url__,
        "config": CONFIG
    }