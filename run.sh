#!/bin/bash
echo "🚀 Đang khởi động Telegram Bot Matrix AI..."

# Dọn dẹp tiến trình cũ đang treo
pkill -f bot.py 2>/dev/null
pkill -f streamlit 2>/dev/null

# Cài đặt các thư viện cần thiết
echo "📦 Đang kiểm tra và cài đặt thư viện..."
pip install -q google-generativeai python-telegram-bot

# Chạy bot Telegram
echo "🤖 Bot đã sẵn sàng!"
python bot.py
