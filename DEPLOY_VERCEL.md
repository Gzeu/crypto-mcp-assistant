# 🚀 Crypto MCP Assistant - Deployment pe Vercel

## 📋 Ghid de Deployment

Acest ghid te ajută să deployezi **Crypto MCP Assistant** pe Vercel pentru a avea o aplicație web live și accesibilă.

## 🛠️ Pregătire pentru Deployment

### 1. Verificare Fișiere

Asigură-te că ai următoarele fișiere în repository:

- ✅ `vercel.json` - Configurația Vercel
- ✅ `requirements-vercel.txt` - Dependencies optimizate
- ✅ `web/app.py` - Streamlit app optimizată
- ✅ `web/api_vercel.py` - FastAPI backend simplificat

### 2. Structura Optimizată

```
crypto-mcp-assistant/
├── web/
│   ├── app.py              # Streamlit app (main UI)
│   └── api_vercel.py       # FastAPI backend (API endpoints)
├── vercel.json             # Vercel configuration
├── requirements-vercel.txt # Optimized dependencies
└── DEPLOY_VERCEL.md       # Acest ghid
```

## 🌐 Deployment Steps

### Opțiunea 1: Deploy prin Vercel CLI (Recomandat)

1. **Instalează Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login la Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy din directorul proiectului:**
   ```bash
   cd crypto-mcp-assistant
   vercel --prod
   ```

4. **Urmează instrucțiunile:**
   - Set up project? **Y**
   - Project name: `crypto-mcp-assistant`
   - Directory: `./` (current directory)
   - Override settings? **Y** (dacă întreabă)

### Opțiunea 2: Deploy prin Vercel Dashboard

1. **Accesează [vercel.com](https://vercel.com) și loghează-te**

2. **Click pe "New Project"**

3. **Conectează GitHub repository-ul:**
   - Selectează `Gzeu/crypto-mcp-assistant`
   - Click "Import"

4. **Configurează Project:**
   - **Project Name:** `crypto-mcp-assistant`
   - **Framework Preset:** `Other`
   - **Root Directory:** `./`
   - **Build Command:** `pip install -r requirements-vercel.txt`
   - **Output Directory:** `./`

5. **Environment Variables (Opțional):**
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ENVIRONMENT=production
   ```

6. **Click "Deploy"**

## 🔧 Configurare Environment Variables

Pentru funcționalitate completă, adaugă următoarele environment variables în Vercel Dashboard:

### Variables Esențiale:
```bash
# API Keys (optional pentru demo)
GROQ_API_KEY=your_groq_api_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret

# App Configuration
ENVIRONMENT=production
TRADING_MODE=paper
RISK_PERCENTAGE=2.0
```

### Cum să adaugi Environment Variables:

1. **În Vercel Dashboard:**
   - Mergi la proiectul tău
   - Click pe "Settings"
   - Scroll la "Environment Variables"
   - Adaugă variabilele necesare

2. **Prin CLI:**
   ```bash
   vercel env add GROQ_API_KEY
   # Introduce valoarea când ești întrebat
   ```

## 📊 Funcționalitățile Disponibile

### 🎯 Demo Mode (Fără API Keys)
Aplicația funcționează perfect în demo mode cu:
- **Mock data** pentru prețuri crypto
- **AI responses** pre-programate
- **Technical analysis** simulată
- **Trading signals** demo
- **Portfolio tracking** simulat

### 🔑 Production Mode (Cu API Keys)
Cu API keys configurate, obții:
- **Real-time crypto data**
- **AI-powered analysis** prin Groq
- **Live trading signals**
- **Binance integration**
- **Advanced features**

## 🌟 Features Principale

### 📱 Web Interface
- **Streamlit Dashboard** - UI principal interactiv
- **Market Overview** - Monitorizare piețe crypto
- **Trading Signals** - Semnale AI generate
- **Portfolio Management** - Tracking poziții
- **Technical Analysis** - Analiză tehnică avansată
- **AI Chat** - Chat cu asistentul AI

### 🔌 API Endpoints
- `GET /` - Homepage și informații API
- `GET /health` - Health check
- `POST /api/v1/chat` - Chat cu AI agent
- `POST /api/v1/analyze` - Analiză simbol specific
- `GET /api/v1/price/{symbol}` - Preț curent
- `GET /api/v1/market/overview` - Overview piață
- `GET /api/v1/signals/generate/{symbol}` - Generare semnal

## 🎨 Customizare UI

### Modificare Tema:
Editeaza `web/app.py` pentru a personaliza:
- **Culori** - Gradients și scheme de culori
- **Layout** - Organizarea elementelor
- **Metrics** - Indicatori și statistici
- **Charts** - Grafice și vizualizări

### Adăugare Simboluri:
```python
# În web/app.py, linia cu symbols
symbols = st.multiselect(
    "Select symbols to monitor",
    ["BTCUSDT", "ETHUSDT", "EGLDUSDT", "ADAUSDT", "SOLUSDT"],  # Adaugă aici
    default=["BTCUSDT", "ETHUSDT", "EGLDUSDT"]
)
```

## 🔍 Monitoring și Debug

### 1. Vercel Logs
```bash
# Vezi logs în timp real
vercel logs --follow

# Logs pentru deployment specific
vercel logs [deployment-url]
```

### 2. Health Check
Accesează: `https://your-app.vercel.app/health`

### 3. API Testing
```bash
# Test API endpoint
curl https://your-app.vercel.app/api/v1/market/overview

# Test chat endpoint
curl -X POST https://your-app.vercel.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Analizează Bitcoin"}'
```

## 🚨 Troubleshooting

### Probleme Comune:

#### 1. **Deployment Failed**
- ✅ Verifică că `requirements-vercel.txt` există
- ✅ Verifică că `vercel.json` este valid JSON
- ✅ Asigură-te că fișierele sunt în paths correct

#### 2. **Module Import Errors**
- ✅ Adaugă dependencies lipsă în `requirements-vercel.txt`
- ✅ Verifică că PYTHONPATH este setat correct în `vercel.json`

#### 3. **Function Timeout**
- ✅ Optimizează codul pentru execuție mai rapidă
- ✅ Folosește cache pentru data expensive
- ✅ Reduce dependencies heavyweight

#### 4. **Memory Limit Exceeded**
- ✅ Optimizează imports (folosește lazy imports)
- ✅ Reduce data payload size
- ✅ Implementează data streaming

### Debugging Steps:

1. **Check Build Logs:**
   ```bash
   vercel logs --since 1h
   ```

2. **Test Local:**
   ```bash
   pip install -r requirements-vercel.txt
   streamlit run web/app.py
   uvicorn web.api_vercel:app --reload
   ```

3. **Environment Check:**
   ```bash
   vercel env ls
   ```

## 📈 Performance Optimization

### 1. **Caching Strategy**
- Implementează in-memory caching pentru API calls
- Folosește session state în Streamlit
- Cache market data pentru perioade scurte

### 2. **Code Optimization**
- Lazy imports pentru libraries mari
- Async/await pentru API calls
- Minimize data processing în frontend

### 3. **Resource Management**
- Optimizează image sizes
- Comprimate JSON responses
- Minimize HTTP requests

## 🔒 Security Best Practices

### 1. **API Keys Protection**
- Nu include API keys în cod
- Folosește Vercel Environment Variables
- Rotate keys periodic

### 2. **Input Validation**
- Validează toate inputs din forms
- Sanitizează user messages
- Implementează rate limiting

### 3. **CORS Configuration**
- Configurează CORS pentru production
- Limitează allowed origins
- Validează request headers

## 🎯 Next Steps După Deployment

### 1. **Testing Complet**
- ✅ Test toate feature-urile
- ✅ Verifică responsive design
- ✅ Test API endpoints
- ✅ Verifică error handling

### 2. **Domain Custom (Opțional)**
```bash
# Adaugă domain custom
vercel domains add crypto-mcp.yourdomain.com
```

### 3. **Analytics Setup**
- Adaugă Vercel Analytics
- Implementează usage tracking
- Monitor performance metrics

### 4. **CI/CD Pipeline**
- Configurează auto-deploy pe git push
- Setup staging environment
- Implementează testing pipeline

## 📞 Support & Resources

### 📚 Documentation
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/vercel/)

### 🆘 Get Help
- **GitHub Issues**: [Create Issue](https://github.com/Gzeu/crypto-mcp-assistant/issues)
- **Vercel Support**: [Vercel Help](https://vercel.com/help)
- **Community**: Discord/Telegram channels

---

## ✅ Deployment Checklist

- [ ] Repository pregătit cu toate fișierele
- [ ] `vercel.json` configurat corect
- [ ] `requirements-vercel.txt` optimizat
- [ ] Environment variables setate (dacă sunt necesare)
- [ ] Deploy făcut prin CLI sau Dashboard
- [ ] Health check funcționează: `/health`
- [ ] UI Streamlit accessible
- [ ] API endpoints funcționează
- [ ] Error handling testat
- [ ] Mobile responsive verificat
- [ ] Performance optimizat

---

**🇷🇴 Made with ❤️ in Romania** | **🚀 Deployed on Vercel** | **⚡ Powered by AI & MCP**

*Dacă acest ghid te-a ajutat, te rog să dai o ⭐ pe GitHub!*