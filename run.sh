#!/bin/bash
echo "🚀 Khởi động hệ thống Matrix AI & Telegram..."
pkill -f streamlit 2>/dev/null
pip install -q streamlit google-generativeai python-telegram-bot
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false
