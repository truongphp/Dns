#!/bin/bash
echo "🚀 Đang khởi động hệ thống Matrix AI..."

# Tắt các tiến trình Streamlit cũ đang chạy treo port (nếu có)
pkill -f streamlit 2>/dev/null

# Cài đặt tự động các thư viện cần thiết
echo "📦 Đang kiểm tra thư viện..."
pip install -q streamlit google-generativeai

# Bật giao diện Web App
echo "✨ Kích hoạt Web App thành công!"
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false

