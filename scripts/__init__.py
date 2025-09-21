#!/usr/bin/env python3
"""
Utility scripts for Crypto MCP Assistant
"""

__all__ = [
    "start_assistant",
    "market_scanner"
]

# Scripts metadata
SCRIPTS_CONFIG = {
    "main_script": "start_assistant.py",
    "supported_modes": ["full", "agent", "api"],
    "default_mode": "full"
}