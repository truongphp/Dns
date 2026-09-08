import threading
import google.generativeai as genai
import streamlit as st
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

st.set_page_config(
    page_title="Matrix AI Command Center", page_icon="🟢", layout="centered"
)

# Giao diện CSS: Phong cách Matrix / Cyberpunk tối đen, chữ xanh lá phát sáng
st.markdown(
    """
    <style>
        .stApp {
            background-color: #000000;
            color: #00ff66;
            font-family: 'Courier New', Courier, monospace;
        }
        .stApp::before {
            content: " ";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(180deg, rgba(0,255,102,0.03) 0%, rgba(0,0,0,0.95) 100%);
            pointer-events: none;
            z-index: 0;
        }
        h1, h2, h3, p, label, .stMarkdown {
            color: #00ff66 !important;
            text-shadow: 0 0 6px rgba(0, 255, 102, 0.6);
            position: relative;
            z-index: 1;
        }
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #00ff6633;
        }
        .stTextInput input, .stChatInput input {
            background-color: #0a0a0a !important;
            color: #00ff66 !important;
            border: 1px solid #00ff6666 !important;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.2);
        }
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

st.markdown(
    "<h1 class='matrix-title'>🟢 MATRIX AI COMMAND CENTER 🟢</h1>",
    unsafe_allow_html=True,
)

# Sidebar cấu hình
with st.sidebar:
  st.markdown("### ⚙️ TRUNG TÂM ĐIỀU KHIỂN")
  gemini_key = st.text_input("Gemini API Key:", type="password")
  tele_token = st.text_input(
      "Telegram Bot Token:",
      value="8890814478:AAE55jsK49r-10722YebbeRu9rK2hTpaOy0",
      type="password",
  )
  st.markdown("---")

  # Nút kích hoạt Bot Telegram chạy ngầm
  if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

  if gemini_key and tele_token:
    if not st.session_state.bot_running:
      if st.button("🚀 Khởi động Telegram Bot"):

        def run_telegram_bot():
          import asyncio

          async def handle_message(
              update: Update, context: ContextTypes.DEFAULT_TYPE
          ):
            genai.configure(api_key=gemini_key)
            bot_model = genai.GenerativeModel("gemini-1.5-flash")
            user_message = update.message.text
            chat_id = update.message.chat_id

            sent_msg = await context.bot.send_message(
                chat_id=chat_id, text="🟢 [Matrix AI] Đang xử lý tín hiệu..."
            )
            try:
              res = bot_model.generate_content(user_message)
              await context.bot.edit_message_text(
                  chat_id=chat_id,
                  message_id=sent_msg.message_id,
                  text=res.text,
              )
            except Exception as e:
              await context.bot.edit_message_text(
                  chat_id=chat_id,
                  message_id=sent_msg.message_id,
                  text=f"⚠️ Lỗi: {e}",
              )

          loop = asyncio.new_event_loop()
          asyncio.set_event_loop(loop)
          app = ApplicationBuilder().token(tele_token).build()
          app.add_handler(
              MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
          )
          app.run_polling()

        threading.Thread(target=run_telegram_bot, daemon=True).start()
        st.session_state.bot_running = True
        st.success("🤖 Bot Telegram đã kích hoạt ngầm!")

    if st.session_state.bot_running:
      st.markdown(
          "<p style='color: #00ff66;'>🟢 Trạng thái: Bot đang online 24/7</p>",
          unsafe_allow_html=True,
      )
  else:
    st.warning("⚠️ Nhập đủ API Key và Token để bật Bot.")

# Giao diện Chat Web trực tiếp
if gemini_key:
  genai.configure(api_key=gemini_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Nhập lệnh trực tiếp trên Terminal..."):
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
  st.warning("⚠️ Vui lòng nhập Gemini API Key vào sidebar để bắt đầu chiến.")
