import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Lấy Token từ GitHub Secrets
TOKEN = os.getenv('BOT_TOKEN')
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_input = update.message.text.strip().lower()

    if user_input == "/start":
        await update.message.reply_text("👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!")

    elif user_input == "/locket" or "locket" in user_input:
        response = (
            "<b>⭐ LOCKET NDTT MODULE - 2026 ⭐</b>\n"
            "────────────────\n"
            "Hướng dẫn giả lập <b>Locket Gold</b> vĩnh viễn:\n\n"
            "1️⃣ <b>Copy URL Module:</b>\n"
            f"<code>{RAW_URL}</code>\n\n"
            "2️⃣ <b>Shadowrocket:</b> Tab Module > Add Module > Dán link.\n\n"
            "3️⃣ <b>HTTPS Decryption:</b> Cài chứng chỉ CA và <b>Bật tin cậy</b>.\n\n"
            "4️⃣ <b>Hoàn tất:</b> Bật VPN và mở Locket hưởng thụ."
        )
        keyboard = [
            [InlineKeyboardButton("🚀 Cài nhanh (Shadowrocket)", url=f"shadowrocket://config/add/{RAW_URL}")],
            [InlineKeyboardButton("💬 Liên hệ Admin", url=CONTACT_URL)],
            [InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
        ]
        await update.message.reply_text(response, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

    elif user_input == "/contact":
        await update.message.reply_text(f"💬 Liên hệ Admin: {CONTACT_URL}")

    elif user_input == "/donate":
        await update.message.reply_text(f"☕ Donate: {DONATE_URL}")

def main():
    if not TOKEN:
        print("Lỗi: Không tìm thấy BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND | filters.COMMAND), handle_logic))
    
    print("--- 🤖 NgDanhThanhTrung_BOT 2026 Ready ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
