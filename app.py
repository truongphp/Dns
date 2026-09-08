import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Matrix AI Terminal", page_icon="🟢", layout="centered"
)

# Giao diện CSS: Hiệu ứng mưa chữ Matrix nền tối, khung chat cyberpunk
st.markdown(
    """
    <style>
        /* Nền tổng thể màu đen tuyền */
        .stApp {
            background-color: #000000;
            color: #00ff66;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Hiệu ứng mưa chữ xanh lá phía sau (Matrix Rain Animation giả lập) */
        .stApp::before {
            content: " ";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, rgba(0,255,102,0.03) 0%, rgba(0,0,0,0.95) 100%);
            pointer-events: none;
            z-index: 0;
        }

        /* Chữ phát sáng xanh lá */
        h1, h2, h3, p, label, .stMarkdown {
            color: #00ff66 !important;
            text-shadow: 0 0 6px rgba(0, 255, 102, 0.6);
            position: relative;
            z-index: 1;
        }

        /* Sidebar tối giản */
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #00ff6633;
        }

        /* Ô nhập liệu và chat input */
        .stTextInput input, .stChatInput input {
            background-color: #0a0a0a !important;
            color: #00ff66 !important;
            border: 1px solid #00ff6666 !important;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.2);
        }
        
        /* Khung chat của User & AI dạng terminal */
        [data-testid="stChatMessage"] {
            background-color: rgba(10, 15, 10, 0.85);
            border: 1px solid #00ff6644;
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.1);
            position: relative;
            z-index: 1;
        }

        .matrix-title {
            text-align: center;
            font-weight: bold;
            letter-spacing: 3px;
            text-shadow: 0 0 15px #00ff66;
            margin-bottom: 20px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Tiêu đề giao diện
st.markdown(
    "<h1 class='matrix-title'>🟢 MATRIX AI TERMINAL 🟢</h1>",
    unsafe_allow_html=True,
)

# Sidebar cấu hình API Key
with st.sidebar:
  st.markdown("### ⚙️ BẢO MẬT HỆ THỐNG")
  api_key = st.text_input("Gemini API Key:", type="password")
  st.markdown("---")
  st.markdown(
      "<p style='font-size: 11px; opacity: 0.8;'>Status: Secure Connection</p>",
      unsafe_allow_html=True,
  )

if api_key:
  genai.configure(api_key=api_key)
  # Sử dụng model chuẩn xác nhất hiện tại
  model = genai.GenerativeModel("gemini-2.5-flash-latest")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Nhập lệnh..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("Đang kết xuất dữ liệu..."):
        try:
          response = model.generate_content(prompt)
          ai_reply = response.text
          st.markdown(ai_reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": ai_reply}
          )
        except Exception as e:
          st.error(f"Lỗi: {e}")
else:
  st.warning("⚠️ Vui lòng nhập API Key vào sidebar để khởi động hệ thống.")
