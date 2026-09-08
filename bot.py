import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Ẩn bớt log rác mạng của thư viện
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

# Dán API Key Gemini thật của bạn vào đây
GEMINI_API_KEY = "AQ.Ab8RN6LFFcjrkwmvxPBY2SEK5ukTUNZx4-Y-gtpcsc_Bu6OGkg"
TELEGRAM_BOT_TOKEN = "8890814478:AAE55jsK49r-10722YebbeRu9rK2hTpaOy0"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  chat_id = update.message.chat_id

  sent_msg = await context.bot.send_message(
      chat_id=chat_id, text="⚡ Đang xử lý..."
  )

  try:
    if GEMINI_API_KEY == "DÁN_GEMINI_API_KEY_CỦA_BẠN_VÀO_ĐÂY":
      await context.bot.edit_message_text(
          chat_id=chat_id,
          message_id=sent_msg.message_id,
          text="⚠️ Chưa cấu hình Gemini API Key trong file bot.py!",
      )
      return

    # Gọi API đồng bộ để phản hồi trực tiếp siêu tốc
    response = model.generate_content(user_message)
    reply_text = (
        response.text if response and response.text else "⚠️ Phản hồi trống."
    )

    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=reply_text
    )
  except Exception as e:
    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=f"⚠️ Lỗi: {e}"
    )


if __name__ == "__main__":
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

  print("🟢 Bot Telegram đang chạy mượt mà...")
  app.run_polling(poll_interval=0.3)
