import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Matrix AI Terminal", page_icon="🟢", layout="centered"
)

st.markdown(
    """
    <style>
        .stApp { background-color: #000000; color: #00ff66; font-family: 'Courier New', Courier, monospace; }
        .stApp::before {
            content: " "; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, rgba(0,255,102,0.03) 0%, rgba(0,0,0,0.95) 100%);
            pointer-events: none; z-index: 0;
        }
        h1, h2, h3, p, label, .stMarkdown { color: #00ff66 !important; text-shadow: 0 0 6px rgba(0, 255, 102, 0.6); position: relative; z-index: 1; }
        [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #00ff6633; }
        .stTextInput input, .stChatInput input { background-color: #0a0a0a !important; color: #00ff66 !important; border: 1px solid #00ff6666 !important; }
        [data-testid="stChatMessage"] { background-color: rgba(10, 15, 10, 0.85); border: 1px solid #00ff6644; position: relative; z-index: 1; }
        .matrix-title { text-align: center; font-weight: bold; letter-spacing: 3px; text-shadow: 0 0 15px #00ff66; margin-bottom: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 class='matrix-title'>🟢 MATRIX AI TERMINAL 🟢</h1>",
    unsafe_allow_html=True,
)

with st.sidebar:
  st.markdown("### ⚙️ CẤU HÌNH HỆ THỐNG")
  gemini_key = st.text_input("Gemini API Key:", type="password")

if gemini_key:
  genai.configure(api_key=gemini_key)
  model = genai.GenerativeModel("gemini-2.0-flash")

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
      # Dùng container rỗng để ép chữ render trực tiếp mượt mà
      response_container = st.empty()
      response_container.markdown("🟢 Đang kết xuất dữ liệu...")
      try:
        response = model.generate_content(prompt)
        response_container.markdown(response.text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
      except Exception as e:
        response_container.error(f"Lỗi: {e}")
else:
  st.warning("⚠️ Nhập Gemini API Key vào sidebar để bắt đầu.")
