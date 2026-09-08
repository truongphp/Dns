import os
from google import genai
import streamlit as st

# Cấu hình trang web
st.set_page_config(
    page_title="Trợ lý AI Cá Nhân", page_icon="🤖", layout="centered"
)

st.title("🤖 Trợ Lý AI Của Riêng Tôi")
st.markdown("---")

# Nhập API Key trực tiếp trên giao diện hoặc lấy từ biến môi trường
api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
  api_key = os.environ.get("GEMINI_API_KEY", "")

if not api_key:
  st.warning("⚠️ Vui lòng nhập Gemini API Key ở thanh bên trái để bắt đầu.")
  st.stop()

# Khởi tạo Gemini Client
client = genai.Client(api_key=api_key)

# Lưu lịch sử chat trong phiên làm việc
if "messages" not in st.session_state:
  st.session_state.messages = []

# Hiển thị lịch sử chat cũ
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Nhập tin nhắn từ người dùng
if prompt := st.chat_input("Nhập tin nhắn cho AI..."):
  # Thêm câu hỏi vào lịch sử
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Gọi API và hiển thị câu trả lời
  with st.chat_message("assistant"):
    with st.spinner("AI đang suy nghĩ..."):
      try:
        # Gửi lịch sử chat hoặc prompt đơn giản
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        ai_reply = response.text
        st.markdown(ai_reply)
        # Lưu phản hồi vào lịch sử
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )
      except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
