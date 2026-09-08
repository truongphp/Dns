import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Cấu hình Token & Key
GEMINI_API_KEY = "NHẬP_GEMINI_API_KEY_CỦA_BẠN_VÀO_ĐÂY"
TELEGRAM_BOT_TOKEN = "8890814478:AAE55jsK49r-10722YebbeRu9rK2hTpaOy0"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  chat_id = update.message.chat_id

  # Gửi tin nhắn phản hồi nhanh
  sent_msg = await context.bot.send_message(
      chat_id=chat_id, text="🟢 [Matrix AI] Đang xử lý..."
  )

  try:
    # Gọi AI xử lý bất đồng bộ (async) siêu tốc
    response = await model.generate_content_async(user_message)
    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=response.text
    )
  except Exception as e:
    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=f"⚠️ Lỗi: {e}"
    )


if __name__ == "__main__":
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

  print("🟢 Telegram Bot standalone đang hoạt động 24/7...")
  app.run_polling()
