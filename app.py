import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="AI Sơ Cấp", page_icon="🤖")
st.title("🤖 AI Thời Kỳ Đầu (Clean & Basic)")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

  for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
      st.markdown(message.parts[0].text)

  if prompt := st.chat_input("Nhập gì đó đi..."):
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("Đang phản hồi..."):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
else:
  st.info("👈 Nhập API key vào sidebar để bắt đầu chiến.")
