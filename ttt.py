import telebot
import requests
import json

# ✅ Burada tokenləri daxil edin
TELEGRAM_BOT_TOKEN = "7275218430:AAGhw3hX_FkI7qjZsfkKUp0SX2WIoR_FgNI"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ İstifadəçinin mesajını qəbul edib CBT cavabı qaytarır
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, "typing")  # 📌 Yazır... effekti əlavə edirik
    
    response = get_cbt_response(user_text)  # ✅ CBT cavabı alırıq
    bot.send_message(message.chat.id, response)

# ✅ OpenAI GPT-4-dən CBT cavabı alan funksiya
def get_cbt_response(user_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Siz CBT terapevtsiniz.  CBT üsullarını və sokratik sorğulama tətbiq edərək, humanist yanaşaraq psixoloji kömək edin."},
            {"role": "user", "content": user_text}
        ],
        "max_tokens": 500
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()
    
    # ✅ Cavabı formatlaşdırırıq
    return response_json.get("choices", [{}])[0].get("message", {}).get("content", "Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.")

# ✅ Botu başladırıq
if __name__ == "__main__":
    print("🤖 Bot işləyir...")
    bot.polling(none_stop=True)
