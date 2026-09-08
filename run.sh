#!/bin/bash
echo "🚀 Đang khởi động hệ thống AI tự do..."

# Cài đặt tự động các thư viện cần thiết nếu chưa có
pip install -q streamlit requests

# Bật Ollama ngầm nếu chưa chạy (dành cho môi trường Codespaces)
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚙️ Đang bật động cơ Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    # Tải sẵn một con model gọn nhẹ không rào cản (ví dụ: llama3 hoặc phi3)
    echo "📥 Đang tải mô hình AI..."
    ollama pull llama3
fi

# Chạy giao diện Streamlit
echo "✨ Mở giao diện Web App..."
streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false
