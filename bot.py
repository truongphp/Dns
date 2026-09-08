import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Tắt log rác của thư viện mạng gRPC/Telegram
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

GEMINI_API_KEY = "NHẬP_GEMINI_API_KEY_CỦA_BẠN_VÀO_ĐÂY"
TELEGRAM_BOT_TOKEN = "8890814478:AAE55jsK49r-10722YebbeRu9rK2hTpaOy0"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  chat_id = update.message.chat_id

  # Gửi tin nhắn chờ
  sent_msg = await context.bot.send_message(
      chat_id=chat_id, text="⚡ Đang xử lý..."
  )

  try:
    # Gọi AI sinh nội dung bất đồng bộ
    response = await model.generate_content_async(user_message)
    reply_text = (
        response.text
        if response and response.text
        else "⚠️ Không nhận được phản hồi từ AI."
    )

    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=reply_text
    )
  except Exception as e:
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=sent_msg.message_id,
        text=f"⚠️ Lỗi hệ thống: {e}",
    )


if __name__ == "__main__":
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

  print("🟢 Bot Telegram đang chạy tốc độ cao...")
  # Giảm thời gian chờ kết nối (poll_interval) để bot mượt hơn
  app.run_polling(poll_interval=0.5)
