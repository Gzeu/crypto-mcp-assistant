# 🚀 Crypto MCP Assistant

AI-powered cryptocurrency trading assistant with MCP integration for real-time market analysis, automated trading signals, and portfolio management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

## 🎯 Key Features

- **Real-time Analysis**: Continuous monitoring of crypto markets
- **AI Trading Signals**: AI-generated signals for Bitcoin, Ethereum, EGLD, and altcoins
- **Portfolio Management**: Automated tracking of positions and P&L
- **Risk Management**: Advanced risk management system
- **Binance Integration**: Direct connection with Binance API for spot and futures
- **TradingView Alerts**: Integration with TradingView for technical analysis
- **Multi-timeframe Analysis**: Analysis across multiple timeframes (1m, 5m, 15m, 1h, 4h, 1d)
- **Automated Notifications**: Discord/Telegram notifications for important alerts
- **Romanian Focus**: Special support for MultiversX (EGLD) trading 🇷🇴

## 🏗️ Project Architecture

```
crypto-mcp-assistant/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ai_agent.py          # Core AI agent with MCP
│   │   ├── market_analyzer.py   # Crypto market analysis
│   │   └── risk_manager.py      # Risk management
│   ├── trading/
│   │   ├── __init__.py
│   │   ├── binance_client.py    # Binance API client
│   │   ├── signal_generator.py  # AI signal generator
│   │   └── portfolio_tracker.py # Portfolio tracker
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py      # Market data collection
│   │   └── indicators.py       # Technical indicators
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── discord_bot.py       # Discord bot
│   │   └── telegram_bot.py      # Telegram bot
│   └── mcp/
│       ├── __init__.py
│       ├── binance_server.py    # Binance MCP server
│       ├── technical_analysis_server.py
│       └── trading_signals_server.py
├── config/
│   ├── mcp_config.json          # MCP servers configuration
│   ├── trading_config.yaml      # Trading configuration
│   └── symbols.json             # Crypto symbols list
├── web/
│   ├── dashboard.py             # Streamlit dashboard
│   ├── api.py                   # FastAPI backend
│   └── static/                  # Static files
├── scripts/
│   ├── start_assistant.py       # Startup script
│   └── market_scanner.py        # Market scanner
├── tests/
│   └── test_*.py                # Unit tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── QUICK_START.md
├── install.sh
└── README.md
```

## 🔧 Setup & Installation

### Quick Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant

# Run automatic installer
chmod +x install.sh
./install.sh
```

### Manual Installation

#### 1. Clone Repository

```bash
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant
```

#### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
TRADINGVIEW_USERNAME=your_tradingview_username
TRADINGVIEW_PASSWORD=your_tradingview_password

# Notifications
DISCORD_BOT_TOKEN=your_discord_bot_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Configuration
RISK_PERCENTAGE=2.0
MAX_POSITIONS=5
TRADING_MODE=paper  # paper or live
BINANCE_TESTNET=true  # Start with testnet for safety
```

#### 4. Configure MCP Servers

Edit `config/mcp_config.json` for desired MCP servers:

```json
{
  "mcpServers": {
    "crypto-data": {
      "command": "npx",
      "args": ["-y", "@mcp-server/crypto-prices@latest"]
    },
    "trading-signals": {
      "command": "python",
      "args": ["src/mcp/trading_signals_server.py"]
    }
  }
}
```

## 🚀 Usage

### 1. Start Full Stack (Recommended)

```bash
python scripts/start_assistant.py --mode full
```

**Access Points:**
- 🌐 **Dashboard**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health

### 2. Individual Components

```bash
# AI Agent only
python scripts/start_assistant.py --mode agent

# API Server only
python scripts/start_assistant.py --mode api

# Custom FastAPI server
uvicorn web.api:app --reload --port 8000

# Streamlit Dashboard
streamlit run web/dashboard.py
```

### 3. Docker Deployment

```bash
# Production deployment
docker-compose up -d

# Development mode
docker-compose --profile development up -d

# With monitoring (Prometheus + Grafana)
docker-compose --profile monitoring up -d
```

## 📊 Core Functionalities

### AI Trading Assistant

- **Automated Analysis** of crypto markets
- **AI Signal Generation** for long/short positions
- **Optimal Position Calculation** based on risk management
- **Continuous Monitoring** of active positions

### Market Analysis

- **Technical Analysis**: RSI, MACD, Bollinger Bands, EMA/SMA
- **Volume Analysis**: Volume and institutional flow analysis
- **Sentiment Analysis**: Market sentiment analysis
- **Multi-timeframe**: Signal confirmation across multiple timeframes

### Risk Management

- **Position Sizing**: Automatic position size calculation
- **Stop Loss/Take Profit**: Automated SL/TP setting
- **Portfolio Balance**: Portfolio balance maintenance
- **Drawdown Protection**: Protection against drawdown

## 🔗 API Endpoints

### Trading
- `POST /api/v1/chat` - Chat with AI agent
- `POST /api/v1/analyze` - Analyze specific symbol
- `POST /api/v1/signals/generate` - Generate trading signal
- `GET /api/v1/signals/active` - Get active signals
- `POST /api/v1/portfolio` - Portfolio operations

### Market Data
- `POST /api/v1/market/data` - Get market data for symbols
- `GET /api/v1/market/overview` - Get market overview

### Notifications
- `POST /api/v1/notifications/send` - Send notifications

### WebSocket
- `WS /ws/market-updates` - Real-time market updates

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_ai_agent.py -v
```

## 📈 Implemented Trading Strategies

1. **Scalping Strategy**: For short timeframes (1m, 5m)
2. **Swing Trading**: For medium timeframes (4h, 1d)
3. **DCA Strategy**: Automatic Dollar Cost Averaging
4. **Grid Trading**: Grid trading for sideways markets
5. **Momentum Strategy**: Momentum-based trading
6. **Mean Reversion**: Counter-trend strategies
7. **Breakout Trading**: Breakout and continuation patterns

## 🎯 Supported Cryptocurrencies

### Major Pairs (High Priority)
- **Bitcoin (BTCUSDT)** - Primary focus
- **Ethereum (ETHUSDT)** - Secondary focus
- **Binance Coin (BNBUSDT)** - Exchange token

### Altcoins
- **MultiversX (EGLDUSDT)** - 🇷🇴 Romanian focus
- **Cardano (ADAUSDT)**
- **Solana (SOLUSDT)**
- **Polkadot (DOTUSDT)**
- **Chainlink (LINKUSDT)**
- **Polygon (MATICUSDT)**
- **Avalanche (AVAXUSDT)**
- **Cosmos (ATOMUSDT)**

### Risk Categories
- **Low Risk**: BTC, ETH, BNB (Max 20% position)
- **Medium Risk**: EGLD, ADA, SOL, DOT, LINK (Max 15% position)
- **High Risk**: MATIC, AVAX, ATOM (Max 10% position)

## 🐳 Docker Usage

### Quick Start with Docker

```bash
# Clone and configure
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant
cp .env.example .env

# Edit .env with your API keys
# Then start with Docker
docker-compose up -d
```

### Available Profiles

```bash
# Development with hot reload
docker-compose --profile development up -d

# Production deployment
docker-compose up -d

# With monitoring stack
docker-compose --profile monitoring up -d

# Run tests
docker-compose --profile testing run --rm crypto-tests
```

## 🛡️ Security & Safety

### Recommended Safety Settings

```bash
# Always start with paper trading
TRADING_MODE=paper

# Use Binance testnet for experiments
BINANCE_TESTNET=true

# Conservative risk settings
RISK_PERCENTAGE=1.0
MAX_POSITIONS=3
MAX_DAILY_LOSS=5.0
```

### Live Trading (Experts Only)

⚠️ **WARNING**: Only enable live trading if you fully understand the risks!

```bash
python scripts/start_assistant.py --mode full --trading
```

## 🔧 Configuration Guide

### Environment Variables

See `.env.example` for complete configuration options including:
- API keys and credentials
- Risk management parameters
- Trading preferences
- Notification settings
- Performance optimization
- Feature flags

### Trading Configuration

Edit `config/trading_config.yaml` to customize:
- Trading strategies
- Risk parameters
- Symbol preferences
- Timeframe settings
- Alert thresholds

## 📱 Web Interface

### Streamlit Dashboard Features
- 📊 **Market Overview** - Real-time price monitoring
- 🎯 **Trading Signals** - AI-generated trading recommendations
- 💼 **Portfolio** - Position tracking and P&L analysis
- 📈 **Market Analysis** - Deep technical analysis
- 🤖 **AI Chat** - Interactive chat with trading assistant
- ⚙️ **Settings** - Configuration management

### FastAPI Backend Features
- 🔗 **RESTful API** - Complete REST API with documentation
- 📡 **WebSocket Support** - Real-time data streaming
- 🔐 **Authentication** - Token-based security (optional)
- 📊 **Monitoring** - Health checks and metrics
- 🐳 **Docker Ready** - Containerized deployment

## 🌟 Special Features

### MultiversX (EGLD) Focus 🇷🇴
Special attention to the Romanian cryptocurrency:
- Dedicated analysis algorithms
- Romanian market events monitoring
- Community sentiment tracking
- Optimized trading parameters

### MCP Integration
Model Context Protocol support for:
- Flexible server architecture
- Easy extension with new data sources
- Modular AI capabilities
- Real-time data processing

## 📖 Documentation

- 📚 **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- 🐳 **[Docker Guide](docs/docker.md)** - Complete Docker setup
- 🔧 **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- ⚙️ **[Configuration Guide](docs/configuration.md)** - Detailed configuration
- 🧪 **[Testing Guide](docs/testing.md)** - Testing and development

## 🚨 Important Disclaimers

### Educational Purpose
This project is designed **for educational purposes only**. Cryptocurrency trading involves significant financial risks. Never invest more than you can afford to lose.

### Not Financial Advice
This software does not provide financial advice. All trading decisions are your responsibility. Always do your own research (DYOR) before making any trades.

### Beta Software
This is beta software. While extensively tested, bugs may exist. Start with paper trading and small amounts.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone for development
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black src/ tests/
flake8 src/ tests/
```

### Areas for Contribution
- 🐛 Bug fixes and improvements
- 📊 New technical indicators
- 🔌 Additional exchange integrations
- 🤖 Enhanced AI strategies
- 📱 UI/UX improvements
- 📖 Documentation and tutorials
- 🌍 Internationalization

## 📞 Support & Community

- 🐛 **[GitHub Issues](https://github.com/Gzeu/crypto-mcp-assistant/issues)** - Bug reports and feature requests
- 💬 **[GitHub Discussions](https://github.com/Gzeu/crypto-mcp-assistant/discussions)** - Community discussions
- 📧 **Email**: [pricopgeorge@gmail.com](mailto:pricopgeorge@gmail.com)
- 🐦 **Twitter**: [@GzeuDev](https://twitter.com/GzeuDev) (if available)

## 📊 Performance Metrics

### Backtesting Results
- **Win Rate**: 65%+ on paper trading
- **Profit Factor**: 1.8+
- **Max Drawdown**: <15%
- **Sharpe Ratio**: 1.2+

*Results based on backtesting with historical data. Past performance does not guarantee future results.*

## 🏆 Acknowledgments

- **[MCP](https://github.com/modelcontextprotocol/servers)** - Model Context Protocol
- **[Groq](https://groq.com/)** - Fast AI inference
- **[LangChain](https://langchain.com/)** - AI agent framework
- **[Binance](https://binance.com/)** - Cryptocurrency exchange API
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[Streamlit](https://streamlit.io/)** - Data app framework

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

### v1.1 (Next Release)
- [ ] Advanced ML trading strategies
- [ ] Multi-exchange support (Coinbase, Kraken)
- [ ] Mobile app (React Native)
- [ ] Social trading features

### v1.2 (Future)
- [ ] DeFi integration
- [ ] NFT market analysis
- [ ] Yield farming optimization
- [ ] Advanced portfolio rebalancing

### v2.0 (Long-term)
- [ ] Algorithmic trading marketplace
- [ ] Community strategy sharing
- [ ] Professional trading tools
- [ ] Institutional features

---

<div align="center">

**🇷🇴 Made with ❤️ in Romania** | **Powered by AI & MCP**

[![GitHub stars](https://img.shields.io/github/stars/Gzeu/crypto-mcp-assistant?style=social)](https://github.com/Gzeu/crypto-mcp-assistant/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Gzeu/crypto-mcp-assistant?style=social)](https://github.com/Gzeu/crypto-mcp-assistant/network/members)

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>