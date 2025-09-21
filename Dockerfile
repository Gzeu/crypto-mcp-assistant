# Crypto MCP Assistant - Docker Image
# Multi-stage build pentru optimizare

# =============================================================================
# Build Stage
# =============================================================================
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for MCP servers
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# =============================================================================
# Production Stage
# =============================================================================
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    GROQ_API_KEY="" \
    BINANCE_API_KEY="" \
    BINANCE_SECRET_KEY="" \
    TRADING_MODE="paper" \
    LOG_LEVEL="INFO"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data backups \
    && chown -R appuser:appuser /app

# Install global MCP servers
RUN npm install -g @mcp-server/crypto-prices@latest \
    && npm install -g @mcp-server/google-search@latest

# Switch to app user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000 8501

# Default command
CMD ["python", "scripts/start_assistant.py", "--mode", "full"]

# =============================================================================
# Development Stage (optional)
# =============================================================================
FROM production as development

# Switch back to root for development tools
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

# Switch back to app user
USER appuser

# Development command
CMD ["python", "scripts/start_assistant.py", "--mode", "full", "--log-level", "DEBUG"]