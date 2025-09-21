# 🚀 Crypto MCP Assistant

AI-powered cryptocurrency trading assistant cu MCP integration pentru analiză real-time, semnale de trading automate și management de portofoliu.

## 🎯 Caracteristici

- **Analiză Real-time**: Monitorizare continuă a piețelor crypto
- **AI Trading Signals**: Semnale generate cu AI pentru Bitcoin, Ethereum, EGLD și altcoins
- **Portfolio Management**: Tracking automat al pozițiilor și P&L
- **Risk Management**: Sistem avansat de management al riscului
- **Binance Integration**: Conectare directă cu API-ul Binance pentru spot și futures
- **TradingView Alerts**: Integrare cu TradingView pentru analiză tehnică
- **Multi-timeframe Analysis**: Analiză pe multiple timeframes (1m, 5m, 15m, 1h, 4h, 1d)
- **Automated Notifications**: Notificări Discord/Telegram pentru alertele importante

## 🏗️ Arhitectura Proiectului

```
crypto-mcp-assistant/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ai_agent.py          # Core AI agent cu MCP
│   │   ├── market_analyzer.py   # Analiză piețe crypto
│   │   └── risk_manager.py      # Management risc
│   ├── trading/
│   │   ├── __init__.py
│   │   ├── binance_client.py    # Client Binance API
│   │   ├── signal_generator.py  # Generator semnale AI
│   │   └── portfolio_tracker.py # Tracker portofoliu
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py      # Colectare date market
│   │   └── indicators.py       # Indicatori tehnici
│   └── notifications/
│       ├── __init__.py
│       ├── discord_bot.py       # Bot Discord
│       └── telegram_bot.py      # Bot Telegram
├── config/
│   ├── mcp_config.json          # Configurare MCP servers
│   ├── trading_config.yaml      # Configurare trading
│   └── symbols.json             # Lista simboluri crypto
├── web/
│   ├── dashboard.py             # Dashboard Streamlit
│   ├── api.py                   # FastAPI backend
│   └── static/                  # Fișiere statice
├── scripts/
│   ├── start_assistant.py       # Script pornire
│   └── market_scanner.py        # Scanner piețe
├── tests/
│   └── test_*.py                # Unit tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Setup și Instalare

### 1. Clonare Repository

```bash
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant
```

### 2. Instalare Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Configurare Environment Variables

Copiază `.env.example` la `.env` și completează:

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
TRADINGVIEW_USERNAME=your_tradingview_username
TRADINGVIEW_PASSWORD=your_tradingview_password

# Notifications
DISCORD_TOKEN=your_discord_bot_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Configuration
RISK_PERCENTAGE=2.0
MAX_POSITIONS=5
TRADING_MODE=paper  # paper sau live
```

### 4. Configurare MCP Servers

Editează `config/mcp_config.json` pentru serverele MCP dorite:

```json
{
  "mcpServers": {
    "crypto-data": {
      "command": "npx",
      "args": ["-y", "@mcp-server/crypto-data@latest"]
    },
    "trading-signals": {
      "command": "python",
      "args": ["src/mcp/trading_signals_server.py"]
    }
  }
}
```

## 🚀 Utilizare

### 1. Start AI Assistant

```bash
python scripts/start_assistant.py
```

### 2. Launch Dashboard

```bash
streamlit run web/dashboard.py
```

### 3. Start API Server

```bash
uvicorn web.api:app --reload --port 8000
```

### 4. Docker Deployment

```bash
docker-compose up -d
```

## 📊 Funcționalități Principale

### AI Trading Assistant

- **Analiză automată** a piețelor crypto
- **Generare semnale** cu AI pentru long/short
- **Calculare poziții** optimale bazate pe risc
- **Monitorizare continuă** a pozițiilor active

### Market Analysis

- **Technical Analysis**: RSI, MACD, Bollinger Bands, EMA/SMA
- **Volume Analysis**: Analiza volumului și flow-ului instituțional
- **Sentiment Analysis**: Analiza sentimentului pieței
- **Multi-timeframe**: Confirmare semnale pe multiple timeframes

### Risk Management

- **Position Sizing**: Calculare automată mărimii pozițiilor
- **Stop Loss/Take Profit**: Setare automată SL/TP
- **Portfolio Balance**: Menținere balanță portofoliu
- **Drawdown Protection**: Protecție împotriva drawdown-ului

## 🔗 API Endpoints

### Trading
- `POST /api/v1/signal` - Generează semnal trading
- `GET /api/v1/positions` - Lista pozițiilor active
- `GET /api/v1/portfolio` - Status portofoliu

### Market Data
- `GET /api/v1/price/{symbol}` - Prețul curent pentru simbol
- `GET /api/v1/analysis/{symbol}` - Analiză tehnică pentru simbol
- `GET /api/v1/signals/{symbol}` - Istoricul semnalelor

### Notifications
- `POST /api/v1/notify/discord` - Trimite notificare Discord
- `POST /api/v1/notify/telegram` - Trimite notificare Telegram

## 🧪 Testing

```bash
pytest tests/ -v
```

## 📈 Strategii Implementate

1. **Scalping Strategy**: Pentru timeframes scurte (1m, 5m)
2. **Swing Trading**: Pentru timeframes medii (4h, 1d)
3. **DCA Strategy**: Dollar Cost Averaging automat
4. **Grid Trading**: Trading în grilă pentru piețe sideways
5. **Momentum Strategy**: Trading bazat pe momentum

## ⚠️ Disclaimer

Acest proiect este destinat **doar pentru scopuri educaționale**. Trading-ul crypto implică riscuri mari de pierdere financiară. Nu utilizați acest sistem cu bani reali fără o înțelegere completă a riscurilor implicate.

## 📝 License

MIT License - vezi [LICENSE](LICENSE) pentru detalii.

## 🤝 Contribuții

Contribuțiile sunt binevenite! Te rog să citești [CONTRIBUTING.md](CONTRIBUTING.md) pentru ghid.

## 📞 Support

- **GitHub Issues**: Pentru bug reports și feature requests
- **Discord**: [Link către server Discord]
- **Telegram**: [@crypto_assistant_bot]

---

**Made with ❤️ by Gzeu** | **Powered by AI & MCP**