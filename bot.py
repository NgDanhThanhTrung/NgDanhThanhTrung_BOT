import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Lấy Token từ GitHub Secrets
TOKEN = os.getenv('BOT_TOKEN')
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\n"
        "Nhắn từ khóa 'locket' để mình gửi hướng dẫn cài đặt Gold nhé."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if "locket" in text:
        caption = (
            "⭐ *LOCKET NDTT MODULE \- 2026* ⭐\n"
            "──────────────\n"
            "Hướng dẫn giả lập *Locket Gold* vĩnh viễn:\n\n"
            "1️⃣ *Copy URL Module:* \(Chạm vào link để copy\)\n"
            f"`{RAW_URL}`\n\n"
            "2️⃣ *Shadowrocket:* Tab Module \> Add Module \> Dán link\.\n\n"
            "3️⃣ *HTTPS Decryption:* Cực kỳ quan trọng\! Bạn phải cài chứng chỉ CA và *Bật tin cậy* trong Cài đặt iPhone\.\n\n"
            "4️⃣ *Hoàn tất:* Bật VPN và mở Locket hưởng thụ\."
        )
        keyboard = [
            [InlineKeyboardButton("🚀 Cài nhanh (Shadowrocket)", url=f"shadowrocket://config/add/{RAW_URL}")],
            [InlineKeyboardButton("💬 Liên hệ Admin", url="https://t.me/NgDanhThanhTrung")],
            [InlineKeyboardButton("☕ Donate", url="https://ngdanhthanhtrung.github.io/Bank/")]
        ]
        await update.message.reply_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN_V2
        )

if __name__ == '__main__':
    if not TOKEN:
        print("Lỗi: Không tìm thấy BOT_TOKEN!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.run_polling()
