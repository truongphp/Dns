import requests
import streamlit as st

st.set_page_config(page_title="AI Tự Do (Local)", page_icon="🔓")
st.title("🔓 AI Tự Chủ - Không Rào Cản")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
  st.session_state.messages = []

# Hiển thị tin nhắn cũ
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Ô nhập liệu chat
if prompt := st.chat_input("Nhập gì tùy thích..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("AI đang nghĩ..."):
      try:
        # Gọi tới mô hình chạy local trên Codespaces (Ollama)
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",  # Hoặc gemma, phi3 tùy bạn chọn
                "messages": st.session_state.messages,
                "stream": False,
            },
        )
        if response.status_code == 200:
          ai_reply = response.json()["message"]["content"]
          st.markdown(ai_reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": ai_reply}
          )
        else:
          st.error(
              "⚠️ Chưa bật động cơ Ollama ở terminal kìa dev ơi! Chạy lệnh"
              " `ollama serve` trước nhé."
          )
      except Exception as e:
        st.error(
            f"Lỗi kết nối tới tiến trình local: {e}. Đảm bảo Ollama đang chạy."
        )
