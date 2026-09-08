#!/bin/bash
echo "🚀 Đang khởi động hệ thống Matrix AI..."

# Tắt các tiến trình cũ đang treo port hoặc chạy ngầm
pkill -f streamlit 2>/dev/null
pkill -f bot.py 2>/dev/null

# Cài đặt đầy đủ thư viện
echo "📦 Đang kiểm tra thư viện..."
pip install -q streamlit google-generativeai python-telegram-bot

# Chạy Bot Telegram ngầm ở background
echo "🤖 Kích hoạt Bot Telegram..."
python bot.py &

# Chạy Web App Streamlit ở foreground
echo "✨ Kích hoạt Web App Matrix AI..."
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false

