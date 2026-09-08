import google.generativeai as genai
import streamlit as st

# Cấu hình trang Dark Mode
st.set_page_config(
    page_title="Matrix AI Terminal", page_icon="🟢", layout="centered"
)

# CSS tùy biến giao diện: Nền đen, chữ xanh lá phát sáng, phong cách terminal ngầu
st.markdown(
    """
    <style>
        /* Tổng thể nền đen */
        .stApp {
            background-color: #050505;
            color: #00ff66;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Hiệu ứng chữ phát sáng xanh lá */
        h1, h2, h3, p, label, .stMarkdown {
            color: #00ff66 !important;
            text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
        }

        /* Sidebar tối màu phong cách hệ thống */
        [data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #00ff6633;
        }

        /* Ô nhập API Key và Input Chat */
        .stTextInput input, .stChatInput input {
            background-color: #111111 !important;
            color: #00ff66 !important;
            border: 1px solid #00ff6655 !important;
            box-shadow: 0 0 5px rgba(0, 255, 102, 0.2);
        }
        
        /* Khung chứa tin nhắn của User và AI */
        [data-testid="stChatMessage"] {
            background-color: #0d0d0d;
            border: 1px solid #00ff6622;
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.05);
        }

        /* Hiệu ứng mưa mã nguồn / chữ phát sáng nhẹ nền */
        .matrix-header {
            text-align: center;
            font-weight: bold;
            letter-spacing: 2px;
            text-shadow: 0 0 12px #00ff66;
            margin-bottom: 20px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Tiêu đề giao diện
st.markdown(
    "<h1 class='matrix-header'>🟢 MATRIX AI TERMINAL 🟢</h1>",
    unsafe_allow_html=True,
)

# Nhập API Key ở sidebar
with st.sidebar:
  st.markdown("### ⚙️ HỆ THỐNG BẢO MẬT")
  api_key = st.text_input("Nhập Gemini API Key:", type="password")
  st.markdown("---")
  st.markdown("<p style='font-size: 12px;'>Trạng thái: Sẵn sàng kết nối</p>", unsafe_allow_html=True)

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  # Lưu lịch sử chat
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Hiển thị lịch sử
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Thanh nhập lệnh chat
  if prompt := st.chat_input("Nhập lệnh hoặc câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("Đang xử lý dữ liệu..."):
        try:
          response = model.generate_content(prompt)
          ai_reply = response.text
          st.markdown(ai_reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": ai_reply}
          )
        except Exception as e:
          st.error(f"Lỗi hệ thống: {e}")
else:
  st.warning(
      "⚠️ Vui lòng nhập API Key vào thanh công cụ bên trái để kích hoạt hệ"
      " thống."
  )
