#!/usr/bin/env python3
"""
Crypto MCP Assistant - Setup Script
Installation configuration pentru proiect
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Remove comments and empty lines from requirements
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

# Package metadata
setup(
    name="crypto-mcp-assistant",
    version="1.0.0",
    author="Gzeu",
    author_email="pricopgeorge@gmail.com",
    description="AI-powered cryptocurrency trading assistant with MCP integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gzeu/crypto-mcp-assistant",
    project_urls={
        "Bug Tracker": "https://github.com/Gzeu/crypto-mcp-assistant/issues",
        "Documentation": "https://github.com/Gzeu/crypto-mcp-assistant/wiki",
        "Source Code": "https://github.com/Gzeu/crypto-mcp-assistant",
    },
    packages=find_packages(include=['src', 'src.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.0.0",
            "pre-commit>=3.0.0",
        ],
        "monitoring": [
            "prometheus-client>=0.17.0",
            "psutil>=5.9.0",
        ],
        "production": [
            "gunicorn>=21.0.0",
            "uvicorn[standard]>=0.20.0",
        ],
    },
    package_data={
        "src": [
            "config/*.json",
            "config/*.yaml",
            "config/*.yml",
        ],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "crypto-assistant=scripts.start_assistant:main",
            "crypto-api=web.api:main",
        ],
    },
    keywords=[
        "cryptocurrency",
        "trading",
        "ai",
        "mcp",
        "bitcoin",
        "ethereum",
        "binance",
        "technical-analysis",
        "automated-trading",
        "portfolio-management",
        "risk-management",
        "machine-learning",
        "fastapi",
        "streamlit",
        "langchain",
        "groq",
    ],
    zip_safe=False,
)