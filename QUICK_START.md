# 🚀 Quick Start Guide - Crypto MCP Assistant

Ghid rapid pentru a porni **Crypto MCP Assistant** în mai puțin de 5 minute!

## 📋 Prerequisite

- Python 3.9+ 
- Node.js 18+ (pentru MCP servers)
- Git
- 8GB RAM recomandat
- Cont Binance (pentru trading real)

## ⚡ Instalare Rapidă

### 1. Clonare și Setup

```bash
# Clonează repository-ul
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant

# Creează environment virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# sau
venv\Scripts\activate     # Windows

# Instalează dependențele
pip install -r requirements.txt
```

### 2. Configurare Environment

```bash
# Copiază template-ul de configurare
cp .env.example .env

# Editează .env cu API keys-urile tale
nano .env  # sau alt editor
```

**Variabile esențiale în .env:**
```bash
GROQ_API_KEY=your_groq_api_key_here
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
BINANCE_TESTNET=true  # IMPORTANT: testnet pentru început
TRADING_MODE=paper   # paper trading pentru început
```

### 3. Pornire Rapidă

```bash
# Pornește tot stack-ul (API + Dashboard + AI Agent)
python scripts/start_assistant.py --mode full
```

**Access Points:**
- 🌐 **Dashboard**: http://localhost:8501
- 📚 **API Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health

## 🐳 Instalare cu Docker (Recomandat)

### Quick Docker Setup

```bash
# Clonează și configurează
git clone https://github.com/Gzeu/crypto-mcp-assistant.git
cd crypto-mcp-assistant
cp .env.example .env

# Editează .env cu API keys
# Apoi pornește cu Docker
docker-compose up -d
```

### Development cu Docker

```bash
# Pentru development cu hot reload
docker-compose --profile development up -d
```

## 🎯 Moduri de Rulare

### 1. Full Stack Mode (Recomandat)
```bash
python scripts/start_assistant.py --mode full
```
**Include:** API + Dashboard + AI Agent

### 2. Agent Only Mode
```bash
python scripts/start_assistant.py --mode agent
```
**Include:** Doar AI Agent pentru chat interactiv

### 3. API Only Mode
```bash
python scripts/start_assistant.py --mode api
```
**Include:** Doar API pentru integrări externe

## 🔧 Configurare Rapidă API Keys

### Groq API Key (OBLIGATORIU)
1. Mergi la [Groq Console](https://console.groq.com/)
2. Creează un cont gratuit
3. Generează API key
4. Adaugă în `.env` ca `GROQ_API_KEY=...`

### Binance API Keys (Pentru trading)
1. Logează-te în [Binance](https://binance.com)
2. Mergi la **API Management**
3. Creează API key nou
4. **ACTIVEAZĂ doar "Read Info" și "Spot & Margin Trading"**
5. **NU activa "Futures" până nu ești expert!**
6. Adaugă în `.env`

⚠️ **IMPORTANT:** Începe cu `BINANCE_TESTNET=true` pentru siguranță!

## 🎮 Primul Test

### 1. Verifică că totul funcționează
```bash
# Test health check
curl http://localhost:8000/health

# Sau deschide în browser
open http://localhost:8501
```

### 2. Prima analiză crypto
```bash
# Test API direct
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Cum arată Bitcoin astăzi?"}'
```

### 3. Dashboard Web
1. Deschide http://localhost:8501
2. Mergi la **AI Chat**
3. Întreabă: "Analizează BTCUSDT și EGLDUSDT"
4. Explorează **Trading Signals** și **Market Analysis**

## 📊 Features Principale

✅ **AI-Powered Analysis** - Analiză crypto cu Groq AI  
✅ **Real-time Market Data** - Date live de pe Binance  
✅ **Trading Signals** - Semnale automate de trading  
✅ **Risk Management** - Management avansat al riscului  
✅ **Web Dashboard** - Interfață Streamlit intuitivă  
✅ **API REST** - FastAPI pentru integrări  
✅ **MCP Integration** - Model Context Protocol support  
✅ **Multi-timeframe** - Analiză pe multiple timeframes  
✅ **Romanian Focus** - Suport special pentru EGLD  

## 🛡️ Siguranță

### Paper Trading (Recomandat pentru început)
```bash
TRADING_MODE=paper  # În .env
```

### Testnet Binance
```bash
BINANCE_TESTNET=true  # În .env
```

### Live Trading (DOAR pentru experți!)
```bash
# ATENȚIE: Folosește bani reali!
python scripts/start_assistant.py --mode full --trading
```

## 🆘 Troubleshooting

### Eroare: "GROQ_API_KEY not found"
**Soluție:** Verifică că ai setat corect variabila în `.env`

### Eroare: "MCP servers failed to start"
**Soluție:** 
```bash
# Instalează MCP servers
npm install -g @mcp-server/crypto-prices
npm install -g @mcp-server/google-search
```

### Port-ul 8000/8501 este ocupat
**Soluție:** Schimbă porturile în `.env`:
```bash
API_PORT=8001
STREAMLIT_PORT=8502
```

### Docker permission errors
**Soluție:** 
```bash
sudo usermod -aG docker $USER
# Logout și login din nou
```

## 📱 Test pe EGLD (Românesc)

Proiectul are focus special pe **MultiversX (EGLD)**:

```bash
# Test analiză EGLD
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "EGLDUSDT", "timeframe": "1h"}'
```

## 🚀 Next Steps

1. **Explorează Dashboard-ul** - Testează toate funcționalitățile
2. **Configurează Notificări** - Discord/Telegram bots
3. **Customizează Strategiile** - Editează `config/trading_config.yaml`
4. **Monitorizează Performance** - Setup Grafana (optional)
5. **Scale Production** - Deploy pe cloud cu Docker

## 🆕 Updates

Pentru update-uri:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
docker-compose pull  # pentru Docker
```

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Gzeu/crypto-mcp-assistant/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Gzeu/crypto-mcp-assistant/discussions)
- 📧 **Email**: pricopgeorge@gmail.com

---

**⚠️ Disclaimer**: Acest proiect este pentru scopuri educaționale. Trading-ul crypto implică riscuri. Nu investiți mai mult decât vă puteți permite să pierdeți!

**🇷🇴 Made with ❤️ in Romania** | **Powered by AI & MCP**