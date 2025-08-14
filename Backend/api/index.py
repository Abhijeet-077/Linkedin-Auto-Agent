#!/usr/bin/env python3
"""
Vercel Serverless Function Entry Point for InfluenceOS Backend
"""

import sys
import os

# Add the parent directory to the Python path so we can import from working_server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from working_server import app

# Export the FastAPI app for Vercel
handler = app
