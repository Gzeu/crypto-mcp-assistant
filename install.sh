#!/bin/bash

# =============================================================================
# CRYPTO MCP ASSISTANT - AUTOMATIC INSTALLATION SCRIPT
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
PROJECT_NAME="crypto-mcp-assistant"
GITHUB_REPO="https://github.com/Gzeu/crypto-mcp-assistant.git"
PYTHON_MIN_VERSION="3.9"
NODE_MIN_VERSION="16"

echo -e "${BLUE}"
echo "==============================================="
echo "    🚀 CRYPTO MCP ASSISTANT INSTALLER"
echo "==============================================="
echo -e "${NC}"
echo "AI-powered cryptocurrency trading assistant"
echo "with MCP integration for real-time analysis"
echo ""

# =============================================================================
# SYSTEM CHECKS
# =============================================================================

echo -e "${YELLOW}🔍 Checking system requirements...${NC}"

# Check if running on supported OS
if [[ "$OSTYPE" != "linux-gnu"* && "$OSTYPE" != "darwin"* ]]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo -e "${YELLOW}⚠️  Windows detected. Please use WSL or Git Bash${NC}"
    else
        echo -e "${RED}❌ Unsupported OS: $OSTYPE${NC}"
        exit 1
    fi
fi

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python not found. Please install Python $PYTHON_MIN_VERSION+${NC}"
    exit 1
fi

# Get Python version
PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d" " -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip not found. Please install pip${NC}"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js not found. Installing Node.js...${NC}"
    
    # Install Node.js based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - assume Homebrew is available
        if command -v brew &> /dev/null; then
            brew install node
        else
            echo -e "${RED}❌ Please install Node.js manually from https://nodejs.org${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Please install Node.js manually from https://nodejs.org${NC}"
        exit 1
    fi
fi

NODE_VERSION=$(node --version 2>/dev/null || echo "none")
echo -e "${GREEN}✅ Node.js $NODE_VERSION found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found. Please install npm${NC}"
    exit 1
fi

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Please install Git${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All system requirements met${NC}"
echo ""

# =============================================================================
# INSTALLATION
# =============================================================================

echo -e "${YELLOW}📦 Starting installation...${NC}"

# Ask for installation directory
read -p "📁 Installation directory (default: ./crypto-mcp-assistant): " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-"./crypto-mcp-assistant"}

# Clone repository
echo -e "${YELLOW}📥 Cloning repository...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory exists. Pulling latest changes...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    git clone $GITHUB_REPO "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo -e "${GREEN}✅ Repository cloned successfully${NC}"

# Create virtual environment
echo -e "${YELLOW}🐍 Creating Python virtual environment...${NC}"
$PYTHON_CMD -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo -e "${GREEN}✅ Virtual environment created${NC}"

# Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install Python dependencies
echo -e "${YELLOW}📚 Installing Python dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Install global MCP servers
echo -e "${YELLOW}🔧 Installing MCP servers...${NC}"
npm install -g @mcp-server/crypto-prices@latest || echo -e "${YELLOW}⚠️  MCP crypto-prices server installation failed${NC}"
npm install -g @mcp-server/google-search@latest || echo -e "${YELLOW}⚠️  MCP google-search server installation failed${NC}"

echo -e "${GREEN}✅ MCP servers installed${NC}"

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p logs data backups

# Copy environment template
echo -e "${YELLOW}⚙️  Setting up configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env file with your API keys${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo -e "${GREEN}✅ Project structure created${NC}"

# =============================================================================
# CONFIGURATION ASSISTANT
# =============================================================================

echo ""
echo -e "${BLUE}⚙️  Configuration Assistant${NC}"
echo -e "${YELLOW}Let's configure your basic settings...${NC}"

# Ask for Groq API key if not set
if ! grep -q "GROQ_API_KEY=." .env; then
    echo ""
    echo -e "${YELLOW}🤖 Groq API Key Required${NC}"
    echo "Get your free API key from: https://console.groq.com/"
    read -p "Enter your Groq API key (or press Enter to skip): " GROQ_KEY
    
    if [ ! -z "$GROQ_KEY" ]; then
        sed -i.bak "s/GROQ_API_KEY=your_groq_api_key_here/GROQ_API_KEY=$GROQ_KEY/" .env
        echo -e "${GREEN}✅ Groq API key configured${NC}"
    else
        echo -e "${YELLOW}⚠️  You'll need to add GROQ_API_KEY to .env later${NC}"
    fi
fi

# Ask about trading mode
echo ""
echo -e "${YELLOW}📊 Trading Configuration${NC}"
echo "1. Paper Trading (Safe - No real money)"
echo "2. Testnet (Binance testnet)"
echo "3. Live Trading (REAL MONEY - Experts only!)"
read -p "Choose trading mode (1-3, default: 1): " TRADING_CHOICE
TRADING_CHOICE=${TRADING_CHOICE:-1}

case $TRADING_CHOICE in
    1)
        sed -i.bak "s/TRADING_MODE=paper/TRADING_MODE=paper/" .env
        sed -i.bak "s/BINANCE_TESTNET=true/BINANCE_TESTNET=true/" .env
        echo -e "${GREEN}✅ Paper trading mode selected (Safe)${NC}"
        ;;
    2)
        sed -i.bak "s/TRADING_MODE=paper/TRADING_MODE=testnet/" .env
        sed -i.bak "s/BINANCE_TESTNET=true/BINANCE_TESTNET=true/" .env
        echo -e "${GREEN}✅ Testnet mode selected${NC}"
        ;;
    3)
        echo -e "${RED}⚠️  LIVE TRADING MODE SELECTED${NC}"
        echo -e "${RED}⚠️  This will use REAL MONEY!${NC}"
        read -p "Are you sure? Type 'YES' to confirm: " CONFIRM
        if [ "$CONFIRM" = "YES" ]; then
            sed -i.bak "s/TRADING_MODE=paper/TRADING_MODE=live/" .env
            sed -i.bak "s/BINANCE_TESTNET=true/BINANCE_TESTNET=false/" .env
            echo -e "${RED}⚠️  Live trading mode enabled${NC}"
        else
            echo -e "${GREEN}✅ Keeping paper trading mode${NC}"
        fi
        ;;
esac

# =============================================================================
# FINAL SETUP
# =============================================================================

echo ""
echo -e "${YELLOW}🔧 Final setup...${NC}"

# Make scripts executable
chmod +x scripts/*.py
chmod +x install.sh

# Test installation
echo -e "${YELLOW}🧪 Testing installation...${NC}"
if $PYTHON_CMD -c "import src; print('✅ Package imports work')"; then
    echo -e "${GREEN}✅ Installation test passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some imports may not work yet (normal during development)${NC}"
fi

# =============================================================================
# COMPLETION MESSAGE
# =============================================================================

echo ""
echo -e "${GREEN}"
echo "==============================================="
echo "    🎉 INSTALLATION COMPLETED!"
echo "==============================================="
echo -e "${NC}"

echo -e "${BLUE}📋 Quick Start Commands:${NC}"
echo ""
echo -e "${YELLOW}1. Activate virtual environment:${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "   source venv/Scripts/activate"
else
    echo "   source venv/bin/activate"
fi

echo ""
echo -e "${YELLOW}2. Edit configuration:${NC}"
echo "   nano .env  # Add your API keys"

echo ""
echo -e "${YELLOW}3. Start the assistant:${NC}"
echo "   python scripts/start_assistant.py --mode full"

echo ""
echo -e "${YELLOW}4. Access interfaces:${NC}"
echo "   🌐 Dashboard: http://localhost:8501"
echo "   📚 API Docs: http://localhost:8000/docs"
echo "   ❤️ Health: http://localhost:8000/health"

echo ""
echo -e "${BLUE}🆘 Need help?${NC}"
echo "   📖 Documentation: https://github.com/Gzeu/crypto-mcp-assistant/blob/main/README.md"
echo "   🏃 Quick Start: https://github.com/Gzeu/crypto-mcp-assistant/blob/main/QUICK_START.md"
echo "   🐛 Issues: https://github.com/Gzeu/crypto-mcp-assistant/issues"

echo ""
echo -e "${RED}⚠️  IMPORTANT SECURITY NOTES:${NC}"
echo -e "${RED}   • Never share your .env file${NC}"
echo -e "${RED}   • Start with paper trading mode${NC}"
echo -e "${RED}   • Use testnet for experiments${NC}"
echo -e "${RED}   • Only use live trading if you're experienced${NC}"

echo ""
echo -e "${GREEN}🇷🇴 Made with ❤️ in Romania${NC}"
echo -e "${GREEN}🚀 Happy trading! 📈${NC}"

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Edit .env file with your API keys"
echo "2. Run: python scripts/start_assistant.py --mode full"
echo "3. Open http://localhost:8501 in your browser"
echo "4. Start with EGLD analysis - it's our Romanian focus! 🇷🇴"

echo ""