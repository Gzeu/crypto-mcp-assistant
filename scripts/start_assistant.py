#!/usr/bin/env python3
"""
Crypto MCP Assistant - Main Startup Script
Script principal pentru pornirea asistentului crypto AI
"""

import asyncio
import os
import sys
import signal
import argparse
from pathlib import Path
from typing import Optional
import subprocess
import time

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from loguru import logger
from dotenv import load_dotenv

# Import our components
from core.ai_agent import CryptoAIAgent

# Load environment variables
load_dotenv()

class CryptoAssistantLauncher:
    """Main launcher pentru Crypto MCP Assistant"""
    
    def __init__(self):
        self.agent: Optional[CryptoAIAgent] = None
        self.api_process: Optional[subprocess.Popen] = None
        self.dashboard_process: Optional[subprocess.Popen] = None
        self.running = False
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", "logs/crypto_assistant.log")
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure loguru
        logger.remove()  # Remove default handler
        
        # Console handler
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True
        )
        
        # File handler
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation="100 MB",
            retention="30 days",
            compression="zip"
        )
        
        logger.info("Logging setup completed")
    
    def _check_prerequisites(self) -> bool:
        """Verifica daca toate prerequisitele sunt indeplinite"""
        logger.info("Checking prerequisites...")
        
        required_env_vars = [
            "GROQ_API_KEY",
        ]
        
        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            logger.error("Please check your .env file")
            return False
        
        # Check if config files exist
        config_files = [
            "config/trading_config.yaml",
            "config/mcp_config.json",
            "config/symbols.json"
        ]
        
        missing_files = []
        for file_path in config_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            logger.error(f"Missing configuration files: {missing_files}")
            return False
        
        logger.info("✅ All prerequisites met")
        return True
    
    async def start_agent(self) -> bool:
        """Porneste agentul AI principal"""
        try:
            logger.info("Starting Crypto AI Agent...")
            self.agent = CryptoAIAgent()
            logger.info("✅ Crypto AI Agent started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start AI Agent: {e}")
            return False
    
    def start_api_server(self) -> bool:
        """Porneste serverul FastAPI"""
        try:
            logger.info("Starting FastAPI server...")
            
            api_host = os.getenv("API_HOST", "127.0.0.1")
            api_port = int(os.getenv("API_PORT", "8000"))
            
            cmd = [
                sys.executable, "-m", "uvicorn",
                "web.api:app",
                "--host", api_host,
                "--port", str(api_port),
                "--reload" if os.getenv("DEVELOPMENT_MODE", "true").lower() == "true" else "--no-reload"
            ]
            
            self.api_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to see if it starts successfully
            time.sleep(3)
            
            if self.api_process.poll() is None:
                logger.info(f"✅ FastAPI server started on http://{api_host}:{api_port}")
                return True
            else:
                stdout, stderr = self.api_process.communicate()
                logger.error(f"❌ FastAPI server failed to start: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start API server: {e}")
            return False
    
    def start_dashboard(self) -> bool:
        """Porneste dashboard-ul Streamlit"""
        try:
            logger.info("Starting Streamlit dashboard...")
            
            streamlit_host = os.getenv("STREAMLIT_HOST", "127.0.0.1")
            streamlit_port = int(os.getenv("STREAMLIT_PORT", "8501"))
            
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "web/dashboard.py",
                "--server.address", streamlit_host,
                "--server.port", str(streamlit_port),
                "--server.headless", "true",
                "--server.enableCORS", "false"
            ]
            
            self.dashboard_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to see if it starts successfully
            time.sleep(5)
            
            if self.dashboard_process.poll() is None:
                logger.info(f"✅ Streamlit dashboard started on http://{streamlit_host}:{streamlit_port}")
                return True
            else:
                stdout, stderr = self.dashboard_process.communicate()
                logger.error(f"❌ Streamlit dashboard failed to start: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start dashboard: {e}")
            return False
    
    async def start_trading_session(self) -> None:
        """Porneste sesiunea de trading"""
        if not self.agent:
            logger.error("Agent not initialized")
            return
        
        try:
            logger.info("Starting trading session...")
            await self.agent.start_trading_session()
        except Exception as e:
            logger.error(f"Error in trading session: {e}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers pentru graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("Starting graceful shutdown...")
        self.running = False
        
        # Stop trading session
        if self.agent:
            try:
                await self.agent.stop_trading_session()
                logger.info("✅ Trading session stopped")
            except Exception as e:
                logger.error(f"Error stopping trading session: {e}")
        
        # Stop API server
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=10)
                logger.info("✅ API server stopped")
            except subprocess.TimeoutExpired:
                self.api_process.kill()
                logger.warning("API server forcefully killed")
            except Exception as e:
                logger.error(f"Error stopping API server: {e}")
        
        # Stop dashboard
        if self.dashboard_process:
            try:
                self.dashboard_process.terminate()
                self.dashboard_process.wait(timeout=10)
                logger.info("✅ Dashboard stopped")
            except subprocess.TimeoutExpired:
                self.dashboard_process.kill()
                logger.warning("Dashboard forcefully killed")
            except Exception as e:
                logger.error(f"Error stopping dashboard: {e}")
        
        logger.info("✅ Shutdown completed")
    
    async def run_full_stack(self, enable_trading: bool = False):
        """Ruleaza intregul stack (API + Dashboard + opțional Trading)"""
        logger.info("🚀 Starting Crypto MCP Assistant - Full Stack Mode")
        
        # Check prerequisites
        if not self._check_prerequisites():
            logger.error("Prerequisites not met, exiting")
            return
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Start components
        success = True
        
        # 1. Start AI Agent
        if not await self.start_agent():
            success = False
        
        # 2. Start API Server
        if success and not self.start_api_server():
            success = False
        
        # 3. Start Dashboard
        if success and not self.start_dashboard():
            success = False
        
        if not success:
            logger.error("❌ Failed to start all components")
            await self.shutdown()
            return
        
        logger.info("✅ All components started successfully!")
        logger.info("")
        logger.info("🌐 Access Points:")
        logger.info(f"  - API Documentation: http://127.0.0.1:8000/docs")
        logger.info(f"  - Dashboard: http://127.0.0.1:8501")
        logger.info(f"  - Health Check: http://127.0.0.1:8000/health")
        logger.info("")
        
        self.running = True
        
        # Start trading session if enabled
        if enable_trading:
            logger.info("🎯 Starting automated trading session...")
            await self.start_trading_session()
        else:
            logger.info("📊 Running in analysis-only mode (no trading)")
            
            # Keep running until interrupted
            try:
                while self.running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
        
        await self.shutdown()
    
    async def run_agent_only(self, enable_trading: bool = False):
        """Ruleaza doar agentul AI (fara web interface)"""
        logger.info("🤖 Starting Crypto MCP Assistant - Agent Only Mode")
        
        if not self._check_prerequisites():
            logger.error("Prerequisites not met, exiting")
            return
        
        self.setup_signal_handlers()
        
        if not await self.start_agent():
            logger.error("❌ Failed to start AI Agent")
            return
        
        self.running = True
        
        if enable_trading:
            logger.info("🎯 Starting automated trading session...")
            await self.start_trading_session()
        else:
            logger.info("📊 Agent ready for manual queries")
            
            # Interactive mode
            while self.running:
                try:
                    user_input = input("\n💬 Enter your query (or 'quit' to exit): ")
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if user_input.strip():
                        logger.info("🧠 Processing query...")
                        response = await self.agent.manual_analysis(user_input)
                        print(f"\n🤖 AI Response:\n{response}\n")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Error processing query: {e}")
        
        await self.shutdown()
    
    async def run_api_only(self):
        """Ruleaza doar API-ul (pentru integrari externe)"""
        logger.info("🌐 Starting Crypto MCP Assistant - API Only Mode")
        
        if not self._check_prerequisites():
            logger.error("Prerequisites not met, exiting")
            return
        
        self.setup_signal_handlers()
        
        # Start AI Agent
        if not await self.start_agent():
            logger.error("❌ Failed to start AI Agent")
            return
        
        # Start API Server
        if not self.start_api_server():
            logger.error("❌ Failed to start API server")
            await self.shutdown()
            return
        
        logger.info("✅ API server started successfully!")
        logger.info(f"📖 API Documentation: http://127.0.0.1:8000/docs")
        
        self.running = True
        
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        
        await self.shutdown()

def main():
    """Main function cu argument parsing"""
    parser = argparse.ArgumentParser(
        description="Crypto MCP Assistant - AI-powered cryptocurrency trading assistant"
    )
    
    parser.add_argument(
        "--mode",
        choices=["full", "agent", "api"],
        default="full",
        help="Modul de rulare: full (toate componentele), agent (doar AI), api (doar API)"
    )
    
    parser.add_argument(
        "--trading",
        action="store_true",
        help="Activeaza trading automat (ATENTIE: foloseste bani reali!)"
    )
    
    parser.add_argument(
        "--config",
        default="config/trading_config.yaml",
        help="Calea catre fisierul de configurare"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nivelul de logging"
    )
    
    args = parser.parse_args()
    
    # Set log level
    os.environ["LOG_LEVEL"] = args.log_level
    
    # Create launcher
    launcher = CryptoAssistantLauncher()
    
    # Warning for trading mode
    if args.trading:
        print("⚠️  WARNING: Trading mode enabled!")
        print("⚠️  This will execute real trades with real money!")
        print("⚠️  Make sure you understand the risks!")
        confirm = input("Do you want to continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Trading mode cancelled.")
            return
    
    # Run based on mode
    try:
        if args.mode == "full":
            asyncio.run(launcher.run_full_stack(enable_trading=args.trading))
        elif args.mode == "agent":
            asyncio.run(launcher.run_agent_only(enable_trading=args.trading))
        elif args.mode == "api":
            asyncio.run(launcher.run_api_only())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()