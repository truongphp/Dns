import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

GEMINI_API_KEY = "AQ.Ab8RN6LFFcjrkwmvxPBY2SEK5ukTUNZx4-Y-gtpcsc_Bu6OGkg"
TELEGRAM_BOT_TOKEN = "8890814478:AAE55jsK49r-10722YebbeRu9rK2hTpaOy0"

genai.configure(api_key=GEMINI_API_KEY)

# Tiêm nhân cách lầy lội, mặn mòi, Gen Z vào thẳng system instruction của model
system_instruction = (
    "Bạn là một trợ lý AI thông minh nhưng có tính cách cực kỳ lầy lội, mặn mòi, "
    "hay cà khịa, nói chuyện tẻn tẻn đúng chất Gen Z chính hiệu. "
    "Tuyệt đối KHÔNG dùng văn phong tổng đài, KHÔNG dạ vâng thưa gửi máy móc, "
    "không nói mấy câu kiểu 'Tôi có thể giúp gì cho bạn'. "
    "Hãy nói chuyện ngắn gọn, trực diện, biết cách 'phản dame' lầy lội với user, "
    "dùng từ lóng trẻ trung (vcl, gét gô, ét o ét,...) và icon linh hoạt. "
    "Nhưng nhớ là vẫn phải trả lời đúng trọng tâm câu hỏi, không xàm ngôn vô ích."
)

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash", system_instruction=system_instruction
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  chat_id = update.message.chat_id

  sent_msg = await context.bot.send_message(
      chat_id=chat_id, text="⏳ Đang check var..."
  )

  try:
    response = model.generate_content(user_message)
    reply_text = (
        response.text if response and response.text else "⚠️ Cạn lời, lười trả lời."
    )
    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=reply_text
    )
  except Exception as e:
    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=sent_msg.message_id, text=f"⚠️ Toang: {e}"
    )


if __name__ == "__main__":
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

  print("🟢 Bot phản dame hệ Gen Z đã online...")
  app.run_polling(poll_interval=0.3)
