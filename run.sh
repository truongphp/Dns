#!/bin/bash
echo "🚀 Khởi động Telegram Bot Matrix AI..."

# Dọn dẹp tiến trình cũ
pkill -f bot.py 2>/dev/null
pkill -f streamlit 2>/dev/null

# Cài thư viện cần thiết
pip install -q google-generativeai python-telegram-bot

# Chạy trực tiếp bot Telegram
python bot.py
